# 🚀 Quick Start - 3 Steps to Get Your Website Running

Your website is ready to go! You just need to add 3 credentials. This should take about **10 minutes total**.

---

## ✅ STEP 1: Get Supabase Credentials (5 minutes)

Supabase is your database where all motorcycle shop information is stored.

### 1.1 Create a Supabase Account (if you don't have one)

1. Open your browser and go to: **https://supabase.com**
2. Click **"Start your project"**
3. Sign up with GitHub, Google, or email

### 1.2 Create a New Project

1. After signing in, click **"New Project"**
2. Fill in the form:
   - **Name**: `motorcycle-shops` (or any name you like)
   - **Database Password**: Create a strong password (save it somewhere!)
   - **Region**: Choose the one closest to you
   - **Pricing Plan**: Select "Free" (it's more than enough)
3. Click **"Create new project"**
4. ⏳ Wait 1-2 minutes while Supabase sets up your database

### 1.3 Get Your Credentials

1. Once your project is ready, look at the left sidebar
2. Click on **Settings** (gear icon at the bottom)
3. Click on **API** in the settings menu
4. You'll see two important values:

   **Project URL** - Copy this entire URL
   ```
   Example: https://abcdefghijklmnop.supabase.co
   ```

   **anon public** key - Click "Copy" next to this long key
   ```
   Example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS...
   ```

### 1.4 Add to Your .env.local File

1. Open `/home/user/motorcycle/.env.local` in a text editor
2. Replace these two lines with your actual values:

   **BEFORE:**
   ```env
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_url_here
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key_here
   ```

   **AFTER (with your actual values):**
   ```env
   NEXT_PUBLIC_SUPABASE_URL=https://abcdefghijklmnop.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBh...
   ```

3. **Save the file!**

### 1.5 Create the Database Table

1. In your Supabase dashboard, click **"SQL Editor"** (in the left sidebar)
2. Click **"New query"**
3. Copy and paste this SQL code:

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

-- Create indexes for better performance
CREATE INDEX idx_motorcycle_shops_country ON motorcycle_shops(country_code);
CREATE INDEX idx_motorcycle_shops_location ON motorcycle_shops(lat, lon);
```

4. Click **"Run"** (or press Ctrl+Enter)
5. You should see: ✅ **"Success. No rows returned"**

✅ **Step 1 Complete!**

---

## ✅ STEP 2: Get Google Maps API Key (5 minutes)

Google Maps displays all the motorcycle shops on an interactive map.

### 2.1 Go to Google Cloud Console

1. Open: **https://console.cloud.google.com/**
2. Sign in with your Google account
3. If prompted, agree to the Terms of Service

### 2.2 Create a New Project

1. At the top of the page, click **"Select a project"**
2. Click **"NEW PROJECT"** (top right of the popup)
3. Enter project name: `motorcycle-shops` (or any name)
4. Click **"CREATE"**
5. Wait a few seconds for the project to be created

### 2.3 Enable Maps JavaScript API

1. Make sure your new project is selected (check the top bar)
2. In the left menu, go to: **APIs & Services** → **Library**
3. In the search bar, type: `Maps JavaScript API`
4. Click on **"Maps JavaScript API"**
5. Click the big **"ENABLE"** button
6. Wait a few seconds

### 2.4 Create an API Key

1. In the left menu, go to: **APIs & Services** → **Credentials**
2. At the top, click **"+ CREATE CREDENTIALS"**
3. Select **"API key"**
4. A popup will show your new API key - **Copy it!**
   ```
   Example: AIzaSyAbCdEfGhIjKlMnOpQrStUvWxYz1234567
   ```

### 2.5 (Optional but Recommended) Restrict the API Key

To prevent unauthorized use:

1. Click **"Edit API key"** (or click on the key name)
2. Under **"API restrictions"**:
   - Select **"Restrict key"**
   - Check only: ☑ **Maps JavaScript API**
3. Click **"SAVE"**

### 2.6 Enable Billing (Required for Maps)

Don't worry - Google gives you **$200 free credit every month**, which is enough for most small projects!

1. In the left menu, click **"Billing"**
2. Click **"LINK A BILLING ACCOUNT"**
3. Click **"CREATE BILLING ACCOUNT"**
4. Fill in your payment information
5. Complete the setup

**Note:** You won't be charged unless you exceed the free $200/month credit.

### 2.7 Add to Your .env.local File

1. Open `/home/user/motorcycle/.env.local` again
2. Replace this line with your actual API key:

   **BEFORE:**
   ```env
   NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
   ```

   **AFTER (with your actual key):**
   ```env
   NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=AIzaSyAbCdEfGhIjKlMnOpQrStUvWxYz1234567
   ```

3. **Save the file!**

✅ **Step 2 Complete!**

---

## ✅ STEP 3: Load Motorcycle Shop Data & Test (2 minutes)

Now let's populate your database with real motorcycle shop data!

### 3.1 Run the Data Fetcher

From your project directory, run:

```bash
npm run fetch:data
```

This will:
- Fetch motorcycle repair shop data from OpenStreetMap
- Cover all 27 EU countries
- Take about 5-10 minutes to complete
- Show progress as it runs

**Wait for it to finish!** You'll see messages like:
```
Processing Germany (DE)...
Inserted 245 shops for DE
Processing France (FR)...
```

### 3.2 Restart Your Development Server

1. **Stop** your current dev server (press **Ctrl+C** in the terminal where it's running)
2. **Start** it again:
   ```bash
   npm run dev
   ```

### 3.3 Test Your Website

1. Open your browser: **http://localhost:3000**
2. You should now see:
   - ✅ No more "Error fetching data"
   - ✅ No more "Please add your Google Maps API key"
   - ✅ A beautiful map showing all motorcycle shops
   - ✅ Country filter buttons at the top
   - ✅ Shop count in the header

### 3.4 Test the Features

Try these:
- Click on **Germany (DE)** - should show only German shops
- Click on **France (FR)** - should show only French shops
- Click on **"🌍 All"** - should show all shops
- Try the **search box** - search for a city name
- Switch between **Map View** and **List View**
- Click on **map markers** to see shop details

✅ **Step 3 Complete! Your website is fully functional! 🎉**

---

## 🐛 Troubleshooting

### Still seeing "Error fetching data"?

1. Run the checker script:
   ```bash
   ./check-setup.sh
   ```
2. Make sure all three credentials show ✅
3. Make sure you **restarted** the dev server after saving .env.local
4. Check browser console (F12) for error details

### Map not loading?

1. Check that billing is enabled in Google Cloud Console
2. Verify "Maps JavaScript API" is enabled
3. Try creating a new API key
4. Wait 1-2 minutes after creating the key (it needs to activate)

### No shops showing up?

1. Make sure you ran `npm run fetch:data` and it completed successfully
2. Check your Supabase dashboard → Table Editor → motorcycle_shops
3. You should see rows of data there
4. If the table is empty, run `npm run fetch:data` again

### Countries not filtering shops?

1. This happens when there's no data in the database
2. Run `npm run fetch:data` to populate the data
3. Refresh your browser after data is loaded

---

## ✅ Final Checklist

- [ ] Supabase URL added to .env.local
- [ ] Supabase ANON key added to .env.local
- [ ] Google Maps API key added to .env.local
- [ ] Created motorcycle_shops table in Supabase
- [ ] Ran `npm run fetch:data` successfully
- [ ] Restarted dev server
- [ ] Website loads without errors
- [ ] Can filter shops by country
- [ ] Map displays correctly

---

## 🎉 You're Done!

Your motorcycle repair shop directory is now fully functional!

**What you can do now:**
- Browse 1000+ motorcycle repair shops across Europe
- Filter by any of 27 EU countries
- Search for specific shops or cities
- View shops on an interactive map
- Get contact information and directions
- Switch between map and list views

Enjoy your new website! 🏍️
