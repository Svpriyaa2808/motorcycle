# Setup Guide - Getting Your API Keys

This guide will help you get all the necessary API keys to run your motorcycle repair shop website.

## 🔑 Step 1: Get Supabase Credentials

### Option A: If you already have a Supabase project

1. Go to [https://supabase.com](https://supabase.com) and sign in
2. Select your project (or create a new one)
3. Go to **Project Settings** (gear icon in the sidebar)
4. Click on **API** in the left menu
5. You'll see:
   - **Project URL** - This is your `NEXT_PUBLIC_SUPABASE_URL`
   - **anon/public key** - This is your `NEXT_PUBLIC_SUPABASE_ANON_KEY`
6. Copy these values to your `.env.local` file

### Option B: Create a new Supabase project

1. Go to [https://supabase.com](https://supabase.com)
2. Click **Start your project**
3. Sign in with GitHub (or create an account)
4. Click **New Project**
5. Fill in:
   - Project name: `motorcycle-shops` (or any name you like)
   - Database password: Create a strong password
   - Region: Choose closest to you
6. Click **Create new project** (wait 1-2 minutes for setup)
7. Once ready, go to **Settings** → **API**
8. Copy the **Project URL** and **anon/public key**

### Create the database table

After getting your Supabase credentials, you need to create the database table:

1. In your Supabase dashboard, click on **SQL Editor** (in the sidebar)
2. Click **New Query**
3. Paste this SQL code:

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
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Create index for faster country filtering
CREATE INDEX idx_motorcycle_shops_country ON motorcycle_shops(country_code);

-- Create index for location queries
CREATE INDEX idx_motorcycle_shops_location ON motorcycle_shops(lat, lon);
```

4. Click **Run** (or press Ctrl+Enter)
5. You should see "Success. No rows returned"

### Populate the database with shop data

Run this command from your project directory to fetch and upload motorcycle shop data:

```bash
npm run fetch:data
```

This will fetch motorcycle repair shop data from OpenStreetMap for all 27 EU countries.

---

## 🗺️ Step 2: Get Google Maps API Key

### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Click **Select a project** at the top
4. Click **NEW PROJECT**
5. Enter a project name: `motorcycle-shops-map` (or any name)
6. Click **CREATE**

### 2. Enable the Maps JavaScript API

1. In the Google Cloud Console, make sure your new project is selected
2. In the left sidebar, go to **APIs & Services** → **Library**
3. Search for "Maps JavaScript API"
4. Click on **Maps JavaScript API**
5. Click **ENABLE**

### 3. Create API Credentials

1. Go to **APIs & Services** → **Credentials** (in the left sidebar)
2. Click **CREATE CREDENTIALS** at the top
3. Select **API key**
4. Your API key will be created and displayed
5. **Copy this key** - this is your `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY`

### 4. (Optional but Recommended) Restrict your API key

To prevent unauthorized use:

1. Click on your newly created API key to edit it
2. Under **Application restrictions**:
   - Select **HTTP referrers (web sites)**
   - Add: `http://localhost:3000/*` (for development)
   - Add your production domain when you deploy
3. Under **API restrictions**:
   - Select **Restrict key**
   - Check **Maps JavaScript API**
4. Click **SAVE**

### 5. (Optional) Enable Billing

Google Maps requires billing to be enabled, but they offer:
- **$200 free credit per month**
- Most small projects stay within the free tier

To enable billing:
1. Go to **Billing** in the left sidebar
2. Click **LINK A BILLING ACCOUNT**
3. Follow the steps to add a payment method
4. Don't worry - you'll get $200 free credit monthly

---

## 📝 Step 3: Update Your .env.local File

Now that you have all your credentials, open the `.env.local` file in your project:

```bash
# From your project directory
nano .env.local
# or use any text editor
```

Replace the placeholder values with your actual credentials:

```env
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh4eHh4eHh4eHh4eHh4eHh4eHh4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2Nzg4ODg4ODgsImV4cCI6MTk5NDQ2NDg4OH0.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Google Maps API Key
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=AIzaSyXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxX
```

**Important:** Replace the example values above with YOUR actual keys!

---

## 🚀 Step 4: Run Your Application

1. **Restart your development server** (if it's running):
   ```bash
   # Press Ctrl+C to stop the current server
   npm run dev
   ```

2. **Open your browser** and go to [http://localhost:3000](http://localhost:3000)

3. **Test the features:**
   - Click on different countries to filter shops
   - Try the search functionality
   - Switch between Map View and List View
   - Click on shop markers to see details

---

## 🐛 Troubleshooting

### "Error fetching data" appears

- Check that your Supabase URL and key are correct in `.env.local`
- Make sure you created the `motorcycle_shops` table
- Make sure you have data in the table (run `npm run fetch:data`)

### "Please add your Google Maps API key" message

- Check that your Google Maps API key is in `.env.local`
- Make sure there are no extra spaces
- Make sure the API key starts with `AIza`
- Restart your development server after adding the key

### Shops not displaying when clicking countries

- This happens when there's no data in the database yet
- Run `npm run fetch:data` to populate the database
- Wait for the script to complete (may take several minutes)
- Check your Supabase dashboard to confirm data was inserted

### Map not loading

- Check browser console for errors
- Verify Google Maps JavaScript API is enabled
- Verify billing is enabled in Google Cloud Console
- Check that API key restrictions allow localhost:3000

---

## 📧 Need Help?

If you're still having issues:
1. Check the browser console for error messages (F12)
2. Check that all environment variables are set correctly
3. Make sure you restarted the dev server after adding credentials
4. Verify your Supabase table has data (check in Supabase dashboard → Table Editor)

---

## 🎉 You're All Set!

Once everything is configured, you should be able to:
- ✅ See all motorcycle shops on the map
- ✅ Filter by country
- ✅ Search for specific shops
- ✅ View shop details and contact information
- ✅ Get directions via Google Maps
