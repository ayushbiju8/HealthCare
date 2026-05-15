import json
import uuid
import datetime

def get_uuid():
    return str(uuid.uuid4())

col_id = get_uuid()

folders = [
    {"_id": get_uuid(), "name": "Auth", "containerId": "", "created": "2026-05-15T00:00:00.000Z", "sortNum": 10000},
    {"_id": get_uuid(), "name": "Records", "containerId": "", "created": "2026-05-15T00:00:00.000Z", "sortNum": 20000},
    {"_id": get_uuid(), "name": "Metrics", "containerId": "", "created": "2026-05-15T00:00:00.000Z", "sortNum": 30000},
]

auth_folder = folders[0]["_id"]
records_folder = folders[1]["_id"]
metrics_folder = folders[2]["_id"]

base_url = "http://127.0.0.1:8000"

requests = [
    {
        "_id": get_uuid(),
        "colId": col_id,
        "containerId": auth_folder,
        "name": "Register User",
        "url": f"{base_url}/api/auth/register/",
        "method": "POST",
        "sortNum": 10000,
        "created": "2026-05-15T00:00:00.000Z",
        "modified": "2026-05-15T00:00:00.000Z",
        "headers": [],
        "body": {
            "type": "json",
            "raw": "{\n  \"email\": \"newuser@example.com\",\n  \"password\": \"password123\",\n  \"first_name\": \"John\",\n  \"last_name\": \"Doe\"\n}"
        }
    },
    {
        "_id": get_uuid(),
        "colId": col_id,
        "containerId": auth_folder,
        "name": "Login (Get JWT)",
        "url": f"{base_url}/api/auth/login/",
        "method": "POST",
        "sortNum": 20000,
        "created": "2026-05-15T00:00:00.000Z",
        "modified": "2026-05-15T00:00:00.000Z",
        "headers": [],
        "body": {
            "type": "json",
            "raw": "{\n  \"email\": \"testuser@example.com\",\n  \"password\": \"testpass123\"\n}"
        }
    },
    {
        "_id": get_uuid(),
        "colId": col_id,
        "containerId": auth_folder,
        "name": "Get Profile",
        "url": f"{base_url}/api/auth/profile/",
        "method": "GET",
        "sortNum": 30000,
        "created": "2026-05-15T00:00:00.000Z",
        "modified": "2026-05-15T00:00:00.000Z",
        "headers": [
            {
                "name": "Authorization",
                "value": "Bearer <paste-token-here>"
            }
        ],
        "body": {}
    },
    {
        "_id": get_uuid(),
        "colId": col_id,
        "containerId": records_folder,
        "name": "Get Medical Reports",
        "url": f"{base_url}/api/records/reports/",
        "method": "GET",
        "sortNum": 40000,
        "created": "2026-05-15T00:00:00.000Z",
        "modified": "2026-05-15T00:00:00.000Z",
        "headers": [
            {
                "name": "Authorization",
                "value": "Bearer <paste-token-here>"
            }
        ],
        "body": {}
    },
    {
        "_id": get_uuid(),
        "colId": col_id,
        "containerId": metrics_folder,
        "name": "Add Health Metric",
        "url": f"{base_url}/api/metrics/health-metrics/",
        "method": "POST",
        "sortNum": 50000,
        "created": "2026-05-15T00:00:00.000Z",
        "modified": "2026-05-15T00:00:00.000Z",
        "headers": [
            {
                "name": "Authorization",
                "value": "Bearer <paste-token-here>"
            }
        ],
        "body": {
            "type": "json",
            "raw": "{\n  \"metric_type\": \"heart_rate\",\n  \"value\": 72.5,\n  \"unit\": \"bpm\",\n  \"source\": \"manual_entry\"\n}"
        }
    }
]

collection = {
    "clientName": "Thunder Client",
    "collectionName": "HealthCare API",
    "dateExported": "2026-05-15T00:00:00.000Z",
    "version": "1.2",
    "coreVersion": "2.2.0",
    "_id": col_id,
    "folders": folders,
    "requests": requests
}

with open("thunder-collection_HealthCare.json", "w") as f:
    json.dump(collection, f, indent=2)

print("Collection created!")
