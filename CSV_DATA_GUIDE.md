# CSV Data Guide for Motorcycle Repair Shops

## Overview
This application now reads motorcycle repair shop data from a CSV file instead of using an external API or database. The CSV file is located at `/public/data/motorcycle_shops.csv`.

## CSV File Structure

The CSV file should follow this format:

```csv
id,name,lat,lon,street,housenumber,postcode,city,country_code,phone,website,email
1,Shop Name,48.8566,2.3522,Street Name,45,75001,City,FR,+33 1 42 60 38 38,https://www.example.com,contact@example.com
```

### Column Descriptions

| Column | Required | Description | Example |
|--------|----------|-------------|---------|
| `id` | Yes | Unique identifier for the shop | 1, 2, 3, etc. |
| `name` | Yes | Name of the motorcycle shop | "Moto Expert Paris" |
| `lat` | Yes | Latitude coordinate | 48.8566 |
| `lon` | Yes | Longitude coordinate | 2.3522 |
| `street` | No | Street name | "Rue de Rivoli" |
| `housenumber` | No | House/building number | "45" |
| `postcode` | No | Postal code | "75001" |
| `city` | No | City name | "Paris" |
| `country_code` | Yes | Two-letter ISO country code | FR, DE, IT, ES, etc. |
| `phone` | No | Contact phone number | "+33 1 42 60 38 38" |
| `website` | No | Shop website URL | "https://www.example.com" |
| `email` | No | Contact email | "contact@example.com" |

## Supported Country Codes

The application supports the following European country codes:

- **FR** - France
- **DE** - Germany
- **IT** - Italy
- **ES** - Spain
- **NL** - Netherlands
- **AT** - Austria
- **BE** - Belgium
- **CZ** - Czech Republic
- **PT** - Portugal
- **DK** - Denmark
- **SE** - Sweden
- **FI** - Finland
- **PL** - Poland
- **HU** - Hungary
- **GR** - Greece
- **IE** - Ireland
- **CH** - Switzerland
- **NO** - Norway
- **SK** - Slovakia
- **SI** - Slovenia
- **EE** - Estonia
- And more...

## How to Add More Shops

1. Open `/public/data/motorcycle_shops.csv`
2. Add a new line with the shop information following the format above
3. Make sure to use the correct country code
4. Save the file
5. Refresh your browser - the new data will be loaded automatically

### Example Entry

```csv
31,Barcelona Custom Bikes,41.3874,2.1686,Carrer de Balmes,156,08008,Barcelona,ES,+34 93 234 5678,https://www.barcelonacustom.es,info@barcelonacustom.es
```

## How It Works

1. **CSV Storage**: The CSV file is stored in the `public/data/` directory, making it accessible via HTTP requests
2. **CSV Parser**: The utility at `src/utils/csvParser.ts` handles:
   - Fetching the CSV file
   - Parsing CSV text into structured data
   - Transforming the data to match the application's interface
3. **Component Integration**: The `MotorcycleShops` component loads the CSV data on mount
4. **Country Filtering**: When a user clicks on a country, the app filters shops by the `country_code` field
5. **Real-time Search**: Users can also search by shop name, city, or street

## Benefits of CSV Approach

- ✅ No API rate limits or quotas
- ✅ No external dependencies
- ✅ Easy to update and maintain
- ✅ Works offline (once loaded)
- ✅ Fast and lightweight
- ✅ No database setup required
- ✅ Version controllable with Git

## Updating Data

To update the motorcycle shop data:

1. Edit the CSV file directly at `/public/data/motorcycle_shops.csv`
2. Or replace it with your own CSV file (maintaining the same format)
3. Ensure the file is properly formatted (comma-separated, no extra commas)
4. The application will automatically load the new data

## Tips

- Keep the `id` column unique for each shop
- Use proper latitude and longitude for accurate map positioning
- Include country codes to enable country-based filtering
- Add contact information (phone, website, email) to make shops more useful
- Use standard ISO country codes for consistency
