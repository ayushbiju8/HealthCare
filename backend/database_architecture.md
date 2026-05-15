# Secure Healthcare Platform - Database Architecture

This document outlines the production-style database architecture for a secure, AI-powered healthcare awareness and monitoring platform built with Django and Django REST Framework.

---

## 1. Complete Modular App Structure

To ensure separation of concerns, maintainability, and microservice-readiness, the Django project is divided into the following modular apps:

*   **`users`**: Handles authentication, user profiles, and emergency contacts.
*   **`records`**: Manages medical reports (uploads, OCR, and API payloads).
*   **`metrics`**: Normalizes and stores structured health data extracted from reports and manual entries.
*   **`fitness`**: Handles wearable device connections and time-series fitness data.
*   **`reminders`**: Manages user alerts, medication schedules, and checkups.
*   **`ai_logs`**: Tracks AI interactions, prompt/response pairs, and token usage for analytics.
*   **`integrations`**: Logs all external API requests (hospitals, wearables) for debugging and auditing.

---

## 2. Detailed Database Design

### App: `users`

**Model: `User`** (Custom User Model)
*   **Purpose**: Core authentication and identity management.
*   **Fields**:
    *   `id` (UUID, Primary Key)
    *   `email` (EmailField, Unique)
    *   `password` (CharField)
    *   `is_active`, `is_staff` (BooleanField)
    *   `created_at`, `updated_at` (DateTimeField)
*   **Nullable**: None.
*   **Indexing**: `email`.

**Model: `HealthProfile`**
*   **Purpose**: Stores sensitive, healthcare-specific personal data.
*   **Fields**:
    *   `user` (OneToOneField -> User)
    *   `date_of_birth` (DateField)
    *   `blood_group` (CharField, Nullable)
    *   `height_cm` (DecimalField, Nullable)
    *   `weight_kg` (DecimalField, Nullable)
    *   `allergies` (JSONField, default=list) - List of known allergies.
    *   `chronic_conditions` (JSONField, default=list) - List of conditions (e.g., Asthma, Type 2 Diabetes).
    *   `updated_at` (DateTimeField)

**Model: `EmergencyContact`**
*   **Purpose**: Quick access to emergency contacts.
*   **Fields**:
    *   `id` (UUID, Primary Key)
    *   `user` (ForeignKey -> User, related_name='emergency_contacts')
    *   `name` (CharField)
    *   `relation` (CharField)
    *   `phone_number` (CharField)
    *   `created_at` (DateTimeField)

### App: `records`

**Model: `MedicalReport`**
*   **Purpose**: The central source of truth for all medical documents, regardless of origin.
*   **Fields**:
    *   `id` (UUID, Primary Key)
    *   `user` (ForeignKey -> User, related_name='reports')
    *   `title` (CharField)
    *   `report_type` (CharField, Choices: `UPLOAD_PDF`, `UPLOAD_IMG`, `API_FETCH`, `OCR_SCAN`)
    *   `date_issued` (DateField)
    *   `source_hospital` (CharField, Nullable)
    *   `file` (FileField, Nullable) - Encrypted S3 bucket path.
    *   `raw_api_payload` (JSONField, Nullable) - Stores the exact response from a hospital API before normalization.
    *   `ocr_extracted_text` (TextField, Nullable) - Text output from the OCR service.
    *   `ai_summary` (TextField, Nullable) - AI generated layman summary.
    *   `processing_status` (CharField, Choices: `PENDING`, `PROCESSED`, `FAILED`)
    *   `created_at`, `updated_at` (DateTimeField)
*   **Indexing**: `user`, `date_issued`, `processing_status`.

### App: `metrics`

**Model: `HealthMetric`**
*   **Purpose**: Normalized, queryable medical values extracted from `MedicalReport` or synced from wearables. This powers analytics and trends.
*   **Fields**:
    *   `id` (UUID, Primary Key)
    *   `user` (ForeignKey -> User, related_name='metrics')
    *   `report` (ForeignKey -> MedicalReport, Nullable, on_delete=SET_NULL) - Links back to the source.
    *   `metric_type` (CharField, Choices: `GLUCOSE`, `CHOLESTEROL`, `BP_SYS`, `BP_DIA`, `HEART_RATE`)
    *   `value_numeric` (DecimalField)
    *   `unit` (CharField) - e.g., 'mg/dL', 'bpm'.
    *   `measured_at` (DateTimeField)
    *   `created_at` (DateTimeField)
*   **Indexing**: `user`, `metric_type`, `measured_at`.

### App: `fitness`

**Model: `WearableIntegration`**
*   **Purpose**: Manages OAuth state for fitness wearables.
*   **Fields**:
    *   `id` (UUID, Primary Key)
    *   `user` (ForeignKey -> User)
    *   `provider` (CharField, Choices: `APPLE_HEALTH`, `GOOGLE_FIT`, `GARMIN`)
    *   `access_token` (TextField) - Encrypted at rest.
    *   `refresh_token` (TextField) - Encrypted at rest.
    *   `token_expires_at` (DateTimeField)
    *   `is_active` (BooleanField, default=True)

**Model: `DailyFitnessSummary`**
*   **Purpose**: Aggregates time-series wearable data to prevent database bloat.
*   **Fields**:
    *   `id` (UUID, Primary Key)
    *   `user` (ForeignKey -> User)
    *   `date` (DateField)
    *   `total_steps` (IntegerField, default=0)
    *   `avg_heart_rate` (IntegerField, Nullable)
    *   `calories_burned` (DecimalField, Nullable)
    *   `sleep_minutes` (IntegerField, Nullable)
    *   `avg_spo2` (DecimalField, Nullable)
    *   `raw_payload` (JSONField, Nullable) - Holds minute-by-minute arrays if deep-dive is needed later.
*   **Constraints**: Unique together on `(user, date)`.

### App: `reminders`

**Model: `Reminder`**
*   **Purpose**: Manages all actionable notifications for the user.
*   **Fields**:
    *   `id` (UUID, Primary Key)
    *   `user` (ForeignKey -> User)
    *   `type` (CharField, Choices: `MEDICINE`, `VACCINATION`, `CHECKUP`)
    *   `title` (CharField)
    *   `due_datetime` (DateTimeField)
    *   `recurrence_rule` (CharField, Nullable) - RRULE string (e.g., `FREQ=DAILY`).
    *   `is_active` (BooleanField, default=True)
    *   `last_triggered_at` (DateTimeField, Nullable)

### App: `ai_logs` & `integrations`

**Model: `AILog`**
*   **Purpose**: Auditability for AI interactions (Prompt/Response tracking).
*   **Fields**: `id`, `user` (Nullable), `context` (Choices: `OCR_SUMMARY`, `GENERAL_CHAT`), `prompt` (TextField), `response` (TextField), `tokens_used` (IntegerField), `created_at`.

**Model: `APILog`**
*   **Purpose**: Tracks stability and errors of external hospital/wearable API calls.
*   **Fields**: `id`, `integration_name`, `endpoint`, `status_code`, `request_payload` (JSONField), `response_payload` (JSONField), `duration_ms`, `created_at`.

---

## 3. Relationship Architecture

*   **Foreign Keys (Many-to-One)**: All domain models (`MedicalReport`, `HealthMetric`, `Reminder`, etc.) have an FK to `User`. This enables complete data isolation and easy GDPR deletion.
*   **One-to-One**: `HealthProfile` is a 1:1 with `User`. It prevents the core auth table from becoming bloated with nullable medical fields.
*   **Loose Coupling via Nullable FKs**: `HealthMetric` has a nullable FK to `MedicalReport`. If a user manually inputs their blood pressure, the report is NULL. If it was extracted via OCR, the FK points to the document for traceability.
*   **Normalization Strategy**:
    *   **Highly Normalized**: `HealthMetric` uses an EAV-like (Entity-Attribute-Value) pattern (`metric_type`, `value_numeric`) to ensure we don't have to alter the schema every time we track a new health marker (e.g., adding Vitamin D).
    *   **Denormalized/Schemaless**: `raw_api_payload` and `allergies` use `JSONField`. Hospital APIs return vastly different JSON structures; forcing them into relational tables immediately loses data. We store the raw JSON, then process it asynchronously to extract standard `HealthMetric` rows.

---

## 4. Suggested Constraints & Database Tuning

1.  **Unique Constraints**:
    *   `User.email` must be unique.
    *   `DailyFitnessSummary`: `UniqueConstraint(fields=['user', 'date'])` prevents duplicate daily aggregates.
2.  **Indexing**:
    *   B-Tree indexes on `(user_id, date_issued)` in `MedicalReport` (most common dashboard query).
    *   Index on `metric_type` and `measured_at` in `HealthMetric` for fast time-series graph generation.
3.  **Cascades**:
    *   `User` deletion should `CASCADE` to `HealthProfile`, `EmergencyContact`, and `WearableIntegration`.
    *   `User` deletion should `SET_NULL` for `AILog` (to retain anonymized AI analytics) or soft-delete depending on legal requirements.
4.  **Validations**:
    *   Add Postgres `CheckConstraint` on `HealthMetric.value_numeric > 0`.

---

## 5. Scalability Considerations

*   **JSONField for Raw Data**: By saving hospital payloads and wearable payloads in `JSONField`s, the ingestion API never drops data if an upstream provider adds a new field. We can re-process historical JSON later if our parsing logic improves.
*   **Metric Normalization (`HealthMetric`)**: By splitting extracted data (e.g., Fasting Glucose: 110) out of the OCR text/JSON and into dedicated `HealthMetric` rows, graphing and trend analysis (e.g., "Show glucose over 6 months") becomes an extremely fast, simple `SELECT` query, rather than an expensive JSON path or full-text search.
*   **Async Processing Compatibility**: The `processing_status` on `MedicalReport` enables an event-driven architecture. The user uploads a PDF -> status is `PENDING` -> Celery worker picks it up -> calls OCR -> calls AI for summary -> saves to `HealthMetric` -> updates status to `PROCESSED`.

---

## 6. Security Considerations

*   **Secure File Handling**: `FileField`s should never be served directly. They should point to a private S3 bucket. Django should generate pre-signed URLs with short expirations (e.g., 5 mins) for the frontend to view PDFs.
*   **Token Encryption**: `access_token` and `refresh_token` in `WearableIntegration` MUST be encrypted at rest using a package like `django-fernet-fields` or Postgres-level encryption. A database dump should not expose user API keys.
*   **Audit Logging**: The `AILog` and `APILog` act as immutable trails. If the AI hallucinates a critical health summary, you have the exact prompt and response stored for debugging and legal protection.
*   **Access Separation**: Using UUIDs instead of sequential Integers prevents an attacker from scraping data by guessing `report/1/`, `report/2/` (Insecure Direct Object Reference - IDOR).

---

## 7. Production-Level Suggestions

*   **Timestamps & Soft Deletes**: Use a base model class for all models that automatically adds `created_at` and `updated_at`. Consider implementing soft deletes (an `is_deleted` boolean) for medical records to prevent accidental data loss.
*   **Status Enums**: Use Django 3.0+ `models.TextChoices` for all status and type fields to ensure type safety in code.
*   **Database Choice**: PostgreSQL is highly recommended due to its superior `JSONB` indexing capabilities (GIN indexes), which are critical for querying `raw_api_payload` or `allergies` efficiently. SQLite can be used for local dev but will lack advanced JSON querying.

---

## 8. Final Recommended MVP Models

For the hackathon MVP, prioritize the following models. The others can be mocked or deferred to post-MVP.

**MUST HAVE MODELS (Core Loop):**
1.  `User`
2.  `HealthProfile`
3.  `MedicalReport` (With OCR/JSON fields)
4.  `HealthMetric` (Crucial for showing graphs/AI insights)
5.  `AILog` (To prove the AI integration works)

**OPTIONAL MODELS (Implement if time permits):**
1.  `Reminder` (Can be simulated on the frontend initially)
2.  `WearableIntegration` & `DailyFitnessSummary` (Complex OAuth flows; consider mocking fitness data via a script for the MVP presentation).
3.  `APILog`
4.  `EmergencyContact`
