import os
import time
import requests
import pandas as pd
from datetime import datetime

print("=" * 60)
print("🏍️  Motorcycle Shop Data Fetcher - Excel Export")
print("=" * 60)
print("")

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
    """Fetch motorcycle shop data from OpenStreetMap for a specific country."""
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

    try:
        response = requests.get(url, params={'data': query}, timeout=90)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print(f"⏱️  Timeout")
        return {"elements": []}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"elements": []}

# ---------- Helper to format data for Excel ----------
def format_records_for_excel(data, country_code):
    """Convert OSM data to flat structure suitable for Excel."""
    records = []
    for element in data.get("elements", []):
        tags = element.get("tags", {})
        if not tags:
            continue

        # Create a flat record
        record = {
            "id": element["id"],
            "name": tags.get("name", ""),
            "country_code": tags.get("addr:country", country_code),
            "city": tags.get("addr:city", ""),
            "street": tags.get("addr:street", ""),
            "housenumber": tags.get("addr:housenumber", ""),
            "postcode": tags.get("addr:postcode", ""),
            "suburb": tags.get("addr:suburb", ""),
            "latitude": element.get("lat", ""),
            "longitude": element.get("lon", ""),
            "phone": tags.get("contact:phone") or tags.get("phone", ""),
            "website": tags.get("contact:website") or tags.get("website", ""),
            "email": tags.get("contact:email") or tags.get("email", ""),
            "shop_type": tags.get("shop", tags.get("craft", tags.get("amenity", ""))),
            "source_country": country_code,
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        records.append(record)

    return records

# ---------- Main data collection ----------
all_records = []
total_shops = 0
successful_countries = 0
failed_countries = []

for code in COUNTRIES:
    try:
        data = fetch_overpass_data(code)
        records = format_records_for_excel(data, code)

        if not records:
            print(f"⚠️  No shops found")
            continue

        all_records.extend(records)
        print(f"✅ Found {len(records)} shops")
        total_shops += len(records)
        successful_countries += 1

        # Be kind to Overpass API - wait between requests
        time.sleep(10)

    except Exception as e:
        print(f"❌ Error: {e}")
        failed_countries.append(code)
        # Wait longer after errors
        time.sleep(20)

# ---------- Export to Excel ----------
print("")
print("=" * 60)
print("📊 Exporting to Excel...")
print("=" * 60)

if all_records:
    # Create DataFrame
    df = pd.DataFrame(all_records)

    # Reorder columns for better readability
    column_order = [
        "id", "name", "country_code", "city", "street", "housenumber",
        "postcode", "suburb", "latitude", "longitude", "phone", "email",
        "website", "shop_type", "source_country", "scraped_at"
    ]
    df = df[column_order]

    # Create output directory if it doesn't exist
    output_dir = "public/data"
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_filename = f"{output_dir}/worldwide_motorcycle_shops_{timestamp}.xlsx"

    # Export to Excel with formatting
    with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Motorcycle Shops')

        # Auto-adjust column widths
        worksheet = writer.sheets['Motorcycle Shops']
        for idx, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).apply(len).max(),
                len(col)
            )
            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)

    print(f"✅ Excel file created: {excel_filename}")
    print(f"📊 Total records: {len(df)}")
    print("")

    # Also save as CSV for web compatibility
    csv_filename = f"{output_dir}/worldwide_motorcycle_shops.csv"
    df.to_csv(csv_filename, index=False)
    print(f"✅ CSV file created: {csv_filename}")

else:
    print("⚠️  No data collected. Excel file not created.")

# ---------- Summary ----------
print("")
print("=" * 60)
print("🎉 Data Collection Complete!")
print("=" * 60)
print(f"✅ Successfully processed: {successful_countries}/{len(COUNTRIES)} countries")
print(f"📊 Total shops collected: {total_shops}")

if failed_countries:
    print(f"⚠️  Failed countries: {', '.join(failed_countries)}")
    print("   You can run the script again to retry failed countries")

print("")
print("🏍️  Next steps:")
print("   1. Open the Excel file to view the data")
print(f"   2. Update your app to use: /data/worldwide_motorcycle_shops.csv")
print("   3. Run: npm run dev")
print("   4. Open: http://localhost:3000")
print("")
