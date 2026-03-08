# Vapi API Key Types Explained

## Quick Answer

You're seeing a **Public API Key**, but you need a **Private API Key** for server-side calls.

## The Difference

### 🔒 Private API Key (What You Need)
- **For**: Server-side API calls from your backend
- **Security**: Must be kept secret, never expose to client
- **Used by**: Your FastAPI backend server
- **Location**: Vapi Dashboard → Settings → API Keys → **Private API Keys**

### 🌐 Public API Key (What You're Seeing)
- **For**: Client-side SDK access (browser/mobile apps)
- **Security**: Can be exposed in client-side code
- **Used by**: Frontend applications directly
- **Location**: Vapi Dashboard → Settings → API Keys → **Public API Keys**

## How to Get Your Private API Key

1. **Go to Vapi Dashboard**: https://dashboard.vapi.ai
2. **Navigate to**: Settings → API Keys
3. **Look for**: "Private API Keys" section (separate from Public API Keys)
4. **If you don't have one**:
   - Click "Create Private API Key" or "Generate New Key"
   - Give it a name (e.g., "Backend Server")
   - Copy the key immediately (you won't see it again!)
5. **Add to .env**:
   ```env
   VAPI_API_KEY=sk-your-private-key-here
   ```

## Visual Guide

In the Vapi Dashboard, you should see:

```
API Keys
├── Private API Keys          ← Use this one!
│   └── [Create New Key]
│
└── Public API Keys           ← Not this one
    └── [Your Public Key]     ← This is what you're seeing
```

## Why This Matters

- **Public Key**: Designed for client-side use, has restrictions
- **Private Key**: Full access for server-side operations
- **401 Error**: Happens when you use Public Key for server-side calls, or no key at all

## After Getting Private Key

1. Add it to your `.env` file
2. Restart your FastAPI server
3. Try the call again - it should work!

## Still Can't Find It?

If you don't see a "Private API Keys" section:
- Make sure you're logged into the correct Vapi account
- Check if your account has API access enabled
- Contact Vapi support if needed

