# Quick Start Guide

## ✅ PostgreSQL is Running!

Your PostgreSQL Docker container is up and running. Now you need to:

## 1. Update Your .env File

Make sure your `.env` file (in the project root) has the correct database URL:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_voice_bots
```

**Full .env example for Docker PostgreSQL:**

```env
# API Configuration
SECRET_KEY=dev-secret-key-change-me
DEBUG=True
API_V1_PREFIX=/api/v1

# Database Configuration (Docker PostgreSQL)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_voice_bots

# Vapi Configuration (REQUIRED)
VAPI_API_KEY=your-vapi-api-key-here
VAPI_BASE_URL=https://api.vapi.ai

# CORS Configuration
CORS_ORIGINS=*
```

## 2. Restart the FastAPI Server

From the `backend` directory:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 3. Verify Everything Works

1. **Check the startup logs** - You should see:
   ```
   ✓ Database initialized successfully
   ```

2. **Visit the API docs**: http://localhost:8000/docs

3. **Test the health endpoint**: http://localhost:8000/health

4. **Test creating a lead**:
   - Go to http://localhost:8000/docs
   - Find `POST /api/v1/leads`
   - Click "Try it out"
   - Use this example:
     ```json
     {
       "name": "John Doe",
       "email": "john@example.com",
       "phone": "+1234567890",
       "company": "Example Corp"
     }
     ```
   - Click "Execute"

## Troubleshooting

### If you see "Database connection failed":
- Make sure the Docker container is running: `docker ps`
- Check the DATABASE_URL in your .env file
- Verify the password matches: `postgres` (as set in the Docker command)

### If the container stops:
```bash
# Start it again
docker start postgres-ai-voice-bots

# Or check logs
docker logs postgres-ai-voice-bots
```

### To stop the database later:
```bash
docker stop postgres-ai-voice-bots
```

### To remove the container (if needed):
```bash
docker rm postgres-ai-voice-bots
```

## Next Steps

1. ✅ PostgreSQL is running
2. ⏳ Update .env with DATABASE_URL
3. ⏳ Restart FastAPI server
4. ⏳ Test the API endpoints

You're almost there! 🚀

