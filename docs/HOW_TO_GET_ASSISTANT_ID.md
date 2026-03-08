# How to Get Your Vapi Assistant ID

## Quick Answer

You need to create an Assistant in the Vapi Dashboard first, then copy its ID.

## Step-by-Step Guide

### Step 1: Go to Vapi Dashboard

1. Open your browser
2. Go to: https://dashboard.vapi.ai
3. Log in to your account

### Step 2: Navigate to Assistants

1. In the left sidebar, click on **"Assistants"**
2. You'll see a list of your assistants (if any) or an empty page

### Step 3: Create an Assistant (If You Don't Have One)

1. Click **"Create Assistant"** or **"New Assistant"** button
2. Fill in the required information:

   **Basic Settings:**
   - **Name**: Give it a name (e.g., "Sales Agent", "Customer Support")
   - **First Message**: What the AI says when the call starts
     - Example: `"Hi! This is Sarah calling from [Company]. Do you have a moment to talk?"`
   
   **Voice Settings:**
   - **Voice**: Select a voice (e.g., "jennifer-playht", "alloy", "echo")
   - **Language**: Usually "en" for English
   
   **AI Configuration:**
   - **Model**: Choose an AI model (e.g., "gpt-3.5-turbo", "gpt-4")
   - **System Prompt**: Instructions for the AI
     - Example: 
       ```
       You are a professional sales representative. Your goal is to:
       1. Introduce yourself and the company
       2. Qualify the lead
       3. Schedule an appointment if interested
       4. Be polite and professional
       ```

3. Click **"Save"** or **"Create"**

### Step 4: Get the Assistant ID

After creating or selecting an assistant, you can find the ID in several ways:

**Method 1: From the URL**
- Look at the browser URL bar
- It might look like: `https://dashboard.vapi.ai/assistants/a1b2c3d4-e5f6-7890-abcd-ef1234567890`
- The part after `/assistants/` is your Assistant ID

**Method 2: From the Assistant Details Page**
- Click on the assistant name to open details
- Look for an "ID" field or "Assistant ID" field
- It will be a UUID format: `a1b2c3d4-e5f6-7890-abcd-ef1234567890`

**Method 3: From the API Response**
- If you use the Vapi API to list assistants, the ID will be in the response

### Step 5: Use the Assistant ID

Copy the Assistant ID and use it in your API call:

```json
{
  "lead_id": 1,
  "assistant_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "phone_number": "+1234567890"
}
```

## Important Notes

1. **Assistant ID is NOT "1"** - It's a long UUID string
2. **You must create an assistant first** - You can't make calls without one
3. **Each assistant has unique settings** - Different voices, prompts, etc.
4. **You can create multiple assistants** - For different use cases

## Example Assistant Configuration

Here's what a typical assistant might look like:

```json
{
  "name": "Sales Agent",
  "firstMessage": "Hi! This is Sarah calling from ABC Company. Do you have a moment?",
  "voice": "jennifer-playht",
  "model": {
    "provider": "openai",
    "model": "gpt-3.5-turbo",
    "temperature": 0.7
  },
  "systemPrompt": "You are a sales representative. Qualify leads and schedule appointments."
}
```

## Troubleshooting

### "I don't see Assistants in the menu"
- Make sure you're logged into the correct Vapi account
- Check if your account has the right permissions
- Try refreshing the page

### "I created an assistant but can't find the ID"
- Check the browser URL when viewing the assistant
- Look for a "Settings" or "Details" section
- The ID might be labeled as "Assistant ID" or just "ID"

### "The assistant ID looks wrong"
- Assistant IDs are UUIDs (long strings with hyphens)
- They look like: `a1b2c3d4-e5f6-7890-abcd-ef1234567890`
- If you see just "1" or a short number, that's not the right ID

## Need Help?

- [Vapi Documentation](https://docs.vapi.ai)
- [Vapi Dashboard](https://dashboard.vapi.ai)
- Check the Vapi support or community forums


