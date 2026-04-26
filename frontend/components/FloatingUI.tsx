"use client";
import { usePathname } from "next/navigation";
import Link from "next/link";
import { useState } from "react";
import { VoiceOrb } from "@/components/voice/VoiceOrb";

const HIDDEN_PATHS = ["/", "/login", "/register", "/onboarding"];

const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };

export function FloatingUI() {
  const pathname = usePathname();
  const [hovered, setHovered] = useState(false);
  if (HIDDEN_PATHS.includes(pathname)) return null;

  return (
    <>
      <VoiceOrb />
      <Link
        href="/wiki"
        style={{
          ...mono,
          position: "fixed",
          bottom: "1.25rem",
          left: "1.25rem",
          zIndex: 50,
          display: "flex",
          alignItems: "center",
          gap: "0.45rem",
          padding: "0.4rem 0.75rem",
          fontSize: "0.52rem",
          letterSpacing: "0.14em",
          textTransform: "uppercase",
          color: hovered ? "var(--cream-0)" : "var(--cream-1)",
          background: "var(--ink-2)",
          border: `1px solid ${hovered ? "rgba(196,152,90,0.5)" : "rgba(240,233,214,0.18)"}`,
          transition: "color 0.2s, border-color 0.2s",
          textDecoration: "none",
        }}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
      >
        <svg viewBox="0 0 16 16" style={{ width: "0.7rem", height: "0.7rem", fill: "currentColor", flexShrink: 0 }} aria-hidden="true">
          <path d="M1 2.5A1.5 1.5 0 0 1 2.5 1h11A1.5 1.5 0 0 1 15 2.5v11a1.5 1.5 0 0 1-1.5 1.5h-11A1.5 1.5 0 0 1 1 13.5v-11zm1.5 0v11h11v-11h-11zM4 5h8v1H4V5zm0 3h8v1H4V8zm0 3h5v1H4v-1z"/>
        </svg>
        Documentation
      </Link>
    </>
  );
}
