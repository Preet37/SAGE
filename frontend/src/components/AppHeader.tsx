"use client";

import Link from "next/link";

interface AppHeaderProps {
  courseId?: string;
  lessonId?: string;
}

export default function AppHeader({ courseId, lessonId }: AppHeaderProps) {
  return (
    <header
      className="flex items-center justify-between rounded-3xl px-5 py-3"
      style={{
        background: "white",
        border: "1px solid var(--color-border)",
        boxShadow: "var(--shadow-sm)",
      }}
    >
      <Link href="/" className="flex items-center gap-2">
        <Logo />
        <span
          className="text-xl"
          style={{ fontFamily: "var(--font-heading)", fontWeight: 700, letterSpacing: "-0.02em" }}
        >
          SAGE
        </span>
      </Link>

      {(courseId || lessonId) && (
        <nav className="flex items-center gap-2 text-sm">
          <Crumb label="Home" href="/" />
          <Sep />
          <Crumb label={`Course ${courseId}`} href={`/learn/${courseId}/1`} />
          <Sep />
          <span
            className="rounded-full px-3 py-1 font-semibold"
            style={{ background: "var(--color-muted)", color: "var(--color-primary)" }}
          >
            Lesson {lessonId}
          </span>
        </nav>
      )}

      <div className="flex items-center gap-3">
        <span
          className="hidden rounded-full px-3 py-1 text-xs font-semibold sm:inline-flex"
          style={{ background: "var(--color-muted)", color: "var(--color-foreground)" }}
        >
          Socratic mode
        </span>
        <button
          aria-label="Profile"
          className="grid h-9 w-9 place-items-center rounded-full text-sm font-bold"
          style={{
            background: "var(--color-primary)",
            color: "var(--color-on-primary)",
            cursor: "pointer",
          }}
        >
          S
        </button>
      </div>
    </header>
  );
}

function Crumb({ label, href }: { label: string; href: string }) {
  return (
    <Link href={href} className="opacity-70 hover:opacity-100">
      {label}
    </Link>
  );
}

function Sep() {
  return <span style={{ color: "var(--color-border)" }}>/</span>;
}

function Logo() {
  return (
    <svg width={32} height={32} viewBox="0 0 32 32" aria-hidden>
      <defs>
        <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="var(--color-primary)" />
          <stop offset="100%" stopColor="var(--color-accent)" />
        </linearGradient>
      </defs>
      <rect x="2" y="2" width="28" height="28" rx="9" fill="url(#g)" />
      <path
        d="M10 20c2 1.5 4 2 6 2s4-.5 6-2M11 13c.7-.7 1.6-1 2.5-1M18.5 12c.9 0 1.8.3 2.5 1"
        stroke="white"
        strokeWidth="2"
        strokeLinecap="round"
        fill="none"
      />
    </svg>
  );
}
