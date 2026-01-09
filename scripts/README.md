# Motorcycle Shop Data Collection Scripts

This directory contains scripts for collecting motorcycle shop data from OpenStreetMap.

## Scripts

### 1. `fetch_osm_to_excel.py` - Export to Excel/CSV (Recommended)

Fetches motorcycle shop data from OpenStreetMap and exports directly to Excel and CSV files.

**Features:**
- Collects data from 81 countries worldwide
- Exports to both Excel (.xlsx) and CSV formats
- No database required
- Easy to review and edit data

**Installation:**

```bash
# Install required packages
pip install -r requirements.txt
```

**Usage:**

```bash
# Run from the project root directory
python scripts/fetch_osm_to_excel.py
```

**Output:**
- Excel file: `public/data/worldwide_motorcycle_shops_YYYYMMDD_HHMMSS.xlsx`
- CSV file: `public/data/worldwide_motorcycle_shops.csv`

**Time Required:** ~13-20 minutes (81 countries × 10 seconds delay)

---

### 2. `fetch_osm_data.py` - Export to Supabase Database

Fetches data and stores it in Supabase database.

**Requirements:**
- Supabase account and credentials in `.env.local`
- Additional package: `supabase`

**Installation:**

```bash
pip install -r requirements.txt
pip install supabase
```

**Usage:**

```bash
python scripts/fetch_osm_data.py
```

---

## Countries Covered (81 Total)

### Europe (34)
Austria, Belgium, Bulgaria, Croatia, Cyprus, Czech Republic, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Iceland, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands, Norway, Poland, Portugal, Romania, Serbia, Slovakia, Slovenia, Spain, Sweden, Switzerland, Turkey, Ukraine, United Kingdom

### North America (3)
Canada, Mexico, United States

### Central & South America (8)
Argentina, Brazil, Chile, Colombia, Costa Rica, Peru, Uruguay, Venezuela

### Asia (16)
Bangladesh, Cambodia, China, India, Indonesia, Japan, Malaysia, Nepal, Pakistan, Philippines, Singapore, South Korea, Sri Lanka, Taiwan, Thailand, Vietnam

### Middle East (3)
United Arab Emirates, Israel, Saudi Arabia

### Oceania (2)
Australia, New Zealand

### Africa (6)
Egypt, Kenya, Morocco, Nigeria, South Africa, Tanzania

---

## Data Fields Collected

- **id** - Unique OpenStreetMap node ID
- **name** - Shop name
- **country_code** - ISO 3166-1 alpha-2 country code
- **city** - City name
- **street** - Street name
- **housenumber** - House/building number
- **postcode** - Postal code
- **suburb** - Suburb/district
- **latitude** - Latitude coordinate
- **longitude** - Longitude coordinate
- **phone** - Contact phone number
- **email** - Contact email
- **website** - Shop website URL
- **shop_type** - Type of shop (motorcycle, craft, car_repair)
- **source_country** - Source country code used for query
- **scraped_at** - Timestamp of data collection

---

## Notes

- The scripts use OpenStreetMap's Overpass API
- Rate limiting: 10-second delay between country queries
- Some countries may have limited or no motorcycle shop data in OSM
- Data quality depends on OSM contributors in each region

---

## Updating Your App

After generating the CSV file, update your app to use it:

1. The CSV file is automatically created at: `public/data/worldwide_motorcycle_shops.csv`
2. Your app already loads from `/data/eu_motorcycle_repairs.csv` by default
3. To use the new worldwide data, either:
   - Rename the file to `eu_motorcycle_repairs.csv`, OR
   - Update the path in your component

---

## Troubleshooting

**Script times out:**
- Some countries have large datasets (US, DE, FR)
- The script will continue with other countries
- Re-run to retry failed countries

**No data for certain countries:**
- Not all countries have motorcycle shops mapped in OpenStreetMap
- Consider contributing to OSM to improve coverage

**Rate limiting errors:**
- Increase the delay between requests (change `time.sleep(10)` to higher value)
- Overpass API has usage quotas

---

## Data Sources

- **OpenStreetMap** - Crowdsourced geographic data
- **Overpass API** - Query interface for OSM data
- Data licensed under ODbL (Open Database License)
