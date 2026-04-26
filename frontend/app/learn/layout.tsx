"use client";
import { useEffect, useState, useMemo, useCallback, useRef } from "react";
import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";
import { api, LearningPathResponse, ProgressResponse } from "@/lib/api";
import { getToken, removeToken } from "@/lib/auth";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { CheckCircle2, Circle, ChevronRight, LogOut, BookOpen, Menu, X, ChevronDown, GripVertical } from "lucide-react";
import { cn } from "@/lib/utils";
import { ThemeToggle } from "@/components/ThemeToggle";
import { AppHeader } from "@/components/AppHeader";

function LevelBadge({ level }: { level: string }) {
  const colors: Record<string, string> = {
    beginner: "bg-green-500/20 text-green-400",
    intermediate: "bg-yellow-500/20 text-yellow-400",
    advanced: "bg-red-500/20 text-red-400",
  };
  return (
    <span className={cn("text-xs px-2 py-0.5 rounded-full font-medium", colors[level] || colors.beginner)}>
      {level}
    </span>
  );
}

export default function LearnLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [paths, setPaths] = useState<LearningPathResponse[]>([]);
  const [progress, setProgress] = useState<Record<string, boolean>>({});
  // Sidebar starts collapsed on small screens to keep the chat the focal point.
  const [sidebarOpen, setSidebarOpen] = useState(() => {
    if (typeof window === "undefined") return true;
    return window.matchMedia("(min-width: 768px)").matches;
  });
  const [sidebarWidth, setSidebarWidth] = useState(280);
  const [loading, setLoading] = useState(true);
  const [pathPickerOpen, setPathPickerOpen] = useState(false);
  const isDragging = useRef(false);

  const handleDragStart = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    isDragging.current = true;
    const startX = e.clientX;
    const startWidth = sidebarWidth;

    const onMouseMove = (ev: MouseEvent) => {
      const newWidth = Math.max(200, Math.min(500, startWidth + (ev.clientX - startX)));
      setSidebarWidth(newWidth);
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

  const [expandedModules, setExpandedModules] = useState<Set<string>>(new Set());

  // Extract the active path slug from the URL: /learn/[pathId]/...
  const segments = pathname.split("/").filter(Boolean);
  const activePathSlug = segments[1] || "";
  const activePath = paths.find((p) => p.slug === activePathSlug);
  const isOnLesson = segments.length >= 3;
  const activeLessonId = isOnLesson ? segments[2] : "";

  // Auto-expand the module containing the active lesson
  const activeModuleId = useMemo(() => {
    if (!activePath || !activeLessonId) return "";
    for (const mod of activePath.modules) {
      if (mod.lessons.some((l) => l.id === activeLessonId)) return mod.id;
    }
    return "";
  }, [activePath, activeLessonId]);

  useEffect(() => {
    if (activeModuleId) {
      setExpandedModules((prev) => {
        if (prev.has(activeModuleId)) return prev;
        const next = new Set(prev);
        next.add(activeModuleId);
        return next;
      });
    }
  }, [activeModuleId]);

  function toggleModule(modId: string) {
    setExpandedModules((prev) => {
      const next = new Set(prev);
      if (next.has(modId)) next.delete(modId);
      else next.add(modId);
      return next;
    });
  }

  useEffect(() => {
    const token = getToken();
    if (!token) { router.push("/login?returnTo=/learn"); return; }

    async function load() {
      try {
        const [summaries, prog] = await Promise.all([
          api.learningPaths.list(token!),
          api.progress.getAll(token!),
        ]);
        const progMap: Record<string, boolean> = {};
        prog.forEach((p) => { progMap[p.lesson_id] = p.completed; });
        setProgress(progMap);

        const full = await Promise.all(
          summaries.map((s) => api.learningPaths.get(s.slug, token!))
        );
        setPaths(full);
      } catch {
        router.push("/login");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [router]);

  function handleLogout() {
    removeToken();
    router.push("/login");
  }

  return (
    <div className="flex h-dvh bg-background overflow-hidden">
      {/* Sidebar — overlay on mobile, inline column on md+ */}
      {sidebarOpen && (
        <>
          {/* Mobile backdrop */}
          <div
            onClick={() => setSidebarOpen(false)}
            aria-hidden="true"
            className="fixed inset-0 z-30 bg-black/40 md:hidden"
          />
          <aside
            aria-label="Course navigation"
            className="fixed inset-y-0 left-0 z-40 flex flex-col h-full border-r border-border bg-card flex-shrink-0 md:static md:z-auto"
            style={{ width: sidebarWidth, maxWidth: "85vw" }}
          >
            <div className="flex items-center justify-between p-4 border-b border-border">
              <div className="flex items-center gap-2">
                <svg viewBox="0 0 24 24" className="h-5 w-5 text-primary" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/>
                  <path d="M8 7h6M8 11h8"/>
                </svg>
                <span className="font-semibold text-sm"><span className="text-primary">Socratic</span>Tutor</span>
              </div>
              <div className="flex items-center gap-0.5">
                <ThemeToggle />
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setSidebarOpen(false)}
                  aria-label="Close sidebar"
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
            </div>

            <ScrollArea className="flex-1">
              {loading ? (
                <div className="p-4 text-sm text-muted-foreground">Loading...</div>
              ) : (
                <nav className="p-2 space-y-1">
                  <div className="relative">
                    <button
                      onClick={() => setPathPickerOpen(!pathPickerOpen)}
                      className="w-full flex items-center gap-2 px-3 py-2 rounded-md text-sm hover:bg-accent transition-colors text-left"
                    >
                      <BookOpen className="h-4 w-4 text-primary flex-shrink-0" />
                      <span className="flex-1 font-medium truncate">
                        {activePath?.title || "Select a course"}
                      </span>
                      <ChevronDown className={cn(
                        "h-3.5 w-3.5 text-muted-foreground transition-transform",
                        pathPickerOpen && "rotate-180"
                      )} />
                    </button>

                    {pathPickerOpen && (
                      <div className="absolute z-10 left-0 right-0 mt-1 rounded-md border border-border bg-popover shadow-lg">
                        {paths.map((path) => (
                          <Link
                            key={path.id}
                            href={`/learn/${path.slug}`}
                            onClick={() => setPathPickerOpen(false)}
                            className={cn(
                              "flex items-center gap-2 px-3 py-2 text-sm hover:bg-accent transition-colors first:rounded-t-md last:rounded-b-md",
                              path.slug === activePathSlug && "bg-accent/50"
                            )}
                          >
                            <span className="flex-1 truncate">{path.title}</span>
                            <LevelBadge level={path.level} />
                          </Link>
                        ))}
                      </div>
                    )}
                  </div>

                  {activePath && (
                    <>
                      <Separator className="my-2" />
                      {activePath.modules.map((mod) => {
                        const isExpanded = expandedModules.has(mod.id);
                        const completedCount = mod.lessons.filter((l) => progress[l.id]).length;
                        const hasActiveLessonInMod = mod.lessons.some((l) => pathname.includes(l.id));
                        return (
                          <div key={mod.id} className="mt-1">
                            <button
                              onClick={() => toggleModule(mod.id)}
                              className={cn(
                                "w-full flex items-center gap-1.5 px-2 py-1.5 rounded-md text-left hover:bg-accent transition-colors group",
                                hasActiveLessonInMod && "bg-accent/30"
                              )}
                            >
                              <ChevronRight className={cn(
                                "h-3 w-3 text-muted-foreground transition-transform flex-shrink-0",
                                isExpanded && "rotate-90"
                              )} />
                              <span className="flex-1 text-xs font-medium text-muted-foreground uppercase tracking-wider leading-tight">
                                {mod.title}
                              </span>
                              <span className="text-[10px] text-muted-foreground/60 flex-shrink-0">
                                {completedCount}/{mod.lessons.length}
                              </span>
                            </button>
                            {isExpanded && (
                              <div className="ml-1.5 mt-0.5 space-y-0.5">
                                {mod.lessons.map((lesson) => {
                                  const done = progress[lesson.id];
                                  const isActive = pathname.includes(lesson.id);
                                  return (
                                    <Link
                                      key={lesson.id}
                                      href={`/learn/${activePath.slug}/${lesson.id}`}
                                      className={cn(
                                        "flex items-center gap-2 px-2 py-1.5 rounded-md text-sm hover:bg-accent hover:text-accent-foreground transition-colors group",
                                        isActive && "bg-accent text-accent-foreground"
                                      )}
                                    >
                                      {done ? (
                                        <CheckCircle2 className="h-4 w-4 text-green-500 flex-shrink-0" />
                                      ) : (
                                        <Circle className={cn(
                                          "h-4 w-4 flex-shrink-0",
                                          isActive ? "text-primary" : "text-muted-foreground"
                                        )} />
                                      )}
                                      <span className="flex-1 leading-tight">{lesson.title}</span>
                                      <ChevronRight className="h-3 w-3 text-muted-foreground opacity-0 group-hover:opacity-100 flex-shrink-0" />
                                    </Link>
                                  );
                                })}
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </>
                  )}

                  {!activePath && paths.length > 0 && (
                    <div className="px-3 py-4 text-sm text-muted-foreground">
                      Select a course above to see its lessons.
                    </div>
                  )}
                </nav>
              )}
            </ScrollArea>

            <div className="p-4 border-t border-border">
              <Button variant="ghost" size="sm" onClick={handleLogout} className="w-full justify-start gap-2 text-muted-foreground">
                <LogOut className="h-4 w-4" />
                Sign out
              </Button>
            </div>
          </aside>

          {/* Drag handle — desktop only */}
          <div
            onMouseDown={handleDragStart}
            role="separator"
            aria-orientation="vertical"
            aria-label="Resize sidebar"
            className="hidden md:flex w-1.5 flex-shrink-0 bg-border hover:bg-primary/30 active:bg-primary/50 transition-colors cursor-col-resize items-center justify-center group"
          >
            <GripVertical className="h-4 w-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
          </div>
        </>
      )}

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden h-full">
        <AppHeader
          leftSlot={
            !sidebarOpen ? (
              <>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setSidebarOpen(true)}
                  aria-label="Open sidebar"
                >
                  <Menu className="h-4 w-4" />
                </Button>
                {!isOnLesson && (
                  <span className="text-sm font-medium"><span className="text-primary">Socratic</span>Tutor</span>
                )}
              </>
            ) : undefined
          }
        />
        <main className="flex-1 min-h-0 overflow-hidden">{children}</main>
      </div>
    </div>
  );
}
