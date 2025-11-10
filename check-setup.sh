#!/bin/bash

echo "=================================="
echo "🏍️ Motorcycle Shop Website Setup Checker"
echo "=================================="
echo ""

# Check if .env.local exists
if [ ! -f .env.local ]; then
    echo "❌ .env.local file not found!"
    echo "   Run: cp .env.local.example .env.local"
    exit 1
fi

echo "✅ .env.local file exists"
echo ""

# Check Supabase URL
SUPABASE_URL=$(grep NEXT_PUBLIC_SUPABASE_URL .env.local | cut -d '=' -f2)
if [[ "$SUPABASE_URL" == *"your_supabase"* ]] || [[ "$SUPABASE_URL" == "" ]]; then
    echo "❌ Supabase URL not configured"
    echo "   Current value: $SUPABASE_URL"
    echo "   Need: https://xxxxxxxxxxxxx.supabase.co"
    echo ""
    echo "📝 How to get it:"
    echo "   1. Go to https://supabase.com"
    echo "   2. Select your project"
    echo "   3. Go to Settings → API"
    echo "   4. Copy 'Project URL'"
    echo ""
else
    echo "✅ Supabase URL is configured"
    echo "   Value: $SUPABASE_URL"
    echo ""
fi

# Check Supabase Key
SUPABASE_KEY=$(grep NEXT_PUBLIC_SUPABASE_ANON_KEY .env.local | cut -d '=' -f2)
if [[ "$SUPABASE_KEY" == *"your_supabase"* ]] || [[ "$SUPABASE_KEY" == "" ]]; then
    echo "❌ Supabase ANON Key not configured"
    echo "   Current value: [placeholder]"
    echo "   Need: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    echo ""
    echo "📝 How to get it:"
    echo "   1. Go to https://supabase.com"
    echo "   2. Select your project"
    echo "   3. Go to Settings → API"
    echo "   4. Copy 'anon public' key"
    echo ""
else
    echo "✅ Supabase ANON Key is configured"
    echo "   Value: ${SUPABASE_KEY:0:30}..."
    echo ""
fi

# Check Google Maps API Key
MAPS_KEY=$(grep NEXT_PUBLIC_GOOGLE_MAPS_API_KEY .env.local | cut -d '=' -f2)
if [[ "$MAPS_KEY" == *"your_google"* ]] || [[ "$MAPS_KEY" == "" ]]; then
    echo "❌ Google Maps API Key not configured"
    echo "   Current value: [placeholder]"
    echo "   Need: AIzaSyXxXxXxXxXxXxXxXxXxXxX"
    echo ""
    echo "📝 How to get it:"
    echo "   1. Go to https://console.cloud.google.com"
    echo "   2. Create a new project"
    echo "   3. Enable 'Maps JavaScript API'"
    echo "   4. Go to Credentials → Create API Key"
    echo ""
else
    echo "✅ Google Maps API Key is configured"
    echo "   Value: ${MAPS_KEY:0:20}..."
    echo ""
fi

echo "=================================="
echo ""

# Check if all are configured
if [[ "$SUPABASE_URL" == *"your_supabase"* ]] || [[ "$SUPABASE_KEY" == *"your_supabase"* ]] || [[ "$MAPS_KEY" == *"your_google"* ]]; then
    echo "⚠️  You need to configure the missing credentials above"
    echo ""
    echo "After adding credentials:"
    echo "  1. Save the .env.local file"
    echo "  2. Stop your dev server (Ctrl+C)"
    echo "  3. Run: npm run dev"
    echo "  4. Refresh your browser"
    echo ""
else
    echo "🎉 All credentials are configured!"
    echo ""
    echo "Next steps:"
    echo "  1. Make sure you created the 'motorcycle_shops' table in Supabase"
    echo "  2. Run: npm run fetch:data (to populate data)"
    echo "  3. Restart dev server: npm run dev"
    echo ""
fi
