# Environment Variables Setup Guide

This guide explains all the environment variables you need to add to your `.env` file.

## Required Variables (Minimum to Run)

These are the **minimum required** variables to get the application running:

```env
# API Configuration - REQUIRED
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=False
API_V1_PREFIX=/api/v1

# Database Configuration - REQUIRED
DATABASE_URL=postgresql://username:password@localhost:5432/ai_voice_bots

# Vapi Configuration - REQUIRED (for voice bot functionality)
VAPI_API_KEY=your-vapi-api-key-here
VAPI_BASE_URL=https://api.vapi.ai
```

## Optional Variables (Based on Features You Need)

### CORS Configuration
```env
# Allow all origins (development)
CORS_ORIGINS=*

# Or specify specific origins (production)
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### HubSpot CRM Integration (Optional)
If you want to sync leads to HubSpot:
```env
HUBSPOT_API_KEY=your-hubspot-private-app-api-key
```

**How to get HubSpot API Key:**
1. Go to HubSpot → Settings → Integrations → Private Apps
2. Create a new private app
3. Grant permissions: `crm.objects.contacts.read`, `crm.objects.contacts.write`
4. Copy the API key

### Salesforce CRM Integration (Optional)
If you want to use Salesforce instead of or alongside HubSpot:
```env
SALESFORCE_CLIENT_ID=your-salesforce-client-id
SALESFORCE_CLIENT_SECRET=your-salesforce-client-secret
SALESFORCE_USERNAME=your-salesforce-username
SALESFORCE_PASSWORD=your-salesforce-password-with-security-token
```

### Google Calendar Integration (Optional)
If you want automatic calendar event creation for appointments:
```env
GOOGLE_CALENDAR_CREDENTIALS=path/to/your/credentials.json
GOOGLE_CALENDAR_ID=primary
```

**How to set up Google Calendar:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google Calendar API
4. Create a Service Account
5. Download the JSON credentials file
6. Share your calendar with the service account email
7. Put the path to the JSON file in `GOOGLE_CALENDAR_CREDENTIALS`

### n8n Workflow Integration (Optional)
If you want to trigger n8n workflows:
```env
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/your-workflow-id
N8N_API_KEY=your-n8n-api-key-if-required
```

## Complete Example .env File

Here's a complete example with all variables (use what you need):

```env
# ============================================
# API Configuration
# ============================================
SECRET_KEY=super-secret-key-change-this-in-production-use-random-string
DEBUG=False
API_V1_PREFIX=/api/v1

# ============================================
# Database Configuration
# ============================================
# Format: postgresql://username:password@host:port/database_name
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/ai_voice_bots

# ============================================
# Vapi Configuration (REQUIRED for voice bots)
# ============================================
# Get your API key from: https://dashboard.vapi.ai
VAPI_API_KEY=vapi_xxxxxxxxxxxxxxxxxxxxx
VAPI_BASE_URL=https://api.vapi.ai

# ============================================
# HubSpot CRM (Optional)
# ============================================
HUBSPOT_API_KEY=pat-na1-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# ============================================
# Salesforce CRM (Optional - alternative to HubSpot)
# ============================================
SALESFORCE_CLIENT_ID=your_client_id_here
SALESFORCE_CLIENT_SECRET=your_client_secret_here
SALESFORCE_USERNAME=your_username@example.com
SALESFORCE_PASSWORD=yourpassword+securitytoken

# ============================================
# Google Calendar (Optional)
# ============================================
# Path to your service account credentials JSON file
GOOGLE_CALENDAR_CREDENTIALS=./credentials/google-calendar-credentials.json
GOOGLE_CALENDAR_ID=primary

# ============================================
# n8n Workflow Automation (Optional)
# ============================================
N8N_WEBHOOK_URL=https://n8n.yourdomain.com/webhook/abc123
N8N_API_KEY=your-n8n-api-key

# ============================================
# CORS Configuration
# ============================================
# For development: use *
# For production: specify your frontend URLs
CORS_ORIGINS=*
```

## Quick Start (Minimum Setup)

If you just want to get started quickly, use this minimal `.env`:

```env
SECRET_KEY=dev-secret-key-change-me
DEBUG=True
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_voice_bots
VAPI_API_KEY=your-vapi-key-here
VAPI_BASE_URL=https://api.vapi.ai
CORS_ORIGINS=*
```

## Important Notes

1. **Never commit your `.env` file to git** - it's already in `.gitignore`
2. **SECRET_KEY**: Generate a strong random string for production:
   ```python
   import secrets
   print(secrets.token_urlsafe(32))
   ```
3. **DATABASE_URL**: Make sure PostgreSQL is running and the database exists
4. **VAPI_API_KEY**: Required for any voice bot functionality
5. **Optional integrations**: You can add them later as needed

## Testing Your Configuration

After setting up your `.env` file, you can test if everything loads correctly:

```python
from app.config import settings

print(f"VAPI API Key set: {bool(settings.VAPI_API_KEY)}")
print(f"Database URL: {settings.DATABASE_URL}")
print(f"HubSpot configured: {bool(settings.HUBSPOT_API_KEY)}")
```

## Troubleshooting

- **"Settings not loading"**: Make sure `.env` is in the project root (`F:\Soykot_podder\AI-Voice-Bots-\.env`)
- **"Database connection failed"**: Check PostgreSQL is running and DATABASE_URL is correct
- **"Vapi API error"**: Verify your VAPI_API_KEY is correct and has proper permissions

