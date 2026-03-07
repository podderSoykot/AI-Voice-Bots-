# API Documentation

This document provides detailed information about the AI Voice Bots API endpoints.

## Base URL

All API endpoints are prefixed with `/api/v1`.

## Authentication

Currently, the API does not require authentication. In production, implement proper authentication (API keys, OAuth, etc.).

## Response Format

All responses follow a standard format:

```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... }
}
```

Error responses:

```json
{
  "success": false,
  "message": "Error message",
  "errors": { ... }
}
```

## Endpoints

### Leads

#### Create Lead
- **POST** `/api/v1/leads`
- **Body**:
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
- **Query Parameters**:
  - `sync_crm` (boolean): Automatically sync to CRM after creation
- **Response**: Lead object

#### Get Leads
- **GET** `/api/v1/leads`
- **Query Parameters**:
  - `skip` (int): Pagination offset (default: 0)
  - `limit` (int): Number of results (default: 100, max: 1000)
  - `status_filter` (enum): Filter by lead status (new, contacted, qualified, etc.)
- **Response**: Array of lead objects

#### Get Lead
- **GET** `/api/v1/leads/{lead_id}`
- **Response**: Lead object with related calls and appointments

#### Update Lead
- **PUT** `/api/v1/leads/{lead_id}`
- **Body**: Partial lead update (all fields optional)
- **Query Parameters**:
  - `sync_crm` (boolean): Sync updates to CRM
- **Response**: Updated lead object

#### Delete Lead
- **DELETE** `/api/v1/leads/{lead_id}`
- **Response**: Success message

#### Bulk Create Leads
- **POST** `/api/v1/leads/bulk`
- **Body**:
  ```json
  {
    "leads": [
      { "name": "John Doe", "phone": "+1234567890", ... },
      { "name": "Jane Smith", "phone": "+0987654321", ... }
    ]
  }
  ```
- **Response**: Array of created leads

#### Sync Lead to CRM
- **POST** `/api/v1/leads/{lead_id}/sync-crm`
- **Query Parameters**:
  - `provider` (string): CRM provider ("hubspot" or "salesforce")
- **Response**: CRM sync result

### Calls

#### Initiate Call
- **POST** `/api/v1/calls/initiate`
- **Body**:
  ```json
  {
    "lead_id": 1,
    "phone_number": "+1234567890"
  }
  ```
- **Query Parameters**:
  - `assistant_id` (string): Vapi assistant ID to use
- **Response**: Call object and Vapi response

#### Get Calls
- **GET** `/api/v1/calls`
- **Query Parameters**:
  - `skip` (int): Pagination offset
  - `limit` (int): Number of results
  - `lead_id` (int): Filter by lead ID
- **Response**: Array of call objects

#### Get Call
- **GET** `/api/v1/calls/{call_id}`
- **Response**: Call object with lead information

#### Get Call by Vapi ID
- **GET** `/api/v1/calls/vapi/{vapi_call_id}`
- **Response**: Call object

#### Update Call
- **PUT** `/api/v1/calls/{call_id}`
- **Body**: Partial call update
- **Response**: Updated call object

#### Get Lead Calls
- **GET** `/api/v1/calls/lead/{lead_id}`
- **Response**: Array of call objects for the lead

### Appointments

#### Create Appointment
- **POST** `/api/v1/appointments`
- **Body**:
  ```json
  {
    "lead_id": 1,
    "scheduled_time": "2024-01-15T10:00:00Z",
    "notes": "Initial consultation"
  }
  ```
- **Query Parameters**:
  - `create_calendar_event` (boolean): Create Google Calendar event (default: true)
- **Response**: Appointment object

#### Get Appointments
- **GET** `/api/v1/appointments`
- **Query Parameters**:
  - `skip` (int): Pagination offset
  - `limit` (int): Number of results
  - `lead_id` (int): Filter by lead ID
  - `status_filter` (enum): Filter by status
- **Response**: Array of appointment objects

#### Get Appointment
- **GET** `/api/v1/appointments/{appointment_id}`
- **Response**: Appointment object with lead information

#### Update Appointment
- **PUT** `/api/v1/appointments/{appointment_id}`
- **Body**: Partial appointment update
- **Query Parameters**:
  - `update_calendar` (boolean): Update Google Calendar event (default: true)
- **Response**: Updated appointment object

#### Delete Appointment
- **DELETE** `/api/v1/appointments/{appointment_id}`
- **Query Parameters**:
  - `delete_calendar_event` (boolean): Delete Google Calendar event (default: true)
- **Response**: Success message

#### Get Lead Appointments
- **GET** `/api/v1/appointments/lead/{lead_id}`
- **Response**: Array of appointment objects for the lead

### Webhooks

#### Vapi Webhook
- **POST** `/api/v1/webhooks/vapi`
- **Body**: Vapi webhook payload
- **Description**: Handles call status updates, transcripts, and recordings from Vapi

#### CRM Webhook
- **POST** `/api/v1/webhooks/crm`
- **Body**: CRM webhook payload
- **Description**: Handles updates from CRM systems

#### Calendar Webhook
- **POST** `/api/v1/webhooks/calendar`
- **Body**: Calendar webhook payload
- **Description**: Handles calendar event updates

#### n8n Webhook
- **POST** `/api/v1/webhooks/n8n`
- **Body**: n8n webhook payload
- **Description**: Receives data from n8n workflows

## Data Models

### Lead
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "company": "Example Corp",
  "status": "new",
  "source": "website",
  "notes": "Interested in demo",
  "crm_id": "hubspot-123",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Call
```json
{
  "id": 1,
  "call_id": "vapi-call-123",
  "lead_id": 1,
  "direction": "outbound",
  "status": "completed",
  "outcome": "appointment_set",
  "duration": 180,
  "transcript": "Call transcript text...",
  "recording_url": "https://...",
  "started_at": "2024-01-01T10:00:00Z",
  "ended_at": "2024-01-01T10:03:00Z",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:03:00Z"
}
```

### Appointment
```json
{
  "id": 1,
  "lead_id": 1,
  "scheduled_time": "2024-01-15T10:00:00Z",
  "status": "scheduled",
  "calendar_event_id": "google-cal-123",
  "notes": "Initial consultation",
  "reminder_sent": "false",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## Error Codes

- `400` - Bad Request: Invalid input data
- `404` - Not Found: Resource not found
- `500` - Internal Server Error: Server error

## Rate Limiting

Currently, there is no rate limiting implemented. In production, implement appropriate rate limiting.

## Webhook Security

In production, implement webhook signature verification for all incoming webhooks to ensure they come from trusted sources.

