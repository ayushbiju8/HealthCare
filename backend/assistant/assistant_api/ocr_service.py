import io
import json
import os
import uuid
from datetime import datetime
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from groq import Groq

# The strict JSON schema we want Groq to return
SYSTEM_PROMPT = """
You are an expert medical data extractor. You will be provided with raw OCR text extracted from a medical report.
Your job is to parse the text and return ONLY a valid JSON object matching the exact schema below. Do not include any markdown formatting, code blocks, or conversational text.

Required JSON Schema:
{
  "report_id": "Generate a unique string if not found",
  "patient_id": "Generate a unique string if not found",
  "name": "Patient Name",
  "age": "Patient Age (integer) - estimate from DOB if needed, else null",
  "date_of_report": "YYYY-MM-DD format",
  "test_results": [
    {
      "test_name": "Name of the test (e.g. Vitamin D)",
      "value": "Value of the test result (number as string)",
      "unit": "Unit of measurement (e.g. ng/mL)",
      "reference_range": "Normal range (e.g. 20-50)",
      "status": "One of: normal, high, low, abnormal"
    }
  ]
}
"""

def ocr_image(image):
    """Run pytesseract on a PIL Image."""
    return pytesseract.image_to_string(image).strip()

def ocr_pdf(file_bytes):
    """Extract text from PDF using PyMuPDF native extraction."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages_text = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text().strip()
        if text:
            pages_text.append(f"--- Page {page_num + 1} ---\n{text}")
    doc.close()
    return "\n\n".join(pages_text)

def process_document(file_bytes, content_type):
    """Process an uploaded document (image or pdf) and return the parsed JSON report."""
    if content_type == "application/pdf":
        raw_text = ocr_pdf(file_bytes)
    elif content_type in ["image/jpeg", "image/png"]:
        image = Image.open(io.BytesIO(file_bytes))
        raw_text = ocr_image(image)
    else:
        raise ValueError(f"Unsupported content type: {content_type}")

    if not raw_text:
        raise ValueError("OCR returned empty text. File may be blank or unreadable.")

    # Call Groq to parse into JSON
    client = Groq()
    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=2048,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"RAW OCR TEXT:\n{raw_text}"},
        ],
    )
    
    groq_raw = chat.choices[0].message.content.strip()
    
    # Strip markdown if present
    if groq_raw.startswith("```"):
        lines = groq_raw.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines[-1].startswith("```"):
            lines = lines[:-1]
        groq_raw = "\n".join(lines).strip()

    try:
        parsed_report = json.loads(groq_raw)
    except json.JSONDecodeError:
        raise ValueError("Failed to parse the LLM output into JSON.")
        
    # Ensure IDs exist
    if not parsed_report.get("report_id"):
        parsed_report["report_id"] = f"R-{uuid.uuid4().hex[:6].upper()}"
    if not parsed_report.get("patient_id"):
        parsed_report["patient_id"] = "P12345" # Default to current user for prototype
        
    return parsed_report
