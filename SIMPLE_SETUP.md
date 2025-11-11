# 🚀 Simple Setup - Just 2 Steps!

Your motorcycle repair shop website is now **100% FREE** to run! No payment required for maps.

---

## ✅ What You Need

**Only ONE thing:** Supabase credentials (for your database)

**NO Google Maps API key needed!** We use OpenStreetMap which is completely free!

---

## Step 1: Get Supabase Credentials (5 minutes)

### 1.1 Create Supabase Account

1. Go to **https://supabase.com**
2. Click **"Start your project"**
3. Sign up with GitHub or email (free account)

### 1.2 Create a Project

1. Click **"New Project"**
2. Fill in:
   - **Name**: `motorcycle-shops`
   - **Database Password**: Create a strong password
   - **Region**: Choose closest to you
3. Click **"Create new project"**
4. Wait 1-2 minutes for setup

### 1.3 Get Your Credentials

1. In Supabase dashboard, click **Settings** (bottom left)
2. Click **API**
3. Copy these two values:

   **Project URL**
   ```
   Example: https://abcdefgh12345678.supabase.co
   ```

   **anon public key**
   ```
   Example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

### 1.4 Update .env.local

Open `/home/user/motorcycle/.env.local` and paste your values:

```env
NEXT_PUBLIC_SUPABASE_URL=https://abcdefgh12345678.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3M...
```

**Save the file!**

### 1.5 Create the Database Table

In Supabase dashboard:

1. Click **SQL Editor** (left sidebar)
2. Click **"New query"**
3. Paste this code:

```sql
CREATE TABLE motorcycle_shops (
  id SERIAL PRIMARY KEY,
  name TEXT,
  lat DOUBLE PRECISION,
  lon DOUBLE PRECISION,
  address JSONB,
  contact JSONB,
  country_code TEXT,
  shop_tags JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_motorcycle_shops_country ON motorcycle_shops(country_code);
CREATE INDEX idx_motorcycle_shops_location ON motorcycle_shops(lat, lon);
```

4. Click **"Run"**
5. Should see: ✅ "Success"

---

## Step 2: Load Data & Run (5 minutes)

### 2.1 Fetch Motorcycle Shop Data

From your project directory:

```bash
npm run fetch:data
```

This fetches real motorcycle shop data from OpenStreetMap for all 27 EU countries.
Takes 5-10 minutes.

### 2.2 Restart Development Server

```bash
# Stop current server (Ctrl+C)
npm run dev
```

### 2.3 Open Your Browser

Go to: **http://localhost:3000**

---

## 🎉 That's It!

You should now see:
- ✅ No errors!
- ✅ Interactive map with OpenStreetMap
- ✅ All motorcycle shops displayed
- ✅ Country filtering works
- ✅ Search works
- ✅ Everything is FREE!

---

## 🗺️ About the Maps

Your application now uses:

- **Leaflet** - Free, open-source mapping library
- **OpenStreetMap** - Free map tiles (like Wikipedia for maps)
- **NO API KEY required** - Completely free to use
- **NO billing** - Never any charges
- **NO limits** - Use as much as you want!

The maps look professional and work just like Google Maps:
- Zoom in/out
- Click markers to see shop details
- Pan around the map
- Fully responsive

---

## 🐛 Troubleshooting

### Still seeing "Error fetching data"?

1. Check that you updated `.env.local` with **your actual** Supabase credentials
2. Make sure there are no extra spaces in the values
3. Restart your dev server after saving `.env.local`

### No shops showing?

1. Make sure `npm run fetch:data` completed successfully
2. Check Supabase dashboard → Table Editor → motorcycle_shops
3. Should see rows of data
4. If empty, run `npm run fetch:data` again

### Map not loading?

1. Check browser console (F12) for errors
2. Make sure Leaflet CSS is loading
3. Try refreshing the page
4. Clear browser cache

---

## ✅ Final Checklist

- [ ] Created Supabase account
- [ ] Created Supabase project
- [ ] Copied URL and API key to `.env.local`
- [ ] Created `motorcycle_shops` table
- [ ] Ran `npm run fetch:data`
- [ ] Restarted dev server
- [ ] Website works!

---

## 💰 Cost Breakdown

**Total Cost: $0/month**

- ✅ Supabase Free Tier: 500MB database, 2GB bandwidth
- ✅ OpenStreetMap: Completely free, no limits
- ✅ Leaflet: Open source, free forever
- ✅ Hosting (when you deploy): Can use Vercel free tier

**This website costs NOTHING to run!** 🎉
