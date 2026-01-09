import { NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';

/**
 * GET /api/stats
 *
 * Get statistics about motorcycle shops in the database
 *
 * Returns:
 * - Total shops
 * - Shops by country
 * - Shops with contact information
 * - Top cities
 */

interface Shop {
  id: string | number;
  name?: string;
  country_code?: string;
  city?: string;
  phone?: string;
  website?: string;
  email?: string;
  [key: string]: any;
}

export async function GET() {
  try {
    // Read CSV file
    const csvPath = path.join(process.cwd(), 'public', 'data', 'eu_motorcycle_repairs.csv');
    const fileContent = await fs.readFile(csvPath, 'utf-8');

    // Parse CSV
    const lines = fileContent.trim().split('\n');
    const headers = lines[0].split(',');

    const shops: Shop[] = [];

    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].split(',');
      const shop: Shop = {};

      headers.forEach((header, index) => {
        shop[header.trim()] = values[index]?.trim() || '';
      });

      shops.push(shop);
    }

    // Calculate statistics
    const total = shops.length;

    // Shops by country
    const byCountry: Record<string, number> = {};
    shops.forEach(shop => {
      const country = shop.country_code || 'Unknown';
      byCountry[country] = (byCountry[country] || 0) + 1;
    });

    // Shops by city (top 20)
    const byCity: Record<string, number> = {};
    shops.forEach(shop => {
      if (shop.city) {
        const city = shop.city;
        byCity[city] = (byCity[city] || 0) + 1;
      }
    });

    const topCities = Object.entries(byCity)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 20)
      .map(([city, count]) => ({ city, count }));

    // Contact information coverage
    const withPhone = shops.filter(s => s.phone && s.phone !== '').length;
    const withWebsite = shops.filter(s => s.website && s.website !== '' && s.website !== 'N/A').length;
    const withEmail = shops.filter(s => s.email && s.email !== '').length;

    return NextResponse.json({
      success: true,
      data: {
        total,
        byCountry: Object.entries(byCountry)
          .sort((a, b) => b[1] - a[1])
          .map(([country, count]) => ({ country, count })),
        topCities,
        contactInfo: {
          withPhone,
          withWebsite,
          withEmail,
          phonePercentage: ((withPhone / total) * 100).toFixed(1) + '%',
          websitePercentage: ((withWebsite / total) * 100).toFixed(1) + '%',
          emailPercentage: ((withEmail / total) * 100).toFixed(1) + '%',
        },
      },
    });

  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to fetch statistics',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}
