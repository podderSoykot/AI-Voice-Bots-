# Database Setup Guide

## Quick Fix Options

### Option 1: Install and Start PostgreSQL (Recommended)

1. **Download PostgreSQL**:
   - Windows: https://www.postgresql.org/download/windows/
   - Or use Chocolatey: `choco install postgresql`

2. **Start PostgreSQL Service**:
   ```powershell
   # Check if PostgreSQL service is running
   Get-Service postgresql*
   
   # Start PostgreSQL service
   Start-Service postgresql-x64-XX  # Replace XX with your version
   ```

3. **Create Database**:
   ```sql
   -- Connect to PostgreSQL (usually via pgAdmin or psql)
   CREATE DATABASE ai_voice_bots;
   ```

4. **Update .env file**:
   ```env
   DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/ai_voice_bots
   ```

### Option 2: Use Docker (Easiest)

If you have Docker installed:

```bash
docker run --name postgres-ai-voice-bots \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=ai_voice_bots \
  -p 5432:5432 \
  -d postgres:15
```

Then in your `.env`:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_voice_bots
```

### Option 3: Use SQLite for Development (No Setup Required)

If you want to test without PostgreSQL, you can temporarily use SQLite:

1. Update `backend/app/database/connection.py`:
   ```python
   # Change from:
   engine = create_async_engine(
       settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
       ...
   )
   
   # To:
   engine = create_async_engine(
       "sqlite+aiosqlite:///./ai_voice_bots.db",
       ...
   )
   ```

2. Install aiosqlite:
   ```bash
   pip install aiosqlite
   ```

3. Update requirements.txt to include `aiosqlite`

**Note**: SQLite has limitations and is not recommended for production.

## Verify Database Connection

After setting up PostgreSQL, test the connection:

```python
# Test script (test_db.py)
import asyncio
from app.database.connection import engine

async def test():
    try:
        async with engine.begin() as conn:
            print("✓ Database connection successful!")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")

asyncio.run(test())
```

## Common Issues

### Error: "Connect call failed"
- **Cause**: PostgreSQL is not running
- **Fix**: Start PostgreSQL service or Docker container

### Error: "password authentication failed"
- **Cause**: Wrong password in DATABASE_URL
- **Fix**: Update password in .env file

### Error: "database does not exist"
- **Cause**: Database not created
- **Fix**: Create database: `CREATE DATABASE ai_voice_bots;`

## Default PostgreSQL Credentials

- **Username**: `postgres` (default)
- **Password**: Set during installation
- **Port**: `5432` (default)
- **Host**: `localhost` (default)

