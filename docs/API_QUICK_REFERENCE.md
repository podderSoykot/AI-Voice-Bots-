# API Quick Reference Guide

Quick reference for the AI Voice Bots API endpoints.

## Base URL
```
http://localhost:8000/api/v1
```

## Leads

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/leads` | Create a new lead |
| GET | `/leads` | Get all leads (with filters) |
| GET | `/leads/{id}` | Get lead by ID |
| PUT | `/leads/{id}` | Update lead |
| DELETE | `/leads/{id}` | Delete lead |
| POST | `/leads/bulk` | Create multiple leads |
| POST | `/leads/{id}/sync-crm` | Sync lead to CRM |

### Create Lead
```bash
POST /api/v1/leads
Body: {
  "name": "John Doe",
  "phone": "+1234567890",
  "email": "john@example.com",
  "company": "Example Corp"
}
Query: ?sync_crm=true
```

## Calls

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/calls/initiate` | Initiate outbound call |
| GET | `/calls` | Get all calls |
| GET | `/calls/{id}` | Get call by ID |
| GET | `/calls/vapi/{vapi_id}` | Get call by Vapi ID |
| PUT | `/calls/{id}` | Update call |
| GET | `/calls/lead/{lead_id}` | Get calls for a lead |

### Initiate Call
```bash
POST /api/v1/calls/initiate
Body: {
  "lead_id": 1,
  "assistant_id": "vapi-assistant-123",
  "phone_number_id": "vapi-phone-456"
}
```

**Required**: `lead_id`, `assistant_id`

## Appointments

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/appointments` | Create appointment |
| GET | `/appointments` | Get all appointments |
| GET | `/appointments/{id}` | Get appointment by ID |
| PUT | `/appointments/{id}` | Update appointment |
| DELETE | `/appointments/{id}` | Delete appointment |
| GET | `/appointments/lead/{lead_id}` | Get appointments for a lead |

### Create Appointment
```bash
POST /api/v1/appointments
Body: {
  "lead_id": 1,
  "scheduled_time": "2024-01-20T14:00:00Z",
  "notes": "Initial consultation"
}
Query: ?create_calendar_event=true
```

## Webhooks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/webhooks/vapi` | Vapi webhook handler |
| POST | `/webhooks/crm` | CRM webhook handler |
| POST | `/webhooks/calendar` | Calendar webhook handler |
| POST | `/webhooks/n8n` | n8n webhook handler |

## Common Query Parameters

### Pagination
- `skip` (int): Offset (default: 0)
- `limit` (int): Limit (default: 100)

### Filters
- `status_filter` (enum): Filter by status
- `lead_id` (int): Filter by lead ID

## Response Format

### Success
```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... }
}
```

### Error
```json
{
  "success": false,
  "message": "Error message"
}
```

## Status Values

### Lead Status
- `new`, `contacted`, `qualified`, `appointment_set`, `converted`, `lost`

### Call Status
- `initiated`, `ringing`, `in_progress`, `completed`, `failed`, `no_answer`, `busy`

### Call Outcome
- `success`, `appointment_set`, `follow_up_needed`, `not_interested`, `wrong_number`, `no_answer`

### Appointment Status
- `scheduled`, `confirmed`, `rescheduled`, `cancelled`, `completed`, `no_show`

## Quick Examples

### Python
```python
import httpx

BASE = "http://localhost:8000/api/v1"

# Create lead
lead = httpx.post(f"{BASE}/leads", json={
    "name": "John Doe",
    "phone": "+1234567890"
}).json()["data"]

# Initiate call
call = httpx.post(f"{BASE}/calls/initiate", json={
    "lead_id": lead["id"],
    "assistant_id": "vapi-assistant-123"
}).json()["data"]
```

### cURL
```bash
# Create lead
curl -X POST "http://localhost:8000/api/v1/leads" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "phone": "+1234567890"}'

# Get leads
curl "http://localhost:8000/api/v1/leads?status_filter=qualified"
```

## Documentation Links

- **Full API Docs**: See `docs/API.md`
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

