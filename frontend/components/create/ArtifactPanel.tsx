"use client";
import { OutlineView } from "./OutlineView";
import { ResearchView } from "./ResearchView";
import { EnrichmentView } from "./EnrichmentView";
import { ProgressView } from "./ProgressView";
import { LessonsView } from "./LessonsView";
import { PublishView } from "./PublishView";
import { List, Search, Zap, Activity, BookOpen, Rocket } from "lucide-react";
import type { useCreatorState } from "@/lib/useCreatorState";
import type { ArtifactView } from "@/lib/useCreatorState";

const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };

interface ArtifactPanelProps {
  state: ReturnType<typeof useCreatorState>;
}

const TAB_CONFIG: { value: ArtifactView; label: string; icon: React.ComponentType<React.SVGProps<SVGSVGElement>> }[] = [
  { value: "outline",    label: "Outline",  icon: List },
  { value: "research",   label: "Research", icon: Search },
  { value: "enrichment", label: "Enrich",   icon: Zap },
  { value: "progress",   label: "Build",    icon: Activity },
  { value: "lessons",    label: "Lessons",  icon: BookOpen },
  { value: "publish",    label: "Publish",  icon: Rocket },
];

export function ArtifactPanel({ state }: ArtifactPanelProps) {
  const active = state.activeView;

  return (
    <div className="dark" style={{ display: "flex", flexDirection: "column", height: "100%", minHeight: 0, background: "var(--ink)" }}>
      {/* Tab bar */}
      <div style={{ display: "flex", alignItems: "center", gap: "0", padding: "0 1rem", borderBottom: "1px solid rgba(240,233,214,0.08)", flexShrink: 0, background: "var(--ink-1)" }}>
        {TAB_CONFIG.map(({ value, label, icon: Icon }) => {
          const isActive = active === value;
          return (
            <button
              key={value}
              onClick={() => state.setActiveView(value)}
              style={{
                display: "flex", alignItems: "center", gap: "0.35rem",
                padding: "0.65rem 0.75rem",
                ...mono, fontSize: "0.48rem", letterSpacing: "0.1em", textTransform: "uppercase",
                color: isActive ? "var(--cream-0)" : "var(--cream-2)",
                background: "transparent",
                border: "none",
                borderBottom: isActive ? "1px solid var(--gold)" : "1px solid transparent",
                marginBottom: "-1px",
                cursor: "pointer",
                transition: "color 0.15s",
              }}
              onMouseEnter={e => { if (!isActive) e.currentTarget.style.color = "var(--cream-1)"; }}
              onMouseLeave={e => { if (!isActive) e.currentTarget.style.color = "var(--cream-2)"; }}
            >
              <Icon style={{ width: "0.7rem", height: "0.7rem" }} />
              {label}
            </button>
          );
        })}
      </div>

      {/* Active content */}
      <div style={{ flex: 1, minHeight: 0, overflow: "hidden", display: "flex", flexDirection: "column" }}>
        {active === "outline"    && <OutlineView    state={state} />}
        {active === "research"   && <ResearchView   state={state} />}
        {active === "enrichment" && <EnrichmentView state={state} />}
        {active === "progress"   && <ProgressView   state={state} />}
        {active === "lessons"    && <LessonsView    state={state} />}
        {active === "publish"    && <PublishView     state={state} />}
      </div>
    </div>
  );
}
