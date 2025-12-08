# 📄 CSV Data Usage Guide

Your motorcycle shop website now loads data from a CSV file instead of Supabase!

---

## 📍 CSV File Location

The data file is located at:
```
public/data/motorcycle_shops.csv
```

---

## 📝 CSV File Format

The CSV file has the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `id` | Unique shop ID | 1 |
| `name` | Shop name | BMW Motorrad Berlin |
| `country_code` | 2-letter country code | DE, FR, IT, ES |
| `lat` | Latitude | 52.5200 |
| `lon` | Longitude | 13.4050 |
| `city` | City name | Berlin |
| `street` | Street name | Hauptstraße |
| `housenumber` | House number | 123 |
| `postcode` | Postal code | 10115 |
| `phone` | Phone number | +49 30 12345678 |
| `website` | Website URL | https://example.com |
| `email` | Email address | info@example.com |

---

## ✏️ How to Add New Shops

### Option 1: Edit in VSCode

1. Open `public/data/motorcycle_shops.csv` in VSCode
2. Add a new line at the end with your shop data
3. Make sure to follow the CSV format (comma-separated)
4. Save the file
5. Refresh your browser - changes appear immediately!

### Example:
```csv
11,Vienna Motorcycles,AT,48.2082,16.3738,Vienna,Mariahilfer Straße,45,1070,+43 1 5234567,https://vienna-moto.at,info@vienna-moto.at
```

### Option 2: Edit in Excel/Google Sheets

1. Open `public/data/motorcycle_shops.csv` in Excel or Google Sheets
2. Add rows as needed
3. Save as CSV format
4. Make sure the file is saved back to `public/data/motorcycle_shops.csv`
5. Refresh your browser

---

## 🗺️ Country Codes Reference

Use these 2-letter codes for the `country_code` column:

| Country | Code | Country | Code |
|---------|------|---------|------|
| Germany | DE | Austria | AT |
| France | FR | Czech Republic | CZ |
| Italy | IT | Slovakia | SK |
| Spain | ES | Hungary | HU |
| Poland | PL | Portugal | PT |
| Netherlands | NL | Ireland | IE |
| Sweden | SE | Denmark | DK |
| Finland | FI | Estonia | EE |
| Belgium | BE | Lithuania | LT |
| Latvia | LV | Slovenia | SI |
| Croatia | HR | Romania | RO |
| Bulgaria | BG | Cyprus | CY |
| Luxembourg | LU | Malta | MT |
| Greece | EL | | |

---

## 🔍 How Country Filtering Works

1. **All shops displayed by default**: When you first open the site, all shops from the CSV are shown
2. **Click a country**: Select a country from the dropdown to filter shops
3. **Automatic filtering**: Only shops with matching `country_code` are displayed
4. **Reset filter**: Select "All Countries" to see all shops again

---

## 🧪 Testing Your Changes

After adding shops to the CSV:

1. Save the CSV file
2. Refresh your browser (http://localhost:3000)
3. Check if the new shops appear in the list
4. Test country filtering by clicking different countries
5. Verify the shop details are correct

---

## 📊 Sample CSV Data

Here's the sample data included in your CSV file:

- **Germany (DE)**: 3 shops (Berlin, Hamburg, Munich)
- **France (FR)**: 3 shops (Paris, Lyon, Nice)
- **Italy (IT)**: 2 shops (Milano, Rome)
- **Spain (ES)**: 2 shops (Madrid, Barcelona)

**Total: 10 sample shops**

---

## 🎯 Tips for Adding Quality Data

1. **Coordinates**: Use Google Maps to find accurate lat/lon
   - Right-click on the location → "What's here?"
   - Copy the coordinates shown
2. **Phone Numbers**: Include country code (e.g., +49 for Germany)
3. **Websites**: Use full URLs starting with `https://`
4. **Country Codes**: Always use 2-letter uppercase codes (DE, not Germany)
5. **Unique IDs**: Make sure each shop has a unique ID number

---

## 🚀 Running the Website

```bash
npm run dev
```

Open http://localhost:3000 in your browser

---

## ❓ Troubleshooting

### Shops not showing up?

1. Check CSV file syntax - ensure commas are in the right places
2. Verify the file is saved at `public/data/motorcycle_shops.csv`
3. Refresh your browser with Ctrl+F5 (hard refresh)
4. Check the browser console for errors (F12 → Console)

### Country filtering not working?

1. Ensure `country_code` column uses correct 2-letter codes
2. Codes must be uppercase (DE, not de)
3. Check that country exists in the dropdown

### Special characters in names/addresses?

- Avoid commas in text fields (use semicolon instead)
- For complex text, consider wrapping in quotes: `"Shop, Inc."`

---

## ✅ Benefits of CSV Approach

- ✅ **Easy to edit**: Use VSCode, Excel, or any text editor
- ✅ **No database needed**: No Supabase configuration required
- ✅ **Version control**: Track changes in Git
- ✅ **Fast**: Instant updates, no API calls
- ✅ **Portable**: Easy to backup and share

---

## 🎉 You're All Set!

Your motorcycle shop website now runs entirely on CSV data. Add, edit, or remove shops anytime by editing the CSV file!

Happy mapping! 🏍️
