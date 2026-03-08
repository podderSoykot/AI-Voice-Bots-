# API Documentation

Complete guide to the AI Voice Bots API for managing leads, calls, appointments, and integrations.

## Table of Contents

- [Base URL & Configuration](#base-url--configuration)
- [Authentication](#authentication)
- [Response Format](#response-format)
- [Leads API](#leads-api)
- [Calls API](#calls-api)
- [Appointments API](#appointments-api)
- [Webhooks API](#webhooks-api)
- [Data Models](#data-models)
- [Usage Examples](#usage-examples)
- [Error Handling](#error-handling)

---

## Base URL & Configuration

**Base URL**: `http://localhost:8000` (development)  
**API Prefix**: `/api/v1`  
**Documentation**: `http://localhost:8000/docs` (Swagger UI)  
**Alternative Docs**: `http://localhost:8000/redoc`

All endpoints are prefixed with `/api/v1`.

---

## Authentication

Currently, the API does not require authentication. In production, implement proper authentication (API keys, OAuth, JWT tokens, etc.).

---

## Response Format

All API responses follow a standardized format:

### Success Response
```json
{
  "success": true,
  "message": "Operation successful",
  "data": {
    // Response data here
  }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error description",
  "errors": {
    // Optional: Detailed error information
  }
}
```

### HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors)
- `404` - Not Found
- `500` - Internal Server Error

---

## Leads API

Manage leads (potential customers) in your system.

### Create Lead

Create a new lead in the system.

**Endpoint**: `POST /api/v1/leads`

**Request Body**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "company": "Example Corp",
  "source": "website",
  "notes": "Interested in product demo"
}
```

**Query Parameters**:
- `sync_crm` (boolean, optional): Automatically sync to CRM after creation (default: `false`)

**Required Fields**:
- `name` (string, 1-255 chars): Lead's full name
- `phone` (string, 10-20 chars): Phone number

**Optional Fields**:
- `email` (string, valid email): Email address
- `company` (string, max 255 chars): Company name
- `source` (string, max 100 chars): Lead source (e.g., "website", "referral", "ad")
- `notes` (string, max 1000 chars): Additional notes

**Response** (201 Created):
```json
{
  "success": true,
  "message": "Lead created successfully",
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "company": "Example Corp",
    "status": "new",
    "source": "website",
    "notes": "Interested in product demo",
    "crm_id": null,
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
  }
}
```

**Usage Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/leads?sync_crm=true" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "company": "Example Corp",
    "source": "website"
  }'
```

---

### Get All Leads

Retrieve a list of leads with optional filtering and pagination.

**Endpoint**: `GET /api/v1/leads`

**Query Parameters**:
- `skip` (int, optional): Number of records to skip (default: `0`)
- `limit` (int, optional): Maximum number of records to return (default: `100`, max: `1000`)
- `status_filter` (enum, optional): Filter by lead status
  - Values: `new`, `contacted`, `qualified`, `appointment_set`, `converted`, `lost`

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Leads retrieved successfully",
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1234567890",
      "status": "new",
      "created_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

**Usage Example**:
```bash
# Get all leads
curl "http://localhost:8000/api/v1/leads"

# Get qualified leads only
curl "http://localhost:8000/api/v1/leads?status_filter=qualified"

# Paginated results
curl "http://localhost:8000/api/v1/leads?skip=0&limit=50"
```

---

### Get Lead by ID

Retrieve a specific lead with all related information.

**Endpoint**: `GET /api/v1/leads/{lead_id}`

**Path Parameters**:
- `lead_id` (int, required): Lead ID

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Lead retrieved successfully",
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "company": "Example Corp",
    "status": "new",
    "source": "website",
    "notes": "Interested in product demo",
    "crm_id": "hubspot-123",
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
  }
}
```

**Error Response** (404 Not Found):
```json
{
  "success": false,
  "message": "Lead with ID 999 not found"
}
```

---

### Update Lead

Update an existing lead's information.

**Endpoint**: `PUT /api/v1/leads/{lead_id}`

**Path Parameters**:
- `lead_id` (int, required): Lead ID

**Request Body** (all fields optional):
```json
{
  "name": "John Smith",
  "email": "john.smith@example.com",
  "phone": "+1234567891",
  "company": "New Company",
  "status": "qualified",
  "source": "referral",
  "notes": "Updated notes",
  "crm_id": "hubspot-456"
}
```

**Query Parameters**:
- `sync_crm` (boolean, optional): Sync updates to CRM (default: `false`)

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Lead updated successfully",
  "data": {
    "id": 1,
    "name": "John Smith",
    "status": "qualified",
    "updated_at": "2024-01-15T11:00:00Z"
  }
}
```

**Usage Example**:
```bash
curl -X PUT "http://localhost:8000/api/v1/leads/1?sync_crm=true" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "qualified",
    "notes": "Lead is interested in enterprise plan"
  }'
```

---

### Delete Lead

Delete a lead from the system. This will also delete all associated calls and appointments.

**Endpoint**: `DELETE /api/v1/leads/{lead_id}`

**Path Parameters**:
- `lead_id` (int, required): Lead ID

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Lead deleted successfully",
  "data": null
}
```

---

### Bulk Create Leads

Create multiple leads in a single request.

**Endpoint**: `POST /api/v1/leads/bulk`

**Request Body**:
```json
{
  "leads": [
    {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1234567890",
      "company": "Company A"
    },
    {
      "name": "Jane Smith",
      "email": "jane@example.com",
      "phone": "+0987654321",
      "company": "Company B"
    }
  ]
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "message": "Successfully created 2 leads",
  "data": {
    "leads": [
      {
        "id": 1,
        "name": "John Doe",
        "phone": "+1234567890"
      },
      {
        "id": 2,
        "name": "Jane Smith",
        "phone": "+0987654321"
      }
    ],
    "count": 2
  }
}
```

---

### Sync Lead to CRM

Manually sync a lead to your CRM system (HubSpot or Salesforce).

**Endpoint**: `POST /api/v1/leads/{lead_id}/sync-crm`

**Path Parameters**:
- `lead_id` (int, required): Lead ID

**Query Parameters**:
- `provider` (string, optional): CRM provider - `"hubspot"` or `"salesforce"` (default: `"hubspot"`)

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Lead synced to CRM successfully",
  "data": {
    "crm_id": "hubspot-12345",
    "provider": "hubspot"
  }
}
```

**Usage Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/leads/1/sync-crm?provider=hubspot"
```

---

## Calls API

Manage AI voice calls initiated through Vapi.

### Initiate Call

Start an outbound AI voice call to a lead.

**Endpoint**: `POST /api/v1/calls/initiate`

**Request Body**:
```json
{
  "lead_id": 1,
  "phone_number": "+1234567890",
  "assistant_id": "vapi-assistant-123",
  "phone_number_id": "vapi-phone-456"
}
```

**Required Fields**:
- `lead_id` (int): ID of the lead to call
- `assistant_id` (string): Vapi assistant ID to use for the call

**Optional Fields**:
- `phone_number` (string): Phone number to call (defaults to lead's phone if not provided)
- `phone_number_id` (string): Vapi phone number ID to call from (your Vapi phone number)

**Response** (201 Created):
```json
{
  "success": true,
  "message": "Call initiated successfully",
  "data": {
    "call": {
      "id": 1,
      "call_id": "vapi-call-789",
      "lead_id": 1,
      "direction": "outbound",
      "status": "initiated",
      "created_at": "2024-01-15T10:00:00Z"
    },
    "vapi_response": {
      "id": "vapi-call-789",
      "status": "queued"
    }
  }
}
```

**Usage Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/calls/initiate" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_id": 1,
    "assistant_id": "vapi-assistant-123",
    "phone_number_id": "vapi-phone-456"
  }'
```

**Important Notes**:
- The `assistant_id` must be a valid Vapi assistant ID created in your Vapi dashboard
- The `phone_number_id` is optional but recommended - it's the ID of the phone number you're calling FROM
- If `phone_number` is not provided, the system uses the lead's phone number
- The call status will be updated automatically via webhooks from Vapi

---

### Get All Calls

Retrieve a list of calls with optional filtering.

**Endpoint**: `GET /api/v1/calls`

**Query Parameters**:
- `skip` (int, optional): Pagination offset (default: `0`)
- `limit` (int, optional): Number of results (default: `100`)
- `lead_id` (int, optional): Filter by lead ID

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Calls retrieved successfully",
  "data": [
    {
      "id": 1,
      "call_id": "vapi-call-789",
      "lead_id": 1,
      "direction": "outbound",
      "status": "completed",
      "outcome": "appointment_set",
      "duration": 180,
      "created_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

---

### Get Call by ID

Retrieve a specific call record.

**Endpoint**: `GET /api/v1/calls/{call_id}`

**Path Parameters**:
- `call_id` (int, required): Call ID

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Call retrieved successfully",
  "data": {
    "id": 1,
    "call_id": "vapi-call-789",
    "lead_id": 1,
    "direction": "outbound",
    "status": "completed",
    "outcome": "appointment_set",
    "duration": 180,
    "transcript": "Call transcript text...",
    "recording_url": "https://vapi.ai/recordings/...",
    "started_at": "2024-01-15T10:00:00Z",
    "ended_at": "2024-01-15T10:03:00Z",
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:03:00Z"
  }
}
```

---

### Get Call by Vapi ID

Retrieve a call using the Vapi call ID.

**Endpoint**: `GET /api/v1/calls/vapi/{vapi_call_id}`

**Path Parameters**:
- `vapi_call_id` (string, required): Vapi call ID

**Response**: Same as Get Call by ID

---

### Update Call

Update a call record (typically used for manual updates or corrections).

**Endpoint**: `PUT /api/v1/calls/{call_id}`

**Path Parameters**:
- `call_id` (int, required): Call ID

**Request Body** (all fields optional):
```json
{
  "status": "completed",
  "outcome": "appointment_set",
  "duration": 180,
  "transcript": "Updated transcript...",
  "recording_url": "https://...",
  "started_at": "2024-01-15T10:00:00Z",
  "ended_at": "2024-01-15T10:03:00Z"
}
```

**Status Values**:
- `initiated` - Call has been initiated
- `ringing` - Phone is ringing
- `in_progress` - Call is in progress
- `completed` - Call completed successfully
- `failed` - Call failed
- `no_answer` - No answer
- `busy` - Line busy

**Outcome Values**:
- `success` - Successful call
- `appointment_set` - Appointment was scheduled
- `follow_up_needed` - Follow-up required
- `not_interested` - Lead not interested
- `wrong_number` - Wrong phone number
- `no_answer` - No answer

---

### Get Lead Calls

Get all calls for a specific lead.

**Endpoint**: `GET /api/v1/calls/lead/{lead_id}`

**Path Parameters**:
- `lead_id` (int, required): Lead ID

**Response**: Array of call objects (same format as Get All Calls)

---

## Appointments API

Manage appointments and calendar integration.

### Create Appointment

Schedule an appointment with a lead.

**Endpoint**: `POST /api/v1/appointments`

**Request Body**:
```json
{
  "lead_id": 1,
  "scheduled_time": "2024-01-20T14:00:00Z",
  "notes": "Initial consultation call"
}
```

**Required Fields**:
- `lead_id` (int): Lead ID
- `scheduled_time` (datetime, ISO 8601): Appointment date and time

**Optional Fields**:
- `notes` (string, max 1000 chars): Appointment notes

**Query Parameters**:
- `create_calendar_event` (boolean, optional): Create Google Calendar event (default: `true`)

**Response** (201 Created):
```json
{
  "success": true,
  "message": "Appointment created successfully",
  "data": {
    "id": 1,
    "lead_id": 1,
    "scheduled_time": "2024-01-20T14:00:00Z",
    "status": "scheduled",
    "calendar_event_id": "google-cal-123",
    "notes": "Initial consultation call",
    "reminder_sent": "false",
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
  }
}
```

**Usage Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/appointments?create_calendar_event=true" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_id": 1,
    "scheduled_time": "2024-01-20T14:00:00Z",
    "notes": "Initial consultation"
  }'
```

---

### Get All Appointments

Retrieve appointments with optional filtering.

**Endpoint**: `GET /api/v1/appointments`

**Query Parameters**:
- `skip` (int, optional): Pagination offset (default: `0`)
- `limit` (int, optional): Number of results (default: `100`)
- `lead_id` (int, optional): Filter by lead ID
- `status_filter` (enum, optional): Filter by status
  - Values: `scheduled`, `confirmed`, `rescheduled`, `cancelled`, `completed`, `no_show`

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Appointments retrieved successfully",
  "data": [
    {
      "id": 1,
      "lead_id": 1,
      "scheduled_time": "2024-01-20T14:00:00Z",
      "status": "scheduled",
      "calendar_event_id": "google-cal-123",
      "notes": "Initial consultation"
    }
  ]
}
```

---

### Get Appointment by ID

Retrieve a specific appointment.

**Endpoint**: `GET /api/v1/appointments/{appointment_id}`

**Path Parameters**:
- `appointment_id` (int, required): Appointment ID

**Response**: Appointment object (same format as Create Appointment)

---

### Update Appointment

Update an existing appointment.

**Endpoint**: `PUT /api/v1/appointments/{appointment_id}`

**Path Parameters**:
- `appointment_id` (int, required): Appointment ID

**Request Body** (all fields optional):
```json
{
  "scheduled_time": "2024-01-21T15:00:00Z",
  "status": "confirmed",
  "notes": "Updated notes",
  "calendar_event_id": "google-cal-456"
}
```

**Query Parameters**:
- `update_calendar` (boolean, optional): Update Google Calendar event (default: `true`)

**Status Values**:
- `scheduled` - Appointment scheduled
- `confirmed` - Appointment confirmed
- `rescheduled` - Appointment rescheduled
- `cancelled` - Appointment cancelled
- `completed` - Appointment completed
- `no_show` - Lead didn't show up

---

### Delete Appointment

Delete an appointment.

**Endpoint**: `DELETE /api/v1/appointments/{appointment_id}`

**Path Parameters**:
- `appointment_id` (int, required): Appointment ID

**Query Parameters**:
- `delete_calendar_event` (boolean, optional): Delete Google Calendar event (default: `true`)

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Appointment deleted successfully",
  "data": null
}
```

---

### Get Lead Appointments

Get all appointments for a specific lead.

**Endpoint**: `GET /api/v1/appointments/lead/{lead_id}`

**Path Parameters**:
- `lead_id` (int, required): Lead ID

**Response**: Array of appointment objects

---

## Webhooks API

Receive events from external services.

### Vapi Webhook

Receive call events from Vapi (call status updates, transcripts, recordings).

**Endpoint**: `POST /api/v1/webhooks/vapi`

**Request Body**: Vapi webhook payload (format depends on event type)

**Event Types Handled**:
- `call-status-update` - Call status changed
- `call-end` - Call ended
- `transcript` - Transcript available
- `recording` - Recording available

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Webhook processed successfully",
  "data": null
}
```

**Setup Instructions**:
1. Configure webhook URL in Vapi dashboard: `https://your-domain.com/api/v1/webhooks/vapi`
2. Select events to receive: status updates, transcripts, recordings
3. Webhook will automatically update call records in the database

---

### CRM Webhook

Receive updates from CRM systems (HubSpot, Salesforce).

**Endpoint**: `POST /api/v1/webhooks/crm`

**Request Body**: CRM webhook payload (provider-specific format)

**Response** (200 OK):
```json
{
  "success": true,
  "message": "CRM webhook processed successfully",
  "data": null
}
```

---

### Calendar Webhook

Receive calendar event updates from Google Calendar.

**Endpoint**: `POST /api/v1/webhooks/calendar`

**Request Body**: Calendar webhook payload

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Calendar webhook processed successfully",
  "data": null
}
```

---

### n8n Webhook

Receive data from n8n automation workflows.

**Endpoint**: `POST /api/v1/webhooks/n8n`

**Request Body**: n8n webhook payload (custom format)

**Response** (200 OK):
```json
{
  "success": true,
  "message": "n8n webhook processed successfully",
  "data": null
}
```

---

## Data Models

### Lead Model

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "company": "Example Corp",
  "status": "new",
  "source": "website",
  "notes": "Interested in product demo",
  "crm_id": "hubspot-123",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

**Status Values**:
- `new` - New lead
- `contacted` - Lead has been contacted
- `qualified` - Lead is qualified
- `appointment_set` - Appointment scheduled
- `converted` - Lead converted to customer
- `lost` - Lead lost

---

### Call Model

```json
{
  "id": 1,
  "call_id": "vapi-call-789",
  "lead_id": 1,
  "direction": "outbound",
  "status": "completed",
  "outcome": "appointment_set",
  "duration": 180,
  "transcript": "Full call transcript text...",
  "recording_url": "https://vapi.ai/recordings/...",
  "started_at": "2024-01-15T10:00:00Z",
  "ended_at": "2024-01-15T10:03:00Z",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:03:00Z"
}
```

**Direction Values**:
- `inbound` - Incoming call
- `outbound` - Outgoing call

---

### Appointment Model

```json
{
  "id": 1,
  "lead_id": 1,
  "scheduled_time": "2024-01-20T14:00:00Z",
  "status": "scheduled",
  "calendar_event_id": "google-cal-123",
  "notes": "Initial consultation call",
  "reminder_sent": "false",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

---

## Usage Examples

### Complete Workflow Example

Here's a complete example of creating a lead, initiating a call, and scheduling an appointment:

```bash
# 1. Create a lead
LEAD_RESPONSE=$(curl -X POST "http://localhost:8000/api/v1/leads" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "company": "Example Corp",
    "source": "website"
  }')

LEAD_ID=$(echo $LEAD_RESPONSE | jq -r '.data.id')
echo "Created lead with ID: $LEAD_ID"

# 2. Initiate a call
curl -X POST "http://localhost:8000/api/v1/calls/initiate" \
  -H "Content-Type: application/json" \
  -d "{
    \"lead_id\": $LEAD_ID,
    \"assistant_id\": \"vapi-assistant-123\",
    \"phone_number_id\": \"vapi-phone-456\"
  }"

# 3. Schedule an appointment (after call)
curl -X POST "http://localhost:8000/api/v1/appointments" \
  -H "Content-Type: application/json" \
  -d "{
    \"lead_id\": $LEAD_ID,
    \"scheduled_time\": \"2024-01-20T14:00:00Z\",
    \"notes\": \"Scheduled during call\"
  }"

# 4. Update lead status
curl -X PUT "http://localhost:8000/api/v1/leads/$LEAD_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "appointment_set"
  }'
```

### Python Example

```python
import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api/v1"

# Create a lead
response = httpx.post(f"{BASE_URL}/leads", json={
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "company": "Example Corp",
    "source": "website"
})
lead = response.json()["data"]
lead_id = lead["id"]

# Initiate a call
call_response = httpx.post(f"{BASE_URL}/calls/initiate", json={
    "lead_id": lead_id,
    "assistant_id": "vapi-assistant-123",
    "phone_number_id": "vapi-phone-456"
})
call = call_response.json()["data"]

# Schedule an appointment
scheduled_time = datetime.utcnow() + timedelta(days=1)
appointment_response = httpx.post(f"{BASE_URL}/appointments", json={
    "lead_id": lead_id,
    "scheduled_time": scheduled_time.isoformat(),
    "notes": "Initial consultation"
})
appointment = appointment_response.json()["data"]

# Sync to CRM
httpx.post(f"{BASE_URL}/leads/{lead_id}/sync-crm?provider=hubspot")
```

### JavaScript/Node.js Example

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000/api/v1';

async function createLeadAndCall() {
  // Create a lead
  const leadResponse = await axios.post(`${BASE_URL}/leads`, {
    name: 'John Doe',
    email: 'john@example.com',
    phone: '+1234567890',
    company: 'Example Corp',
    source: 'website'
  });
  
  const lead = leadResponse.data.data;
  const leadId = lead.id;
  
  // Initiate a call
  const callResponse = await axios.post(`${BASE_URL}/calls/initiate`, {
    lead_id: leadId,
    assistant_id: 'vapi-assistant-123',
    phone_number_id: 'vapi-phone-456'
  });
  
  // Schedule an appointment
  const appointmentTime = new Date();
  appointmentTime.setDate(appointmentTime.getDate() + 1);
  
  const appointmentResponse = await axios.post(`${BASE_URL}/appointments`, {
    lead_id: leadId,
    scheduled_time: appointmentTime.toISOString(),
    notes: 'Initial consultation'
  });
  
  return {
    lead: lead,
    call: callResponse.data.data,
    appointment: appointmentResponse.data.data
  };
}

createLeadAndCall().then(console.log);
```

---

## Error Handling

### Common Errors

**400 Bad Request** - Validation Error:
```json
{
  "detail": "assistant_id is required to initiate a call"
}
```

**404 Not Found**:
```json
{
  "detail": "Lead with ID 999 not found"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "Error creating lead: Database connection failed"
}
```

### Best Practices

1. **Always check response status**: Check the `success` field in the response
2. **Handle errors gracefully**: Implement retry logic for transient errors
3. **Validate input**: Ensure required fields are provided and properly formatted
4. **Use pagination**: For list endpoints, use `skip` and `limit` to paginate results
5. **Monitor webhooks**: Ensure webhook endpoints are accessible and properly configured

---

## Rate Limiting

Currently, there is no rate limiting implemented. In production, implement appropriate rate limiting to prevent abuse.

---

## Webhook Security

In production, implement webhook signature verification for all incoming webhooks to ensure they come from trusted sources:

- **Vapi**: Verify webhook signatures using your Vapi webhook secret
- **HubSpot**: Verify webhook signatures using HubSpot's signature verification
- **Google Calendar**: Use proper authentication and verification

---

## Additional Resources

- **Swagger UI**: `http://localhost:8000/docs` - Interactive API documentation
- **ReDoc**: `http://localhost:8000/redoc` - Alternative API documentation
- **Health Check**: `GET /health` - Check API health status

---

## Support

For issues or questions:
1. Check the Swagger UI documentation at `/docs`
2. Review error messages in API responses
3. Check server logs for detailed error information
4. Ensure all required environment variables are configured

---

**Last Updated**: 2024-01-15  
**API Version**: 1.0.0
