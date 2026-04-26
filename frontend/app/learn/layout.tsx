"use client";
import { useEffect, useState, useCallback, useRef } from "react";
import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";
import { api, CourseOut, LessonOut } from "@/lib/api";
import { getToken, removeToken } from "@/lib/auth";
import { ScrollArea } from "@/components/ui/scroll-area";
import { CheckCircle2, Circle, LogOut, BookOpen, Menu, X, ChevronDown, GripVertical } from "lucide-react";
import { AppHeader } from "@/components/AppHeader";

const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };
const serif: React.CSSProperties = { fontFamily: "var(--font-cormorant)" };

function LevelBadge({ level }: { level: string }) {
  const colors: Record<string, string> = {
    beginner:     "var(--sage-c)",
    intermediate: "var(--gold)",
    advanced:     "var(--rose)",
  };
  return (
    <span style={{
      ...mono,
      fontSize: "0.5rem",
      letterSpacing: "0.1em",
      textTransform: "uppercase",
      color: colors[level] || colors.beginner,
      border: `1px solid ${colors[level] || colors.beginner}`,
      padding: "0.1rem 0.4rem",
    }}>
      {level}
    </span>
  );
}

export default function LearnLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [paths, setPaths] = useState<CourseOut[]>([]);
  const [lessons, setLessons] = useState<LessonOut[]>([]);
  const [progress, setProgress] = useState<Record<string, boolean>>({});
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [sidebarWidth, setSidebarWidth] = useState(260);
  const [loading, setLoading] = useState(true);
  const [pathPickerOpen, setPathPickerOpen] = useState(false);
  const isDragging = useRef(false);

  const handleDragStart = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    isDragging.current = true;
    const startX = e.clientX;
    const startWidth = sidebarWidth;
    const onMouseMove = (ev: MouseEvent) => {
      setSidebarWidth(Math.max(200, Math.min(480, startWidth + (ev.clientX - startX))));
    };
    const onMouseUp = () => {
      isDragging.current = false;
      document.removeEventListener("mousemove", onMouseMove);
      document.removeEventListener("mouseup", onMouseUp);
      document.body.style.cursor = "";
      document.body.style.userSelect = "";
    };
    document.body.style.cursor = "col-resize";
    document.body.style.userSelect = "none";
    document.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseup", onMouseUp);
  }, [sidebarWidth]);

  const segments = pathname.split("/").filter(Boolean);
  const activePathSlug = segments[1] || "";
  const activePath = paths.find((p) => p.slug === activePathSlug);
  const isOnLesson = segments.length >= 3;
  const activeLessonSlug = isOnLesson ? segments[2] : "";

  // Load lessons whenever the active course changes
  useEffect(() => {
    if (!activePathSlug) return;
    const token = getToken();
    if (!token) return;
    api.courses.lessons(activePathSlug, token).then(setLessons).catch(() => {});
  }, [activePathSlug]);


  useEffect(() => {
    const token = getToken();
    if (!token) { router.push("/login?returnTo=/learn"); return; }

    async function load() {
      try {
        const courseList = await api.courses.list(token!);
        setPaths(courseList);
      } catch {
        // 401s handled inside request(); other failures show empty state
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [router]);

  function handleLogout() { removeToken(); router.push("/login"); }

  return (
    <div className="flex h-dvh overflow-hidden" style={{ background: "var(--ink)", color: "var(--cream-0)" }}>
      {/* Sidebar */}
      {sidebarOpen && (
        <>
          <aside
            className="flex flex-col h-full flex-shrink-0"
            style={{
              width: sidebarWidth,
              background: "var(--ink-1)",
              borderRight: "1px solid rgba(240,233,214,0.07)",
            }}
          >
            {/* Sidebar header */}
            <div
              className="flex items-center justify-between px-4"
              style={{
                height: "3rem",
                borderBottom: "1px solid rgba(240,233,214,0.07)",
                flexShrink: 0,
              }}
            >
              <span style={{ ...serif, fontWeight: 600, fontStyle: "italic", fontSize: "1.05rem", color: "var(--cream-0)" }}>
                Courses
              </span>
              <button
                onClick={() => setSidebarOpen(false)}
                style={{ background: "none", border: "none", cursor: "pointer", color: "var(--cream-2)", display: "flex", alignItems: "center", padding: "0.25rem" }}
              >
                <X style={{ width: "0.85rem", height: "0.85rem" }} />
              </button>
            </div>

            <ScrollArea className="flex-1">
              {loading ? (
                <div style={{ ...mono, fontSize: "0.6rem", letterSpacing: "0.1em", color: "var(--cream-2)", padding: "1rem 1rem" }}>
                  Loading...
                </div>
              ) : (
                <nav style={{ padding: "0.5rem" }}>
                  {/* Course picker */}
                  <div style={{ position: "relative" }}>
                    <button
                      onClick={() => setPathPickerOpen(!pathPickerOpen)}
                      className="w-full"
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "0.5rem",
                        padding: "0.6rem 0.75rem",
                        background: pathPickerOpen ? "rgba(240,233,214,0.05)" : "none",
                        border: "1px solid rgba(240,233,214,0.08)",
                        cursor: "pointer",
                        textAlign: "left",
                      }}
                    >
                      <BookOpen style={{ width: "0.8rem", height: "0.8rem", color: "var(--gold)", flexShrink: 0 }} />
                      <span style={{ ...mono, fontSize: "0.58rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-1)", flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                        {activePath?.title || "Select a course"}
                      </span>
                      <ChevronDown style={{ width: "0.7rem", height: "0.7rem", color: "var(--cream-2)", transform: pathPickerOpen ? "rotate(180deg)" : "none", transition: "transform 0.2s", flexShrink: 0 }} />
                    </button>

                    {pathPickerOpen && (
                      <div style={{
                        position: "absolute",
                        left: 0, right: 0,
                        marginTop: "0.25rem",
                        background: "var(--ink-2)",
                        border: "1px solid rgba(240,233,214,0.08)",
                        zIndex: 10,
                      }}>
                        {paths.length === 0 && (
                          <div style={{ ...mono, fontSize: "0.58rem", color: "var(--cream-2)", padding: "0.75rem" }}>No courses yet</div>
                        )}
                        {paths.map((path) => (
                          <Link
                            key={path.id}
                            href={`/learn/${path.slug}`}
                            onClick={() => setPathPickerOpen(false)}
                          >
                            <div style={{
                              display: "flex",
                              alignItems: "center",
                              justifyContent: "space-between",
                              gap: "0.5rem",
                              padding: "0.65rem 0.75rem",
                              background: path.slug === activePathSlug ? "rgba(196,152,90,0.07)" : "none",
                              borderLeft: path.slug === activePathSlug ? "2px solid var(--gold)" : "2px solid transparent",
                              cursor: "pointer",
                            }}>
                              <span style={{ ...mono, fontSize: "0.58rem", letterSpacing: "0.08em", color: path.slug === activePathSlug ? "var(--cream-0)" : "var(--cream-1)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{path.title}</span>
                              <LevelBadge level={path.level} />
                            </div>
                          </Link>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Lesson list */}
                  {activePath && lessons.length > 0 && (
                    <div style={{ marginTop: "0.75rem" }}>
                      <div style={{ height: "1px", background: "rgba(240,233,214,0.07)", marginBottom: "0.5rem" }} />
                      {lessons.map((lesson) => {
                        const done = progress[String(lesson.id)];
                        const isActive = activeLessonSlug === lesson.slug;
                        return (
                          <Link key={lesson.id} href={`/learn/${activePath.slug}/${lesson.slug}`}>
                            <div style={{
                              display: "flex",
                              alignItems: "center",
                              gap: "0.5rem",
                              padding: "0.45rem 0.5rem",
                              background: isActive ? "rgba(196,152,90,0.08)" : "none",
                              borderLeft: isActive ? "1px solid var(--gold)" : "1px solid transparent",
                              cursor: "pointer",
                              transition: "background 0.15s",
                            }}>
                              {done
                                ? <CheckCircle2 style={{ width: "0.75rem", height: "0.75rem", color: "var(--sage-c)", flexShrink: 0 }} />
                                : <Circle style={{ width: "0.75rem", height: "0.75rem", color: isActive ? "var(--gold)" : "var(--cream-2)", flexShrink: 0 }} />
                              }
                              <span style={{ fontFamily: "var(--font-crimson)", fontSize: "0.85rem", color: isActive ? "var(--cream-0)" : "var(--cream-1)", lineHeight: 1.3, flex: 1 }}>
                                {lesson.title}
                              </span>
                            </div>
                          </Link>
                        );
                      })}
                    </div>
                  )}

                  {!activePath && paths.length > 0 && (
                    <p style={{ ...mono, fontSize: "0.55rem", color: "var(--cream-2)", padding: "0.75rem 0.5rem", letterSpacing: "0.08em" }}>
                      Select a course above to see its lessons.
                    </p>
                  )}
                </nav>
              )}
            </ScrollArea>

            {/* Sign out */}
            <div style={{ padding: "0.75rem", borderTop: "1px solid rgba(240,233,214,0.07)", flexShrink: 0 }}>
              <button
                onClick={handleLogout}
                className="w-full"
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "0.5rem",
                  padding: "0.5rem 0.6rem",
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                  color: "var(--cream-2)",
                  transition: "color 0.2s",
                }}
                onMouseEnter={e => (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-1)"}
                onMouseLeave={e => (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-2)"}
              >
                <LogOut style={{ width: "0.75rem", height: "0.75rem" }} />
                <span style={{ ...mono, fontSize: "0.55rem", letterSpacing: "0.12em", textTransform: "uppercase" }}>Sign out</span>
              </button>
            </div>
          </aside>

          {/* Drag handle */}
          <div
            onMouseDown={handleDragStart}
            style={{
              width: "4px",
              flexShrink: 0,
              background: "rgba(240,233,214,0.04)",
              cursor: "col-resize",
              transition: "background 0.2s",
            }}
            onMouseEnter={e => (e.currentTarget as HTMLDivElement).style.background = "rgba(196,152,90,0.25)"}
            onMouseLeave={e => (e.currentTarget as HTMLDivElement).style.background = "rgba(240,233,214,0.04)"}
          />
        </>
      )}

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden h-full">
        <AppHeader
          leftSlot={
            !sidebarOpen ? (
              <button
                onClick={() => setSidebarOpen(true)}
                style={{ background: "none", border: "none", cursor: "pointer", color: "var(--cream-2)", display: "flex", alignItems: "center", padding: "0.25rem" }}
              >
                <Menu style={{ width: "0.9rem", height: "0.9rem" }} />
              </button>
            ) : undefined
          }
        />
        <main className="flex-1 min-h-0 overflow-hidden">{children}</main>
      </div>
    </div>
  );
}
