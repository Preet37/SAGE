import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SAGE — Socratic Agent for Guided Education",
  description: "Multi-agent AI tutoring platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-background text-foreground antialiased">{children}</body>
    </html>
  );
}
