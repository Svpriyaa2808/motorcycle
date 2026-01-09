import os
import json
import time
import requests
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env.local (same as Next.js)
load_dotenv('.env.local')

# ---------- Supabase setup ----------
# Use the same env vars as Next.js
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

# Validate credentials
if not SUPABASE_URL or SUPABASE_URL == "https://placeholder.supabase.co":
    print("")
    print("❌ ERROR: Please set your actual Supabase credentials in .env.local")
    print("")
    print("📝 Steps to fix:")
    print("   1. Go to https://supabase.com")
    print("   2. Select your project")
    print("   3. Go to Settings → API")
    print("   4. Copy 'Project URL' and 'anon public' key")
    print("   5. Update .env.local with your actual values")
    print("")
    exit(1)

if not SUPABASE_KEY or "placeholder" in SUPABASE_KEY:
    print("")
    print("❌ ERROR: Please set your actual Supabase ANON key in .env.local")
    print("")
    print("📝 Steps to fix:")
    print("   1. Go to https://supabase.com → Your Project → Settings → API")
    print("   2. Copy the 'anon public' key")
    print("   3. Update NEXT_PUBLIC_SUPABASE_ANON_KEY in .env.local")
    print("")
    exit(1)

print("=" * 60)
print("🏍️  Motorcycle Shop Data Fetcher")
print("=" * 60)
print(f"✅ Supabase URL: {SUPABASE_URL}")
print(f"✅ Supabase Key: {SUPABASE_KEY[:20]}...")
print("")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Connected to Supabase successfully")
except Exception as e:
    print(f"❌ Failed to connect to Supabase: {e}")
    print("   Please check your credentials in .env.local")
    exit(1)

# ---------- Worldwide country codes ----------
COUNTRIES = [
    # Europe
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU",
    "IS", "IE", "IT", "LV", "LT", "LU", "MT", "NL", "NO", "PL", "PT", "RO", "RS",
    "SK", "SI", "ES", "SE", "CH", "TR", "UA", "GB",
    # North America
    "CA", "MX", "US",
    # Central & South America
    "AR", "BR", "CL", "CO", "CR", "PE", "UY", "VE",
    # Asia
    "BD", "KH", "CN", "IN", "ID", "JP", "MY", "NP", "PK", "PH", "SG", "KR", "LK",
    "TW", "TH", "VN",
    # Middle East
    "AE", "IL", "SA",
    # Oceania
    "AU", "NZ",
    # Africa
    "EG", "KE", "MA", "NG", "ZA", "TZ",
]

print(f"📍 Fetching data for {len(COUNTRIES)} countries worldwide")
print("")

# ---------- Helper function to fetch data ----------
def fetch_overpass_data(country_code):
    url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json][timeout:60];
    area["ISO3166-1"="{country_code}"][admin_level=2];
    (
      node["shop"="motorcycle"](area);
      node["craft"="motorcycle"](area);
      node["amenity"="car_repair"]["motorcycle"="yes"](area);
    );
    out center;
    """
    print(f"🔍 Fetching {country_code}...", end=" ", flush=True)
    response = requests.get(url, params={'data': query})
    response.raise_for_status()
    return response.json()

# ---------- Helper to format data ----------
def format_records(data, country_code):
    records = []
    for element in data.get("elements", []):
        tags = element.get("tags", {})
        if not tags:
            continue

        record = {
            "id": element["id"],
            "country_code": tags.get("addr:country", country_code),
            "name": tags.get("name"),
            "lat": element.get("lat"),
            "lon": element.get("lon"),
            "address": {
                "city": tags.get("addr:city"),
                "street": tags.get("addr:street"),
                "housenumber": tags.get("addr:housenumber"),
                "postcode": tags.get("addr:postcode"),
                "suburb": tags.get("addr:suburb")
            },
            "contact": {
                "phone": tags.get("contact:phone") or tags.get("phone"),
                "fax": tags.get("contact:fax"),
                "website": tags.get("contact:website") or tags.get("website"),
                "email": tags.get("contact:email") or tags.get("email")
            },
            "shop_tags": tags,
            "source_country": country_code
        }
        records.append(record)
    return records

# ---------- Main loop ----------
total_shops = 0
successful_countries = 0
failed_countries = []

for code in COUNTRIES:
    try:
        data = fetch_overpass_data(code)
        records = format_records(data, code)

        if not records:
            print(f"⚠️  No shops found")
            continue

        # Batch insert (100 rows at a time)
        inserted = 0
        for i in range(0, len(records), 100):
            chunk = records[i:i+100]
            result = supabase.table("motorcycle_shops").upsert(chunk).execute()
            inserted += len(chunk)

        print(f"✅ Inserted {inserted} shops")
        total_shops += inserted
        successful_countries += 1

        # Be kind to Overpass API - wait between requests
        time.sleep(10)

    except Exception as e:
        print(f"❌ Error: {e}")
        failed_countries.append(code)
        # Wait longer after errors
        time.sleep(20)

# ---------- Summary ----------
print("")
print("=" * 60)
print("🎉 Data Fetch Complete!")
print("=" * 60)
print(f"✅ Successfully processed: {successful_countries}/{len(COUNTRIES)} countries")
print(f"📊 Total shops inserted: {total_shops}")

if failed_countries:
    print(f"⚠️  Failed countries: {', '.join(failed_countries)}")
    print("   You can run the script again to retry failed countries")

print("")
print("🏍️  Your motorcycle shop database is ready!")
print("   Run: npm run dev")
print("   Open: http://localhost:3000")
print("")
