# 📊 Data Setup Guide

Follow these steps to populate your motorcycle shop database with real data from OpenStreetMap.

---

## ✅ Prerequisites

Before running the data fetcher, make sure you have:

1. **Supabase credentials** set in `.env.local`
2. **Python 3.7+** installed
3. **Database table** created in Supabase

---

## Step 1: Install Python Dependencies

From your project directory:

```bash
pip install -r requirements.txt
```

This installs:
- `requests` - For API calls to OpenStreetMap
- `supabase` - Python client for Supabase
- `python-dotenv` - To load environment variables

---

## Step 2: Set Up Supabase Credentials

### 2.1 Get Your Credentials

1. Go to [https://supabase.com](https://supabase.com)
2. Sign in and select your project
3. Go to **Settings** → **API**
4. Copy these two values:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon public** key (long string starting with `eyJ...`)

### 2.2 Update .env.local

Open `.env.local` and replace the placeholder values:

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-actual-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.your-actual-key...
```

**Important:** Use your ACTUAL credentials, not the placeholder values!

---

## Step 3: Create the Database Table

If you haven't already, create the table in Supabase:

1. Go to Supabase dashboard → **SQL Editor**
2. Click **New query**
3. Paste this SQL:

```sql
CREATE TABLE public.motorcycle_shops (
  id bigint primary key,
  country_code text,
  name text,
  lat double precision,
  lon double precision,
  address jsonb,
  contact jsonb,
  shop_tags jsonb,
  source_country text,
  created_at timestamptz default now()
);

-- Create indexes for better performance
CREATE INDEX idx_motorcycle_shops_country ON motorcycle_shops(country_code);
CREATE INDEX idx_motorcycle_shops_location ON motorcycle_shops(lat, lon);
```

4. Click **Run**
5. You should see: ✅ "Success"

---

## Step 4: Run the Data Fetcher

Now you're ready to fetch the data!

```bash
npm run fetch:data
```

### What This Does:

- Fetches motorcycle repair shop data from OpenStreetMap
- Covers all 27 EU countries
- Inserts data into your Supabase database
- Takes 5-10 minutes to complete

### Expected Output:

```
============================================================
🏍️  Motorcycle Shop Data Fetcher
============================================================
✅ Supabase URL: https://xxxxx.supabase.co
✅ Supabase Key: eyJhbGciOiJIUzI1NiIsI...
✅ Connected to Supabase successfully
📍 Fetching data for 27 EU countries

🔍 Fetching DE... ✅ Inserted 245 shops
🔍 Fetching FR... ✅ Inserted 189 shops
🔍 Fetching IT... ✅ Inserted 156 shops
...
============================================================
🎉 Data Fetch Complete!
============================================================
✅ Successfully processed: 27/27 countries
📊 Total shops inserted: 3,456

🏍️  Your motorcycle shop database is ready!
   Run: npm run dev
   Open: http://localhost:3000
```

---

## Step 5: Test Your Website

After the data is loaded:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

You should see:
- ✅ Map with motorcycle shop markers
- ✅ Shop count in the header
- ✅ Country filter working
- ✅ Shops display when you click countries

---

## 🐛 Troubleshooting

### Error: "Please set your actual Supabase credentials"

**Problem:** You're still using placeholder values in `.env.local`

**Solution:**
1. Check `.env.local` - should NOT contain `placeholder`
2. Update with your real Supabase URL and key
3. Run `npm run fetch:data` again

### Error: "No such file or directory"

**Problem:** Running from wrong directory or Python not found

**Solution:**
1. Make sure you're in the project root directory
2. Check Python is installed: `python --version` or `python3 --version`
3. Use `python3` instead: `python3 scripts/fetch_osm_data.py`

### Error: "Module not found: requests/supabase/dotenv"

**Problem:** Python dependencies not installed

**Solution:**
```bash
pip install -r requirements.txt
# or if pip doesn't work:
pip3 install -r requirements.txt
```

### Data fetch is very slow

**This is normal!** The script:
- Waits 10 seconds between each country (API rate limiting)
- Processes 27 countries
- Takes 5-10 minutes total

Don't interrupt it - let it finish!

### Some countries fail to fetch

**This can happen** due to:
- Temporary API issues
- Network problems
- Rate limiting

**Solution:** Just run the script again - it uses `upsert` so it won't duplicate data.

---

## 📊 Data Statistics

After completion, you should have approximately:

- **3,000-5,000 motorcycle shops** total
- **Coverage across all 27 EU countries**
- **Most shops in**: Germany, France, Italy, Spain

Countries with fewer shops are normal (smaller countries have fewer shops).

---

## 🔄 Re-running the Script

You can run `npm run fetch:data` multiple times:

- ✅ **Safe to re-run** - uses upsert (updates existing, adds new)
- ✅ **Updates data** - refreshes shop information
- ✅ **No duplicates** - shops are identified by OSM ID

---

## ✅ You're All Set!

Your motorcycle shop database is now populated with real data from OpenStreetMap!

Enjoy your FREE, fully functional motorcycle repair shop directory! 🏍️
