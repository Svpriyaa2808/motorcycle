/**
 * Simple CSV parser utility
 * Parses CSV text into an array of objects
 */

interface MotorcycleShopCSV {
  id: string;
  name: string;
  country_code: string;
  lat: string;
  lon: string;
  city: string;
  street: string;
  housenumber: string;
  postcode: string;
  phone: string;
  website: string;
  email: string;
}

interface MotorcycleShop {
  id: number;
  name?: string;
  lat?: number;
  lon?: number;
  address?: {
    city?: string;
    street?: string;
    housenumber?: string;
    postcode?: string;
    suburb?: string;
  };
  contact?: {
    phone?: string;
    fax?: string;
    website?: string;
    email?: string;
  };
  country_code?: string;
  shop_tags?: Record<string, string>;
}

export function parseCSV(csvText: string): MotorcycleShop[] {
  const lines = csvText.trim().split('\n');

  if (lines.length < 2) {
    return [];
  }

  // Get headers
  const headers = lines[0].split(',').map(h => h.trim());

  // Parse data rows
  const data: MotorcycleShop[] = [];

  for (let i = 1; i < lines.length; i++) {
    const line = lines[i];

    // Parse CSV line respecting quotes
    const values: string[] = [];
    let currentValue = '';
    let insideQuotes = false;

    for (let j = 0; j < line.length; j++) {
      const char = line[j];

      if (char === '"') {
        insideQuotes = !insideQuotes;
      } else if (char === ',' && !insideQuotes) {
        values.push(currentValue.trim());
        currentValue = '';
      } else {
        currentValue += char;
      }
    }
    values.push(currentValue.trim());

    // Create object from headers and values
    const row: any = {};
    headers.forEach((header, index) => {
      row[header] = values[index] || '';
    });

    // Extract country code from city field (format: "City, Country")
    let cityName = row.city || '';
    let countryName = '';
    if (cityName.includes(',')) {
      const parts = cityName.split(',');
      cityName = parts[0].trim();
      countryName = parts[1]?.trim() || '';
    }

    // Map country names to codes
    const countryCodeMap: Record<string, string> = {
      'France': 'FR',
      'Germany': 'DE',
      'Italy': 'IT',
      'Spain': 'ES',
      'Netherlands': 'NL',
      'Belgium': 'BE',
      'Austria': 'AT',
      'Poland': 'PL',
      'Portugal': 'PT',
      'Greece': 'GR',
      'Czech Republic': 'CZ',
      'Hungary': 'HU',
      'Sweden': 'SE',
      'Denmark': 'DK',
      'Finland': 'FI',
      'Ireland': 'IE',
      'Romania': 'RO',
      'Bulgaria': 'BG',
      'Croatia': 'HR',
      'Slovakia': 'SK',
      'Slovenia': 'SI',
      'Lithuania': 'LT',
      'Latvia': 'LV',
      'Estonia': 'EE',
      'Luxembourg': 'LU',
      'Malta': 'MT',
      'Cyprus': 'CY',
    };

    // Transform CSV row to MotorcycleShop format
    const shop: MotorcycleShop = {
      id: row.id ? parseInt(row.id) : i,
      name: row.name || undefined,
      lat: row.latitude ? parseFloat(row.latitude) : (row.lat ? parseFloat(row.lat) : undefined),
      lon: row.longitude ? parseFloat(row.longitude) : (row.lon ? parseFloat(row.lon) : undefined),
      country_code: row.country_code || countryCodeMap[countryName] || undefined,
      address: {
        city: cityName || row.city || undefined,
        street: row.address || row.street || undefined,
        housenumber: row.housenumber || undefined,
        postcode: row.postcode || undefined,
      },
      contact: {
        phone: row.phone || undefined,
        website: row.website !== 'N/A' ? row.website : undefined,
        email: row.email || undefined,
      },
    };

    data.push(shop);
  }

  return data;
}

export async function fetchCSVData(csvPath: string = '/data/eu_motorcycle_repairs.csv'): Promise<MotorcycleShop[]> {
  try {
    const response = await fetch(csvPath);

    if (!response.ok) {
      throw new Error(`Failed to fetch CSV: ${response.statusText}`);
    }

    const csvText = await response.text();
    return parseCSV(csvText);
  } catch (error) {
    console.error('Error fetching CSV data:', error);
    return [];
  }
}
