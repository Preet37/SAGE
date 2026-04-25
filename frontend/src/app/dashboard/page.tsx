"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import AppHeader from "@/components/AppHeader";
import ProtectedRoute from "@/components/ProtectedRoute";
import { getDashboard, type Dashboard } from "@/lib/api";
import { clearAuth, useAuth } from "@/lib/auth";

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <DashboardBody />
    </ProtectedRoute>
  );
}

function DashboardBody() {
  const { token, user } = useAuth();
  const [data, setData] = useState<Dashboard | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    getDashboard(token).then(setData).catch((err) => setError(String(err)));
  }, [token]);

  return (
    <main className="bg-blobs flex min-h-screen flex-col gap-4 p-4">
      <AppHeader />
      <section className="mx-auto w-full max-w-5xl space-y-5">
        <header className="card flex items-center justify-between p-5">
          <div>
            <h1 className="text-2xl" style={{ fontFamily: "var(--font-heading)", fontWeight: 700 }}>
              Hi {user?.name || user?.email}
            </h1>
            <p className="mt-1 text-sm opacity-70">Your learning, summarised.</p>
          </div>
          <div className="flex items-center gap-2">
            <Link href="/learn" className="btn-primary">
              Continue learning
            </Link>
            <button
              type="button"
              onClick={() => {
                clearAuth();
                window.location.href = "/login";
              }}
              className="rounded-full px-3 py-1.5 text-xs font-semibold"
              style={{
                background: "var(--color-muted)",
                color: "var(--color-foreground)",
                border: "1px solid var(--color-border)",
              }}
            >
              Sign out
            </button>
          </div>
        </header>

        {error && (
          <p role="alert" className="rounded-xl px-3 py-2 text-sm" style={{ color: "var(--color-destructive)" }}>
            {error}
          </p>
        )}

        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          <Stat
            label="Catalog"
            value={data ? `${data.my_courses} / ${data.catalog_size}` : "–"}
          />
          <Stat label="Sessions" value={data?.sessions ?? 0} />
          <Stat
            label="Concepts mastered"
            value={`${data?.concepts_mastered ?? 0} / ${data?.concepts_total ?? 0}`}
          />
          <Stat
            label="Grounded rate"
            value={data ? `${Math.round(data.grounded_rate * 100)}%` : "–"}
          />
        </div>

        <section className="card p-5">
          <h2 className="text-lg" style={{ fontFamily: "var(--font-heading)" }}>
            Recent sessions
          </h2>
          <ul className="mt-3 divide-y" style={{ borderColor: "var(--color-border)" }}>
            {data?.recent_sessions?.length ? (
              data.recent_sessions.map((s) => (
                <li key={s.id} className="flex items-center justify-between py-3 text-sm">
                  <span>
                    Session #{s.id}
                    {s.lesson_id ? ` · lesson ${s.lesson_id}` : ""}
                  </span>
                  <Link
                    href={`/learn/${s.lesson_id ?? 0}/${s.id}`}
                    className="font-semibold"
                    style={{ color: "var(--color-primary)" }}
                  >
                    Review →
                  </Link>
                </li>
              ))
            ) : (
              <li className="py-6 text-center text-sm opacity-70">
                No sessions yet — start one from the course list.
              </li>
            )}
          </ul>
        </section>
      </section>
    </main>
  );
}

function Stat({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="card p-4">
      <p className="text-xs uppercase tracking-wide opacity-60">{label}</p>
      <p
        className="mt-1 text-2xl"
        style={{ fontFamily: "var(--font-heading)", fontWeight: 700 }}
      >
        {value}
      </p>
    </div>
  );
}
