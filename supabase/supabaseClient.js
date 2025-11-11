'use client'
import { createClient } from "@supabase/supabase-js";
// Use placeholder values during build if env vars are not set
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://gogupstledtvfitbjwhh.supabase.co';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdvZ3Vwc3RsZWR0dmZpdGJqd2hoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE1NDc1NjIsImV4cCI6MjA3NzEyMzU2Mn0.z_Yj1tzoYmubHNDOVyD2xHbpNUjL4Lip7M2qf5nM7Jc';


export const supabase = createClient(supabaseUrl, supabaseAnonKey);