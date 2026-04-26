"use client";
import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import Link from "next/link";
import { api, CourseOut, LessonOut } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { CheckCircle2, Circle, PlayCircle, FileText, ArrowLeft, Loader2 } from "lucide-react";

const mono: React.CSSProperties  = { fontFamily: "var(--font-dm-mono)" };
const serif: React.CSSProperties = { fontFamily: "var(--font-cormorant)" };
const body: React.CSSProperties  = { fontFamily: "var(--font-crimson)" };

export default function PathPage() {
  const router = useRouter();
  const params = useParams();
  const pathId = params.pathId as string;
  const [course, setCourse] = useState<CourseOut | null>(null);
  const [lessons, setLessons] = useState<LessonOut[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (!token) { router.push("/login"); return; }

    Promise.all([
      api.courses.list(token),
      api.courses.lessons(pathId, token),
    ])
      .then(([courseList, lessonList]) => {
        const found = courseList.find((c) => c.slug === pathId);
        if (!found) { router.push("/learn"); return; }
        setCourse(found);
        setLessons(lessonList);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [pathId, router]);

  if (loading) {
    return (
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "100%" }}>
        <Loader2 style={{ width: "1.25rem", height: "1.25rem", color: "var(--gold)" }} className="animate-spin" />
      </div>
    );
  }

  if (!course) return null;

  return (
    <div className="thin-scrollbar" style={{ height: "100%", overflowY: "auto" }}>
      <div style={{ maxWidth: "42rem", margin: "0 auto", padding: "2.5rem 2rem 4rem" }}>

        {/* Back */}
        <Link href="/learn" style={{ display: "inline-flex", alignItems: "center", gap: "0.35rem", ...mono, fontSize: "0.52rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)", textDecoration: "none", marginBottom: "1.75rem" }}>
          <ArrowLeft style={{ width: "0.75rem", height: "0.75rem" }} />
          All Courses
        </Link>

        {/* Header */}
        <div style={{ marginBottom: "2rem" }}>
          <span style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--gold)", border: "1px solid var(--gold)", padding: "0.1rem 0.4rem", marginBottom: "0.75rem", display: "inline-block" }}>
            {course.level}
          </span>
          <h1 style={{ ...serif, fontWeight: 700, fontStyle: "italic", fontSize: "clamp(1.75rem,4vw,2.5rem)", color: "var(--cream-0)", lineHeight: 1.1, marginBottom: "0.5rem" }}>
            {course.title}
          </h1>
          <p style={{ ...body, fontSize: "0.95rem", color: "var(--cream-1)", lineHeight: 1.6 }}>
            {course.description}
          </p>
        </div>

        {/* Lesson count */}
        <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "1.5rem" }}>
          <div style={{ height: "1px", width: "1.5rem", background: "var(--gold)" }} />
          <span style={{ ...mono, fontSize: "0.55rem", letterSpacing: "0.14em", textTransform: "uppercase", color: "var(--cream-2)" }}>
            {lessons.length} {lessons.length === 1 ? "lesson" : "lessons"}
          </span>
          <div style={{ flex: 1, height: "1px", background: "rgba(240,233,214,0.07)" }} />
        </div>

        {/* Lessons */}
        <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          {lessons.map((lesson, i) => (
            <Link key={lesson.id} href={`/learn/${pathId}/${lesson.slug}`} style={{ textDecoration: "none" }}>
              <div
                className="topic-card"
                style={{ background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.07)", padding: "1rem 1.25rem", display: "flex", alignItems: "center", gap: "1rem" }}
              >
                <span style={{ ...mono, fontSize: "0.5rem", color: "var(--cream-2)", flexShrink: 0, width: "1.5rem", textAlign: "right" }}>{String(i + 1).padStart(2, "0")}</span>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <p style={{ ...body, fontSize: "1rem", color: "var(--cream-0)", lineHeight: 1.3, marginBottom: lesson.key_concepts.length ? "0.3rem" : 0 }}>
                    {lesson.title}
                  </p>
                  {lesson.key_concepts.length > 0 && (
                    <p style={{ ...mono, fontSize: "0.48rem", letterSpacing: "0.06em", color: "var(--cream-2)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                      {lesson.key_concepts.slice(0, 4).join(" · ")}
                    </p>
                  )}
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: "0.4rem", flexShrink: 0 }}>
                  {lesson.estimated_minutes > 0 && (
                    <span style={{ ...mono, fontSize: "0.48rem", color: "var(--cream-2)" }}>{lesson.estimated_minutes}m</span>
                  )}
                  {lesson.video_url && <PlayCircle style={{ width: "0.85rem", height: "0.85rem", color: "var(--cream-2)" }} />}
                  <FileText style={{ width: "0.85rem", height: "0.85rem", color: "var(--cream-2)" }} />
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
