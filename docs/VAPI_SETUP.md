# Vapi API Setup Guide

## Error: 401 Unauthorized

If you're getting a `401 Unauthorized` error when trying to initiate calls, it means your Vapi API key is missing or invalid.

## Quick Fix

### Step 1: Get Your Vapi Private API Key

**Important**: You need a **Private API Key** (server-side), NOT a Public API Key (client-side).

1. Go to [Vapi Dashboard](https://dashboard.vapi.ai)
2. Sign up or log in to your account
3. Navigate to **Settings** → **API Keys**
4. Look for **Private API Keys** section (NOT Public API Keys)
5. If you don't have one, click **Create Private API Key** or **Generate New Key**
6. Copy your **Private API key** (it should look like: `sk-...` or similar)

**Note**: 
- **Private API Key** = For server-side API calls (what you need)
- **Public API Key** = For client-side SDK access (not what you need for this)

### Step 2: Add API Key to .env File

1. Open your `.env` file in the project root directory
2. Find or add the `VAPI_API_KEY` line:
   ```env
   VAPI_API_KEY=your-actual-api-key-here
   ```
3. Replace `your-actual-api-key-here` with the API key you copied
4. Save the file

### Step 3: Restart the Server

After updating the `.env` file, restart your FastAPI server:

```bash
# Stop the current server (Ctrl+C)
# Then restart it
cd backend
uvicorn app.main:app --reload
```

## Verify Your Setup

After restarting, the server will load the new API key. Try initiating a call again.

## Example .env File

```env
# Vapi Configuration
# IMPORTANT: Use PRIVATE API KEY (not Public API Key)
VAPI_API_KEY=sk-your-private-vapi-api-key-here
VAPI_BASE_URL=https://api.vapi.ai
```

## Public vs Private API Keys

### Private API Key (What You Need)
- **Purpose**: Server-side API calls
- **Use Case**: Making calls from your backend server
- **Security**: Keep this secret, never expose to client-side
- **Location**: Settings → API Keys → **Private API Keys**

### Public API Key (What You DON'T Need)
- **Purpose**: Client-side SDK access
- **Use Case**: Making calls directly from browser/mobile app
- **Security**: Can be exposed in client-side code
- **Location**: Settings → API Keys → **Public API Keys**

**For this application, you MUST use a Private API Key.**

## Additional Vapi Setup

### 1. Create an Assistant

Before you can make calls, you need to create an assistant in Vapi:

1. Go to [Vapi Dashboard](https://dashboard.vapi.ai)
2. Navigate to **Assistants**
3. Click **Create Assistant**
4. Configure your assistant:
   - Name
   - First message
   - Voice
   - System prompt
5. Save and copy the **Assistant ID**

### 2. Get Phone Number ID (Optional)

If you want to use a specific phone number to call from:

1. Go to **Phone Numbers** in Vapi dashboard
2. Select or purchase a phone number
3. Copy the **Phone Number ID**

### 3. Use the Assistant ID in API Calls

When initiating a call, include the assistant ID:

```json
{
  "lead_id": 1,
  "assistant_id": "your-assistant-id-from-vapi",
  "phone_number_id": "your-phone-number-id"  // Optional
}
```

## Troubleshooting

### Still Getting 401 Error?

1. **Check the API key format**: Make sure there are no extra spaces or quotes
   ```env
   # Wrong:
   VAPI_API_KEY="sk-123..."
   VAPI_API_KEY= sk-123...
   
   # Correct:
   VAPI_API_KEY=sk-123...
   ```

2. **Verify the key is loaded**: Check server startup logs - if there's an error loading .env, it will show

3. **Check file location**: Make sure `.env` is in the project root (same level as `backend` folder)

4. **Restart the server**: Environment variables are loaded at startup, so you must restart

### Other Common Errors

- **404 Not Found**: Check that `VAPI_BASE_URL` is correct (should be `https://api.vapi.ai`)
- **Invalid Assistant ID**: Make sure the assistant ID exists in your Vapi account
- **Phone Number Issues**: Verify the phone number ID is valid and active

## Need Help?

- [Vapi Documentation](https://docs.vapi.ai)
- [Vapi Dashboard](https://dashboard.vapi.ai)
- Check your API key status in the Vapi dashboard

