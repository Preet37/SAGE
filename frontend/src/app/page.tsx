"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

import { useAuth } from "@/lib/auth";

export default function Home() {
  const { token, ready } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (ready && token) router.replace("/learn");
  }, [ready, token, router]);

  return (
    <main className="bg-blobs relative grid min-h-screen place-items-center overflow-hidden p-6">
      <section className="card relative z-10 max-w-3xl space-y-6 p-10 text-center">
        <Logo />
        <h1
          className="text-4xl sm:text-5xl"
          style={{ fontFamily: "var(--font-heading)", fontWeight: 700, letterSpacing: "-0.02em" }}
        >
          The Socratic AI tutor that asks the right questions.
        </h1>
        <p className="mx-auto max-w-xl text-base opacity-80">
          SAGE coordinates a six-agent swarm to teach you concept-by-concept,
          ground every claim in your sources, and adapt to how <em>you</em> learn.
        </p>
        <ul className="mx-auto grid max-w-xl grid-cols-1 gap-3 text-sm sm:grid-cols-3">
          <Feature title="Live agents" body="Pedagogy, content, and verification stream in real time." />
          <Feature title="Verified" body="Every answer is grounded in retrieved sources." />
          <Feature title="Adaptive" body="Concept mastery shapes the next question." />
        </ul>

        <div className="flex flex-wrap justify-center gap-3 pt-2">
          <Link href="/register" className="btn-primary">
            Create account
          </Link>
          <Link
            href="/login"
            className="rounded-full px-5 py-3 font-semibold"
            style={{
              background: "var(--color-muted)",
              color: "var(--color-primary)",
              border: "1px solid var(--color-border)",
            }}
          >
            Sign in
          </Link>
        </div>
        <p className="text-xs opacity-60">
          Demo credentials: <code>demo@sage.ai</code> · <code>demo1234</code>
        </p>
      </section>
    </main>
  );
}

function Feature({ title, body }: { title: string; body: string }) {
  return (
    <li
      className="rounded-2xl p-4 text-left"
      style={{
        background: "var(--color-muted)",
        border: "1px solid var(--color-border)",
      }}
    >
      <p className="font-semibold" style={{ fontFamily: "var(--font-heading)" }}>
        {title}
      </p>
      <p className="mt-1 text-xs opacity-70">{body}</p>
    </li>
  );
}

function Logo() {
  return (
    <div className="mx-auto" aria-hidden>
      <svg width={56} height={56} viewBox="0 0 32 32">
        <defs>
          <linearGradient id="g-home" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="var(--color-primary)" />
            <stop offset="100%" stopColor="var(--color-accent)" />
          </linearGradient>
        </defs>
        <rect x="2" y="2" width="28" height="28" rx="9" fill="url(#g-home)" />
        <path
          d="M10 20c2 1.5 4 2 6 2s4-.5 6-2M11 13c.7-.7 1.6-1 2.5-1M18.5 12c.9 0 1.8.3 2.5 1"
          stroke="white"
          strokeWidth="2"
          strokeLinecap="round"
          fill="none"
        />
      </svg>
    </div>
  );
}
