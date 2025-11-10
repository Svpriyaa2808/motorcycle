'use client';

import React, { useCallback, useState } from 'react';
import { GoogleMap, LoadScript, Marker, InfoWindow } from '@react-google-maps/api';

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

interface ShopMapProps {
  shops: MotorcycleShop[];
  apiKey: string;
}

const containerStyle = {
  width: '100%',
  height: '600px',
  borderRadius: '12px',
};

export default function ShopMap({ shops, apiKey }: ShopMapProps) {
  const [selectedShop, setSelectedShop] = useState<MotorcycleShop | null>(null);
  const [mapCenter, setMapCenter] = useState<{ lat: number; lng: number }>({ lat: 50.0, lng: 10.0 });
  const [mapZoom, setMapZoom] = useState<number>(4);

  // Calculate map center based on shops
  React.useEffect(() => {
    if (shops.length > 0) {
      const validShops = shops.filter(shop => shop.lat && shop.lon);
      if (validShops.length > 0) {
        const avgLat = validShops.reduce((sum, shop) => sum + (shop.lat || 0), 0) / validShops.length;
        const avgLng = validShops.reduce((sum, shop) => sum + (shop.lon || 0), 0) / validShops.length;
        setMapCenter({ lat: avgLat, lng: avgLng });
        // Adjust zoom based on number of shops
        setMapZoom(shops.length === 1 ? 12 : shops.length < 10 ? 8 : 6);
      }
    } else {
      // Default to Europe center
      setMapCenter({ lat: 50.0, lng: 10.0 });
      setMapZoom(4);
    }
  }, [shops]);

  const onMapLoad = useCallback((map: google.maps.Map) => {
    // Optionally customize map on load
  }, []);

  if (!apiKey || apiKey === 'YOUR_GOOGLE_MAPS_API_KEY') {
    return (
      <div className="bg-yellow-50 border-l-4 border-yellow-400 p-6 rounded-lg">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <svg className="h-6 w-6 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <p className="text-sm text-yellow-700">
              Please add your Google Maps API key to the <code className="bg-yellow-100 px-2 py-1 rounded">.env.local</code> file:
              <br />
              <code className="bg-yellow-100 px-2 py-1 rounded mt-2 block">NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_api_key_here</code>
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      <LoadScript googleMapsApiKey={apiKey}>
        <GoogleMap
          mapContainerStyle={containerStyle}
          center={mapCenter}
          zoom={mapZoom}
          onLoad={onMapLoad}
          options={{
            streetViewControl: false,
            mapTypeControl: true,
            fullscreenControl: true,
          }}
        >
          {shops.map((shop) => {
            if (!shop.lat || !shop.lon) return null;

            return (
              <Marker
                key={shop.id}
                position={{ lat: shop.lat, lng: shop.lon }}
                onClick={() => setSelectedShop(shop)}
                icon={{
                  url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="%23DC2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                      <circle cx="12" cy="10" r="3"></circle>
                    </svg>
                  `),
                  scaledSize: new window.google.maps.Size(32, 32),
                }}
              />
            );
          })}

          {selectedShop && selectedShop.lat && selectedShop.lon && (
            <InfoWindow
              position={{ lat: selectedShop.lat, lng: selectedShop.lon }}
              onCloseClick={() => setSelectedShop(null)}
            >
              <div className="p-2 max-w-xs">
                <h3 className="font-bold text-lg mb-2 text-gray-800">
                  {selectedShop.name || 'Motorcycle Shop'}
                </h3>
                {selectedShop.address?.city && (
                  <p className="text-sm text-gray-600 mb-1">
                    📍 {selectedShop.address.street && `${selectedShop.address.street}, `}
                    {selectedShop.address.city}
                    {selectedShop.address.postcode && `, ${selectedShop.address.postcode}`}
                  </p>
                )}
                {selectedShop.country_code && (
                  <p className="text-sm text-gray-600 mb-2">
                    🌍 {selectedShop.country_code}
                  </p>
                )}
                {selectedShop.contact?.phone && (
                  <p className="text-sm text-blue-600 mb-1">
                    📞 <a href={`tel:${selectedShop.contact.phone}`}>{selectedShop.contact.phone}</a>
                  </p>
                )}
                {selectedShop.contact?.website && (
                  <p className="text-sm text-blue-600">
                    🌐 <a href={selectedShop.contact.website} target="_blank" rel="noopener noreferrer" className="underline">
                      Visit Website
                    </a>
                  </p>
                )}
              </div>
            </InfoWindow>
          )}
        </GoogleMap>
      </LoadScript>
    </div>
  );
}
