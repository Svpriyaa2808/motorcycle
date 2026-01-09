import { NextRequest, NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';

/**
 * GET /api/shops/[id]
 *
 * Get a specific shop by ID
 *
 * Examples:
 * - GET /api/shops/123
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

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const shopId = params.id;

    // Read CSV file
    const csvPath = path.join(process.cwd(), 'public', 'data', 'eu_motorcycle_repairs.csv');
    const fileContent = await fs.readFile(csvPath, 'utf-8');

    // Parse CSV
    const lines = fileContent.trim().split('\n');
    const headers = lines[0].split(',');

    // Find shop by ID
    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].split(',');
      const shop: Shop = {};

      headers.forEach((header, index) => {
        shop[header.trim()] = values[index]?.trim() || '';
      });

      if (shop.id?.toString() === shopId) {
        return NextResponse.json({
          success: true,
          data: shop,
        });
      }
    }

    // Shop not found
    return NextResponse.json(
      {
        success: false,
        error: 'Shop not found',
        message: `No shop found with ID: ${shopId}`,
      },
      { status: 404 }
    );

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
