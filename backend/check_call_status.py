"""Check call status from Vapi API."""
import asyncio
from app.services.vapi_service import VapiService
from app.database.connection import AsyncSessionLocal
from app.services.database_service import DatabaseService

async def check_call_status():
    """Check the status of the call."""
    vapi_service = VapiService()
    
    # Get call from database
    async with AsyncSessionLocal() as session:
        call = await DatabaseService.get_call(session, 1)
        
        if not call:
            print("Call not found in database")
            return
        
        print("=" * 60)
        print("CALL STATUS CHECK")
        print("=" * 60)
        print(f"\nDatabase Call Status: {call.status.value}")
        print(f"Vapi Call ID: {call.call_id}")
        print(f"Lead Phone: {call.lead.phone if call.lead else 'N/A'}")
        print()
        
        # Get latest status from Vapi
        try:
            vapi_call = await vapi_service.get_call(call.call_id)
            print("Vapi API Status:")
            print(f"  Status: {vapi_call.get('status', 'N/A')}")
            print(f"  Cost: ${vapi_call.get('cost', 0)}")
            print(f"  Customer: {vapi_call.get('customer', {}).get('name', 'N/A')} - {vapi_call.get('customer', {}).get('number', 'N/A')}")
            print()
            
            if vapi_call.get('status') == 'queued':
                print("Call is still queued - Vapi is processing it")
            elif vapi_call.get('status') == 'ringing':
                print("Phone is ringing - waiting for answer")
            elif vapi_call.get('status') == 'in-progress':
                print("Call is in progress - conversation happening")
            elif vapi_call.get('status') == 'ended':
                print("Call has ended")
                print(f"  Duration: {vapi_call.get('duration', 'N/A')} seconds")
            elif vapi_call.get('status') == 'failed':
                print("Call failed - check the reason below")
            else:
                print(f"Current status: {vapi_call.get('status')}")
            
        except Exception as e:
            print(f"Error getting call status from Vapi: {str(e)}")
        
        print("\n" + "=" * 60)
        print("IMPORTANT:")
        print("=" * 60)
        print("The system calls the LEAD's phone number, not yours!")
        print(f"Lead's phone: {call.lead.phone if call.lead else 'N/A'}")
        print("\nTo test, use a phone number you have access to.")
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(check_call_status())


