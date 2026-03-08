# Call Troubleshooting Guide

## Understanding the Call Flow

### Important: Who Gets Called?

The system calls the **lead's phone number**, NOT your phone number.

- **Lead's Phone**: `+8801734537627` (the number being called)
- **Your Phone**: Not called (you're the caller, not the recipient)

## Check Call Status

### Method 1: Via API

Check the call status using the call ID:

```bash
# Get call by database ID
GET http://127.0.0.1:8000/api/v1/calls/1

# Or by Vapi call ID
GET http://127.0.0.1:8000/api/v1/calls/vapi/019cccb0-f945-766e-8742-8347b9a56b55
```

### Method 2: Check Database

Run the database check script:

```bash
cd backend
python check_database.py
```

Look for the call status in the CSV output.

## Common Call Statuses

- `queued` - Call is waiting to be processed
- `ringing` - Phone is ringing
- `in_progress` - Call is active
- `completed` - Call finished successfully
- `failed` - Call failed (wrong number, no answer, etc.)
- `no_answer` - No one answered
- `busy` - Line was busy

## Why You Might Not See a Call

### 1. Call Status is Still "Queued"
- The call might still be processing
- Wait a few seconds and check again

### 2. Wrong Phone Number
- Verify the lead's phone number is correct: `+8801734537627`
- Make sure it includes country code (+880 for Bangladesh)

### 3. Call Failed
- Check the call status - it might show `failed`, `no_answer`, or `busy`
- The phone might be off, unreachable, or the number might be wrong

### 4. SIP Number Issue
- Free SIP numbers might have limitations
- Check if your SIP number is properly configured

## Check Call Details

To see what happened with your call:

1. **Check the call status**:
   ```bash
   curl http://127.0.0.1:8000/api/v1/calls/1
   ```

2. **Look for**:
   - `status`: Current call status
   - `outcome`: What happened (success, no_answer, failed, etc.)
   - `duration`: How long the call lasted (if any)
   - `transcript`: What was said (if call connected)

## Next Steps

1. Check the call status using the API
2. Verify the phone number is correct
3. Check if the lead's phone is on and can receive calls
4. Review the call outcome in the database

## Testing Tips

- Use a phone number you have access to for testing
- Make sure the phone is on and can receive calls
- Check the timezone - calls might be scheduled for a different time
- Verify the country code is correct (+880 for Bangladesh)

