"""
Test script for the Medicine Info API.
Tests all endpoints: health, text lookup, image lookup, and error cases.
"""

import io
import json
import sys

import requests
from PIL import Image, ImageDraw, ImageFont

BASE_URL = "http://localhost:8002"


def create_medicine_image():
    """Generate a fake medicine label image."""
    img = Image.new("RGB", (600, 400), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
        font_sm = font

    draw.text((40, 30), "PARACETAMOL 500mg", fill=(0, 0, 150), font=font)
    draw.text((40, 80), "Acetaminophen Tablets", fill=(80, 80, 80), font=font_sm)
    draw.text((40, 130), "Each tablet contains:", fill=(0, 0, 0), font=font_sm)
    draw.text((40, 160), "Paracetamol IP 500mg", fill=(0, 0, 0), font=font_sm)
    draw.text((40, 210), "Dosage: 1-2 tablets every", fill=(0, 0, 0), font=font_sm)
    draw.text((40, 240), "4-6 hours. Max 8 tablets/day", fill=(0, 0, 0), font=font_sm)
    draw.text((40, 290), "Mfg: PharmaCorp Ltd.", fill=(100, 100, 100), font=font_sm)
    draw.text((40, 320), "Exp: 12/2027  Batch: PC-2026-A1", fill=(100, 100, 100), font=font_sm)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    img.save("test_medicine_label.png")
    print("[+] Test image saved to test_medicine_label.png")

    return buf


def test_health():
    print("\n=== GET /api/health/ ===")
    r = requests.get(f"{BASE_URL}/api/health/")
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
    assert r.status_code == 200
    print("[PASS]")


def test_text_lookup():
    print("\n=== POST /api/medicine/text/ (paracetamol) ===")
    r = requests.post(
        f"{BASE_URL}/api/medicine/text/",
        json={"medicine_name": "paracetamol"},
    )
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"Medicine info: {json.dumps(data.get('medicine_info', {}), indent=2)}")
    assert r.status_code == 200
    print("[PASS]")


def test_text_missing_field():
    print("\n=== POST /api/medicine/text/ (no field) ===")
    r = requests.post(
        f"{BASE_URL}/api/medicine/text/",
        json={},
    )
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
    assert r.status_code == 400
    print("[PASS]")


def test_text_empty_name():
    print("\n=== POST /api/medicine/text/ (empty name) ===")
    r = requests.post(
        f"{BASE_URL}/api/medicine/text/",
        json={"medicine_name": "   "},
    )
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
    assert r.status_code == 422
    print("[PASS]")


def test_image_bad_type():
    print("\n=== POST /api/medicine/image/ (bad file type) ===")
    r = requests.post(
        f"{BASE_URL}/api/medicine/image/",
        files={"file": ("test.txt", b"hello", "text/plain")},
    )
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
    assert r.status_code == 400
    print("[PASS]")


def test_image_no_file():
    print("\n=== POST /api/medicine/image/ (no file) ===")
    r = requests.post(f"{BASE_URL}/api/medicine/image/")
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
    assert r.status_code == 400
    print("[PASS]")


def test_image_lookup(image_path=None):
    print("\n=== POST /api/medicine/image/ (medicine label) ===")

    if image_path:
        print(f"[+] Using custom image: {image_path}")
        filename = image_path.rsplit("/", 1)[-1]
        mime = "image/png" if filename.endswith(".png") else "image/jpeg"
        with open(image_path, "rb") as f:
            r = requests.post(
                f"{BASE_URL}/api/medicine/image/",
                files={"file": (filename, f, mime)},
            )
    else:
        img_buf = create_medicine_image()
        r = requests.post(
            f"{BASE_URL}/api/medicine/image/",
            files={"file": ("medicine.png", img_buf, "image/png")},
        )

    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"Raw text (first 200 chars): {data.get('raw_text', '')[:200]}...")
    print(f"Medicine info: {json.dumps(data.get('medicine_info', {}), indent=2)}")
    assert r.status_code == 200
    print("[PASS]")


if __name__ == "__main__":
    print("Medicine Info API Test Suite")
    print("=" * 40)

    # Optional: pass your own image path as argument
    # Usage: python3 test_medicine.py /path/to/medicine_image.jpg
    custom_image = sys.argv[1] if len(sys.argv) > 1 else None

    try:
        test_health()
        test_text_missing_field()
        test_text_empty_name()
        test_image_bad_type()
        test_image_no_file()
        test_text_lookup()
        test_image_lookup(image_path=custom_image)
        print("\n" + "=" * 40)
        print("ALL TESTS PASSED")
    except requests.ConnectionError:
        print(f"\n[ERROR] Cannot connect to {BASE_URL}. Is the server running?")
        sys.exit(1)
    except AssertionError as e:
        print(f"\n[FAIL] {e}")
        sys.exit(1)

