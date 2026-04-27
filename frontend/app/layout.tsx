import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "VibeMatch AI",
  description: "A local full-stack music recommender app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body>{children}</body>
    </html>
  );
}
