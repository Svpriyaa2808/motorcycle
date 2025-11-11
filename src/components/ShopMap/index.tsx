'use client';

import React, { useState, useEffect, useMemo } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

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
}

// Custom marker icon
const createCustomIcon = () => {
  return L.divIcon({
    className: 'custom-marker',
    html: `
      <div style="
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #DC2626;
        border: 3px solid white;
        border-radius: 50%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
      ">
        <span style="font-size: 18px;">🏍️</span>
      </div>
    `,
    iconSize: [32, 32],
    iconAnchor: [16, 16],
    popupAnchor: [0, -16],
  });
};

// Component to handle map bounds and center updates
function MapBoundsHandler({ shops }: { shops: MotorcycleShop[] }) {
  const map = useMap();

  useEffect(() => {
    if (shops.length === 0) {
      // Default to Europe view
      map.setView([50.0, 10.0], 4);
      return;
    }

    const validShops = shops.filter(shop => shop.lat && shop.lon);

    if (validShops.length === 1) {
      // Single shop - center on it
      const shop = validShops[0];
      map.setView([shop.lat!, shop.lon!], 12);
    } else if (validShops.length > 1) {
      // Multiple shops - fit bounds
      const bounds = L.latLngBounds(
        validShops.map(shop => [shop.lat!, shop.lon!] as [number, number])
      );
      map.fitBounds(bounds, { padding: [50, 50], maxZoom: 12 });
    }
  }, [shops, map]);

  return null;
}

export default function ShopMap({ shops }: ShopMapProps) {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  // Calculate initial center and zoom
  const { center, zoom } = useMemo(() => {
    if (shops.length === 0) {
      return { center: [50.0, 10.0] as [number, number], zoom: 4 };
    }

    const validShops = shops.filter(shop => shop.lat && shop.lon);
    if (validShops.length === 0) {
      return { center: [50.0, 10.0] as [number, number], zoom: 4 };
    }

    const avgLat = validShops.reduce((sum, shop) => sum + (shop.lat || 0), 0) / validShops.length;
    const avgLng = validShops.reduce((sum, shop) => sum + (shop.lon || 0), 0) / validShops.length;

    return {
      center: [avgLat, avgLng] as [number, number],
      zoom: validShops.length === 1 ? 12 : validShops.length < 10 ? 8 : 6,
    };
  }, [shops]);

  // Don't render on server side to avoid hydration issues
  if (!isMounted) {
    return (
      <div className="bg-white rounded-xl shadow-lg overflow-hidden" style={{ height: '600px' }}>
        <div className="h-full flex items-center justify-center bg-gray-50">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading map...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden" style={{ height: '600px' }}>
      <MapContainer
        center={center}
        zoom={zoom}
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <MapBoundsHandler shops={shops} />

        {shops.map((shop) => {
          if (!shop.lat || !shop.lon) return null;

          return (
            <Marker
              key={shop.id}
              position={[shop.lat, shop.lon]}
              icon={createCustomIcon()}
            >
              <Popup maxWidth={300}>
                <div className="p-2">
                  <h3 className="font-bold text-lg mb-2 text-gray-800">
                    {shop.name || 'Motorcycle Shop'}
                  </h3>

                  {shop.address?.city && (
                    <p className="text-sm text-gray-600 mb-1">
                      📍 {shop.address.street && `${shop.address.street}, `}
                      {shop.address.city}
                      {shop.address.postcode && `, ${shop.address.postcode}`}
                    </p>
                  )}

                  {shop.country_code && (
                    <p className="text-sm text-gray-600 mb-2">
                      🌍 {shop.country_code}
                    </p>
                  )}

                  {shop.contact?.phone && (
                    <p className="text-sm text-blue-600 mb-1">
                      📞 <a href={`tel:${shop.contact.phone}`} className="hover:underline">
                        {shop.contact.phone}
                      </a>
                    </p>
                  )}

                  {shop.contact?.email && (
                    <p className="text-sm text-blue-600 mb-1">
                      ✉️ <a href={`mailto:${shop.contact.email}`} className="hover:underline">
                        {shop.contact.email}
                      </a>
                    </p>
                  )}

                  {shop.contact?.website && (
                    <p className="text-sm text-blue-600 mb-2">
                      🌐 <a
                        href={shop.contact.website}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="hover:underline"
                      >
                        Visit Website
                      </a>
                    </p>
                  )}

                  <a
                    href={`https://www.google.com/maps/search/?api=1&query=${shop.lat},${shop.lon}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-block mt-2 px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition-colors"
                  >
                    View on Google Maps →
                  </a>
                </div>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>

      <style jsx global>{`
        .leaflet-container {
          font-family: inherit;
        }
        .custom-marker {
          background: transparent;
          border: none;
        }
        .leaflet-popup-content-wrapper {
          border-radius: 8px;
        }
        .leaflet-popup-content {
          margin: 0;
          min-width: 250px;
        }
      `}</style>
    </div>
  );
}
