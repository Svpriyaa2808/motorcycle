'use client'

import { useEffect, useState, useMemo } from "react";
import dynamic from 'next/dynamic';
import { fetchCSVData } from "@/utils/csvParser";
import CountrySelector from "../CountrySelector";
import { EU_COUNTRIES } from "@/data/countries";

// Dynamically import ShopMap to prevent SSR issues with Leaflet
const ShopMap = dynamic(() => import('../ShopMap'), {
  ssr: false,
  loading: () => (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden" style={{ height: '600px' }}>
      <div className="h-full flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading map...</p>
        </div>
      </div>
    </div>
  ),
});

// Define TypeScript types for your table
interface Address {
  city?: string;
  street?: string;
  housenumber?: string;
  postcode?: string;
  suburb?: string;
}

interface Contact {
  phone?: string;
  fax?: string;
  website?: string;
  email?: string;
}

interface MotorcycleShop {
  id: number;
  name?: string;
  lat?: number;
  lon?: number;
  address?: Address;
  contact?: Contact;
  country_code?: string;
  shop_tags?: Record<string, string>;
}

export default function MotorcycleShops() {
  const [allShops, setAllShops] = useState<MotorcycleShop[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedCountry, setSelectedCountry] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [viewMode, setViewMode] = useState<'map' | 'list'>('map');

  useEffect(() => {
    async function fetchShops() {
      try {
        const data = await fetchCSVData();
        setAllShops(data);
      } catch (error) {
        console.error("Error fetching CSV data:", error);
      }
      setLoading(false);
    }

    fetchShops();
  }, []);

  // Filter shops based on selected country and search query
  const filteredShops = useMemo(() => {
    let result = allShops;

    // Filter by country
    if (selectedCountry) {
      result = result.filter(shop => shop.country_code === selectedCountry);
    }

    // Filter by search query
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      result = result.filter(shop =>
        shop.name?.toLowerCase().includes(query) ||
        shop.address?.city?.toLowerCase().includes(query) ||
        shop.address?.street?.toLowerCase().includes(query) ||
        shop.country_code?.toLowerCase().includes(query)
      );
    }

    return result;
  }, [allShops, selectedCountry, searchQuery]);

  // Get country name from code
  const getCountryName = (code?: string) => {
    if (!code) return '';
    const country = EU_COUNTRIES.find(c => c.code === code);
    return country ? `${country.flag} ${country.name}` : code;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
          <p className="text-xl text-gray-700 font-semibold">Loading motorcycle shops...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-gray-900">
                🏍️ Motorcycle Repair Shops
              </h1>
              <p className="text-gray-600 mt-2">
                Find trusted motorcycle repair shops across Europe
              </p>
            </div>
            <div className="text-right">
              <p className="text-3xl font-bold text-blue-600">{filteredShops.length}</p>
              <p className="text-sm text-gray-600">
                {selectedCountry ? 'shops in country' : 'total shops'}
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Country Selector */}
        <CountrySelector
          selectedCountry={selectedCountry}
          onCountryChange={setSelectedCountry}
        />

        {/* Search and View Toggle */}
        <div className="mb-6 flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <input
                type="text"
                placeholder="Search by shop name, city, or street..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full px-5 py-3 pl-12 rounded-lg border-2 border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all"
              />
              <svg
                className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>

          <div className="flex gap-2 bg-white rounded-lg p-1 shadow-md">
            <button
              onClick={() => setViewMode('map')}
              className={`px-6 py-2 rounded-md font-medium transition-all ${
                viewMode === 'map'
                  ? 'bg-blue-600 text-white shadow-md'
                  : 'bg-transparent text-gray-600 hover:bg-gray-100'
              }`}
            >
              🗺️ Map View
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`px-6 py-2 rounded-md font-medium transition-all ${
                viewMode === 'list'
                  ? 'bg-blue-600 text-white shadow-md'
                  : 'bg-transparent text-gray-600 hover:bg-gray-100'
              }`}
            >
              📋 List View
            </button>
          </div>
        </div>

        {/* Results Count */}
        {searchQuery && (
          <div className="mb-4 text-gray-600">
            Found <span className="font-bold text-blue-600">{filteredShops.length}</span> shops matching your search
          </div>
        )}

        {/* Map View */}
        {viewMode === 'map' && (
          <div className="mb-8">
            <ShopMap shops={filteredShops} />
          </div>
        )}

        {/* List View */}
        {viewMode === 'list' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredShops.length === 0 ? (
              <div className="col-span-full text-center py-12">
                <div className="text-6xl mb-4">🔍</div>
                <h3 className="text-2xl font-semibold text-gray-700 mb-2">No shops found</h3>
                <p className="text-gray-500">Try selecting a different country or adjusting your search</p>
              </div>
            ) : (
              filteredShops.map((shop) => (
                <div
                  key={shop.id}
                  className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-100 hover:border-blue-300"
                >
                  {/* Card Header */}
                  <div className="bg-gradient-to-r from-blue-500 to-purple-500 px-6 py-4">
                    <h3 className="text-xl font-bold text-white truncate">
                      {shop.name || 'Motorcycle Shop'}
                    </h3>
                  </div>

                  {/* Card Body */}
                  <div className="px-6 py-4 space-y-3">
                    {/* Location */}
                    <div className="flex items-start">
                      <span className="text-2xl mr-3">📍</span>
                      <div className="flex-1">
                        <p className="text-gray-800 font-medium">
                          {shop.address?.street && `${shop.address.street}${shop.address.housenumber ? ' ' + shop.address.housenumber : ''}`}
                        </p>
                        <p className="text-gray-600">
                          {shop.address?.postcode && `${shop.address.postcode} `}
                          {shop.address?.city || 'Unknown City'}
                        </p>
                        <p className="text-sm text-gray-500 mt-1">
                          {getCountryName(shop.country_code)}
                        </p>
                      </div>
                    </div>

                    {/* Contact Information */}
                    {(shop.contact?.phone || shop.contact?.website || shop.contact?.email) && (
                      <div className="border-t pt-3 space-y-2">
                        {shop.contact?.phone && (
                          <a
                            href={`tel:${shop.contact.phone}`}
                            className="flex items-center text-blue-600 hover:text-blue-800 transition-colors"
                          >
                            <span className="text-lg mr-2">📞</span>
                            <span className="text-sm">{shop.contact.phone}</span>
                          </a>
                        )}

                        {shop.contact?.email && (
                          <a
                            href={`mailto:${shop.contact.email}`}
                            className="flex items-center text-blue-600 hover:text-blue-800 transition-colors"
                          >
                            <span className="text-lg mr-2">✉️</span>
                            <span className="text-sm">{shop.contact.email}</span>
                          </a>
                        )}

                        {shop.contact?.website && (
                          <a
                            href={shop.contact.website}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center text-blue-600 hover:text-blue-800 transition-colors"
                          >
                            <span className="text-lg mr-2">🌐</span>
                            <span className="text-sm underline">Visit Website</span>
                          </a>
                        )}
                      </div>
                    )}
                  </div>

                  {/* Card Footer */}
                  {shop.lat && shop.lon && (
                    <div className="bg-gray-50 px-6 py-3 border-t">
                      <a
                        href={`https://www.google.com/maps/search/?api=1&query=${shop.lat},${shop.lon}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm text-blue-600 hover:text-blue-800 font-medium flex items-center justify-center"
                      >
                        <span className="mr-1">🗺️</span>
                        View on Google Maps
                      </a>
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white mt-12 border-t">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-gray-600">
          <p>Data loaded from CSV file</p>
          <p className="text-sm mt-2">Find the best motorcycle repair shops across Europe</p>
        </div>
      </footer>
    </div>
  );
}