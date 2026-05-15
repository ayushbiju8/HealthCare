import json

base_url = "http://127.0.0.1:8000"

collection = {
    "info": {
        "name": "HealthCare MVP API",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": [
        {
            "name": "Auth",
            "item": [
                {
                    "name": "Register User",
                    "request": {
                        "method": "POST",
                        "header": [{"key": "Content-Type", "value": "application/json"}],
                        "body": {
                            "mode": "raw",
                            "raw": "{\n  \"email\": \"newuser@example.com\",\n  \"password\": \"password123\",\n  \"first_name\": \"John\",\n  \"last_name\": \"Doe\"\n}"
                        },
                        "url": {"raw": f"{base_url}/api/auth/register/", "host": ["127", "0", "0", "1"], "port": "8000", "path": ["api", "auth", "register", ""]}
                    }
                },
                {
                    "name": "Login (Get JWT)",
                    "request": {
                        "method": "POST",
                        "header": [{"key": "Content-Type", "value": "application/json"}],
                        "body": {
                            "mode": "raw",
                            "raw": "{\n  \"email\": \"testuser@example.com\",\n  \"password\": \"testpass123\"\n}"
                        },
                        "url": {"raw": f"{base_url}/api/auth/login/", "host": ["127", "0", "0", "1"], "port": "8000", "path": ["api", "auth", "login", ""]}
                    }
                },
                {
                    "name": "Get Profile",
                    "request": {
                        "method": "GET",
                        "header": [{"key": "Authorization", "value": "Bearer <paste-token-here>"}],
                        "url": {"raw": f"{base_url}/api/auth/profile/", "host": ["127", "0", "0", "1"], "port": "8000", "path": ["api", "auth", "profile", ""]}
                    }
                }
            ]
        },
        {
            "name": "Records",
            "item": [
                {
                    "name": "Get Medical Reports",
                    "request": {
                        "method": "GET",
                        "header": [{"key": "Authorization", "value": "Bearer <paste-token-here>"}],
                        "url": {"raw": f"{base_url}/api/records/reports/", "host": ["127", "0", "0", "1"], "port": "8000", "path": ["api", "records", "reports", ""]}
                    }
                }
            ]
        },
        {
            "name": "Metrics",
            "item": [
                {
                    "name": "Add Health Metric",
                    "request": {
                        "method": "POST",
                        "header": [{"key": "Content-Type", "value": "application/json"}, {"key": "Authorization", "value": "Bearer <paste-token-here>"}],
                        "body": {
                            "mode": "raw",
                            "raw": "{\n  \"metric_type\": \"heart_rate\",\n  \"value\": 72.5,\n  \"unit\": \"bpm\",\n  \"source\": \"manual_entry\"\n}"
                        },
                        "url": {"raw": f"{base_url}/api/metrics/health-metrics/", "host": ["127", "0", "0", "1"], "port": "8000", "path": ["api", "metrics", "health-metrics", ""]}
                    }
                }
            ]
        }
    ]
}

with open("postman_collection_HealthCare.json", "w") as f:
    json.dump(collection, f, indent=2)

print("Postman Collection created!")
