# Vapi Phone Number Setup

## Error: 400 Bad Request

If you're getting a 400 Bad Request error when initiating calls, it usually means you need to set up a phone number in Vapi.

## Why You Need a Phone Number

Vapi needs to know **which phone number to call FROM**. This is different from the number you're calling TO (the customer's number).

## How to Set Up a Phone Number in Vapi

### Step 1: Go to Phone Numbers

1. Open [Vapi Dashboard](https://dashboard.vapi.ai)
2. Navigate to **"Phone Numbers"** in the left menu
3. You'll see your phone numbers or an option to purchase/add one

### Step 2: Get or Add a Phone Number

**Option A: Use Existing Number**
- If you already have a phone number, click on it
- Copy the **Phone Number ID** (looks like a UUID)

**Option B: Purchase/Add a New Number**
1. Click **"Add Phone Number"** or **"Purchase Number"**
2. Select your country/region
3. Choose a number
4. Complete the purchase/setup
5. Copy the **Phone Number ID**

### Step 3: Use the Phone Number ID

Once you have the Phone Number ID, include it in your API call:

```json
{
  "lead_id": 1,
  "phone_number": "+8801734537627",
  "assistant_id": "9f0ecf8b-4676-4c02-afcd-ea7fddd1d1a2",
  "phone_number_id": "your-phone-number-id-here"
}
```

## Alternative: Set Default Phone Number

Some Vapi accounts allow you to set a default phone number in the assistant settings. Check your assistant configuration in the dashboard.

## Finding Your Phone Number ID

The Phone Number ID can be found:
- In the URL when viewing the phone number: `/phone-numbers/[PHONE_NUMBER_ID]`
- On the phone number details page
- In the phone number list (hover or click to see details)

## Common Issues

### "I don't see Phone Numbers in the menu"
- Make sure you're on a paid plan (free plans may have limitations)
- Check if phone numbers are available in your region
- Contact Vapi support if needed

### "I have a number but can't find the ID"
- Click on the phone number to open details
- The ID is usually displayed prominently
- Check the browser URL for the ID

### "Do I need a phone number for every call?"
- You can reuse the same phone number for all calls
- Just include the `phone_number_id` in each request
- Or set it as default in your assistant settings

## Quick Test

After getting your phone number ID, try the call again:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/calls/initiate" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_id": 1,
    "assistant_id": "9f0ecf8b-4676-4c02-afcd-ea7fddd1d1a2",
    "phone_number_id": "your-phone-number-id"
  }'
```

## Need Help?

- [Vapi Phone Numbers Documentation](https://docs.vapi.ai)
- [Vapi Dashboard](https://dashboard.vapi.ai)
- Check the error message details - it will tell you exactly what's missing

