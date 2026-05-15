import base64
import json
import os

import requests as http_requests
from groq import Groq
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Single Groq client instance
client = Groq(api_key=os.environ["GROQ_API_KEY"])

OPENFDA_API_KEY = os.environ.get("OPENFDA_API_KEY", "")
OPENFDA_BASE = "https://api.fda.gov/drug/label.json"

ALLOWED_TYPES = {"image/jpeg", "image/png"}

SYSTEM_PROMPT = (
    "You are a clinical pharmacist. You will receive FDA drug label data. "
    "Parse it and return ONLY JSON with these keys: "
    "medicine_name (string), generic_name (string), use_cases (array of strings), "
    "dosage { adult, child, elderly } (strings with mg and frequency), "
    "side_effects (array of strings), warnings (array of strings), "
    "contraindications (array of strings). "
    "Fill ALL fields from the provided data. If data is missing for a field, "
    "use your pharmaceutical knowledge to fill it. No extra text."
)

SYSTEM_PROMPT_NO_FDA = (
    "You are a clinical pharmacist with deep pharmacological knowledge. "
    "Given a medicine name, use your knowledge to provide comprehensive details. "
    "Return ONLY JSON: "
    "medicine_name (string), generic_name (string), use_cases (array of strings), "
    "dosage { adult, child, elderly } (strings with mg and frequency), "
    "side_effects (array of strings), warnings (array of strings), "
    "contraindications (array of strings). "
    "Fill ALL fields using your pharmaceutical knowledge. No extra text."
)

TEXT_MODEL = "llama-3.3-70b-versatile"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
MAX_TOKENS = 1024


def parse_groq_json(raw):
    """Parse JSON from Groq response, stripping markdown fences if present."""
    json_str = raw
    if json_str.startswith("```"):
        json_str = json_str.split("\n", 1)[1]
    if json_str.endswith("```"):
        json_str = json_str[: json_str.rfind("```")]
    json_str = json_str.strip()

    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return {"raw_parse": raw}


def fetch_openfda(medicine_name):
    """Query openFDA drug label API. Returns extracted label data or None."""
    params = {"limit": 3}
    if OPENFDA_API_KEY:
        params["api_key"] = OPENFDA_API_KEY

    # Search strategies: brand_name, generic_name, substance_name
    search_strategies = [
        f'openfda.brand_name:"{medicine_name}"',
        f'openfda.generic_name:"{medicine_name}"',
        f'openfda.substance_name:"{medicine_name}"',
    ]

    name_lower = medicine_name.lower()

    for search_query in search_strategies:
        params["search"] = search_query
        try:
            resp = http_requests.get(OPENFDA_BASE, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])
                for result in results:
                    # Validate the result actually matches the searched medicine
                    if _result_matches(result, name_lower):
                        return _extract_fda_fields(result)
        except Exception:
            continue

    return None


def _result_matches(result, name_lower):
    """Check if an openFDA result actually matches the medicine we searched for."""
    openfda = result.get("openfda", {})
    searchable = []
    searchable.extend(openfda.get("brand_name", []))
    searchable.extend(openfda.get("generic_name", []))
    searchable.extend(openfda.get("substance_name", []))

    for field_val in searchable:
        if name_lower in field_val.lower():
            return True
    return False


def _extract_fda_fields(result):
    """Extract relevant fields from an openFDA result."""
    def first(field_name):
        val = result.get(field_name, [])
        return val[0] if val else None

    openfda = result.get("openfda", {})
    brand_names = openfda.get("brand_name", [])
    generic_names = openfda.get("generic_name", [])

    return {
        "brand_name": brand_names[0] if brand_names else None,
        "generic_name": generic_names[0] if generic_names else None,
        "indications_and_usage": first("indications_and_usage"),
        "purpose": first("purpose"),
        "warnings": first("warnings"),
        "do_not_use": first("do_not_use"),
        "dosage_and_administration": first("dosage_and_administration"),
        "active_ingredient": first("active_ingredient"),
        "adverse_reactions": first("adverse_reactions"),
        "contraindications": first("contraindications"),
        "drug_interactions": first("drug_interactions"),
        "pregnancy_or_breast_feeding": first("pregnancy_or_breast_feeding"),
        "keep_out_of_reach_of_children": first("keep_out_of_reach_of_children"),
        "stop_use": first("stop_use"),
    }


def query_medicine_info(medicine_name):
    """
    1. Fetch real data from openFDA
    2. Send to Groq for structured parsing
    Falls back to Groq knowledge if openFDA has no results.
    """
    fda_data = fetch_openfda(medicine_name)

    if fda_data:
        # Use real FDA data + Groq to structure it
        user_content = (
            f"Medicine: {medicine_name}\n\n"
            f"FDA Label Data:\n{json.dumps(fda_data, indent=2)}\n\n"
            f"Parse this FDA data into the required JSON format."
        )
        system = SYSTEM_PROMPT
    else:
        # Fallback: no FDA data, use Groq knowledge
        user_content = f"Provide complete pharmaceutical information for: {medicine_name}"
        system = SYSTEM_PROMPT_NO_FDA

    chat = client.chat.completions.create(
        model=TEXT_MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ],
    )
    raw = chat.choices[0].message.content.strip()
    parsed = parse_groq_json(raw)

    # Tag the source
    if isinstance(parsed, dict) and "raw_parse" not in parsed:
        parsed["data_source"] = "openFDA" if fda_data else "ai_knowledge"

    return parsed


class MedicineTextView(APIView):
    """POST /api/medicine/text/ — Get medicine info from text name."""

    def post(self, request):
        medicine_name = request.data.get("medicine_name")

        if not medicine_name:
            return Response(
                {"error": "Missing required field: 'medicine_name'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        medicine_name = str(medicine_name).strip()
        if not medicine_name:
            return Response(
                {"error": "medicine_name cannot be empty."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        try:
            medicine_info = query_medicine_info(medicine_name)
        except Exception as e:
            return Response(
                {"error": f"Groq API call failed: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(
            {"medicine_info": medicine_info},
            status=status.HTTP_200_OK,
        )


class MedicineImageView(APIView):
    """POST /api/medicine/image/ — Extract medicine info from image."""

    def post(self, request):
        uploaded = request.FILES.get("file")
        if not uploaded:
            return Response(
                {"error": "No file provided. Use field name 'file'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if uploaded.content_type not in ALLOWED_TYPES:
            return Response(
                {"error": f"Unsupported file type: {uploaded.content_type}. Only JPEG/PNG allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Read and encode image to base64
        image_bytes = uploaded.read()
        if not image_bytes:
            return Response(
                {"error": "Uploaded image is empty."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        base64_data = base64.b64encode(image_bytes).decode("utf-8")
        mime_type = uploaded.content_type

        # Step 1: Vision model — extract medicine name from image
        try:
            vision_response = client.chat.completions.create(
                model=VISION_MODEL,
                max_tokens=MAX_TOKENS,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{base64_data}"
                                },
                            },
                            {
                                "type": "text",
                                "text": "Identify the medicine name from this image. Return ONLY the medicine name, nothing else.",
                            },
                        ],
                    }
                ],
            )
            raw_text = vision_response.choices[0].message.content.strip()
        except Exception as e:
            return Response(
                {"error": f"Vision model call failed: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        if not raw_text:
            return Response(
                {"error": "Vision model returned empty text. Image may be unreadable."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        # Step 2: openFDA + Groq — get full medicine info
        try:
            medicine_info = query_medicine_info(raw_text)
        except Exception as e:
            return Response(
                {"error": f"Groq API call failed: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(
            {"raw_text": raw_text, "medicine_info": medicine_info},
            status=status.HTTP_200_OK,
        )


class HealthView(APIView):
    """GET /api/health/ — Liveness check."""

    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
