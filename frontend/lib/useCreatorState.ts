"use client";
import { useState, useCallback, useRef, useEffect } from "react";
import { api, DraftDetailResponse } from "./api";
import { getToken } from "./auth";
import { useCreatorStream, SSEEvent, uid } from "./useCreatorStream";

/* ── Types ──────────────────────────────────────────── */

export interface OutlineLesson {
  slug: string;
  title: string;
  summary: string;
  concepts: string[];
}

export interface OutlineModule {
  title: string;
  lessons: OutlineLesson[];
}

export interface Outline {
  title: string;
  description?: string;
  modules: OutlineModule[];
}

/**
 * Old drafts store outline modules with `lesson_slugs: string[]` instead of
 * `lessons: OutlineLesson[]`. This converts either format to the canonical one
 * so the rest of the frontend never has to care about the old schema.
 */
function normalizeOutline(
  rawOutline: Record<string, unknown>,
  lessonsDict: Record<string, Record<string, unknown>>,
): Outline {
  const modules = (rawOutline.modules as Array<Record<string, unknown>> || []).map((m) => {
    let lessons: OutlineLesson[];
    if (Array.isArray(m.lessons) && m.lessons.length > 0 && typeof m.lessons[0] === "object") {
      // Already the new format
      lessons = m.lessons as OutlineLesson[];
    } else {
      // Old format: lesson_slugs is a string[]
      const slugs = (m.lesson_slugs as string[] | undefined) || [];
      lessons = slugs.map((slug) => {
        const stored = lessonsDict[slug] || {};
        return {
          slug,
          title: (stored.title as string) || slug,
          summary: (stored.summary as string) || "",
          concepts: (stored.concepts as string[]) || [],
        };
      });
    }
    return { title: m.title as string, lessons };
  });
  return {
    title: rawOutline.title as string || "",
    description: rawOutline.description as string | undefined,
    modules,
  };
}

export type LessonGenStatus = "queued" | "generating" | "done" | "error";

export interface LessonProgress {
  slug: string;
  title: string;
  module?: string;
  status: LessonGenStatus;
  words?: number;
  sources?: number;
  sourceUrls?: string[];
  concepts?: string[];
  images?: number;
  hasKb?: boolean;
  error?: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  pendingActions?: PendingAction[];
}

export interface PendingAction {
  id: string;  // client-generated uid for tracking
  action: string;
  slug?: string;
  label: string;       // human-readable description
  status: "pending" | "approved" | "skipped" | "loading";
}

export type ArtifactView = "outline" | "research" | "enrichment" | "progress" | "lessons" | "publish";

export type CreatorPhase = "shaping" | "researching" | "building" | "reviewing" | "published";

/* ── Coverage / Enrichment types ───────────────────── */

export interface ConceptVerdict {
  verdict: "covered" | "thin" | "missing";
  explanation?: string;
}

export interface LessonAssessment {
  slug: string;
  title: string;
  verdict: "fully_covered" | "needs_research" | "no_match";
  topics: string[];
  conceptVerdicts: Record<string, ConceptVerdict | string>;
  sourceCount: number;
  sources: string[];
  researchTopics?: string[];
  unmapped?: string[];
}

export interface CoverageAssessment {
  lessons: LessonAssessment[];
  summary: { fullyCovered: number; needsResearch: number; noMatch: number };
  assessedAt: string;
}

export interface EnrichmentEvent {
  id: string;
  type: string;
  slug?: string;
  timestamp: number;
  data: Record<string, unknown>;
}

/* ── Hook ───────────────────────────────────────────── */

export function useCreatorState(draftId: string) {
  const [draft, setDraft] = useState<DraftDetailResponse | null>(null);
  const [outline, setOutline] = useState<Outline | null>(null);
  const [coverage, setCoverage] = useState<Record<string, unknown> | null>(null);
  const [lessonProgress, setLessonProgress] = useState<LessonProgress[]>([]);
  const [quality, setQuality] = useState<Record<string, unknown> | null>(null);
  const [activeView, setActiveView] = useState<ArtifactView>("outline");
  const [phase, setPhase] = useState<CreatorPhase>("shaping");
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [chatStreaming, setChatStreaming] = useState(false);
  const [publishedSlug, setPublishedSlug] = useState<string | null>(null);
  const [coverageAssessment, setCoverageAssessment] = useState<CoverageAssessment | null>(null);
  const [assessingCoverage, setAssessingCoverage] = useState(false);
  const [enriching, setEnriching] = useState(false);
  const [enrichmentLog, setEnrichmentLog] = useState<EnrichmentEvent[]>([]);

  const { stream, cancelAll } = useCreatorStream();
  const enrichControllerRef = useRef<AbortController | null>(null);
  const generateControllerRef = useRef<AbortController | null>(null);

  /* ── Load draft from backend ──────────────────────── */

  const loadDraft = useCallback(async () => {
    const token = getToken();
    if (!token) return;
    setLoading(true);
    try {
      const d = await api.courseCreator.getDraft(draftId, token);
      setDraft(d);

      const data = d.data as Record<string, unknown>;
      const lessonsDict = (data.lessons && typeof data.lessons === "object"
        ? data.lessons
        : {}) as Record<string, Record<string, unknown>>;

      if (data.outline) {
        setOutline(normalizeOutline(data.outline as Record<string, unknown>, lessonsDict));
      }

      // Restore coverage assessment if present
      if (data.coverage_assessment) {
        const raw = data.coverage_assessment as Record<string, unknown>;
        const lessons: LessonAssessment[] = [];
        for (const entry of (raw.fully_covered as Array<Record<string, unknown>>) || []) {
          lessons.push({
            slug: entry.slug as string,
            title: entry.title as string,
            verdict: "fully_covered",
            topics: (entry.topics as string[]) || [],
            conceptVerdicts: (entry.concept_verdicts as Record<string, ConceptVerdict | string>) || {},
            sourceCount: (entry.source_count as number) || 0,
            sources: (entry.sources as string[]) || [],
          });
        }
        for (const entry of (raw.needs_research as Array<Record<string, unknown>>) || []) {
          lessons.push({
            slug: entry.slug as string,
            title: entry.title as string,
            verdict: "needs_research",
            topics: (entry.topics as string[]) || [],
            conceptVerdicts: (entry.concept_verdicts as Record<string, ConceptVerdict | string>) || {},
            sourceCount: (entry.source_count as number) || 0,
            sources: (entry.sources as string[]) || [],
            researchTopics: (entry.research_topics as string[]) || [],
          });
        }
        for (const entry of (raw.no_match as Array<Record<string, unknown>>) || []) {
          lessons.push({
            slug: entry.slug as string,
            title: entry.title as string,
            verdict: "no_match",
            topics: [],
            conceptVerdicts: {},
            sourceCount: 0,
            sources: [],
            unmapped: (entry.unmapped as string[]) || [],
          });
        }
        const fc = ((raw.fully_covered as unknown[]) || []).length;
        const nr = ((raw.needs_research as unknown[]) || []).length;
        const nm = ((raw.no_match as unknown[]) || []).length;
        setCoverageAssessment({
          lessons,
          summary: { fullyCovered: fc, needsResearch: nr, noMatch: nm },
          assessedAt: (raw.assessed_at as string) || "",
        });
      }

      // Restore chat history from backend
      const savedChat = data.chat_history as { role: string; content: string }[] | undefined;
      if (savedChat && savedChat.length > 0) {
        setChatMessages(
          savedChat.map((m) => ({
            id: uid(),
            role: m.role as "user" | "assistant",
            content: m.content,
          })),
        );
      }

      // Restore enrichment log from backend
      const savedEnrich = data.enrichment_log as Record<string, unknown>[] | undefined;
      if (savedEnrich && savedEnrich.length > 0) {
        setEnrichmentLog(
          savedEnrich.map((evt) => ({
            id: uid(),
            type: (evt.type as string) || "status",
            slug: evt.slug as string | undefined,
            timestamp: Date.now(),
            data: evt,
          })),
        );
      }

      // Rebuild lessonProgress from stored data (always, regardless of phase)
      if (data.lessons && typeof data.lessons === "object") {
        const lessons = lessonsDict;
        const normalizedOutline = data.outline
          ? normalizeOutline(data.outline as Record<string, unknown>, lessons)
          : null;
        const lessonsWithContent = Object.values(lessons).filter(
          (l) => l.content || l.reference_kb,
        );
        const totalLessons = Object.keys(lessons).length;

        if (normalizedOutline && lessonsWithContent.length > 0) {
          const restored: LessonProgress[] = normalizedOutline.modules.flatMap((m) =>
            m.lessons.map((l) => {
              const stored = lessons[l.slug];
              const hasContent = stored && (stored.content || stored.reference_kb);
              const rawSources = hasContent ? (stored.sources_used as (string | { url: string })[] || []) : [];
              const urls = rawSources.map((s: string | { url: string }) => typeof s === "string" ? s : s.url);
              return {
                slug: l.slug,
                title: l.title,
                module: m.title,
                concepts: l.concepts,
                status: (hasContent ? "done" : "queued") as LessonGenStatus,
                words: hasContent
                  ? (stored.content as string || "").split(/\s+/).length
                  : undefined,
                sources: urls.length || undefined,
                sourceUrls: urls.length > 0 ? urls : undefined,
                hasKb: !!stored?.reference_kb,
              };
            }),
          );
          setLessonProgress(restored);
        }

        // Determine phase and active view
        if (d.phase === "published") {
          setPhase("published");
          setActiveView("publish");
          if (data.published_slug) {
            setPublishedSlug(data.published_slug as string);
          }
        } else if (lessonsWithContent.length === 0 && data.coverage_assessment) {
          setPhase("researching");
          setActiveView("research");
        } else if (lessonsWithContent.length > 0) {
          if (lessonsWithContent.length >= totalLessons) {
            setPhase("reviewing");
            setActiveView("lessons");
          } else {
            setPhase("building");
            setActiveView("progress");
          }
        }
      } else if (d.phase === "published") {
        setPhase("published");
        setActiveView("publish");
        if (data.published_slug) {
          setPublishedSlug(data.published_slug as string);
        }
      }
    } catch (err) {
      console.error("Failed to load draft:", err);
    } finally {
      setLoading(false);
    }
  }, [draftId]);

  /* ── Outline generation (SSE) ────────────────────── */

  const generateOutline = useCallback(() => {
    setGenerating(true);
    setActiveView("outline");

    stream(
      `/course-creator/drafts/${draftId}/generate-outline`,
      {},
      (event: SSEEvent) => {
        if (event.type === "partial_outline") {
          setOutline(event.data as Outline);
        }
        if (event.type === "outline") {
          setOutline(event.data as Outline);
        }
      },
      async () => {
        setGenerating(false);
        const token = getToken();
        if (token) {
          const d = await api.courseCreator.getDraft(draftId, token);
          setDraft(d);
          const data = d.data as Record<string, unknown>;
          if (data.outline) {
            const ld = (data.lessons && typeof data.lessons === "object"
              ? data.lessons
              : {}) as Record<string, Record<string, unknown>>;
            setOutline(normalizeOutline(data.outline as Record<string, unknown>, ld));
          }
        }
      },
      (err) => {
        console.error("Outline generation error:", err);
        setGenerating(false);
      },
    );
  }, [draftId, stream]);

  /* ── Content generation (SSE) ────────────────────── */

  const generateContent = useCallback(
    (resume = false, forceSlugs?: string[]) => {
      if (!outline) return;
      setPhase("building");
      setActiveView("progress");
      setGenerating(true);

      const forceSet = new Set(forceSlugs || []);

      // Initialize progress: keep done lessons (unless force-regenerating them)
      setLessonProgress((prev) => {
        const existing = new Map(prev.map((l) => [l.slug, l]));
        return outline.modules.flatMap((m) =>
          m.lessons.map((l) => {
            if (forceSet.has(l.slug)) {
              return { slug: l.slug, title: l.title, module: m.title, concepts: l.concepts, status: "queued" as LessonGenStatus };
            }
            const ex = existing.get(l.slug);
            if ((resume || forceSet.size > 0) && ex && ex.status === "done") return { ...ex, module: m.title };
            return { slug: l.slug, title: l.title, module: m.title, concepts: l.concepts, status: "queued" as LessonGenStatus };
          }),
        );
      });

      const body: Record<string, unknown> = {};
      if (forceSlugs && forceSlugs.length > 0) {
        body.force_slugs = forceSlugs;
      }

      const qs = (resume || (forceSlugs && forceSlugs.length > 0)) ? "?resume=true" : "";
      const path = `/course-creator/drafts/${draftId}/generate-content${qs}`;

      const controller = stream(
        path,
        body,
        (event: SSEEvent) => {
          if (event.type === "progress") {
            const status = event.status as string;
            const lesson = event.lesson as Record<string, unknown> | undefined;
            const slug = lesson?.slug as string || "";
            const evtTitle = event.lesson_title as string || "";

            if (status === "done" && slug) {
              const rawSources = (lesson?.sources_used as (string | { url: string })[]) || [];
              const urls = rawSources.map((s) => typeof s === "string" ? s : s.url);
              setLessonProgress((prev) =>
                prev.map((l) =>
                  l.slug === slug
                    ? {
                        ...l,
                        status: "done",
                        words: (event.word_count as number) || undefined,
                        sources: urls.length || undefined,
                        sourceUrls: urls.length > 0 ? urls : undefined,
                        concepts: (lesson?.concepts as string[]) || l.concepts,
                        hasKb: (event.has_reference_kb as boolean) || false,
                      }
                    : l,
                ),
              );
            } else if (status === "error") {
              setLessonProgress((prev) =>
                prev.map((l) =>
                  l.title === evtTitle
                    ? { ...l, status: "error", error: (event.error as string) || "Unknown error" }
                    : l,
                ),
              );
            } else if (status === "generating") {
              setLessonProgress((prev) =>
                prev.map((l) =>
                  l.title === evtTitle && l.status === "queued"
                    ? { ...l, status: "generating" }
                    : l,
                ),
              );
            }
          }
        },
        () => {
          setGenerating(false);
          generateControllerRef.current = null;
          setPhase("reviewing");
          setActiveView("lessons");
          loadDraft();
        },
        (err) => {
          console.error("Content generation error:", err);
          setGenerating(false);
          generateControllerRef.current = null;
        },
      );
      generateControllerRef.current = controller;
    },
    [draftId, outline, stream, loadDraft],
  );

  const cancelGeneration = useCallback(() => {
    if (generateControllerRef.current) {
      generateControllerRef.current.abort();
      generateControllerRef.current = null;
    }
    setGenerating(false);
  }, []);

  /* ── Chat (SSE) ──────────────────────────────────── */

  const sendChat = useCallback(
    (message: string) => {
      const userMsg: ChatMessage = { id: uid(), role: "user", content: message };
      setChatMessages((prev) => [...prev, userMsg]);
      setChatStreaming(true);

      const assistantId = uid();
      let assistantText = "";

      setChatMessages((prev) => [
        ...prev,
        { id: assistantId, role: "assistant", content: "" },
      ]);

      const history = chatMessages.map((m) => ({
        role: m.role,
        content: m.content,
      }));

      stream(
        `/course-creator/drafts/${draftId}/chat`,
        { message, history },
        (event: SSEEvent) => {
          if (event.type === "token") {
            assistantText += event.content as string;
            setChatMessages((prev) =>
              prev.map((m) =>
                m.id === assistantId ? { ...m, content: assistantText } : m,
              ),
            );
          } else if (event.type === "draft_actions") {
            const applied = event.auto_applied as Array<Record<string, unknown>> | undefined;
            const pending = event.pending as Array<Record<string, unknown>> | undefined;
            const lines: string[] = [];

            if (applied && applied.length > 0) {
              const successes = applied
                .filter((a) => a.status === "success")
                .map((a) => `✓ ${a.summary as string}`)
                .filter(Boolean);
              const errors = applied
                .filter((a) => a.status === "error")
                .map((a) => `✗ ${a.summary as string}`)
                .filter(Boolean);
              lines.push(...successes, ...errors);
            }

            // Strip raw action JSON blocks from the displayed text
            assistantText = assistantText.replace(/```json\s*\n[\s\S]*?"draft_actions"[\s\S]*?\n```/g, "").trim();
            assistantText = assistantText.replace(/```json\s*\n[\s\S]*?"outline_actions"[\s\S]*?\n```/g, "").trim();

            if (lines.length > 0) {
              const notice = "\n\n---\n" + lines.join("\n");
              assistantText += notice;
            }

            // Build typed pending action cards (rendered inline in ChatPanel)
            const pendingActions: PendingAction[] = (pending || []).map((p) => {
              const action = p.action as string;
              const slug = p.slug as string | undefined;
              let label = action;
              if (action === "regenerate_lesson" && slug) {
                label = `Regenerate lesson: "${slug}"`;
              }
              return { id: uid(), action, slug, label, status: "pending" as const };
            });

            setChatMessages((prev) =>
              prev.map((m) =>
                m.id === assistantId
                  ? { ...m, content: assistantText, pendingActions: pendingActions.length > 0 ? pendingActions : undefined }
                  : m,
              ),
            );
            loadDraft();
          }
        },
        () => setChatStreaming(false),
        (err) => {
          console.error("Chat error:", err);
          setChatMessages((prev) =>
            prev.map((m) =>
              m.id === assistantId
                ? { ...m, content: "Something went wrong. Please try again." }
                : m,
            ),
          );
          setChatStreaming(false);
        },
      );
    },
    [draftId, chatMessages, stream, loadDraft],
  );

  /* ── Coverage ─────────────────────────────────────── */

  const loadCoverage = useCallback(async () => {
    const token = getToken();
    if (!token) return;
    try {
      const cov = await api.courseCreator.getWikiCoverage(draftId, token);
      setCoverage(cov);
    } catch (err) {
      console.error("Failed to load coverage:", err);
    }
  }, [draftId]);

  /* ── Coverage assessment (SSE) ─────────────────────── */

  const assessCoverage = useCallback(() => {
    setAssessingCoverage(true);
    setActiveView("research");
    setPhase("researching");

    const incoming: LessonAssessment[] = [];

    stream(
      `/course-creator/drafts/${draftId}/assess-coverage`,
      {},
      (event: SSEEvent) => {
        if (event.type === "lesson_assessed") {
          const entry: LessonAssessment = {
            slug: event.slug as string,
            title: event.title as string,
            verdict: event.verdict as LessonAssessment["verdict"],
            topics: (event.topics as string[]) || [],
            conceptVerdicts: (event.concept_verdicts as Record<string, ConceptVerdict | string>) || {},
            sourceCount: (event.source_count as number) || 0,
            sources: (event.sources as string[]) || [],
            researchTopics: (event.research_topics as string[]) || [],
            unmapped: (event.unmapped as string[]) || [],
          };
          incoming.push(entry);
          const fc = incoming.filter((l) => l.verdict === "fully_covered").length;
          const nr = incoming.filter((l) => l.verdict === "needs_research").length;
          const nm = incoming.filter((l) => l.verdict === "no_match").length;
          setCoverageAssessment({
            lessons: [...incoming],
            summary: { fullyCovered: fc, needsResearch: nr, noMatch: nm },
            assessedAt: new Date().toISOString(),
          });
        }
      },
      () => {
        setAssessingCoverage(false);
      },
      (err) => {
        console.error("Coverage assessment error:", err);
        setAssessingCoverage(false);
      },
    );
  }, [draftId, stream]);

  /* ── Enrichment (SSE) ────────────────────────────── */

  const enrichCoverage = useCallback((lessonSlugs?: string[]) => {
    setEnriching(true);
    setActiveView("enrichment");

    const body: Record<string, unknown> = {};
    if (lessonSlugs && lessonSlugs.length > 0) {
      body.lesson_slugs = lessonSlugs;
    }

    const controller = stream(
      `/course-creator/drafts/${draftId}/enrich-coverage`,
      body,
      (event: SSEEvent) => {
        const entry: EnrichmentEvent = {
          id: uid(),
          type: event.type as string,
          slug: event.slug as string | undefined,
          timestamp: Date.now(),
          data: event as Record<string, unknown>,
        };
        setEnrichmentLog((prev) => [...prev, entry]);
      },
      () => {
        setEnriching(false);
        enrichControllerRef.current = null;
      },
      (err) => {
        console.error("Enrichment error:", err);
        setEnriching(false);
        enrichControllerRef.current = null;
      },
    );
    enrichControllerRef.current = controller;
  }, [draftId, stream]);

  const cancelEnrichment = useCallback(() => {
    if (enrichControllerRef.current) {
      enrichControllerRef.current.abort();
      enrichControllerRef.current = null;
    }
    setEnriching(false);
  }, []);

  /* ── Promote near-miss source ─────────────────────── */

  const promoteSource = useCallback(
    async (topicSlug: string, url: string, title: string) => {
      const token = getToken();
      if (!token) throw new Error("Not authenticated");
      return api.courseCreator.promoteSource(draftId, topicSlug, url, title, token);
    },
    [draftId],
  );

  /* ── Quality ──────────────────────────────────────── */

  const loadQuality = useCallback(async () => {
    const token = getToken();
    if (!token) return;
    try {
      const q = await api.courseCreator.getQualityGate(draftId, token);
      setQuality(q);
    } catch (err) {
      console.error("Failed to load quality:", err);
    }
  }, [draftId]);

  /* ── Dashboard ───────────────────────────────────── */

  const [dashboard, setDashboard] = useState<Record<string, unknown> | null>(null);

  const loadDashboard = useCallback(async () => {
    const token = getToken();
    if (!token) return;
    try {
      const d = await api.courseCreator.getFinalDashboard(draftId, token);
      setDashboard(d);
    } catch (err) {
      console.error("Failed to load dashboard:", err);
    }
  }, [draftId]);

  /* ── Publish ──────────────────────────────────────── */

  const publish = useCallback(async () => {
    const token = getToken();
    if (!token) return;
    try {
      const result = await api.courseCreator.publish(draftId, token);
      setPhase("published");
      setPublishedSlug((result as { slug?: string }).slug || null);
      return result;
    } catch (err) {
      console.error("Publish failed:", err);
      throw err;
    }
  }, [draftId]);

  /* ── Pending action approval ─────────────────────── */

  const approvePendingAction = useCallback(
    async (messageId: string, actionId: string) => {
      const token = getToken();
      if (!token) return;

      // Find the action details
      let actionPayload: Record<string, unknown> | null = null;
      setChatMessages((prev) =>
        prev.map((m) => {
          if (m.id !== messageId) return m;
          const updated = (m.pendingActions || []).map((a) => {
            if (a.id !== actionId) return a;
            actionPayload = { action: a.action, slug: a.slug };
            return { ...a, status: "loading" as const };
          });
          return { ...m, pendingActions: updated };
        }),
      );

      if (!actionPayload) return;

      try {
        await api.courseCreator.applyChatAction(draftId, actionPayload, token);
        setChatMessages((prev) =>
          prev.map((m) => {
            if (m.id !== messageId) return m;
            const updated = (m.pendingActions || []).map((a) =>
              a.id === actionId ? { ...a, status: "approved" as const } : a,
            );
            return { ...m, pendingActions: updated };
          }),
        );
        loadDraft();
      } catch (err) {
        console.error("Failed to apply action:", err);
        setChatMessages((prev) =>
          prev.map((m) => {
            if (m.id !== messageId) return m;
            const updated = (m.pendingActions || []).map((a) =>
              a.id === actionId ? { ...a, status: "pending" as const } : a,
            );
            return { ...m, pendingActions: updated };
          }),
        );
      }
    },
    [draftId, loadDraft],
  );

  const dismissPendingAction = useCallback(
    (messageId: string, actionId: string) => {
      setChatMessages((prev) =>
        prev.map((m) => {
          if (m.id !== messageId) return m;
          const updated = (m.pendingActions || []).map((a) =>
            a.id === actionId ? { ...a, status: "skipped" as const } : a,
          );
          return { ...m, pendingActions: updated };
        }),
      );
    },
    [],
  );

  /* ── Outline editing ──────────────────────────────── */

  const updateOutline = useCallback(
    async (newOutline: Outline) => {
      setOutline(newOutline);
      const token = getToken();
      if (!token) return;
      try {
        await api.courseCreator.patchDraft(
          draftId,
          { outline: newOutline },
          token,
        );
      } catch (err) {
        console.error("Failed to save outline:", err);
      }
    },
    [draftId],
  );

  return {
    // State
    draft,
    outline,
    coverage,
    lessonProgress,
    quality,
    activeView,
    phase,
    loading,
    generating,
    chatMessages,
    chatStreaming,
    publishedSlug,
    coverageAssessment,
    assessingCoverage,
    enriching,
    enrichmentLog,
    dashboard,

    // Actions
    loadDraft,
    generateOutline,
    generateContent,
    cancelGeneration,
    sendChat,
    approvePendingAction,
    dismissPendingAction,
    loadCoverage,
    assessCoverage,
    enrichCoverage,
    cancelEnrichment,
    promoteSource,
    loadQuality,
    loadDashboard,
    publish,
    updateOutline,
    setActiveView,
    setChatMessages,
    cancelAll,
  };
}
