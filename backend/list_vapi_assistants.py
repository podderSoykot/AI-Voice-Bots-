"""Script to list your Vapi assistants and phone numbers."""
import asyncio
from app.services.vapi_service import VapiService
from app.config import settings

async def list_assistants():
    """List all assistants from Vapi."""
    print("=" * 60)
    print("VAPI ASSISTANTS & PHONE NUMBERS")
    print("=" * 60)
    
    if not settings.VAPI_API_KEY or settings.VAPI_API_KEY == "":
        print("\n[ERROR] VAPI_API_KEY is not set in .env file")
        return
    
    vapi_service = VapiService()
    
    try:
        # Try to get phone numbers (this endpoint might not exist, but let's try)
        print("\n[PHONE NUMBERS]")
        print("-" * 60)
        try:
            phone_numbers = await vapi_service.get_phone_numbers()
            if phone_numbers:
                if isinstance(phone_numbers, list):
                    for phone in phone_numbers:
                        print(f"  ID: {phone.get('id', 'N/A')}")
                        print(f"  Number: {phone.get('number', 'N/A')}")
                        print()
                elif isinstance(phone_numbers, dict):
                    items = phone_numbers.get('data', phone_numbers.get('phoneNumbers', []))
                    if items:
                        for phone in items:
                            print(f"  ID: {phone.get('id', 'N/A')}")
                            print(f"  Number: {phone.get('number', 'N/A')}")
                            print()
                    else:
                        print("  No phone numbers found")
            else:
                print("  No phone numbers found or endpoint not available")
        except Exception as e:
            print(f"  Could not fetch phone numbers: {str(e)}")
            print("  (This is normal if you haven't set up phone numbers yet)")
        
        print("\n" + "=" * 60)
        print("HOW TO GET YOUR ASSISTANT ID")
        print("=" * 60)
        print("""
1. Go to Vapi Dashboard: https://dashboard.vapi.ai
2. Navigate to "Assistants" in the left menu
3. You'll see a list of your assistants OR a button to "Create Assistant"
4. If you need to create one:
   - Click "Create Assistant" or "New Assistant"
   - Fill in:
     * Name: e.g., "Sales Agent"
     * First Message: e.g., "Hi! This is [name] calling..."
     * Voice: Select a voice (e.g., "jennifer-playht")
     * System Prompt: Instructions for the AI
   - Click "Save" or "Create"
5. Once created, you'll see the Assistant ID (looks like a UUID)
   - It might be in the URL: /assistants/[ASSISTANT_ID]
   - Or displayed on the assistant details page
6. Copy that Assistant ID and use it in your API calls

Note: The Assistant ID is NOT just "1" - it's a long UUID like:
"a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        """)
        
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        print("\nThis might mean:")
        print("  1. Your VAPI_API_KEY is invalid")
        print("  2. You need to create an assistant first in the dashboard")
        print("  3. The API endpoint structure might be different")

if __name__ == "__main__":
    asyncio.run(list_assistants())

