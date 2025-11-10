import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Motorcycle Repair Shops - European Directory",
  description: "Find trusted motorcycle repair shops across 27 European countries. Interactive maps, country filtering, and comprehensive shop information.",
  keywords: ["motorcycle", "repair", "shops", "Europe", "EU", "service", "maintenance"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
