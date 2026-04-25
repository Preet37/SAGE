"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

import AppHeader from "@/components/AppHeader";
import ProtectedRoute from "@/components/ProtectedRoute";
import { createCourse, createSession, getCourses, type Lesson } from "@/lib/api";
import { useAuth } from "@/lib/auth";

export default function LearnPage() {
  return (
    <ProtectedRoute>
      <CourseList />
    </ProtectedRoute>
  );
}

function CourseList() {
  const { token } = useAuth();
  const router = useRouter();
  const [courses, setCourses] = useState<Lesson[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [creating, setCreating] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newSubject, setNewSubject] = useState("");

  const refresh = useCallback(async () => {
    if (!token) return;
    setLoading(true);
    setError(null);
    try {
      setCourses(await getCourses(token));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load courses");
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const onOpen = useCallback(
    async (lesson: Lesson) => {
      if (!token) return;
      try {
        const session = await createSession(lesson.id, token);
        router.push(`/learn/${lesson.id}/${session.id}`);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to start session");
      }
    },
    [router, token],
  );

  const onCreate = useCallback(async () => {
    if (!token || !newTitle.trim()) return;
    setCreating(true);
    try {
      await createCourse(token, {
        title: newTitle.trim(),
        subject: newSubject.trim(),
        objective: "",
      });
      setNewTitle("");
      setNewSubject("");
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create course");
    } finally {
      setCreating(false);
    }
  }, [newSubject, newTitle, refresh, token]);

  return (
    <main className="bg-blobs flex min-h-screen flex-col gap-4 p-4">
      <AppHeader />
      <section className="card mx-auto w-full max-w-5xl flex-1 p-6">
        <header className="flex items-baseline justify-between">
          <div>
            <h1 className="text-2xl" style={{ fontFamily: "var(--font-heading)", fontWeight: 700 }}>
              Choose a course
            </h1>
            <p className="mt-1 text-sm opacity-70">
              Pick a topic to start a fresh tutor session, or create your own.
            </p>
          </div>
          <Link
            href="/dashboard"
            className="rounded-full px-3 py-1.5 text-xs font-semibold"
            style={{
              background: "var(--color-muted)",
              color: "var(--color-primary)",
              border: "1px solid var(--color-border)",
            }}
          >
            Open dashboard
          </Link>
        </header>

        {error && (
          <p
            role="alert"
            className="mt-4 rounded-xl px-3 py-2 text-sm"
            style={{
              background: "color-mix(in srgb, var(--color-destructive) 10%, white)",
              color: "var(--color-destructive)",
              border: "1px solid var(--color-destructive)",
            }}
          >
            {error}
          </p>
        )}

        <ul className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-2">
          {loading && <SkeletonRow count={3} />}
          {!loading && courses.length === 0 && (
            <li className="col-span-full rounded-2xl p-6 text-center text-sm opacity-70" style={{ background: "var(--color-muted)" }}>
              No courses yet — create your first below.
            </li>
          )}
          {!loading &&
            courses.map((c) => (
              <li key={c.id}>
                <button
                  type="button"
                  onClick={() => onOpen(c)}
                  className="block w-full rounded-2xl p-4 text-left transition hover:translate-y-[-1px]"
                  style={{
                    background: "var(--color-muted)",
                    border: "1px solid var(--color-border)",
                    boxShadow: "var(--shadow-sm)",
                    cursor: "pointer",
                  }}
                >
                  <p
                    className="text-base"
                    style={{ fontFamily: "var(--font-heading)", fontWeight: 600 }}
                  >
                    {c.title}
                  </p>
                  <p className="mt-0.5 text-xs opacity-70">{c.subject || "General"}</p>
                  <p className="mt-2 line-clamp-3 text-xs opacity-80">
                    {c.objective ? c.objective.split("\n\n")[0] : "Tap to begin tutoring."}
                  </p>
                </button>
              </li>
            ))}
        </ul>

        <section
          className="mt-6 rounded-2xl p-4"
          style={{ background: "var(--color-muted)", border: "1px dashed var(--color-border)" }}
        >
          <p className="text-sm font-semibold" style={{ fontFamily: "var(--font-heading)" }}>
            Add your own
          </p>
          <div className="mt-2 grid grid-cols-1 gap-2 sm:grid-cols-[2fr_1fr_auto]">
            <input
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              placeholder="Title"
              className="rounded-xl border bg-white px-3 py-2 text-sm"
              style={{ borderColor: "var(--color-border)" }}
            />
            <input
              value={newSubject}
              onChange={(e) => setNewSubject(e.target.value)}
              placeholder="Subject (optional)"
              className="rounded-xl border bg-white px-3 py-2 text-sm"
              style={{ borderColor: "var(--color-border)" }}
            />
            <button
              type="button"
              onClick={onCreate}
              disabled={creating || !newTitle.trim()}
              className="btn-primary disabled:opacity-60"
            >
              {creating ? "Creating…" : "Create"}
            </button>
          </div>
        </section>
      </section>
    </main>
  );
}

function SkeletonRow({ count }: { count: number }) {
  return (
    <>
      {Array.from({ length: count }).map((_, i) => (
        <li
          key={i}
          className="h-24 rounded-2xl shimmer"
          style={{ background: "var(--color-muted)" }}
        />
      ))}
    </>
  );
}
