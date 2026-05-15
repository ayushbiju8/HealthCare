import requests

with open("/home/user/HealthCare/backend/ocr/samplereports/medical_report_sample.pdf", "rb") as f:
    r = requests.post("http://localhost:8001/api/ocr/", files={"file": ("medical_report_sample.pdf", f, "application/pdf")})
    print(r.json())
