import os
import sys
import time
import requests
import pandas as pd
from datetime import datetime
import argparse

"""
OpenStreetMap Data Extractor - By Country/Region

Extract motorcycle shop data for specific countries or regions from OpenStreetMap.

USAGE:
    # Single country
    python scripts/fetch_by_country.py --country US

    # Multiple countries
    python scripts/fetch_by_country.py --countries US CA MX

    # Region
    python scripts/fetch_by_country.py --region north_america

    # Custom list from file
    python scripts/fetch_by_country.py --file countries.txt

    # List available regions
    python scripts/fetch_by_country.py --list-regions
"""

# ---------- Region Definitions ----------
REGIONS = {
    "europe": [
        "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU",
        "IS", "IE", "IT", "LV", "LT", "LU", "MT", "NL", "NO", "PL", "PT", "RO", "RS",
        "SK", "SI", "ES", "SE", "CH", "TR", "UA", "GB"
    ],
    "north_america": ["CA", "MX", "US"],
    "south_america": ["AR", "BR", "CL", "CO", "CR", "PE", "UY", "VE"],
    "asia": [
        "BD", "KH", "CN", "IN", "ID", "JP", "MY", "NP", "PK", "PH", "SG", "KR", "LK",
        "TW", "TH", "VN"
    ],
    "middle_east": ["AE", "IL", "SA"],
    "oceania": ["AU", "NZ"],
    "africa": ["EG", "KE", "MA", "NG", "ZA", "TZ"],
    "eu": [
        "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR",
        "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL",
        "PL", "PT", "RO", "SK", "SI", "ES", "SE"
    ],
    "asia_southeast": ["TH", "VN", "PH", "MY", "SG", "ID", "KH"],
    "asia_south": ["IN", "PK", "BD", "LK", "NP"],
    "asia_east": ["JP", "KR", "CN", "TW"],
}

COUNTRY_NAMES = {
    # Europe
    "AT": "Austria", "BE": "Belgium", "BG": "Bulgaria", "HR": "Croatia",
    "CY": "Cyprus", "CZ": "Czech Republic", "DK": "Denmark", "EE": "Estonia",
    "FI": "Finland", "FR": "France", "DE": "Germany", "GR": "Greece",
    "HU": "Hungary", "IS": "Iceland", "IE": "Ireland", "IT": "Italy",
    "LV": "Latvia", "LT": "Lithuania", "LU": "Luxembourg", "MT": "Malta",
    "NL": "Netherlands", "NO": "Norway", "PL": "Poland", "PT": "Portugal",
    "RO": "Romania", "RS": "Serbia", "SK": "Slovakia", "SI": "Slovenia",
    "ES": "Spain", "SE": "Sweden", "CH": "Switzerland", "TR": "Turkey",
    "UA": "Ukraine", "GB": "United Kingdom",
    # Americas
    "CA": "Canada", "MX": "Mexico", "US": "United States",
    "AR": "Argentina", "BR": "Brazil", "CL": "Chile", "CO": "Colombia",
    "CR": "Costa Rica", "PE": "Peru", "UY": "Uruguay", "VE": "Venezuela",
    # Asia
    "BD": "Bangladesh", "KH": "Cambodia", "CN": "China", "IN": "India",
    "ID": "Indonesia", "JP": "Japan", "MY": "Malaysia", "NP": "Nepal",
    "PK": "Pakistan", "PH": "Philippines", "SG": "Singapore", "KR": "South Korea",
    "LK": "Sri Lanka", "TW": "Taiwan", "TH": "Thailand", "VN": "Vietnam",
    # Middle East
    "AE": "UAE", "IL": "Israel", "SA": "Saudi Arabia",
    # Oceania
    "AU": "Australia", "NZ": "New Zealand",
    # Africa
    "EG": "Egypt", "KE": "Kenya", "MA": "Morocco", "NG": "Nigeria",
    "ZA": "South Africa", "TZ": "Tanzania",
}

# ---------- Helper Functions ----------

def fetch_overpass_data(country_code):
    """Fetch motorcycle shop data from OpenStreetMap."""
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

    country_name = COUNTRY_NAMES.get(country_code, country_code)
    print(f"🔍 Fetching {country_name} ({country_code})...", end=" ", flush=True)

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


def format_records(data, country_code):
    """Convert OSM data to flat structure."""
    records = []
    for element in data.get("elements", []):
        tags = element.get("tags", {})
        if not tags:
            continue

        record = {
            "id": element["id"],
            "name": tags.get("name", ""),
            "country_code": tags.get("addr:country", country_code),
            "country_name": COUNTRY_NAMES.get(country_code, country_code),
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
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        records.append(record)

    return records


def list_regions():
    """Display available regions."""
    print("")
    print("=" * 60)
    print("Available Regions")
    print("=" * 60)
    print("")

    for region, countries in REGIONS.items():
        country_names = [COUNTRY_NAMES.get(c, c) for c in countries[:5]]
        more = f" (+{len(countries)-5} more)" if len(countries) > 5 else ""
        print(f"  {region:20} - {len(countries):2} countries - {', '.join(country_names)}{more}")

    print("")


def export_data(records, countries_str, output_format="both"):
    """Export data to Excel and/or CSV."""
    if not records:
        print("⚠️  No data to export")
        return

    df = pd.DataFrame(records)

    # Create output directory
    output_dir = "public/data"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"motorcycle_shops_{countries_str}_{timestamp}"

    files_created = []

    # Export to Excel
    if output_format in ["both", "excel"]:
        excel_file = f"{output_dir}/{base_name}.xlsx"
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Motorcycle Shops')

            # Auto-adjust columns
            worksheet = writer.sheets['Motorcycle Shops']
            for idx, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).apply(len).max(), len(col))
                worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)

        files_created.append(excel_file)

    # Export to CSV
    if output_format in ["both", "csv"]:
        csv_file = f"{output_dir}/{base_name}.csv"
        df.to_csv(csv_file, index=False)
        files_created.append(csv_file)

    print("")
    print("=" * 60)
    print("📊 Export Complete")
    print("=" * 60)
    for file in files_created:
        print(f"✅ {file}")
    print(f"📊 Total records: {len(df)}")
    print("")

    # Statistics
    print("📈 Statistics by Country:")
    country_stats = df.groupby('country_name').size().sort_values(ascending=False)
    for country, count in country_stats.items():
        print(f"   {country:25} {count:4} shops")

    print("")


# ---------- Main Function ----------

def main():
    parser = argparse.ArgumentParser(
        description="Extract motorcycle shop data by country or region from OpenStreetMap"
    )
    parser.add_argument("--country", help="Single country code (e.g., US)")
    parser.add_argument("--countries", nargs="+", help="Multiple country codes (e.g., US CA MX)")
    parser.add_argument("--region", choices=REGIONS.keys(), help="Region name")
    parser.add_argument("--file", help="File with country codes (one per line)")
    parser.add_argument("--list-regions", action="store_true", help="List available regions")
    parser.add_argument("--format", choices=["excel", "csv", "both"], default="both",
                       help="Output format (default: both)")
    parser.add_argument("--delay", type=int, default=10,
                       help="Delay between requests in seconds (default: 10)")

    args = parser.parse_args()

    # List regions and exit
    if args.list_regions:
        list_regions()
        return

    # Determine countries to process
    countries = []

    if args.country:
        countries = [args.country.upper()]
    elif args.countries:
        countries = [c.upper() for c in args.countries]
    elif args.region:
        countries = REGIONS[args.region]
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                countries = [line.strip().upper() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"❌ File not found: {args.file}")
            return
    else:
        parser.print_help()
        return

    # Display summary
    print("")
    print("=" * 60)
    print("🏍️  OSM Data Extractor - By Country/Region")
    print("=" * 60)
    print(f"📍 Countries to process: {len(countries)}")
    print(f"⏱️  Delay between requests: {args.delay}s")
    print("")

    # Collect data
    all_records = []
    successful = 0
    failed = []

    for country_code in countries:
        try:
            data = fetch_overpass_data(country_code)
            records = format_records(data, country_code)

            if records:
                all_records.extend(records)
                print(f"✅ Found {len(records)} shops")
                successful += 1
            else:
                print(f"⚠️  No shops found")

            # Rate limiting
            time.sleep(args.delay)

        except Exception as e:
            print(f"❌ Error: {e}")
            failed.append(country_code)
            time.sleep(args.delay * 2)

    # Export results
    countries_str = "_".join(countries[:3])
    if len(countries) > 3:
        countries_str += f"_and_{len(countries)-3}_more"

    export_data(all_records, countries_str, args.format)

    # Summary
    print("=" * 60)
    print("🎉 Data Collection Complete")
    print("=" * 60)
    print(f"✅ Successful: {successful}/{len(countries)} countries")
    print(f"📊 Total shops: {len(all_records)}")

    if failed:
        print(f"⚠️  Failed: {', '.join(failed)}")

    print("")


if __name__ == "__main__":
    main()
