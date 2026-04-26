"use client";
import { Panel, Group as PanelGroup, Separator as PanelResizeHandle } from "react-resizable-panels";
import { ChatPanel } from "./ChatPanel";
import { ArtifactPanel } from "./ArtifactPanel";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import type { useCreatorState } from "@/lib/useCreatorState";

const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };
const serif: React.CSSProperties = { fontFamily: "var(--font-cormorant)" };

interface CreateCanvasProps {
  state: ReturnType<typeof useCreatorState>;
}

export function CreateCanvas({ state }: CreateCanvasProps) {
  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh", width: "100vw", overflow: "hidden", background: "var(--ink)" }}>
      {/* Top bar */}
      <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", padding: "0.6rem 1rem", borderBottom: "1px solid rgba(240,233,214,0.08)", background: "var(--ink-1)", flexShrink: 0 }}>
        <Link
          href="/create"
          style={{ display: "flex", alignItems: "center", justifyContent: "center", width: "1.75rem", height: "1.75rem", color: "var(--cream-1)", borderRadius: "4px", transition: "color 0.15s", textDecoration: "none" }}
          onMouseEnter={e => (e.currentTarget.style.color = "var(--cream-0)")}
          onMouseLeave={e => (e.currentTarget.style.color = "var(--cream-1)")}
        >
          <ArrowLeft style={{ width: "0.9rem", height: "0.9rem" }} />
        </Link>
        <div style={{ width: "1px", height: "1rem", background: "rgba(240,233,214,0.1)" }} />
        <h1 style={{ ...serif, fontSize: "1rem", fontStyle: "italic", fontWeight: 600, color: "var(--cream-0)", flex: 1, minWidth: 0, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
          {state.draft?.title || "Untitled Course"}
        </h1>
        <PhaseIndicator phase={state.phase} />
      </div>

      {/* Canvas — two resizable panels */}
      <div style={{ flex: 1, minHeight: 0 }}>
        <PanelGroup orientation="horizontal" style={{ height: "100%" }}>
          <Panel defaultSize={35} minSize={25}>
            <div style={{ height: "100%", overflow: "hidden" }}>
              <ChatPanel state={state} />
            </div>
          </Panel>
          <PanelResizeHandle style={{ width: "1px", background: "rgba(240,233,214,0.08)", cursor: "col-resize", flexShrink: 0 }} />
          <Panel defaultSize={65} minSize={30}>
            <div style={{ height: "100%", overflow: "hidden" }}>
              <ArtifactPanel state={state} />
            </div>
          </Panel>
        </PanelGroup>
      </div>
    </div>
  );
}

const PHASE_CONFIG: Record<string, { label: string; color: string; bg: string }> = {
  shaping:     { label: "Shaping",     color: "var(--gold)",              bg: "rgba(196,152,90,0.12)" },
  researching: { label: "Researching", color: "rgba(146,188,158,0.9)",    bg: "rgba(146,188,158,0.1)" },
  building:    { label: "Building",    color: "rgba(196,152,90,0.8)",     bg: "rgba(196,152,90,0.1)" },
  reviewing:   { label: "Reviewing",   color: "var(--cream-1)",           bg: "rgba(240,233,214,0.08)" },
  published:   { label: "Published",   color: "rgba(146,188,158,0.9)",    bg: "rgba(146,188,158,0.1)" },
};

function PhaseIndicator({ phase }: { phase: string }) {
  const info = PHASE_CONFIG[phase] || PHASE_CONFIG.shaping;
  return (
    <span style={{
      fontFamily: "var(--font-dm-mono)", fontSize: "0.48rem", letterSpacing: "0.12em",
      textTransform: "uppercase", padding: "0.25rem 0.6rem",
      color: info.color, background: info.bg,
      border: `1px solid ${info.color}30`, flexShrink: 0,
    }}>
      {info.label}
    </span>
  );
}
