import json
import uuid

def get_uuid():
    return str(uuid.uuid4())

base_url = "http://127.0.0.1:8000"
auth_header = {"name": "Authorization", "value": "Bearer <paste-token-here>"}
auth_header_pm = {"key": "Authorization", "value": "Bearer <paste-token-here>"}
content_type_pm = {"key": "Content-Type", "value": "application/json"}

# Endpoint definitions — bodies match actual model fields
endpoints = [
    {
        "folder": "Auth & Users",
        "requests": [
            {
                "name": "Register User", "method": "POST", "path": "api/auth/register/", "auth": False,
                "body": '{\n  "email": "testuser@example.com",\n  "password": "testpass123",\n  "username": "testuser",\n  "first_name": "John",\n  "last_name": "Doe"\n}'
            },
            {
                "name": "Login (Get JWT)", "method": "POST", "path": "api/auth/login/", "auth": False,
                "body": '{\n  "email": "testuser@example.com",\n  "password": "testpass123"\n}'
            },
            {
                "name": "Refresh Token", "method": "POST", "path": "api/auth/refresh/", "auth": False,
                "body": '{\n  "refresh": "<paste-refresh-token-here>"\n}'
            },
            {"name": "List User Profiles", "method": "GET", "path": "api/auth/profile/", "auth": True},
            {
                "name": "Update User Profile", "method": "PATCH", "path": "api/auth/profile/1/", "auth": True,
                "body": '{\n  "first_name": "Updated"\n}'
            },
            {"name": "Get Health Profile", "method": "GET", "path": "api/auth/health-profile/", "auth": True},
            {
                "name": "Update Health Profile", "method": "PATCH", "path": "api/auth/health-profile/1/", "auth": True,
                "body": '{\n  "blood_group": "A+",\n  "height_cm": "175.00",\n  "weight_kg": "70.00"\n}'
            },
            {"name": "List Emergency Contacts", "method": "GET", "path": "api/auth/emergency-contacts/", "auth": True},
            {
                "name": "Create Emergency Contact", "method": "POST", "path": "api/auth/emergency-contacts/", "auth": True,
                "body": '{\n  "name": "Jane Doe",\n  "relation": "Spouse",\n  "phone_number": "555-1234"\n}'
            },
            {"name": "Delete Emergency Contact", "method": "DELETE", "path": "api/auth/emergency-contacts/1/", "auth": True},
        ]
    },
    {
        "folder": "Medical Records",
        "requests": [
            {"name": "List Medical Reports", "method": "GET", "path": "api/records/reports/", "auth": True},
            {
                "name": "Create Medical Report (Manual)", "method": "POST", "path": "api/records/reports/", "auth": True,
                "body": '{\n  "title": "Annual Blood Test",\n  "report_type": "UPLOAD_PDF",\n  "date_issued": "2026-05-15",\n  "source_hospital": "City Hospital"\n}'
            },
            {"name": "Get Medical Report", "method": "GET", "path": "api/records/reports/1/", "auth": True},
            {"name": "Delete Medical Report", "method": "DELETE", "path": "api/records/reports/1/", "auth": True},
            {
                "name": "OCR Parse Report (Upload PDF/Image)", "method": "POST", "path": "api/records/ocr/",
                "body_type": "formdata", "auth": True,
                "note": "Upload a PDF or JPEG/PNG. Returns report_id, metrics_extracted, and parsed JSON."
            },
        ]
    },
    {
        "folder": "Health Metrics",
        "requests": [
            {"name": "List Health Metrics", "method": "GET", "path": "api/metrics/health-metrics/", "auth": True},
            {
                "name": "Create Health Metric (Manual)", "method": "POST", "path": "api/metrics/health-metrics/", "auth": True,
                "body": '{\n  "metric_type": "GLUCOSE",\n  "value_numeric": "95.00",\n  "unit": "mg/dL"\n}'
            },
            {"name": "Get Health Metric", "method": "GET", "path": "api/metrics/health-metrics/1/", "auth": True},
            {"name": "Delete Health Metric", "method": "DELETE", "path": "api/metrics/health-metrics/1/", "auth": True},
        ]
    },
    {
        "folder": "Fitness Data",
        "requests": [
            {"name": "List Wearable Integrations", "method": "GET", "path": "api/fitness/integrations/", "auth": True},
            {
                "name": "Create Wearable Integration", "method": "POST", "path": "api/fitness/integrations/", "auth": True,
                "body": '{\n  "provider": "GOOGLE_FIT",\n  "access_token": "access_token_here",\n  "refresh_token": "refresh_token_here",\n  "token_expires_at": "2027-01-01T00:00:00Z"\n}'
            },
            {"name": "List Daily Summaries", "method": "GET", "path": "api/fitness/daily-summaries/", "auth": True},
            {
                "name": "Create Daily Summary", "method": "POST", "path": "api/fitness/daily-summaries/", "auth": True,
                "body": '{\n  "date": "2026-05-15",\n  "total_steps": 10000,\n  "avg_heart_rate": 72,\n  "calories_burned": "2500.00",\n  "sleep_minutes": 480\n}'
            },
        ]
    },
    {
        "folder": "Reminders",
        "requests": [
            {"name": "List Reminders", "method": "GET", "path": "api/reminders/reminders/", "auth": True},
            {
                "name": "Create Reminder", "method": "POST", "path": "api/reminders/reminders/", "auth": True,
                "body": '{\n  "title": "Take Medication",\n  "type": "MEDICINE",\n  "due_datetime": "2026-05-15T08:00:00Z"\n}'
            },
            {
                "name": "Update Reminder", "method": "PATCH", "path": "api/reminders/reminders/1/", "auth": True,
                "body": '{\n  "is_active": false\n}'
            },
            {"name": "Delete Reminder", "method": "DELETE", "path": "api/reminders/reminders/1/", "auth": True},
        ]
    },
    {
        "folder": "AI System Logs",
        "requests": [
            {"name": "List AI Logs", "method": "GET", "path": "api/ai-logs/logs/", "auth": True},
            {
                "name": "Create AI Log (Manual)", "method": "POST", "path": "api/ai-logs/logs/", "auth": True,
                "body": '{\n  "context": "GENERAL_CHAT",\n  "prompt": "What is my glucose level?",\n  "response": "Your last recorded glucose was 95 mg/dL.",\n  "tokens_used": 120\n}'
            },
            {"name": "Delete AI Log", "method": "DELETE", "path": "api/ai-logs/logs/1/", "auth": True},
        ]
    },
    {
        "folder": "Medicine Analysis",
        "requests": [
            {
                "name": "Analyse Medicine (by Name)", "method": "POST", "path": "api/medicine/text/", "auth": True,
                "body": '{\n  "medicine_name": "Ibuprofen"\n}'
            },
            {
                "name": "Analyse Medicine (by Image)", "method": "POST", "path": "api/medicine/image/",
                "body_type": "formdata", "auth": True,
                "note": "Upload a JPEG/PNG photo of the medicine packaging. Returns name + full pharmaceutical info."
            },
        ]
    },
    {
        "folder": "Hospital Integrations (Audit Logs)",
        "requests": [
            {"name": "List API Audit Logs", "method": "GET", "path": "api/integrations/logs/", "auth": True},
        ]
    }
]


# ─── Thunder Client Collection ────────────────────────────────────────────────

tc_col_id = get_uuid()
tc_folders = []
tc_requests = []
sort_folder = 10000

for folder_data in endpoints:
    f_id = get_uuid()
    tc_folders.append({
        "_id": f_id, "name": folder_data["folder"], "containerId": "",
        "created": "2026-05-15T00:00:00.000Z", "sortNum": sort_folder
    })
    sort_req = 10000
    for req in folder_data["requests"]:
        headers = [auth_header] if req["auth"] else []
        if "body" in req:
            body = {"type": "json", "raw": req["body"]}
        elif req.get("body_type") == "formdata":
            body = {"type": "formdata", "form": [{"name": "file", "value": "", "type": "file"}]}
        else:
            body = {}

        tc_requests.append({
            "_id": get_uuid(), "colId": tc_col_id, "containerId": f_id,
            "name": req["name"], "url": f"{base_url}/{req['path']}",
            "method": req["method"], "sortNum": sort_req,
            "created": "2026-05-15T00:00:00.000Z", "modified": "2026-05-15T00:00:00.000Z",
            "headers": headers, "body": body
        })
        sort_req += 10000
    sort_folder += 10000

tc_collection = {
    "clientName": "Thunder Client",
    "collectionName": "HealthCare API v2",
    "dateExported": "2026-05-15T00:00:00.000Z",
    "version": "1.2", "coreVersion": "2.2.0",
    "_id": tc_col_id, "folders": tc_folders, "requests": tc_requests
}

with open("thunder-collection_HealthCare.json", "w") as f:
    json.dump(tc_collection, f, indent=2)


# ─── Postman Collection ───────────────────────────────────────────────────────

pm_items = []

for folder_data in endpoints:
    pm_folder_items = []
    for req in folder_data["requests"]:
        headers = [auth_header_pm] if req["auth"] else []

        if "body" in req:
            headers.append(content_type_pm)
            body = {"mode": "raw", "raw": req["body"],
                    "options": {"raw": {"language": "json"}}}
        elif req.get("body_type") == "formdata":
            body = {"mode": "formdata",
                    "formdata": [{"key": "file", "type": "file", "src": ""}]}
        else:
            body = None

        path_str = req["path"]
        if path_str.startswith("/"):
            path_str = path_str[1:]
        path_list = path_str.split("/")

        item = {
            "name": req["name"],
            "request": {
                "method": req["method"],
                "header": headers,
                "url": {
                    "raw": f"{base_url}/{req['path']}",
                    "host": ["127", "0", "0", "1"],
                    "port": "8000",
                    "path": path_list
                }
            }
        }
        if body:
            item["request"]["body"] = body
        if req.get("note"):
            item["request"]["description"] = req["note"]

        pm_folder_items.append(item)

    pm_items.append({"name": folder_data["folder"], "item": pm_folder_items})

pm_collection = {
    "info": {
        "name": "HealthCare API v2",
        "description": "Complete Healthcare Platform API — JWT authenticated. All POST bodies match Django model fields.",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": pm_items
}

with open("postman_collection_HealthCare.json", "w") as f:
    json.dump(pm_collection, f, indent=2)

print("✅ Both collections updated — Thunder Client + Postman (v2)")
print(f"   Folders: {len(endpoints)}")
print(f"   Requests: {sum(len(f['requests']) for f in endpoints)}")
