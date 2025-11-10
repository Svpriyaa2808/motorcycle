# 🏍️ Motorcycle Repair Shops - European Directory

A modern web application built with Next.js to help users find motorcycle repair shops across 27 European countries. Features interactive maps, country filtering, and comprehensive shop information.

## ✨ Features

- **🗺️ Interactive Google Maps** - Visualize all motorcycle repair shops on an interactive map
- **🌍 Country Filtering** - Filter shops by any of the 27 EU countries
- **🔍 Smart Search** - Search shops by name, city, or street address
- **📱 Responsive Design** - Fully optimized for desktop, tablet, and mobile devices
- **🎨 Modern UI** - Beautiful gradient design with Tailwind CSS
- **📊 Real-time Statistics** - See shop counts and filtering results instantly
- **🔄 Dual View Modes** - Switch between map view and list view
- **📍 Direct Maps Integration** - Click to view any shop location on Google Maps

## 🚀 Tech Stack

- **Frontend**: Next.js 16, React 19, TypeScript
- **Styling**: Tailwind CSS 4
- **Database**: Supabase (PostgreSQL)
- **Maps**: Google Maps API with @react-google-maps/api
- **Data Source**: OpenStreetMap (Overpass API)

## 📋 Prerequisites

Before you begin, ensure you have:

- Node.js 18+ installed
- npm or yarn package manager
- A Supabase account and project
- A Google Maps API key

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd motorcycle
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**

   Copy the example environment file:
   ```bash
   cp .env.local.example .env.local
   ```

   Edit `.env.local` and add your credentials:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_url_here
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key_here
   NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
   ```

4. **Set up Supabase database**

   Create a table named `motorcycle_shops` with the following structure:
   ```sql
   CREATE TABLE motorcycle_shops (
     id SERIAL PRIMARY KEY,
     name TEXT,
     lat DOUBLE PRECISION,
     lon DOUBLE PRECISION,
     address JSONB,
     contact JSONB,
     country_code TEXT,
     shop_tags JSONB
   );
   ```

5. **Fetch shop data (optional)**
   ```bash
   npm run fetch:data
   ```

## 🎯 Getting Started

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

## 🗺️ Google Maps API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - Maps JavaScript API
   - Geocoding API (optional)
4. Create credentials (API Key)
5. Add the API key to your `.env.local` file

## 📁 Project Structure

```
motorcycle/
├── src/
│   ├── app/                    # Next.js app directory
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Home page
│   │   └── globals.css        # Global styles
│   ├── components/
│   │   ├── CountrySelector/   # Country filtering component
│   │   ├── MotorcycleShops/   # Main shops component
│   │   └── ShopMap/           # Google Maps component
│   └── data/
│       └── countries.ts       # EU countries data
├── supabase/
│   └── supabaseClient.js      # Supabase configuration
├── scripts/
│   └── fetchOSM_Data.py       # Data fetching script
└── .env.local.example         # Environment variables template
```

## 🎨 Key Features Explained

### Country Filtering
Users can filter shops by selecting any EU country from an interactive grid (desktop) or dropdown (mobile). The app displays:
- Austria, Belgium, Bulgaria, Croatia, Cyprus, Czech Republic, Denmark, Estonia, Finland, France
- Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands
- Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden

### Map View
- Displays all filtered shops as markers on Google Maps
- Automatically centers and zooms based on selected shops
- Click markers to see shop details in info windows
- Custom motorcycle-themed map markers

### List View
- Beautiful card-based layout with gradient headers
- Shows shop name, full address, and contact information
- Direct links to phone, email, and website
- Quick link to view location on Google Maps

## 🔧 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run fetch:data` - Fetch motorcycle shop data from OpenStreetMap

## 🌐 Data Source

All motorcycle shop data is sourced from OpenStreetMap using the Overpass API. The data includes shops tagged as:
- `shop=motorcycle` - Motorcycle shops
- `craft=motorcycle` - Motorcycle craft/repair services
- `amenity=car_repair` with `motorcycle=yes` - Car repair shops that service motorcycles

## 📱 Responsive Design

The application is fully responsive and optimized for:
- Desktop (1920px+)
- Laptop (1024px - 1919px)
- Tablet (768px - 1023px)
- Mobile (320px - 767px)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Data from [OpenStreetMap](https://www.openstreetmap.org/) contributors
- Maps powered by [Google Maps Platform](https://developers.google.com/maps)
- Built with [Next.js](https://nextjs.org/) and [Tailwind CSS](https://tailwindcss.com/)
