"use client";
import { useState } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import {
  ChevronDown,
  ChevronRight,
  GripVertical,
  ArrowUp,
  ArrowDown,
  Plus,
  Trash2,
  Loader2,
  Play,
  Pencil,
  Check,
  X,
  Search,
} from "lucide-react";
import type { useCreatorState } from "@/lib/useCreatorState";
import type { Outline, OutlineModule, OutlineLesson } from "@/lib/useCreatorState";

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
      <div className="flex flex-col items-center justify-center h-full gap-3 text-muted-foreground">
        <Loader2 className="h-6 w-6 animate-spin" />
        <p className="text-sm">Building your course outline...</p>
        <p className="text-xs text-muted-foreground/60">
          Analyzing wiki sources and structuring lessons
        </p>
      </div>
    );
  }

  if (!outline) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground text-sm">
        No outline yet. Describe what you want to learn in the chat.
      </div>
    );
  }

  const totalLessons = outline.modules.reduce(
    (acc, m) => acc + m.lessons.length,
    0,
  );

  const allSlugs = outline.modules.flatMap((m) => m.lessons.map((l) => l.slug));

  const toggleSlug = (slug: string) => {
    setSelectedSlugs((prev) => {
      const next = new Set(prev);
      if (next.has(slug)) next.delete(slug);
      else next.add(slug);
      return next;
    });
  };

  const toggleSelectAll = () => {
    if (selectedSlugs.size === allSlugs.length) {
      setSelectedSlugs(new Set());
    } else {
      setSelectedSlugs(new Set(allSlugs));
    }
  };

  const enterSelectionMode = () => {
    setSelectedSlugs(new Set(allSlugs));
    setSelectionMode(true);
  };

  const buildSelected = () => {
    const slugs = Array.from(selectedSlugs);
    setSelectionMode(false);
    state.generateContent(false, slugs);
  };

  function handleMoveLesson(
    moduleIdx: number,
    lessonIdx: number,
    direction: "up" | "down",
  ) {
    if (!outline) return;
    const newModules = outline.modules.map((m) => ({
      ...m,
      lessons: [...m.lessons],
    }));
    const mod = newModules[moduleIdx];
    const target = direction === "up" ? lessonIdx - 1 : lessonIdx + 1;
    if (target < 0 || target >= mod.lessons.length) return;
    [mod.lessons[lessonIdx], mod.lessons[target]] = [
      mod.lessons[target],
      mod.lessons[lessonIdx],
    ];
    state.updateOutline({ ...outline, modules: newModules });
  }

  function handleDeleteLesson(moduleIdx: number, lessonIdx: number) {
    if (!outline) return;
    const newModules = outline.modules.map((m, i) =>
      i === moduleIdx
        ? { ...m, lessons: m.lessons.filter((_, j) => j !== lessonIdx) }
        : m,
    );
    state.updateOutline({ ...outline, modules: newModules });
  }

  function handleAddLesson(moduleIdx: number) {
    if (!outline) return;
    const newModules = outline.modules.map((m, i) =>
      i === moduleIdx
        ? {
            ...m,
            lessons: [
              ...m.lessons,
              {
                slug: `new-lesson-${Date.now()}`,
                title: "New Lesson",
                summary: "",
                concepts: [],
              },
            ],
          }
        : m,
    );
    state.updateOutline({ ...outline, modules: newModules });
  }

  return (
    <div className="flex flex-col flex-1 min-h-0">
      <ScrollArea className="flex-1 min-h-0">
        <div className="p-6 space-y-4">
          {/* Header */}
          <div className="space-y-1">
            {editingTitle ? (
              <div className="flex items-center gap-1.5">
                <input
                  value={titleDraft}
                  onChange={(e) => setTitleDraft(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      state.updateOutline({ ...outline, title: titleDraft.trim() || outline.title });
                      setEditingTitle(false);
                    }
                    if (e.key === "Escape") setEditingTitle(false);
                  }}
                  className="flex-1 text-lg font-semibold bg-transparent border-b-2 border-primary focus:outline-none"
                  autoFocus
                />
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-7 w-7 p-0"
                  onClick={() => {
                    state.updateOutline({ ...outline, title: titleDraft.trim() || outline.title });
                    setEditingTitle(false);
                  }}
                >
                  <Check className="h-3.5 w-3.5" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-7 w-7 p-0"
                  onClick={() => setEditingTitle(false)}
                >
                  <X className="h-3.5 w-3.5" />
                </Button>
              </div>
            ) : (
              <h2
                className="text-lg font-semibold cursor-pointer hover:text-primary transition-colors group/title"
                onClick={() => { setTitleDraft(outline.title); setEditingTitle(true); }}
              >
                {outline.title}
                <Pencil className="inline h-3 w-3 ml-1.5 opacity-0 group-hover/title:opacity-60 transition-opacity" />
              </h2>
            )}
            <p className="text-sm text-muted-foreground">
              {outline.modules.length} modules &middot; {totalLessons} lessons
            </p>
            {outline.description && !editingDesc && (
              <p
                className="text-xs text-muted-foreground/80 line-clamp-2 cursor-pointer hover:text-muted-foreground transition-colors group/desc"
                onClick={() => { setDescDraft(outline.description || ""); setEditingDesc(true); }}
                title="Click to edit description"
              >
                {outline.description}
                <Pencil className="inline h-3 w-3 ml-1 opacity-0 group-hover/desc:opacity-60 transition-opacity" />
              </p>
            )}
            {editingDesc && (
              <div className="space-y-1.5">
                <textarea
                  value={descDraft}
                  onChange={(e) => setDescDraft(e.target.value)}
                  rows={3}
                  className="w-full text-xs bg-transparent border border-border rounded-md px-2 py-1.5 focus:outline-none focus:border-primary/40 resize-none"
                  autoFocus
                />
                <div className="flex items-center gap-1">
                  <Button
                    variant="secondary"
                    size="sm"
                    className="h-6 px-2 text-xs gap-1"
                    onClick={() => {
                      state.updateOutline({ ...outline, description: descDraft.trim() });
                      setEditingDesc(false);
                    }}
                  >
                    <Check className="h-3 w-3" /> Save
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="h-6 px-2 text-xs"
                    onClick={() => setEditingDesc(false)}
                  >
                    Cancel
                  </Button>
                </div>
              </div>
            )}
          </div>

          {/* Modules */}
          <div className="space-y-3">
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
                  const newModules = outline.modules.map((m, i) =>
                    i === mi
                      ? {
                          ...m,
                          lessons: m.lessons.map((l, j) =>
                            j === li ? { ...l, ...updates } : l,
                          ),
                        }
                      : m,
                  );
                  state.updateOutline({ ...outline, modules: newModules });
                }}
              />
            ))}
            {generating && (
              <div className="flex items-center gap-2 px-4 py-3 text-muted-foreground">
                <Loader2 className="h-4 w-4 animate-spin" />
                <span className="text-sm">Generating more modules...</span>
              </div>
            )}
          </div>
        </div>
      </ScrollArea>

      {/* Prepare / Build button */}
      {phase !== "published" && outline && (
        <div className="p-4 border-t border-border shrink-0 space-y-3">
          {!state.coverageAssessment && phase === "shaping" ? (
            <Button
              onClick={() => state.assessCoverage()}
              disabled={state.assessingCoverage || totalLessons === 0}
              className="w-full gap-2"
            >
              {state.assessingCoverage ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Assessing Coverage...
                </>
              ) : (
                <>
                  <Search className="h-4 w-4" />
                  Prepare Content ({totalLessons} lessons)
                </>
              )}
            </Button>
          ) : selectionMode ? (
            <>
              <div className="space-y-1 max-h-48 overflow-y-auto rounded-md border border-border p-2">
                <label className="flex items-center gap-2 px-2 py-1 text-xs text-muted-foreground cursor-pointer hover:text-foreground">
                  <input
                    type="checkbox"
                    checked={selectedSlugs.size === allSlugs.length}
                    onChange={toggleSelectAll}
                    className="h-3.5 w-3.5 rounded border-border accent-primary"
                  />
                  {selectedSlugs.size === allSlugs.length ? "Deselect all" : "Select all"}
                </label>
                {outline.modules.flatMap((m) =>
                  m.lessons.map((l) => (
                    <label
                      key={l.slug}
                      className="flex items-center gap-2 px-2 py-1 text-xs cursor-pointer hover:bg-accent/20 rounded"
                    >
                      <input
                        type="checkbox"
                        checked={selectedSlugs.has(l.slug)}
                        onChange={() => toggleSlug(l.slug)}
                        className="h-3.5 w-3.5 rounded border-border accent-primary"
                      />
                      <span className="truncate">{l.title}</span>
                    </label>
                  )),
                )}
              </div>
              <div className="flex items-center gap-2">
                <Button
                  onClick={buildSelected}
                  disabled={selectedSlugs.size === 0 || generating}
                  className="flex-1 gap-2"
                >
                  <Play className="h-4 w-4" />
                  Build {selectedSlugs.size} Lesson{selectedSlugs.size !== 1 ? "s" : ""}
                </Button>
                <Button
                  variant="ghost"
                  onClick={() => setSelectionMode(false)}
                >
                  Cancel
                </Button>
              </div>
            </>
          ) : (
            <div className="flex items-center gap-2">
              <Button
                onClick={() => state.generateContent()}
                disabled={generating || totalLessons === 0 || state.enriching || state.assessingCoverage}
                className="flex-1 gap-2"
              >
                {generating ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Generating...
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4" />
                    Build All ({totalLessons} lessons)
                  </>
                )}
              </Button>
              {totalLessons > 1 && !generating && (
                <Button
                  variant="outline"
                  onClick={enterSelectionMode}
                  disabled={state.enriching || state.assessingCoverage}
                >
                  Select Lessons...
                </Button>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

/* ── Module Card ───────────────────────────────────── */

function ModuleCard({
  module,
  moduleIndex,
  onMoveLesson,
  onDeleteLesson,
  onAddLesson,
  onUpdateLesson,
}: {
  module: OutlineModule;
  moduleIndex: number;
  onMoveLesson: (lessonIdx: number, dir: "up" | "down") => void;
  onDeleteLesson: (lessonIdx: number) => void;
  onAddLesson: () => void;
  onUpdateLesson: (lessonIdx: number, updates: Partial<OutlineLesson>) => void;
}) {
  const [expanded, setExpanded] = useState(true);

  return (
    <Card className="overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-2 w-full px-4 py-3 text-left hover:bg-accent/30 transition-colors"
      >
        {expanded ? (
          <ChevronDown className="h-4 w-4 text-muted-foreground shrink-0" />
        ) : (
          <ChevronRight className="h-4 w-4 text-muted-foreground shrink-0" />
        )}
        <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
          Module {moduleIndex + 1}
        </span>
        <span className="text-sm font-medium flex-1">{module.title}</span>
        <Badge variant="secondary" className="text-xs">
          {module.lessons.length} lessons
        </Badge>
      </button>

      {expanded && (
        <div className="border-t border-border">
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
            className="flex items-center gap-2 w-full px-4 py-2 text-xs text-muted-foreground hover:text-foreground hover:bg-accent/30 transition-colors"
          >
            <Plus className="h-3 w-3" />
            Add lesson
          </button>
        </div>
      )}
    </Card>
  );
}

/* ── Lesson Row ────────────────────────────────────── */

function LessonRow({
  lesson,
  lessonIndex,
  totalLessons,
  onMove,
  onDelete,
  onUpdate,
}: {
  lesson: OutlineLesson;
  lessonIndex: number;
  totalLessons: number;
  onMove: (dir: "up" | "down") => void;
  onDelete: () => void;
  onUpdate: (updates: Partial<OutlineLesson>) => void;
}) {
  const [editing, setEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(lesson.title);

  function saveEdit() {
    if (editTitle.trim()) {
      onUpdate({ title: editTitle.trim() });
    }
    setEditing(false);
  }

  return (
    <div className="flex items-center gap-2 px-4 py-2 border-t border-border/50 group hover:bg-accent/20 transition-colors">
      <GripVertical className="h-3.5 w-3.5 text-muted-foreground/40 shrink-0" />
      <span className="text-xs text-muted-foreground w-5 shrink-0">
        {lessonIndex + 1}
      </span>

      {editing ? (
        <div className="flex-1 flex items-center gap-1">
          <input
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") saveEdit();
              if (e.key === "Escape") setEditing(false);
            }}
            className="flex-1 text-sm bg-transparent border-b border-primary focus:outline-none"
            autoFocus
          />
          <Button variant="ghost" size="sm" className="h-6 w-6 p-0" onClick={saveEdit}>
            <Check className="h-3 w-3" />
          </Button>
          <Button variant="ghost" size="sm" className="h-6 w-6 p-0" onClick={() => setEditing(false)}>
            <X className="h-3 w-3" />
          </Button>
        </div>
      ) : (
        <span
          className="flex-1 text-sm cursor-pointer hover:text-primary transition-colors"
          onClick={() => {
            setEditTitle(lesson.title);
            setEditing(true);
          }}
        >
          {lesson.title}
        </span>
      )}

      {/* Concepts */}
      <div className="hidden lg:flex gap-1 shrink-0">
        {lesson.concepts.slice(0, 3).map((c) => (
          <Badge key={c} variant="secondary" className="text-[10px] px-1.5 py-0">
            {c}
          </Badge>
        ))}
        {lesson.concepts.length > 3 && (
          <Badge variant="secondary" className="text-[10px] px-1.5 py-0">
            +{lesson.concepts.length - 3}
          </Badge>
        )}
      </div>

      {/* Actions */}
      <div className="flex items-center gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity shrink-0">
        <Button
          variant="ghost"
          size="sm"
          className="h-6 w-6 p-0"
          onClick={() => onMove("up")}
          disabled={lessonIndex === 0}
        >
          <ArrowUp className="h-3 w-3" />
        </Button>
        <Button
          variant="ghost"
          size="sm"
          className="h-6 w-6 p-0"
          onClick={() => onMove("down")}
          disabled={lessonIndex === totalLessons - 1}
        >
          <ArrowDown className="h-3 w-3" />
        </Button>
        <Button
          variant="ghost"
          size="sm"
          className="h-6 w-6 p-0"
          onClick={() => {
            setEditTitle(lesson.title);
            setEditing(true);
          }}
        >
          <Pencil className="h-3 w-3" />
        </Button>
        <Button
          variant="ghost"
          size="sm"
          className="h-6 w-6 p-0 text-destructive"
          onClick={onDelete}
        >
          <Trash2 className="h-3 w-3" />
        </Button>
      </div>
    </div>
  );
}
