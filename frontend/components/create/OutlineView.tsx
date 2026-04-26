"use client";
import { useState } from "react";
import {
  ChevronDown, ChevronRight, GripVertical, ArrowUp, ArrowDown,
  Plus, Trash2, Loader2, Play, Pencil, Check, X, Search,
} from "lucide-react";
import type { useCreatorState } from "@/lib/useCreatorState";
import type { Outline, OutlineModule, OutlineLesson } from "@/lib/useCreatorState";

const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };
const serif: React.CSSProperties = { fontFamily: "var(--font-cormorant)" };
const body: React.CSSProperties = { fontFamily: "var(--font-crimson)" };

interface OutlineViewProps {
  state: ReturnType<typeof useCreatorState>;
}

export function OutlineView({ state }: OutlineViewProps) {
  const { outline, generating, phase } = state;
  const [selectionMode, setSelectionMode] = useState(false);
  const [selectedSlugs, setSelectedSlugs] = useState<Set<string>>(new Set());
  const [editingTitle, setEditingTitle] = useState(false);
  const [titleDraft, setTitleDraft] = useState("");
  const [editingDesc, setEditingDesc] = useState(false);
  const [descDraft, setDescDraft] = useState("");

  if (!outline && generating) {
    return (
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100%", gap: "0.75rem", color: "var(--cream-2)" }}>
        <Loader2 style={{ width: "1.5rem", height: "1.5rem" }} className="animate-spin" />
        <p style={{ ...body, fontSize: "0.95rem" }}>Building your course outline…</p>
        <p style={{ ...mono, fontSize: "0.45rem", letterSpacing: "0.1em", opacity: 0.6 }}>Analysing wiki sources and structuring lessons</p>
      </div>
    );
  }

  if (!outline) {
    return (
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "100%", color: "var(--cream-2)", ...body, fontSize: "0.95rem" }}>
        No outline yet. Describe what you want to learn in the chat.
      </div>
    );
  }

  const totalLessons = outline.modules.reduce((acc, m) => acc + m.lessons.length, 0);
  const allSlugs = outline.modules.flatMap((m) => m.lessons.map((l) => l.slug));

  const toggleSlug = (slug: string) => {
    setSelectedSlugs((prev) => {
      const next = new Set(prev);
      if (next.has(slug)) next.delete(slug); else next.add(slug);
      return next;
    });
  };

  const toggleSelectAll = () => {
    setSelectedSlugs(selectedSlugs.size === allSlugs.length ? new Set() : new Set(allSlugs));
  };

  const enterSelectionMode = () => { setSelectedSlugs(new Set(allSlugs)); setSelectionMode(true); };
  const buildSelected = () => { const slugs = Array.from(selectedSlugs); setSelectionMode(false); state.generateContent(false, slugs); };

  function handleMoveLesson(moduleIdx: number, lessonIdx: number, direction: "up" | "down") {
    if (!outline) return;
    const newModules = outline.modules.map((m) => ({ ...m, lessons: [...m.lessons] }));
    const mod = newModules[moduleIdx];
    const target = direction === "up" ? lessonIdx - 1 : lessonIdx + 1;
    if (target < 0 || target >= mod.lessons.length) return;
    [mod.lessons[lessonIdx], mod.lessons[target]] = [mod.lessons[target], mod.lessons[lessonIdx]];
    state.updateOutline({ ...outline, modules: newModules });
  }

  function handleDeleteLesson(moduleIdx: number, lessonIdx: number) {
    if (!outline) return;
    state.updateOutline({ ...outline, modules: outline.modules.map((m, i) => i === moduleIdx ? { ...m, lessons: m.lessons.filter((_, j) => j !== lessonIdx) } : m) });
  }

  function handleAddLesson(moduleIdx: number) {
    if (!outline) return;
    state.updateOutline({ ...outline, modules: outline.modules.map((m, i) => i === moduleIdx ? { ...m, lessons: [...m.lessons, { slug: `new-lesson-${Date.now()}`, title: "New Lesson", summary: "", concepts: [] }] } : m) });
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", flex: 1, minHeight: 0 }}>
      <div style={{ flex: 1, minHeight: 0, overflowY: "auto", padding: "1.5rem" }}>
        {/* Header */}
        <div style={{ marginBottom: "1.25rem" }}>
          {editingTitle ? (
            <div style={{ display: "flex", alignItems: "center", gap: "0.4rem" }}>
              <input
                value={titleDraft}
                onChange={(e) => setTitleDraft(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") { state.updateOutline({ ...outline, title: titleDraft.trim() || outline.title }); setEditingTitle(false); }
                  if (e.key === "Escape") setEditingTitle(false);
                }}
                style={{ flex: 1, ...serif, fontSize: "1.2rem", fontStyle: "italic", fontWeight: 600, background: "transparent", borderBottom: "1px solid var(--gold)", color: "var(--cream-0)", outline: "none" }}
                autoFocus
              />
              <IconBtn onClick={() => { state.updateOutline({ ...outline, title: titleDraft.trim() || outline.title }); setEditingTitle(false); }}><Check style={{ width: "0.75rem", height: "0.75rem" }} /></IconBtn>
              <IconBtn onClick={() => setEditingTitle(false)}><X style={{ width: "0.75rem", height: "0.75rem" }} /></IconBtn>
            </div>
          ) : (
            <h2
              style={{ ...serif, fontSize: "1.2rem", fontStyle: "italic", fontWeight: 600, color: "var(--cream-0)", cursor: "pointer", display: "flex", alignItems: "center", gap: "0.4rem" }}
              onClick={() => { setTitleDraft(outline.title); setEditingTitle(true); }}
            >
              {outline.title}
              <Pencil style={{ width: "0.65rem", height: "0.65rem", opacity: 0.4 }} />
            </h2>
          )}
          <p style={{ ...mono, fontSize: "0.45rem", letterSpacing: "0.1em", color: "var(--cream-2)", marginTop: "0.3rem" }}>
            {outline.modules.length} modules · {totalLessons} lessons
          </p>
          {outline.description && !editingDesc && (
            <p
              style={{ ...body, fontSize: "0.875rem", color: "var(--cream-2)", marginTop: "0.4rem", cursor: "pointer", display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical", overflow: "hidden" }}
              onClick={() => { setDescDraft(outline.description || ""); setEditingDesc(true); }}
            >
              {outline.description}
            </p>
          )}
          {editingDesc && (
            <div style={{ marginTop: "0.5rem", display: "flex", flexDirection: "column", gap: "0.4rem" }}>
              <textarea
                value={descDraft}
                onChange={(e) => setDescDraft(e.target.value)}
                rows={3}
                style={{ ...body, fontSize: "0.875rem", background: "var(--ink-2)", border: "1px solid rgba(240,233,214,0.12)", color: "var(--cream-0)", padding: "0.5rem", outline: "none", resize: "none", width: "100%", boxSizing: "border-box" }}
                autoFocus
              />
              <div style={{ display: "flex", gap: "0.4rem" }}>
                <GoldBtn onClick={() => { state.updateOutline({ ...outline, description: descDraft.trim() }); setEditingDesc(false); }}>Save</GoldBtn>
                <GhostBtn onClick={() => setEditingDesc(false)}>Cancel</GhostBtn>
              </div>
            </div>
          )}
        </div>

        {/* Modules */}
        <div style={{ display: "flex", flexDirection: "column", gap: "0.625rem" }}>
          {outline.modules.map((mod, mi) => (
            <ModuleCard
              key={mi}
              module={mod}
              moduleIndex={mi}
              onMoveLesson={(li, dir) => handleMoveLesson(mi, li, dir)}
              onDeleteLesson={(li) => handleDeleteLesson(mi, li)}
              onAddLesson={() => handleAddLesson(mi)}
              onUpdateLesson={(li, updates) => {
                if (!outline) return;
                state.updateOutline({ ...outline, modules: outline.modules.map((m, i) => i === mi ? { ...m, lessons: m.lessons.map((l, j) => j === li ? { ...l, ...updates } : l) } : m) });
              }}
            />
          ))}
          {generating && (
            <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", padding: "0.75rem 1rem", color: "var(--cream-2)", ...body, fontSize: "0.9rem" }}>
              <Loader2 style={{ width: "0.85rem", height: "0.85rem" }} className="animate-spin" />
              Generating more modules…
            </div>
          )}
        </div>
      </div>

      {/* Footer actions */}
      {phase !== "published" && outline && (
        <div style={{ padding: "0.875rem 1rem", borderTop: "1px solid rgba(240,233,214,0.08)", flexShrink: 0, display: "flex", flexDirection: "column", gap: "0.6rem" }}>
          {!state.coverageAssessment && phase === "shaping" ? (
            <GoldBtn
              onClick={() => state.assessCoverage()}
              disabled={state.assessingCoverage || totalLessons === 0}
              wide
            >
              {state.assessingCoverage ? <><Loader2 style={{ width: "0.75rem", height: "0.75rem" }} className="animate-spin" /> Assessing Coverage…</> : <><Search style={{ width: "0.75rem", height: "0.75rem" }} /> Prepare Content ({totalLessons} lessons)</>}
            </GoldBtn>
          ) : selectionMode ? (
            <>
              <div style={{ border: "1px solid rgba(240,233,214,0.1)", background: "var(--ink-2)", padding: "0.4rem", maxHeight: "10rem", overflowY: "auto" }}>
                <label style={{ display: "flex", alignItems: "center", gap: "0.5rem", padding: "0.3rem 0.5rem", ...mono, fontSize: "0.45rem", letterSpacing: "0.08em", color: "var(--cream-2)", cursor: "pointer" }}>
                  <input type="checkbox" checked={selectedSlugs.size === allSlugs.length} onChange={toggleSelectAll} style={{ accentColor: "var(--gold)" }} />
                  {selectedSlugs.size === allSlugs.length ? "Deselect all" : "Select all"}
                </label>
                {outline.modules.flatMap((m) => m.lessons.map((l) => (
                  <label key={l.slug} style={{ display: "flex", alignItems: "center", gap: "0.5rem", padding: "0.3rem 0.5rem", ...body, fontSize: "0.85rem", color: "var(--cream-1)", cursor: "pointer" }}>
                    <input type="checkbox" checked={selectedSlugs.has(l.slug)} onChange={() => toggleSlug(l.slug)} style={{ accentColor: "var(--gold)" }} />
                    <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{l.title}</span>
                  </label>
                )))}
              </div>
              <div style={{ display: "flex", gap: "0.5rem" }}>
                <GoldBtn onClick={buildSelected} disabled={selectedSlugs.size === 0 || generating} wide>
                  <Play style={{ width: "0.75rem", height: "0.75rem" }} /> Build {selectedSlugs.size} Lesson{selectedSlugs.size !== 1 ? "s" : ""}
                </GoldBtn>
                <GhostBtn onClick={() => setSelectionMode(false)}>Cancel</GhostBtn>
              </div>
            </>
          ) : (
            <div style={{ display: "flex", gap: "0.5rem" }}>
              <GoldBtn
                onClick={() => state.generateContent()}
                disabled={generating || totalLessons === 0 || state.enriching || state.assessingCoverage}
                wide
              >
                {generating ? <><Loader2 style={{ width: "0.75rem", height: "0.75rem" }} className="animate-spin" /> Generating…</> : <><Play style={{ width: "0.75rem", height: "0.75rem" }} /> Build All ({totalLessons} lessons)</>}
              </GoldBtn>
              {totalLessons > 1 && !generating && (
                <OutlineBtn onClick={enterSelectionMode} disabled={state.enriching || state.assessingCoverage}>Select…</OutlineBtn>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

/* ── Shared primitive buttons ─────────────────────── */

function GoldBtn({ onClick, disabled, wide, children }: { onClick?: () => void; disabled?: boolean; wide?: boolean; children: React.ReactNode }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        display: "flex", alignItems: "center", justifyContent: "center", gap: "0.4rem",
        ...(wide ? { flex: 1 } : {}),
        padding: "0.5rem 0.875rem",
        fontFamily: "var(--font-dm-mono)", fontSize: "0.48rem", letterSpacing: "0.1em", textTransform: "uppercase",
        background: disabled ? "var(--ink-3)" : "var(--gold)",
        color: disabled ? "var(--cream-2)" : "var(--ink)",
        border: "none", cursor: disabled ? "not-allowed" : "pointer", transition: "background 0.15s",
      }}
    >
      {children}
    </button>
  );
}

function GhostBtn({ onClick, children }: { onClick?: () => void; children: React.ReactNode }) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: "0.5rem 0.75rem",
        fontFamily: "var(--font-dm-mono)", fontSize: "0.48rem", letterSpacing: "0.1em", textTransform: "uppercase",
        background: "transparent", color: "var(--cream-2)",
        border: "1px solid rgba(240,233,214,0.12)", cursor: "pointer", transition: "color 0.15s",
      }}
      onMouseEnter={e => (e.currentTarget.style.color = "var(--cream-1)")}
      onMouseLeave={e => (e.currentTarget.style.color = "var(--cream-2)")}
    >
      {children}
    </button>
  );
}

function OutlineBtn({ onClick, disabled, children }: { onClick?: () => void; disabled?: boolean; children: React.ReactNode }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        padding: "0.5rem 0.75rem",
        fontFamily: "var(--font-dm-mono)", fontSize: "0.48rem", letterSpacing: "0.1em", textTransform: "uppercase",
        background: "transparent", color: disabled ? "var(--cream-2)" : "var(--cream-1)",
        border: "1px solid rgba(240,233,214,0.15)", cursor: disabled ? "not-allowed" : "pointer",
      }}
    >
      {children}
    </button>
  );
}

function IconBtn({ onClick, children }: { onClick?: () => void; children: React.ReactNode }) {
  return (
    <button
      onClick={onClick}
      style={{ display: "flex", alignItems: "center", justifyContent: "center", width: "1.5rem", height: "1.5rem", background: "transparent", border: "1px solid rgba(240,233,214,0.1)", color: "var(--cream-2)", cursor: "pointer" }}
    >
      {children}
    </button>
  );
}

/* ── Module Card ───────────────────────────────────── */

function ModuleCard({ module, moduleIndex, onMoveLesson, onDeleteLesson, onAddLesson, onUpdateLesson }: {
  module: OutlineModule; moduleIndex: number;
  onMoveLesson: (li: number, dir: "up" | "down") => void;
  onDeleteLesson: (li: number) => void;
  onAddLesson: () => void;
  onUpdateLesson: (li: number, updates: Partial<OutlineLesson>) => void;
}) {
  const [expanded, setExpanded] = useState(true);

  return (
    <div style={{ border: "1px solid rgba(240,233,214,0.08)", background: "var(--ink-1)", overflow: "hidden" }}>
      <button
        onClick={() => setExpanded(!expanded)}
        style={{ display: "flex", alignItems: "center", gap: "0.5rem", width: "100%", padding: "0.65rem 0.875rem", background: "transparent", border: "none", cursor: "pointer", textAlign: "left" }}
      >
        {expanded
          ? <ChevronDown style={{ width: "0.85rem", height: "0.85rem", color: "var(--cream-2)", flexShrink: 0 }} />
          : <ChevronRight style={{ width: "0.85rem", height: "0.85rem", color: "var(--cream-2)", flexShrink: 0 }} />}
        <span style={{ ...mono, fontSize: "0.42rem", letterSpacing: "0.12em", textTransform: "uppercase", color: "var(--cream-2)" }}>
          Module {moduleIndex + 1}
        </span>
        <span style={{ ...body, fontSize: "0.9rem", color: "var(--cream-0)", flex: 1 }}>{module.title}</span>
        <span style={{ ...mono, fontSize: "0.42rem", letterSpacing: "0.08em", color: "var(--cream-2)", background: "var(--ink-2)", padding: "0.15rem 0.4rem", border: "1px solid rgba(240,233,214,0.08)", flexShrink: 0 }}>
          {module.lessons.length}
        </span>
      </button>

      {expanded && (
        <div style={{ borderTop: "1px solid rgba(240,233,214,0.08)" }}>
          {module.lessons.map((lesson, li) => (
            <LessonRow
              key={lesson.slug}
              lesson={lesson}
              lessonIndex={li}
              totalLessons={module.lessons.length}
              onMove={(dir) => onMoveLesson(li, dir)}
              onDelete={() => onDeleteLesson(li)}
              onUpdate={(updates) => onUpdateLesson(li, updates)}
            />
          ))}
          <button
            onClick={onAddLesson}
            style={{ display: "flex", alignItems: "center", gap: "0.4rem", width: "100%", padding: "0.5rem 0.875rem", background: "transparent", border: "none", borderTop: "1px solid rgba(240,233,214,0.05)", ...mono, fontSize: "0.42rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)", cursor: "pointer" }}
            onMouseEnter={e => (e.currentTarget.style.color = "var(--cream-1)")}
            onMouseLeave={e => (e.currentTarget.style.color = "var(--cream-2)")}
          >
            <Plus style={{ width: "0.65rem", height: "0.65rem" }} />
            Add lesson
          </button>
        </div>
      )}
    </div>
  );
}

/* ── Lesson Row ────────────────────────────────────── */

function LessonRow({ lesson, lessonIndex, totalLessons, onMove, onDelete, onUpdate }: {
  lesson: OutlineLesson; lessonIndex: number; totalLessons: number;
  onMove: (dir: "up" | "down") => void;
  onDelete: () => void;
  onUpdate: (updates: Partial<OutlineLesson>) => void;
}) {
  const [editing, setEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(lesson.title);
  const [hovered, setHovered] = useState(false);

  function saveEdit() { if (editTitle.trim()) onUpdate({ title: editTitle.trim() }); setEditing(false); }

  return (
    <div
      style={{ display: "flex", alignItems: "center", gap: "0.4rem", padding: "0.45rem 0.875rem", borderTop: "1px solid rgba(240,233,214,0.05)", background: hovered ? "var(--ink-2)" : "transparent", transition: "background 0.1s" }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <GripVertical style={{ width: "0.7rem", height: "0.7rem", color: "var(--cream-2)", opacity: 0.4, flexShrink: 0 }} />
      <span style={{ ...mono, fontSize: "0.42rem", color: "var(--cream-2)", width: "1rem", flexShrink: 0 }}>{lessonIndex + 1}</span>

      {editing ? (
        <div style={{ flex: 1, display: "flex", alignItems: "center", gap: "0.3rem" }}>
          <input
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter") saveEdit(); if (e.key === "Escape") setEditing(false); }}
            style={{ flex: 1, ...body, fontSize: "0.875rem", background: "transparent", borderBottom: "1px solid var(--gold)", color: "var(--cream-0)", outline: "none" }}
            autoFocus
          />
          <IconBtn onClick={saveEdit}><Check style={{ width: "0.6rem", height: "0.6rem" }} /></IconBtn>
          <IconBtn onClick={() => setEditing(false)}><X style={{ width: "0.6rem", height: "0.6rem" }} /></IconBtn>
        </div>
      ) : (
        <span
          style={{ flex: 1, ...body, fontSize: "0.875rem", color: "var(--cream-0)", cursor: "pointer" }}
          onClick={() => { setEditTitle(lesson.title); setEditing(true); }}
        >
          {lesson.title}
        </span>
      )}

      {/* Concept tags */}
      {lesson.concepts.slice(0, 3).map((c) => (
        <span key={c} style={{ ...mono, fontSize: "0.38rem", letterSpacing: "0.06em", color: "var(--cream-2)", background: "var(--ink-3)", padding: "0.1rem 0.35rem", border: "1px solid rgba(240,233,214,0.07)", flexShrink: 0 }}>
          {c}
        </span>
      ))}
      {lesson.concepts.length > 3 && (
        <span style={{ ...mono, fontSize: "0.38rem", letterSpacing: "0.06em", color: "var(--cream-2)", background: "var(--ink-3)", padding: "0.1rem 0.35rem", border: "1px solid rgba(240,233,214,0.07)" }}>
          +{lesson.concepts.length - 3}
        </span>
      )}

      {/* Row actions */}
      <div style={{ display: "flex", alignItems: "center", gap: "0.15rem", opacity: hovered ? 1 : 0, transition: "opacity 0.15s", flexShrink: 0 }}>
        {[
          { icon: ArrowUp, action: () => onMove("up"), disabled: lessonIndex === 0 },
          { icon: ArrowDown, action: () => onMove("down"), disabled: lessonIndex === totalLessons - 1 },
          { icon: Pencil, action: () => { setEditTitle(lesson.title); setEditing(true); }, disabled: false },
          { icon: Trash2, action: onDelete, disabled: false, danger: true },
        ].map(({ icon: Icon, action, disabled, danger }, i) => (
          <button
            key={i}
            onClick={action}
            disabled={disabled}
            style={{ display: "flex", alignItems: "center", justifyContent: "center", width: "1.25rem", height: "1.25rem", background: "transparent", border: "none", color: danger ? "rgba(188,106,90,0.7)" : "var(--cream-2)", cursor: disabled ? "not-allowed" : "pointer", opacity: disabled ? 0.3 : 1 }}
          >
            <Icon style={{ width: "0.65rem", height: "0.65rem" }} />
          </button>
        ))}
      </div>
    </div>
  );
}
