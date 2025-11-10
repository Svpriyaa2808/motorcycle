'use client';

import React from 'react';
import { EU_COUNTRIES, Country } from '@/data/countries';

interface CountrySelectorProps {
  selectedCountry: string | null;
  onCountryChange: (countryCode: string | null) => void;
}

export default function CountrySelector({ selectedCountry, onCountryChange }: CountrySelectorProps) {
  return (
    <div className="w-full mb-8">
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-6 rounded-lg shadow-xl">
        <h2 className="text-white text-2xl font-bold mb-4">Select a Country</h2>
        <p className="text-blue-100 mb-6">Choose a country to view motorcycle repair shops in that region</p>

        {/* Mobile Dropdown View */}
        <div className="block lg:hidden">
          <select
            value={selectedCountry || 'all'}
            onChange={(e) => onCountryChange(e.target.value === 'all' ? null : e.target.value)}
            className="w-full px-4 py-3 rounded-lg border-2 border-blue-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all bg-white text-gray-800 font-medium"
          >
            <option value="all">🌍 All Countries</option>
            {EU_COUNTRIES.map((country) => (
              <option key={country.code} value={country.code}>
                {country.flag} {country.name}
              </option>
            ))}
          </select>
        </div>

        {/* Desktop Grid View */}
        <div className="hidden lg:block">
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3">
            {/* All Countries Button */}
            <button
              onClick={() => onCountryChange(null)}
              className={`px-4 py-3 rounded-lg font-semibold transition-all duration-200 transform hover:scale-105 ${
                selectedCountry === null
                  ? 'bg-white text-blue-600 shadow-lg ring-2 ring-white'
                  : 'bg-blue-500 text-white hover:bg-blue-400'
              }`}
            >
              🌍 All
            </button>

            {EU_COUNTRIES.map((country: Country) => (
              <button
                key={country.code}
                onClick={() => onCountryChange(country.code)}
                className={`px-4 py-3 rounded-lg font-semibold transition-all duration-200 transform hover:scale-105 ${
                  selectedCountry === country.code
                    ? 'bg-white text-blue-600 shadow-lg ring-2 ring-white'
                    : 'bg-blue-500 text-white hover:bg-blue-400'
                }`}
                title={country.name}
              >
                <div className="flex flex-col items-center">
                  <span className="text-2xl mb-1">{country.flag}</span>
                  <span className="text-xs">{country.code}</span>
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
