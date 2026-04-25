"use client";

import Link from "next/link";
import { useCallback, useState } from "react";

import TeachingModeSelector from "@/components/TeachingModeSelector";
import { updateTeachingMode, type TeachingMode } from "@/lib/api";
import { clearAuth, setAuth, useAuth } from "@/lib/auth";

interface AppHeaderProps {
  courseId?: string;
  lessonId?: string;
  onOpenAccessibility?: () => void;
}

export default function AppHeader({ courseId, lessonId, onOpenAccessibility }: AppHeaderProps) {
  const { user, token } = useAuth();
  const initial = (user?.name || user?.email || "?").charAt(0).toUpperCase();
  const [busy, setBusy] = useState(false);

  const onModeChange = useCallback(
    async (mode: TeachingMode) => {
      if (!token || !user) return;
      setBusy(true);
      try {
        const updated = await updateTeachingMode(mode, token);
        setAuth(token, updated);
      } finally {
        setBusy(false);
      }
    },
    [token, user],
  );

  return (
    <header
      className="flex flex-wrap items-center justify-between gap-2 rounded-3xl px-5 py-3"
      style={{
        background: "white",
        border: "1px solid var(--color-border)",
        boxShadow: "var(--shadow-sm)",
      }}
    >
      <Link href="/learn" className="flex items-center gap-2">
        <Logo />
        <span
          className="text-xl"
          style={{ fontFamily: "var(--font-heading)", fontWeight: 700, letterSpacing: "-0.02em" }}
        >
          SAGE
        </span>
      </Link>

      {(courseId || lessonId) && (
        <nav aria-label="Breadcrumb" className="flex items-center gap-2 text-sm">
          <Link href="/learn" className="opacity-70 hover:opacity-100">
            Courses
          </Link>
          <Sep />
          <span
            className="rounded-full px-3 py-1 font-semibold"
            style={{ background: "var(--color-muted)", color: "var(--color-primary)" }}
          >
            {courseId ? `Course ${courseId}` : ""}
            {lessonId ? ` · Session ${lessonId}` : ""}
          </span>
        </nav>
      )}

      <div className="flex items-center gap-2">
        {user && (
          <TeachingModeSelector
            value={user.teaching_mode}
            onChange={onModeChange}
            disabled={busy}
          />
        )}
        {onOpenAccessibility && (
          <button
            type="button"
            onClick={onOpenAccessibility}
            className="rounded-full px-3 py-1.5 text-xs font-semibold"
            style={{
              background: "var(--color-muted)",
              color: "var(--color-primary)",
              border: "1px solid var(--color-border)",
              cursor: "pointer",
            }}
          >
            Accessibility
          </button>
        )}
        <Link
          href="/dashboard"
          className="rounded-full px-3 py-1.5 text-xs font-semibold"
          style={{
            background: "var(--color-muted)",
            color: "var(--color-primary)",
            border: "1px solid var(--color-border)",
          }}
        >
          Dashboard
        </Link>
        <button
          type="button"
          onClick={() => {
            clearAuth();
            window.location.href = "/login";
          }}
          aria-label="Sign out"
          className="grid h-9 w-9 place-items-center rounded-full text-sm font-bold"
          style={{
            background: "var(--color-primary)",
            color: "var(--color-on-primary)",
            cursor: "pointer",
          }}
          title="Sign out"
        >
          {initial}
        </button>
      </div>
    </header>
  );
}

function Sep() {
  return <span style={{ color: "var(--color-border)" }}>/</span>;
}

function Logo() {
  return (
    <svg width={32} height={32} viewBox="0 0 32 32" aria-hidden>
      <defs>
        <linearGradient id="g-header" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="var(--color-primary)" />
          <stop offset="100%" stopColor="var(--color-accent)" />
        </linearGradient>
      </defs>
      <rect x="2" y="2" width="28" height="28" rx="9" fill="url(#g-header)" />
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
