import { NextRequest, NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';

/**
 * GET /api/shops
 *
 * Query parameters:
 * - country: Filter by country code (e.g., ?country=US)
 * - limit: Limit results (e.g., ?limit=100)
 * - offset: Skip results (e.g., ?offset=50)
 * - search: Search by name or city (e.g., ?search=honda)
 *
 * Examples:
 * - GET /api/shops
 * - GET /api/shops?country=US
 * - GET /api/shops?country=US&limit=50
 * - GET /api/shops?search=repair&limit=20
 */

interface Shop {
  id: string | number;
  name?: string;
  country_code?: string;
  city?: string;
  latitude?: string | number;
  longitude?: string | number;
  phone?: string;
  website?: string;
  email?: string;
  [key: string]: any;
}

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const country = searchParams.get('country')?.toUpperCase();
    const limit = parseInt(searchParams.get('limit') || '0');
    const offset = parseInt(searchParams.get('offset') || '0');
    const search = searchParams.get('search')?.toLowerCase();

    // Read CSV file
    const csvPath = path.join(process.cwd(), 'public', 'data', 'eu_motorcycle_repairs.csv');
    const fileContent = await fs.readFile(csvPath, 'utf-8');

    // Parse CSV
    const lines = fileContent.trim().split('\n');
    const headers = lines[0].split(',');

    let shops: Shop[] = [];

    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].split(',');
      const shop: Shop = {};

      headers.forEach((header, index) => {
        shop[header.trim()] = values[index]?.trim() || '';
      });

      shops.push(shop);
    }

    // Apply filters
    let filteredShops = shops;

    if (country) {
      filteredShops = filteredShops.filter(
        shop => shop.country_code?.toUpperCase() === country
      );
    }

    if (search) {
      filteredShops = filteredShops.filter(
        shop =>
          shop.name?.toLowerCase().includes(search) ||
          shop.city?.toLowerCase().includes(search) ||
          shop.country_code?.toLowerCase().includes(search)
      );
    }

    // Pagination
    const total = filteredShops.length;
    if (offset > 0) {
      filteredShops = filteredShops.slice(offset);
    }
    if (limit > 0) {
      filteredShops = filteredShops.slice(0, limit);
    }

    return NextResponse.json({
      success: true,
      data: filteredShops,
      meta: {
        total,
        returned: filteredShops.length,
        offset,
        limit: limit || null,
      },
    });

  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to fetch shop data',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}
