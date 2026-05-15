import io
import json
import os

import fitz  # PyMuPDF
import pytesseract
from groq import Groq
from PIL import Image
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

ALLOWED_TYPES = {"image/jpeg", "image/png", "application/pdf"}

SYSTEM_PROMPT = (
    "Medical report parser. Return ONLY JSON with keys: "
    "patient_info, diagnosis, medications, lab_values, doctor_notes. "
    "Null for missing. No extra text."
)


def ocr_image(image):
    """Run pytesseract on a PIL Image."""
    return pytesseract.image_to_string(image).strip()


def ocr_pdf(file_bytes):
    """Convert each PDF page to image, OCR, and combine text."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages_text = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        # Render at 300 DPI for good OCR quality
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        text = pytesseract.image_to_string(img).strip()
        if text:
            pages_text.append(f"--- Page {page_num + 1} ---\n{text}")
    doc.close()
    return "\n\n".join(pages_text)


class OCRView(APIView):
    """POST /api/ocr/ — OCR an image or PDF and parse with Groq LLM."""

    def post(self, request):
        uploaded = request.FILES.get("file")
        if not uploaded:
            return Response(
                {"error": "No file provided. Use field name 'file'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if uploaded.content_type not in ALLOWED_TYPES:
            return Response(
                {"error": f"Unsupported file type: {uploaded.content_type}. Only JPEG/PNG/PDF allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # OCR
        try:
            if uploaded.content_type == "application/pdf":
                raw_text = ocr_pdf(uploaded.read())
            else:
                image = Image.open(uploaded)
                raw_text = ocr_image(image)
        except Exception as e:
            return Response(
                {"error": f"OCR processing failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if not raw_text:
            return Response(
                {"error": "OCR returned empty text. File may be blank or unreadable."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        # Groq LLM parse
        try:
            client = Groq(api_key=os.environ["GROQ_API_KEY"])
            chat = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                max_tokens=1024,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": raw_text},
                ],
            )
            groq_raw = chat.choices[0].message.content.strip()
        except KeyError:
            return Response(
                {"error": "GROQ_API_KEY not set in environment."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": f"Groq API call failed: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        # Safe JSON parse — strip markdown fences if present
        json_str = groq_raw
        if json_str.startswith("```"):
            json_str = json_str.split("\n", 1)[1]  # remove ```json line
        if json_str.endswith("```"):
            json_str = json_str[: json_str.rfind("```")]
        json_str = json_str.strip()

        try:
            parsed_report = json.loads(json_str)
        except (json.JSONDecodeError, TypeError):
            parsed_report = {"raw_parse": groq_raw}

        return Response(
            {"raw_text": raw_text, "parsed_report": parsed_report},
            status=status.HTTP_200_OK,
        )


class HealthView(APIView):
    """GET /api/health/ — Liveness check."""

    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
