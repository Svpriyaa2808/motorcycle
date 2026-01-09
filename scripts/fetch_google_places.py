import os
import time
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

"""
Google Places API Data Extractor for Motorcycle Shops

This script uses Google Places API to get detailed motorcycle shop information
including ratings, reviews, business hours, and photos.

SETUP:
1. Get a Google Places API key from: https://console.cloud.google.com/
2. Enable "Places API" in your Google Cloud project
3. Add to .env.local: GOOGLE_PLACES_API_KEY=your_key_here
4. Note: Google Places API has usage costs - check pricing at:
   https://developers.google.com/maps/billing-and-pricing/pricing
"""

# Load environment variables
load_dotenv('.env.local')

GOOGLE_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your_api_key_here":
    print("")
    print("❌ ERROR: Google Places API key not configured")
    print("")
    print("📝 Steps to set up:")
    print("   1. Go to https://console.cloud.google.com/")
    print("   2. Create/select a project")
    print("   3. Enable 'Places API'")
    print("   4. Create credentials → API Key")
    print("   5. Add to .env.local: GOOGLE_PLACES_API_KEY=your_key")
    print("")
    print("⚠️  Note: Google Places API is a paid service")
    print("   Check pricing: https://developers.google.com/maps/billing-and-pricing/pricing")
    print("")
    exit(1)

print("=" * 60)
print("🏍️  Google Places API - Motorcycle Shop Extractor")
print("=" * 60)
print(f"✅ API Key configured: {GOOGLE_API_KEY[:10]}...")
print("")

# ---------- Configuration ----------
# Cities to search (you can customize this list)
CITIES = [
    # USA Major Cities
    {"city": "New York", "country": "US", "radius": 50000},
    {"city": "Los Angeles", "country": "US", "radius": 50000},
    {"city": "Chicago", "country": "US", "radius": 50000},
    {"city": "Houston", "country": "US", "radius": 50000},
    {"city": "Miami", "country": "US", "radius": 50000},

    # European Cities
    {"city": "London", "country": "GB", "radius": 50000},
    {"city": "Paris", "country": "FR", "radius": 50000},
    {"city": "Berlin", "country": "DE", "radius": 50000},
    {"city": "Rome", "country": "IT", "radius": 50000},
    {"city": "Madrid", "country": "ES", "radius": 50000},

    # Asian Cities
    {"city": "Tokyo", "country": "JP", "radius": 50000},
    {"city": "Bangkok", "country": "TH", "radius": 50000},
    {"city": "Mumbai", "country": "IN", "radius": 50000},
    {"city": "Singapore", "country": "SG", "radius": 30000},

    # Other Major Cities
    {"city": "Sydney", "country": "AU", "radius": 50000},
    {"city": "Toronto", "country": "CA", "radius": 50000},
    {"city": "Mexico City", "country": "MX", "radius": 50000},
]

# Search keywords
SEARCH_QUERIES = [
    "motorcycle repair shop",
    "motorcycle service",
    "motorcycle dealer",
    "bike repair shop"
]

# ---------- Helper Functions ----------

def geocode_city(city_name):
    """Get latitude/longitude for a city using Google Geocoding API."""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": city_name,
        "key": GOOGLE_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"] == "OK" and data["results"]:
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        else:
            print(f"⚠️  Geocoding failed for {city_name}: {data.get('status')}")
            return None, None
    except Exception as e:
        print(f"❌ Geocoding error for {city_name}: {e}")
        return None, None


def search_nearby(lat, lng, radius, query):
    """Search for motorcycle shops near a location."""
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "keyword": query,
        "type": "motorcycle_repair",
        "key": GOOGLE_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Search error: {e}")
        return {"results": []}


def get_place_details(place_id):
    """Get detailed information about a specific place."""
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,geometry,formatted_phone_number,website,rating,user_ratings_total,opening_hours,reviews,price_level,business_status",
        "key": GOOGLE_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"] == "OK":
            return data["result"]
        else:
            return None
    except Exception as e:
        print(f"❌ Details error: {e}")
        return None


def format_place_data(place, city_name, country_code):
    """Format place data for export."""
    location = place.get("geometry", {}).get("location", {})

    return {
        "place_id": place.get("place_id", ""),
        "name": place.get("name", ""),
        "address": place.get("formatted_address", place.get("vicinity", "")),
        "city": city_name,
        "country_code": country_code,
        "latitude": location.get("lat", ""),
        "longitude": location.get("lng", ""),
        "phone": place.get("formatted_phone_number", ""),
        "website": place.get("website", ""),
        "rating": place.get("rating", ""),
        "reviews_count": place.get("user_ratings_total", 0),
        "price_level": place.get("price_level", ""),
        "business_status": place.get("business_status", ""),
        "is_open": "Yes" if place.get("opening_hours", {}).get("open_now") else "No",
        "hours": str(place.get("opening_hours", {}).get("weekday_text", [])),
        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


# ---------- Main Extraction ----------
all_places = []
total_found = 0
processed_ids = set()  # Avoid duplicates

print(f"🔍 Searching {len(CITIES)} cities...")
print(f"📝 Using {len(SEARCH_QUERIES)} search queries per city")
print("")

for city_info in CITIES:
    city_name = city_info["city"]
    country_code = city_info["country"]
    radius = city_info["radius"]

    print(f"📍 Processing: {city_name}, {country_code}")

    # Get city coordinates
    lat, lng = geocode_city(f"{city_name}, {country_code}")

    if not lat or not lng:
        print(f"   ⚠️  Skipped (geocoding failed)")
        continue

    city_total = 0

    # Search with different queries
    for query in SEARCH_QUERIES:
        print(f"   🔍 Searching: '{query}'...", end=" ", flush=True)

        results = search_nearby(lat, lng, radius, query)
        places = results.get("results", [])

        if not places:
            print("No results")
            continue

        new_places = 0
        for place in places:
            place_id = place.get("place_id")

            # Skip duplicates
            if place_id in processed_ids:
                continue

            processed_ids.add(place_id)

            # Get detailed information
            details = get_place_details(place_id)
            if details:
                place_data = format_place_data(details, city_name, country_code)
                all_places.append(place_data)
                new_places += 1
                city_total += 1

            # Rate limiting (Google allows ~100 requests per second)
            time.sleep(0.1)

        print(f"Found {new_places} new shops")
        time.sleep(1)  # Extra delay between queries

    print(f"   ✅ Total for {city_name}: {city_total} shops")
    total_found += city_total
    print("")

    # Longer delay between cities
    time.sleep(2)

# ---------- Export Results ----------
print("")
print("=" * 60)
print("📊 Exporting Results...")
print("=" * 60)

if all_places:
    df = pd.DataFrame(all_places)

    # Create output directory
    output_dir = "public/data"
    os.makedirs(output_dir, exist_ok=True)

    # Generate filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_file = f"{output_dir}/google_places_motorcycle_shops_{timestamp}.xlsx"
    csv_file = f"{output_dir}/google_places_motorcycle_shops.csv"

    # Export to Excel
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Motorcycle Shops')

        # Auto-adjust column widths
        worksheet = writer.sheets['Motorcycle Shops']
        for idx, col in enumerate(df.columns):
            max_length = max(df[col].astype(str).apply(len).max(), len(col))
            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)

    # Export to CSV
    df.to_csv(csv_file, index=False)

    print(f"✅ Excel file: {excel_file}")
    print(f"✅ CSV file: {csv_file}")
    print(f"📊 Total records: {len(df)}")

    # Show statistics
    print("")
    print("📈 Statistics:")
    print(f"   Cities processed: {len([c for c in CITIES if True])}")
    print(f"   Total shops found: {total_found}")
    print(f"   Unique shops: {len(df)}")
    print(f"   Avg rating: {df['rating'].mean():.2f}" if df['rating'].mean() else "N/A")
    print(f"   Shops with websites: {df['website'].notna().sum()}")
    print(f"   Shops with phones: {df['phone'].notna().sum()}")

else:
    print("⚠️  No data collected")

print("")
print("=" * 60)
print("🎉 Extraction Complete!")
print("=" * 60)
print("")
print("💡 Tips:")
print("   - Customize CITIES list to focus on specific regions")
print("   - Adjust radius to search wider/narrower areas")
print("   - Monitor Google API usage in Cloud Console")
print("   - Estimated cost: ~$0.017 per place details request")
print("")
