import type { Metadata } from "next";
import { Cormorant_Garamond, Crimson_Pro, DM_Mono, Inter } from "next/font/google";
import { ThemeProvider } from "@/components/ThemeProvider";
import { FloatingUI } from "@/components/FloatingUI";
import "./globals.css";

const cormorant = Cormorant_Garamond({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  style: ["normal", "italic"],
  variable: "--font-cormorant",
});

const crimson = Crimson_Pro({
  subsets: ["latin"],
  weight: ["300", "400", "600"],
  style: ["normal", "italic"],
  variable: "--font-crimson",
});

const dmMono = DM_Mono({
  subsets: ["latin"],
  weight: ["300", "400", "500"],
  variable: "--font-dm-mono",
});

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "SAGE",
  description: "SAGE — AI-powered adaptive learning platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning style={{ background: "#0D0B08" }}>
      <body
        className={`${cormorant.variable} ${crimson.variable} ${dmMono.variable} ${inter.variable}`}
        style={{ background: "#0D0B08" }}
      >
        <ThemeProvider>
          {children}
          <FloatingUI />
        </ThemeProvider>
      </body>
    </html>
  );
}
