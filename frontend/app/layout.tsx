import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { ThemeProvider } from "@/components/ThemeProvider";
import { VoiceOrb } from "@/components/voice/VoiceOrb";
import Link from "next/link";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

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
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider>
          {children}
          <VoiceOrb />
          {/* Documentation link — bottom-left fixed */}
          <Link
            href="https://socratic-tutor-pi.vercel.app"
            target="_blank"
            rel="noopener noreferrer"
            className="fixed bottom-4 left-4 z-50 flex items-center gap-1.5 rounded-lg border border-border/60 bg-card/80 backdrop-blur-sm px-3 py-1.5 text-xs text-muted-foreground hover:text-foreground hover:border-border transition-colors shadow-sm"
          >
            <svg viewBox="0 0 16 16" className="h-3.5 w-3.5 fill-current flex-shrink-0" aria-hidden="true">
              <path d="M1 2.5A1.5 1.5 0 0 1 2.5 1h11A1.5 1.5 0 0 1 15 2.5v11a1.5 1.5 0 0 1-1.5 1.5h-11A1.5 1.5 0 0 1 1 13.5v-11zm1.5 0v11h11v-11h-11zM4 5h8v1H4V5zm0 3h8v1H4V8zm0 3h5v1H4v-1z"/>
            </svg>
            Documentation
          </Link>
        </ThemeProvider>
      </body>
    </html>
  );
}
