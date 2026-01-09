# Motorcycle Shops API Documentation

This document describes how to extract and access motorcycle shop data using various APIs.

---

## Table of Contents

1. [Data Extraction Methods](#data-extraction-methods)
2. [REST API Endpoints](#rest-api-endpoints)
3. [Python Scripts](#python-scripts)
4. [Usage Examples](#usage-examples)

---

## Data Extraction Methods

### 1. OpenStreetMap (OSM) Overpass API

**Advantages:**
- Free to use
- Global coverage
- Open data (ODbL license)
- No API key required

**Limitations:**
- Data quality varies by region
- Rate limits (avoid excessive requests)
- Limited commercial information

**Scripts:**
- `scripts/fetch_osm_to_excel.py` - Export worldwide data to Excel/CSV
- `scripts/fetch_by_country.py` - Extract data by country or region
- `scripts/fetch_osm_data.py` - Export to Supabase database

### 2. Google Places API

**Advantages:**
- High-quality commercial data
- Ratings, reviews, photos
- Business hours, phone numbers
- Comprehensive coverage

**Limitations:**
- Paid service ($0.017 per place details request)
- Requires API key
- Usage quotas

**Scripts:**
- `scripts/fetch_google_places.py` - Extract data using Google Places API

---

## REST API Endpoints

Your Next.js app provides REST API endpoints to access the collected data.

### Base URL

```
http://localhost:3000/api
```

In production:
```
https://your-domain.com/api
```

---

### 1. Get All Shops

```http
GET /api/shops
```

**Query Parameters:**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| country | string | Filter by country code | `?country=US` |
| limit | number | Limit results | `?limit=100` |
| offset | number | Skip results (pagination) | `?offset=50` |
| search | string | Search by name or city | `?search=honda` |

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": "123",
      "name": "Honda Motorcycle Shop",
      "country_code": "US",
      "city": "New York",
      "latitude": "40.7128",
      "longitude": "-74.0060",
      "phone": "+1-212-555-0100",
      "website": "https://example.com",
      "email": "info@example.com"
    }
  ],
  "meta": {
    "total": 3150,
    "returned": 100,
    "offset": 0,
    "limit": 100
  }
}
```

**Examples:**

```bash
# Get all shops
curl http://localhost:3000/api/shops

# Get shops in United States
curl http://localhost:3000/api/shops?country=US

# Get first 50 shops
curl http://localhost:3000/api/shops?limit=50

# Search for "repair" with pagination
curl http://localhost:3000/api/shops?search=repair&limit=20&offset=40

# Get shops in France, limit 100
curl http://localhost:3000/api/shops?country=FR&limit=100
```

---

### 2. Get Single Shop

```http
GET /api/shops/[id]
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| id | string | Shop ID |

**Response:**

```json
{
  "success": true,
  "data": {
    "id": "123",
    "name": "Honda Motorcycle Shop",
    "country_code": "US",
    "city": "New York",
    "latitude": "40.7128",
    "longitude": "-74.0060",
    "phone": "+1-212-555-0100",
    "website": "https://example.com"
  }
}
```

**Examples:**

```bash
# Get shop by ID
curl http://localhost:3000/api/shops/123
```

---

### 3. Get Statistics

```http
GET /api/stats
```

**Response:**

```json
{
  "success": true,
  "data": {
    "total": 3150,
    "byCountry": [
      { "country": "US", "count": 450 },
      { "country": "FR", "count": 380 },
      { "country": "DE", "count": 350 }
    ],
    "topCities": [
      { "city": "Paris", "count": 45 },
      { "city": "Berlin", "count": 38 }
    ],
    "contactInfo": {
      "withPhone": 2500,
      "withWebsite": 1800,
      "withEmail": 1200,
      "phonePercentage": "79.4%",
      "websitePercentage": "57.1%",
      "emailPercentage": "38.1%"
    }
  }
}
```

**Examples:**

```bash
# Get statistics
curl http://localhost:3000/api/stats
```

---

## Python Scripts

### 1. OpenStreetMap to Excel/CSV

**File:** `scripts/fetch_osm_to_excel.py`

**Description:** Extract worldwide motorcycle shop data from OpenStreetMap and export to Excel and CSV.

**Usage:**

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Run the script
python scripts/fetch_osm_to_excel.py
```

**Output:**
- `public/data/worldwide_motorcycle_shops_YYYYMMDD_HHMMSS.xlsx`
- `public/data/worldwide_motorcycle_shops.csv`

**Time:** ~13-20 minutes for 81 countries

---

### 2. Extract by Country/Region

**File:** `scripts/fetch_by_country.py`

**Description:** Extract data for specific countries or regions from OpenStreetMap.

**Usage:**

```bash
# Single country
python scripts/fetch_by_country.py --country US

# Multiple countries
python scripts/fetch_by_country.py --countries US CA MX

# By region
python scripts/fetch_by_country.py --region europe
python scripts/fetch_by_country.py --region asia
python scripts/fetch_by_country.py --region north_america

# List available regions
python scripts/fetch_by_country.py --list-regions

# From file
echo "US\nCA\nMX" > countries.txt
python scripts/fetch_by_country.py --file countries.txt

# Only CSV output
python scripts/fetch_by_country.py --country US --format csv
```

**Available Regions:**
- `europe` - 34 countries
- `north_america` - 3 countries
- `south_america` - 8 countries
- `asia` - 16 countries
- `middle_east` - 3 countries
- `oceania` - 2 countries
- `africa` - 6 countries
- `eu` - 27 EU countries
- `asia_southeast` - Southeast Asia
- `asia_south` - South Asia
- `asia_east` - East Asia

---

### 3. Google Places API Extractor

**File:** `scripts/fetch_google_places.py`

**Description:** Extract detailed motorcycle shop data using Google Places API.

**Setup:**

1. Get Google Places API key:
   - Go to https://console.cloud.google.com/
   - Create/select project
   - Enable "Places API"
   - Create credentials → API Key

2. Add to `.env.local`:
   ```
   GOOGLE_PLACES_API_KEY=your_api_key_here
   ```

**Usage:**

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Run the script
python scripts/fetch_google_places.py
```

**Customization:**

Edit the `CITIES` list in the script to target specific cities:

```python
CITIES = [
    {"city": "New York", "country": "US", "radius": 50000},
    {"city": "Los Angeles", "country": "US", "radius": 50000},
    # Add more cities...
]
```

**Cost Estimation:**
- Nearby Search: $32 per 1,000 requests
- Place Details: $17 per 1,000 requests
- Estimated total: ~$0.05 per shop with details

---

## Usage Examples

### Using the REST API in JavaScript

```javascript
// Fetch all shops in USA
async function getUSAShops() {
  const response = await fetch('/api/shops?country=US');
  const data = await response.json();
  console.log(data.data); // Array of shops
}

// Search for shops
async function searchShops(query) {
  const response = await fetch(`/api/shops?search=${encodeURIComponent(query)}&limit=20`);
  const data = await response.json();
  return data.data;
}

// Get shop by ID
async function getShop(id) {
  const response = await fetch(`/api/shops/${id}`);
  const data = await response.json();
  return data.data;
}

// Get statistics
async function getStats() {
  const response = await fetch('/api/stats');
  const data = await response.json();
  console.log(data.data);
}
```

### Using the REST API with curl

```bash
# Get all shops with pagination
curl "http://localhost:3000/api/shops?limit=100&offset=0"

# Get shops in multiple requests
curl "http://localhost:3000/api/shops?country=US" > us_shops.json
curl "http://localhost:3000/api/shops?country=CA" > ca_shops.json

# Pipe to jq for formatting
curl "http://localhost:3000/api/shops?limit=10" | jq '.data'

# Download as CSV using Python script
python scripts/fetch_by_country.py --country US --format csv
```

### Integrating with Python

```python
import requests

# Get all shops
response = requests.get('http://localhost:3000/api/shops')
shops = response.json()['data']

# Filter by country
response = requests.get('http://localhost:3000/api/shops', params={'country': 'US'})
us_shops = response.json()['data']

# Search
response = requests.get('http://localhost:3000/api/shops', params={
    'search': 'honda',
    'limit': 50
})
results = response.json()['data']

# Get statistics
response = requests.get('http://localhost:3000/api/stats')
stats = response.json()['data']
print(f"Total shops: {stats['total']}")
```

---

## Rate Limits & Best Practices

### OpenStreetMap Overpass API

- **Rate Limit:** ~2 requests per second
- **Recommendation:** Use 10-second delay between country queries
- **Usage:** Free for reasonable use
- **Documentation:** https://wiki.openstreetmap.org/wiki/Overpass_API

### Google Places API

- **Rate Limit:** 100 requests per second
- **Cost:** Pay-per-use (see pricing)
- **Recommendation:** Batch requests, cache results
- **Documentation:** https://developers.google.com/maps/documentation/places/web-service

### Your Next.js API

- **Rate Limit:** None (add if needed)
- **Recommendation:** Implement caching for performance
- **Authentication:** Add if exposing publicly

---

## Error Handling

All API endpoints return errors in this format:

```json
{
  "success": false,
  "error": "Error description",
  "message": "Detailed error message"
}
```

**Common Status Codes:**
- `200` - Success
- `404` - Resource not found
- `500` - Server error

---

## Data Format

### CSV Structure

```csv
id,name,country_code,city,street,housenumber,postcode,latitude,longitude,phone,email,website,shop_type,scraped_at
123,Honda Shop,US,New York,5th Ave,100,10001,40.7128,-74.0060,+1-212-555-0100,info@example.com,https://example.com,motorcycle,2025-01-09 10:30:00
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| id | string/number | Unique shop identifier |
| name | string | Shop name |
| country_code | string | ISO 3166-1 alpha-2 code |
| city | string | City name |
| street | string | Street name |
| housenumber | string | Building number |
| postcode | string | Postal/ZIP code |
| latitude | number | GPS latitude |
| longitude | number | GPS longitude |
| phone | string | Contact phone |
| email | string | Contact email |
| website | string | Website URL |
| shop_type | string | Type of shop |
| scraped_at | datetime | Collection timestamp |

---

## Support & Resources

- **OpenStreetMap Wiki:** https://wiki.openstreetmap.org/
- **Google Places API Docs:** https://developers.google.com/maps/documentation/places/
- **Project Repository:** Your GitHub repo URL
- **Issues:** Report bugs and feature requests on GitHub

---

## License

- OSM Data: Open Database License (ODbL)
- Google Places Data: Subject to Google's terms of service
- This API: Check your project license
