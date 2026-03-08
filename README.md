# AI Voice Bots - Sales & Marketing Engine

A comprehensive AI Voice Bot system built with FastAPI for managing sales calls, lead qualification, and appointment setting. This system integrates with Vapi for voice AI, HubSpot/Salesforce for CRM, Google Calendar for scheduling, and n8n for workflow automation.

## Features

- **AI Voice Bot Management**: Create and configure Vapi agents for sales calls
- **Lead Management**: Complete CRUD operations for leads with CRM synchronization
- **Call Orchestration**: Initiate outbound calls, track call history, and store transcripts
- **Appointment Setting**: Automated scheduling with Google Calendar integration
- **CRM Integration**: Real-time synchronization with HubSpot and Salesforce
- **Workflow Automation**: n8n integration for complex automation workflows
- **Webhook System**: Handle events from Vapi, CRM, and calendar services
- **Call Analytics**: Track call performance and conversion metrics

## Technology Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy ORM (async)
- **Voice AI**: Vapi API
- **Workflow**: n8n (via webhooks)
- **CRM**: HubSpot API (extensible to Salesforce)
- **Calendar**: Google Calendar API
- **Validation**: Pydantic v2
- **Migrations**: Alembic

## Project Structure

```
AI-Voice-Bots/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── config.py               # Configuration management
│   │   ├── models/                 # SQLAlchemy database models
│   │   ├── schemas/                # Pydantic schemas for API
│   │   ├── api/routes/             # API route handlers
│   │   ├── services/               # Business logic services
│   │   ├── database/               # Database connection and setup
│   │   └── utils/                  # Utility functions
│   ├── requirements.txt
│   └── .env.example
├── docs/
│   └── API.md                      # API documentation
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- Vapi API account and API key
- (Optional) HubSpot API key
- (Optional) Google Calendar API credentials
- (Optional) n8n instance

### Installation

1. **Clone the repository** (if applicable) or navigate to the project directory

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and fill in your API keys and configuration values.

5. **Set up the database**:
   - Create a PostgreSQL database
   - Update `DATABASE_URL` in `.env` with your database credentials
   - Run migrations (if using Alembic):
     ```bash
     alembic upgrade head
     ```
   - Or the database tables will be created automatically on first run

6. **Run the application**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access the API**:
   - API Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc
   - Health check: http://localhost:8000/health

## API Documentation

For complete API documentation, see:
- **[Full API Documentation](docs/API.md)** - Comprehensive guide with examples
- **[Quick Reference Guide](docs/API_QUICK_REFERENCE.md)** - Quick lookup for endpoints
- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc

### Quick API Overview

**Leads**
- `POST /api/v1/leads` - Create a new lead
- `GET /api/v1/leads` - Get all leads (with pagination and filtering)
- `GET /api/v1/leads/{lead_id}` - Get a specific lead
- `PUT /api/v1/leads/{lead_id}` - Update a lead
- `DELETE /api/v1/leads/{lead_id}` - Delete a lead
- `POST /api/v1/leads/bulk` - Create multiple leads
- `POST /api/v1/leads/{lead_id}/sync-crm` - Manually sync lead to CRM

**Calls**
- `POST /api/v1/calls/initiate` - Initiate an outbound call (requires `assistant_id` in body)
- `GET /api/v1/calls` - Get all calls (with pagination and filtering)
- `GET /api/v1/calls/{call_id}` - Get a specific call
- `GET /api/v1/calls/vapi/{vapi_call_id}` - Get call by Vapi ID
- `PUT /api/v1/calls/{call_id}` - Update a call record
- `GET /api/v1/calls/lead/{lead_id}` - Get all calls for a lead

**Appointments**
- `POST /api/v1/appointments` - Create a new appointment
- `GET /api/v1/appointments` - Get all appointments
- `GET /api/v1/appointments/{appointment_id}` - Get a specific appointment
- `PUT /api/v1/appointments/{appointment_id}` - Update an appointment
- `DELETE /api/v1/appointments/{appointment_id}` - Delete an appointment
- `GET /api/v1/appointments/lead/{lead_id}` - Get all appointments for a lead

**Webhooks**
- `POST /api/v1/webhooks/vapi` - Handle Vapi webhooks
- `POST /api/v1/webhooks/crm` - Handle CRM webhooks
- `POST /api/v1/webhooks/calendar` - Handle calendar webhooks
- `POST /api/v1/webhooks/n8n` - Handle n8n webhooks

## Configuration

### Vapi Setup

1. Sign up for a Vapi account at https://vapi.ai
2. Get your API key from the dashboard
3. Add it to `.env` as `VAPI_API_KEY`
4. Configure your phone numbers in Vapi dashboard
5. Set up webhook URL in Vapi: `https://your-domain.com/api/v1/webhooks/vapi`

### HubSpot Setup

1. Create a HubSpot account or use existing
2. Generate a private app API key
3. Add it to `.env` as `HUBSPOT_API_KEY`
4. The system will automatically sync leads to HubSpot when created/updated

### Google Calendar Setup

1. Create a Google Cloud Project
2. Enable Google Calendar API
3. Create a service account and download credentials JSON
4. Share your calendar with the service account email
5. Add path to credentials in `.env` as `GOOGLE_CALENDAR_CREDENTIALS`

### n8n Setup

1. Set up an n8n instance (cloud or self-hosted)
2. Create webhook workflows
3. Add webhook URL to `.env` as `N8N_WEBHOOK_URL`
4. Configure workflows to receive events from the API

## Usage Examples

### Creating a Lead and Initiating a Call

```python
import httpx

# Create a lead
response = httpx.post("http://localhost:8000/api/v1/leads", json={
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "company": "Example Corp",
    "source": "website"
})
lead = response.json()["data"]

# Initiate a call
response = httpx.post("http://localhost:8000/api/v1/calls/initiate", json={
    "lead_id": lead["id"],
    "assistant_id": "your-vapi-assistant-id"
})
call = response.json()["data"]
```

### Creating an Appointment

```python
from datetime import datetime, timedelta

# Schedule an appointment
scheduled_time = datetime.utcnow() + timedelta(days=1)
response = httpx.post("http://localhost:8000/api/v1/appointments", json={
    "lead_id": lead["id"],
    "scheduled_time": scheduled_time.isoformat(),
    "notes": "Initial consultation call"
})
appointment = response.json()["data"]
```

## Development

### Running Tests

```bash
pytest
```

### Database Migrations

If using Alembic for migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Environment Variables

See `.env.example` for all available configuration options.

## License

This project is created for Brainlancer application submission.

## Support

For issues or questions, please refer to the API documentation at `/docs` endpoint or check the individual service documentation.

