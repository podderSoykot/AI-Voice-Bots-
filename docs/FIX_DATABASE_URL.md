# Fix Database URL

Your PostgreSQL Docker container is running! Now update your `.env` file.

## Update Your .env File

Add or update this line in your `.env` file:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_voice_bots
```

## Complete .env File Should Look Like:

```env
# API Configuration
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=False
API_V1_PREFIX=/api/v1

# Database Configuration (Docker PostgreSQL)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_voice_bots

# Vapi Configuration
VAPI_API_KEY=your-vapi-api-key-here
VAPI_BASE_URL=https://api.vapi.ai

# CORS Configuration
CORS_ORIGINS=*
```

## After Updating

1. **Save the .env file**
2. **Restart your FastAPI server** (important!)
3. **Try your API call again**

The database connection should work now!


