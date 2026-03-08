"""Check if DATABASE_URL is correctly configured."""
from app.config import settings

print("=" * 60)
print("DATABASE URL CHECK")
print("=" * 60)
print(f"\nDATABASE_URL: {settings.DATABASE_URL}")
print()

# Parse the URL
url = settings.DATABASE_URL
if "postgresql://" in url:
    # Extract parts
    parts = url.replace("postgresql://", "").split("@")
    if len(parts) == 2:
        auth = parts[0].split(":")
        if len(auth) == 2:
            username = auth[0]
            password = auth[1]
            print(f"Username: {username}")
            print(f"Password: {'*' * len(password) if password != 'password' else 'password (PLACEHOLDER!)'}")
            print(f"Host/DB: {parts[1]}")
            print()
            
            if username == "user" or password == "password":
                print("❌ ERROR: DATABASE_URL still has placeholder values!")
                print("\nYour .env file should have:")
                print("DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_voice_bots")
                print("\nCurrent value uses placeholder 'user:password' which won't work.")
            else:
                print("[OK] DATABASE_URL looks correct")
        else:
            print("❌ ERROR: DATABASE_URL format is incorrect")
    else:
        print("❌ ERROR: DATABASE_URL format is incorrect")
else:
    print("❌ ERROR: DATABASE_URL doesn't start with postgresql://")

print("\n" + "=" * 60)

