import io
import json
import os
from datetime import date

from dotenv import load_dotenv
load_dotenv()

import fitz  # PyMuPDF
import pytesseract
from groq import Groq
from PIL import Image

from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import MedicalReport
from .serializers import MedicalReportSerializer

ALLOWED_TYPES = {"image/jpeg", "image/png", "application/pdf"}

SYSTEM_PROMPT = (
    "Medical report parser. Return ONLY valid JSON with keys: "
    "patient_info (object), diagnosis (array of strings), medications (array of strings), "
    "lab_values (object where keys are metric names and values are objects with 'value' (number) and 'unit' (string)), "
    "doctor_notes (string). "
    "Example lab_values: {\"glucose\": {\"value\": 95.0, \"unit\": \"mg/dL\"}, \"heart_rate\": {\"value\": 72, \"unit\": \"bpm\"}}. "
    "Null for missing fields. No extra text outside JSON."
)

# Map lab value names → HealthMetric.METRIC_TYPES choices
LAB_VALUE_MAP = {
    "glucose": "GLUCOSE",
    "blood glucose": "GLUCOSE",
    "fasting glucose": "GLUCOSE",
    "cholesterol": "CHOLESTEROL",
    "total cholesterol": "CHOLESTEROL",
    "systolic": "BP_SYS",
    "blood pressure systolic": "BP_SYS",
    "bp systolic": "BP_SYS",
    "diastolic": "BP_DIA",
    "blood pressure diastolic": "BP_DIA",
    "bp diastolic": "BP_DIA",
    "heart rate": "HEART_RATE",
    "pulse": "HEART_RATE",
}


def ocr_image(image):
    """Run pytesseract on a PIL Image."""
    return pytesseract.image_to_string(image).strip()


def ocr_pdf(file_bytes):
    """Convert each PDF page to image, OCR, and combine text."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages_text = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        text = pytesseract.image_to_string(img).strip()
        if text:
            pages_text.append(f"--- Page {page_num + 1} ---\n{text}")
    doc.close()
    return "\n\n".join(pages_text)


def parse_groq_json(raw):
    """Strip markdown fences and parse JSON."""
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


def extract_and_save_metrics(user, report, lab_values):
    """
    Read parsed lab_values from OCR result and create HealthMetric records.
    lab_values format: {"glucose": {"value": 95.0, "unit": "mg/dL"}, ...}
    """
    from metrics.models import HealthMetric

    created = []
    if not isinstance(lab_values, dict):
        return created

    now = timezone.now()
    for lab_name, lab_data in lab_values.items():
        if not isinstance(lab_data, dict):
            continue

        metric_key = LAB_VALUE_MAP.get(lab_name.lower().strip())
        if not metric_key:
            continue

        try:
            value = float(lab_data.get("value", 0))
            unit = str(lab_data.get("unit", ""))
            if value <= 0:
                continue
            metric = HealthMetric.objects.create(
                user=user,
                report=report,
                metric_type=metric_key,
                value_numeric=value,
                unit=unit,
                measured_at=now,
            )
            created.append(metric)
        except Exception:
            continue

    return created


def update_health_profile(user, diagnosis):
    """
    Append new diagnoses to user's HealthProfile.chronic_conditions.
    diagnosis is a list of strings.
    """
    if not isinstance(diagnosis, list) or not diagnosis:
        return

    try:
        profile = user.health_profile
        existing = list(profile.chronic_conditions or [])
        new_conditions = [d for d in diagnosis if d and d not in existing]
        if new_conditions:
            profile.chronic_conditions = existing + new_conditions
            profile.save()
    except Exception:
        pass  # HealthProfile may not exist yet


def log_ai_interaction(user, prompt_summary, response_summary, tokens=None):
    """Create an AILog entry for the OCR LLM call."""
    from ai_logs.models import AILog
    try:
        AILog.objects.create(
            user=user,
            context="OCR_SUMMARY",
            prompt=prompt_summary[:2000],
            response=response_summary[:2000],
            tokens_used=tokens,
        )
    except Exception:
        pass


class OCRView(APIView):
    """
    POST /api/records/ocr/
    Upload a PDF or image. The endpoint will:
      1. Extract text via OCR (pytesseract / PyMuPDF)
      2. Parse text with Groq LLM → structured JSON
      3. Save a MedicalReport to the database
      4. Extract lab_values → create HealthMetric records
      5. Extract diagnosis → update HealthProfile.chronic_conditions
      6. Log the AI interaction to AILog
    Returns the saved report ID, parsed data, and counts of metrics created.
    """
    permission_classes = [IsAuthenticated]

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

        # --- Step 1: OCR ---
        file_bytes = uploaded.read()
        try:
            if uploaded.content_type == "application/pdf":
                raw_text = ocr_pdf(file_bytes)
                report_type = "OCR_SCAN"
            else:
                image = Image.open(io.BytesIO(file_bytes))
                raw_text = ocr_image(image)
                report_type = "UPLOAD_IMG"
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

        # --- Step 2: Groq LLM parse ---
        try:
            client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
            chat = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                max_tokens=1024,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": raw_text},
                ],
            )
            groq_raw = chat.choices[0].message.content.strip()
            tokens_used = getattr(chat.usage, "total_tokens", None)
        except Exception as e:
            return Response(
                {"error": f"Groq API call failed: {str(e)}. Make sure GROQ_API_KEY is set."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        parsed_report = parse_groq_json(groq_raw)

        # --- Step 3: Save MedicalReport ---
        title = uploaded.name or "Uploaded Report"
        report = MedicalReport.objects.create(
            user=request.user,
            title=title,
            report_type=report_type,
            date_issued=date.today(),
            ocr_extracted_text=raw_text,
            ai_summary=json.dumps(parsed_report),
            processing_status="PROCESSED",
        )

        # --- Step 4: Extract metrics → HealthMetric ---
        lab_values = parsed_report.get("lab_values") if isinstance(parsed_report, dict) else None
        metrics_created = extract_and_save_metrics(request.user, report, lab_values)

        # --- Step 5: Update HealthProfile chronic conditions ---
        diagnosis = parsed_report.get("diagnosis") if isinstance(parsed_report, dict) else None
        update_health_profile(request.user, diagnosis)

        # --- Step 6: Log AI interaction ---
        log_ai_interaction(
            user=request.user,
            prompt_summary=f"OCR parse of: {title}",
            response_summary=groq_raw,
            tokens=tokens_used,
        )

        return Response(
            {
                "report_id": str(report.id),
                "processing_status": "PROCESSED",
                "metrics_extracted": len(metrics_created),
                "raw_text": raw_text,
                "parsed_report": parsed_report,
            },
            status=status.HTTP_201_CREATED,
        )


class MedicalReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MedicalReportSerializer

    def get_queryset(self):
        return MedicalReport.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
