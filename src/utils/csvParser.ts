// Utility to parse CSV files
export interface MotorcycleShopCSV {
  id: string;
  name: string;
  lat: string;
  lon: string;
  street?: string;
  housenumber?: string;
  postcode?: string;
  city?: string;
  country_code: string;
  phone?: string;
  website?: string;
  email?: string;
}

export interface MotorcycleShop {
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

/**
 * Parse CSV text into an array of objects
 */
export function parseCSV(csvText: string): MotorcycleShopCSV[] {
  const lines = csvText.trim().split('\n');

  if (lines.length < 2) {
    return [];
  }

  // Get headers from first line
  const headers = lines[0].split(',').map(h => h.trim());

  // Parse data lines
  const data: MotorcycleShopCSV[] = [];

  for (let i = 1; i < lines.length; i++) {
    const values = lines[i].split(',').map(v => v.trim());
    const row: any = {};

    headers.forEach((header, index) => {
      row[header] = values[index] || '';
    });

    data.push(row as MotorcycleShopCSV);
  }

  return data;
}

/**
 * Transform CSV data to match the MotorcycleShop interface
 */
export function transformCSVToShops(csvData: MotorcycleShopCSV[]): MotorcycleShop[] {
  return csvData.map(row => ({
    id: parseInt(row.id, 10),
    name: row.name || undefined,
    lat: row.lat ? parseFloat(row.lat) : undefined,
    lon: row.lon ? parseFloat(row.lon) : undefined,
    address: {
      city: row.city || undefined,
      street: row.street || undefined,
      housenumber: row.housenumber || undefined,
      postcode: row.postcode || undefined,
    },
    contact: {
      phone: row.phone || undefined,
      website: row.website || undefined,
      email: row.email || undefined,
    },
    country_code: row.country_code || undefined,
  }));
}

/**
 * Fetch and parse CSV file from public directory
 */
export async function fetchMotorcycleShops(csvPath: string = '/data/motorcycle_shops.csv'): Promise<MotorcycleShop[]> {
  try {
    const response = await fetch(csvPath);

    if (!response.ok) {
      throw new Error(`Failed to fetch CSV: ${response.statusText}`);
    }

    const csvText = await response.text();
    const csvData = parseCSV(csvText);
    const shops = transformCSVToShops(csvData);

    return shops;
  } catch (error) {
    console.error('Error fetching motorcycle shops:', error);
    return [];
  }
}
