"""
Test script for the Medical OCR API.
Generates a fake medical report image with Pillow, then POSTs it to /api/ocr/.
"""

import io
import json
import sys

import requests
from PIL import Image, ImageDraw, ImageFont

BASE_URL = "http://localhost:8001"

SAMPLE_REPORT = """
PATIENT MEDICAL REPORT

Patient Name: John Doe
Date of Birth: 15/03/1985
Patient ID: MRN-2024-00491
Date: 14/05/2026

DIAGNOSIS:
- Type 2 Diabetes Mellitus (E11.9)
- Essential Hypertension (I10)

MEDICATIONS:
1. Metformin 500mg - twice daily
2. Amlodipine 5mg - once daily
3. Atorvastatin 20mg - at bedtime

LAB VALUES:
- HbA1c: 7.2%
- Fasting Glucose: 142 mg/dL
- Total Cholesterol: 210 mg/dL
- LDL: 130 mg/dL
- HDL: 45 mg/dL
- Creatinine: 1.1 mg/dL
- Blood Pressure: 138/88 mmHg

DOCTOR NOTES:
Patient shows improvement in glycemic control
since last visit. Continue current medications.
Follow up in 3 months. Recommend dietary changes
and 30 min daily exercise.

Dr. Sarah Smith, MD
Internal Medicine
License: MD-20145
"""


def create_test_image():
    """Generate a medical report image with text."""
    img = Image.new("RGB", (800, 1100), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
        font_bold = font

    y = 30
    for line in SAMPLE_REPORT.strip().split("\n"):
        is_header = line.isupper() or line.startswith("PATIENT")
        draw.text((40, y), line, fill=(0, 0, 0), font=font_bold if is_header else font)
        y += 24

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    # Also save locally for reference
    img.save("test_report.png")
    print("[+] Test image saved to test_report.png")

    return buf


def test_health():
    print("\n=== GET /api/health/ ===")
    r = requests.get(f"{BASE_URL}/api/health/")
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
    assert r.status_code == 200
    print("[PASS]")


def test_ocr():
    print("\n=== POST /api/ocr/ (valid image) ===")
    img_buf = create_test_image()
    r = requests.post(
        f"{BASE_URL}/api/ocr/",
        files={"file": ("report.png", img_buf, "image/png")},
    )
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"Raw text (first 200 chars): {data.get('raw_text', '')[:200]}...")
    print(f"Parsed report: {json.dumps(data.get('parsed_report', {}), indent=2)}")
    assert r.status_code == 200
    print("[PASS]")


def test_bad_file_type():
    print("\n=== POST /api/ocr/ (bad file type) ===")
    r = requests.post(
        f"{BASE_URL}/api/ocr/",
        files={"file": ("test.txt", b"hello world", "text/plain")},
    )
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
    assert r.status_code == 400
    print("[PASS]")


def test_no_file():
    print("\n=== POST /api/ocr/ (no file) ===")
    r = requests.post(f"{BASE_URL}/api/ocr/")
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
    assert r.status_code == 400
    print("[PASS]")


if __name__ == "__main__":
    print("Medical OCR API Test Suite")
    print("=" * 40)

    try:
        test_health()
        test_bad_file_type()
        test_no_file()
        test_ocr()
        print("\n" + "=" * 40)
        print("ALL TESTS PASSED")
    except requests.ConnectionError:
        print(f"\n[ERROR] Cannot connect to {BASE_URL}. Is the server running?")
        sys.exit(1)
    except AssertionError as e:
        print(f"\n[FAIL] {e}")
        sys.exit(1)
