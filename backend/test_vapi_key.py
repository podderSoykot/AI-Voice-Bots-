"""Quick script to test if VAPI_API_KEY is loaded correctly."""
from app.config import settings

print("=" * 60)
print("VAPI API KEY CHECK")
print("=" * 60)
print(f"\nVAPI_API_KEY loaded: {bool(settings.VAPI_API_KEY)}")
print(f"VAPI_API_KEY value: {settings.VAPI_API_KEY[:10]}..." if settings.VAPI_API_KEY else "VAPI_API_KEY: (empty)")
print(f"VAPI_API_KEY length: {len(settings.VAPI_API_KEY)}")
print(f"VAPI_BASE_URL: {settings.VAPI_BASE_URL}")
print("\n" + "=" * 60)

if not settings.VAPI_API_KEY or settings.VAPI_API_KEY == "":
    print("❌ ERROR: VAPI_API_KEY is not set or is empty!")
    print("\nMake sure:")
    print("  1. .env file exists in project root")
    print("  2. VAPI_API_KEY=your-key-here is in .env")
    print("  3. No quotes around the key value")
    print("  4. Server was restarted after adding the key")
else:
    print("[OK] VAPI_API_KEY is loaded")
    print(f"  Key starts with: {settings.VAPI_API_KEY[:8]}...")
    print(f"  Key length: {len(settings.VAPI_API_KEY)} characters")

