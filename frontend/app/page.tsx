"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { getToken } from "@/lib/auth";
import { KnowledgeGraph } from "@/components/KnowledgeGraph";

export default function Home() {
  const [authed, setAuthed] = useState<boolean | null>(null);

  useEffect(() => {
    setAuthed(!!getToken());
  }, []);

  return (
    <div
      className="h-screen overflow-hidden flex"
      style={{ background: "var(--ink)", color: "var(--cream-0)" }}
    >
      {/* ── Left column ─────────────────────────────────── */}
      <div className="relative z-10 flex flex-col justify-center px-14 lg:px-20 shrink-0 w-[44%]">
        {/* Wordmark */}
        <h1
          className="leading-none mb-7"
          style={{
            fontFamily: "var(--font-cormorant)",
            fontWeight: 700,
            fontStyle: "italic",
            fontSize: "clamp(4.5rem, 10.5vw, 9.5rem)",
            color: "var(--cream-0)",
            letterSpacing: "-0.01em",
          }}
        >
          SAGE
          <span style={{ color: "var(--gold)" }}>.</span>
        </h1>

        {/* Tagline */}
        <p
          className="mb-10 leading-relaxed"
          style={{
            fontFamily: "var(--font-crimson)",
            fontWeight: 300,
            fontSize: "clamp(0.95rem, 1.35vw, 1.1rem)",
            color: "var(--cream-1)",
            maxWidth: "26rem",
          }}
        >
          Six AI agents question, challenge, and guide you toward genuine
          understanding — not rote answers.
        </p>

        {/* CTAs */}
        <div className="flex items-center gap-7">
          <Link href={authed ? "/learn" : "/register"}>
            <button
              style={{
                fontFamily: "var(--font-dm-mono)",
                fontSize: "0.68rem",
                letterSpacing: "0.13em",
                textTransform: "uppercase",
                color: "var(--gold)",
                border: "1px solid var(--gold)",
                padding: "0.75rem 1.4rem",
                background: "transparent",
                cursor: "pointer",
                transition: "background 0.2s",
              }}
              onMouseEnter={(e) =>
                ((e.currentTarget as HTMLButtonElement).style.background =
                  "rgba(196,152,90,0.1)")
              }
              onMouseLeave={(e) =>
                ((e.currentTarget as HTMLButtonElement).style.background =
                  "transparent")
              }
            >
              {authed ? "Continue Learning" : "Begin Learning"} →
            </button>
          </Link>
          <Link
            href="/login"
            style={{
              fontFamily: "var(--font-dm-mono)",
              fontSize: "0.68rem",
              letterSpacing: "0.13em",
              textTransform: "uppercase",
              color: "var(--cream-1)",
              textDecoration: "none",
              transition: "color 0.2s",
            }}
            onMouseEnter={(e) =>
              ((e.currentTarget as HTMLAnchorElement).style.color =
                "var(--cream-0)")
            }
            onMouseLeave={(e) =>
              ((e.currentTarget as HTMLAnchorElement).style.color =
                "var(--cream-1)")
            }
          >
            Sign In
          </Link>
        </div>
      </div>

      {/* ── Right column — knowledge graph ───────────────── */}
      <div className="relative flex-1 overflow-hidden">
        {/* Vignette: fade left edge into background */}
        <div
          className="absolute inset-y-0 left-0 z-10 pointer-events-none"
          style={{
            width: "8rem",
            background: `linear-gradient(to right, var(--ink), transparent)`,
          }}
        />
        {/* Vignette: top + bottom soft edges */}
        <div
          className="absolute inset-x-0 top-0 z-10 pointer-events-none"
          style={{
            height: "6rem",
            background: `linear-gradient(to bottom, var(--ink), transparent)`,
          }}
        />
        <div
          className="absolute inset-x-0 bottom-0 z-10 pointer-events-none"
          style={{
            height: "6rem",
            background: `linear-gradient(to top, var(--ink), transparent)`,
          }}
        />
        <KnowledgeGraph />
      </div>
    </div>
  );
}
