import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'SAGE — Socratic Agent for Guided Education',
  description: 'Multi-agent AI tutor powered by Fetch.ai agents, real-time concept maps, and voice interaction.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-bg min-h-screen antialiased">{children}</body>
    </html>
  );
}
