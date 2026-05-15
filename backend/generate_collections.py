import json
import uuid

def get_uuid():
    return str(uuid.uuid4())

base_url = "http://127.0.0.1:8000"
auth_header = {"name": "Authorization", "value": "Bearer <paste-token-here>"}
auth_header_pm = {"key": "Authorization", "value": "Bearer <paste-token-here>"}
content_type = {"name": "Content-Type", "value": "application/json"}
content_type_pm = {"key": "Content-Type", "value": "application/json"}

# Endpoint definitions
endpoints = [
    {
        "folder": "Auth & Users",
        "requests": [
            {"name": "Register User", "method": "POST", "path": "api/auth/register/", "body": '{\n  "email": "newuser@example.com",\n  "password": "password123",\n  "first_name": "John",\n  "last_name": "Doe"\n}', "auth": False},
            {"name": "Login (Get JWT)", "method": "POST", "path": "api/auth/login/", "body": '{\n  "email": "testuser@example.com",\n  "password": "testpass123"\n}', "auth": False},
            {"name": "Refresh Token", "method": "POST", "path": "api/auth/refresh/", "body": '{\n  "refresh": "<paste-refresh-token-here>"\n}', "auth": False},
            {"name": "Get User Profile", "method": "GET", "path": "api/auth/profile/", "auth": True},
            {"name": "Update User Profile", "method": "PATCH", "path": "api/auth/profile/1/", "body": '{\n  "first_name": "Updated"\n}', "auth": True},
            {"name": "Get Health Profile", "method": "GET", "path": "api/auth/health-profile/", "auth": True},
            {"name": "Update Health Profile", "method": "PATCH", "path": "api/auth/health-profile/1/", "body": '{\n  "blood_group": "A+"\n}', "auth": True},
            {"name": "Get Emergency Contacts", "method": "GET", "path": "api/auth/emergency-contacts/", "auth": True},
            {"name": "Create Emergency Contact", "method": "POST", "path": "api/auth/emergency-contacts/", "body": '{\n  "name": "Jane Doe",\n  "relation": "Spouse",\n  "phone_number": "555-1234"\n}', "auth": True},
            {"name": "Delete Emergency Contact", "method": "DELETE", "path": "api/auth/emergency-contacts/1/", "auth": True},
        ]
    },
    {
        "folder": "Medical Records",
        "requests": [
            {"name": "Get Medical Reports", "method": "GET", "path": "api/records/reports/", "auth": True},
            {"name": "Create Medical Report", "method": "POST", "path": "api/records/reports/", "body": '{\n  "title": "Annual Blood Test",\n  "report_type": "blood_test"\n}', "auth": True},
            {"name": "Delete Medical Report", "method": "DELETE", "path": "api/records/reports/1/", "auth": True},
            {"name": "Parse Report (OCR & LLM)", "method": "POST", "path": "api/records/ocr/", "body_type": "formdata", "auth": True},
        ]
    },
    {
        "folder": "Health Metrics",
        "requests": [
            {"name": "Get Health Metrics", "method": "GET", "path": "api/metrics/health-metrics/", "auth": True},
            {"name": "Create Health Metric", "method": "POST", "path": "api/metrics/health-metrics/", "body": '{\n  "metric_type": "heart_rate",\n  "value": 72.5,\n  "unit": "bpm"\n}', "auth": True},
            {"name": "Delete Health Metric", "method": "DELETE", "path": "api/metrics/health-metrics/1/", "auth": True},
        ]
    },
    {
        "folder": "Fitness Data",
        "requests": [
            {"name": "Get Wearable Integrations", "method": "GET", "path": "api/fitness/integrations/", "auth": True},
            {"name": "Create Wearable Integration", "method": "POST", "path": "api/fitness/integrations/", "body": '{\n  "provider": "apple_health",\n  "access_token": "token123"\n}', "auth": True},
            {"name": "Get Daily Summaries", "method": "GET", "path": "api/fitness/daily-summaries/", "auth": True},
            {"name": "Create Daily Summary", "method": "POST", "path": "api/fitness/daily-summaries/", "body": '{\n  "date": "2026-05-15",\n  "steps": 10000,\n  "calories_burned": 2500.0\n}', "auth": True},
        ]
    },
    {
        "folder": "Reminders",
        "requests": [
            {"name": "Get Reminders", "method": "GET", "path": "api/reminders/reminders/", "auth": True},
            {"name": "Create Reminder", "method": "POST", "path": "api/reminders/reminders/", "body": '{\n  "title": "Take Medication",\n  "reminder_type": "medication",\n  "scheduled_time": "2026-05-15T08:00:00Z"\n}', "auth": True},
            {"name": "Delete Reminder", "method": "DELETE", "path": "api/reminders/reminders/1/", "auth": True},
        ]
    },
    {
        "folder": "AI System Logs",
        "requests": [
            {"name": "Get AI Logs", "method": "GET", "path": "api/ai-logs/logs/", "auth": True},
            {"name": "Create AI Log", "method": "POST", "path": "api/ai-logs/logs/", "body": '{\n  "interaction_type": "ocr_analysis",\n  "prompt": "Analyze this report",\n  "response": "Patient is healthy"\n}', "auth": True},
        ]
    },
    {
        "folder": "Hospital Integrations",
        "requests": [
            {"name": "Get API Logs", "method": "GET", "path": "api/integrations/logs/", "auth": True},
        ]
    }
]

# Generate Thunder Client
tc_col_id = get_uuid()
tc_folders = []
tc_requests = []
sort_folder = 10000

for folder_data in endpoints:
    f_id = get_uuid()
    tc_folders.append({
        "_id": f_id, "name": folder_data["folder"], "containerId": "", "created": "2026-05-15T00:00:00.000Z", "sortNum": sort_folder
    })
    sort_req = 10000
    for req in folder_data["requests"]:
        headers = []
        if req["auth"]: headers.append(auth_header)
        body = {}
        if "body" in req:
            body = {"type": "json", "raw": req["body"]}
        elif req.get("body_type") == "formdata":
            body = {"type": "formdata", "form": [{"name": "file", "value": "", "type": "file"}]}
            
        tc_requests.append({
            "_id": get_uuid(),
            "colId": tc_col_id,
            "containerId": f_id,
            "name": req["name"],
            "url": f"{base_url}/{req['path']}",
            "method": req["method"],
            "sortNum": sort_req,
            "created": "2026-05-15T00:00:00.000Z",
            "modified": "2026-05-15T00:00:00.000Z",
            "headers": headers,
            "body": body
        })
        sort_req += 10000
    sort_folder += 10000

tc_collection = {
    "clientName": "Thunder Client",
    "collectionName": "HealthCare API Complete",
    "dateExported": "2026-05-15T00:00:00.000Z",
    "version": "1.2",
    "coreVersion": "2.2.0",
    "_id": tc_col_id,
    "folders": tc_folders,
    "requests": tc_requests
}

with open("thunder-collection_HealthCare.json", "w") as f:
    json.dump(tc_collection, f, indent=2)


# Generate Postman Collection
pm_items = []

for folder_data in endpoints:
    pm_folder_items = []
    for req in folder_data["requests"]:
        headers = []
        if req["auth"]: headers.append(auth_header_pm)
        
        body = {}
        if "body" in req:
            headers.append(content_type_pm)
            body = {"mode": "raw", "raw": req["body"]}
        elif req.get("body_type") == "formdata":
            body = {"mode": "formdata", "formdata": [{"key": "file", "type": "file", "src": ""}]}
            
        path_list = req["path"].strip("/").split("/")
        
        pm_folder_items.append({
            "name": req["name"],
            "request": {
                "method": req["method"],
                "header": headers,
                "body": body if body else None,
                "url": {
                    "raw": f"{base_url}/{req['path']}",
                    "host": ["127", "0", "0", "1"],
                    "port": "8000",
                    "path": path_list
                }
            }
        })
        
    pm_items.append({
        "name": folder_data["folder"],
        "item": pm_folder_items
    })

pm_collection = {
    "info": {
        "name": "HealthCare API Complete",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": pm_items
}

with open("postman_collection_HealthCare.json", "w") as f:
    json.dump(pm_collection, f, indent=2)

print("Both Thunder Client and Postman Collections updated with OCR endpoint!")
