"use client";
import { useState } from "react";
import { Maximize2, X, Zap } from "lucide-react";

interface VisualPlotRendererProps {
  html: string;
  topic: string;
}

const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };

export function VisualPlotRenderer({ html, topic }: VisualPlotRendererProps) {
  const [fullscreen, setFullscreen] = useState(false);

  const iframe = (
    <iframe
      srcDoc={html}
      sandbox="allow-scripts allow-same-origin"
      style={{ width: "100%", height: "100%", border: "none", display: "block" }}
      title={`Interactive simulation: ${topic}`}
    />
  );

  if (fullscreen) {
    return (
      <div style={{ position: "fixed", inset: 0, zIndex: 50, background: "var(--ink)", display: "flex", flexDirection: "column" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0.4rem 0.75rem", background: "var(--ink-1)", borderBottom: "1px solid rgba(240,233,214,0.08)", flexShrink: 0 }}>
          <div style={{ display: "flex", alignItems: "center", gap: "0.4rem" }}>
            <Zap style={{ width: "0.75rem", height: "0.75rem", color: "var(--gold)" }} />
            <span style={{ ...mono, fontSize: "0.52rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-1)" }}>{topic}</span>
          </div>
          <button
            onClick={() => setFullscreen(false)}
            style={{ display: "flex", alignItems: "center", justifyContent: "center", padding: "0.3rem", background: "transparent", border: "1px solid rgba(240,233,214,0.12)", borderRadius: "3px", cursor: "pointer", color: "var(--cream-2)", transition: "color 0.15s, border-color 0.15s" }}
            onMouseEnter={e => { e.currentTarget.style.color = "var(--cream-0)"; e.currentTarget.style.borderColor = "rgba(240,233,214,0.3)"; }}
            onMouseLeave={e => { e.currentTarget.style.color = "var(--cream-2)"; e.currentTarget.style.borderColor = "rgba(240,233,214,0.12)"; }}
          >
            <X style={{ width: "0.8rem", height: "0.8rem" }} />
          </button>
        </div>
        <div style={{ flex: 1, overflow: "hidden" }}>{iframe}</div>
      </div>
    );
  }

  return (
    <div style={{ borderRadius: "6px", overflow: "hidden", border: "1px solid rgba(240,233,214,0.1)", margin: "0.75rem 0", background: "var(--ink)", height: 520, display: "flex", flexDirection: "column" }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0.4rem 0.75rem", background: "var(--ink-1)", borderBottom: "1px solid rgba(240,233,214,0.08)", flexShrink: 0 }}>
        <div style={{ display: "flex", alignItems: "center", gap: "0.4rem", minWidth: 0 }}>
          <Zap style={{ width: "0.7rem", height: "0.7rem", color: "var(--gold)", flexShrink: 0 }} />
          <span style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-1)" }}>Interactive Simulation</span>
          <span style={{ ...mono, fontSize: "0.48rem", color: "var(--cream-2)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", maxWidth: "12rem" }}>{topic}</span>
        </div>
        <button
          onClick={() => setFullscreen(true)}
          title="Fullscreen"
          style={{ display: "flex", alignItems: "center", justifyContent: "center", padding: "0.25rem", background: "transparent", border: "1px solid rgba(240,233,214,0.1)", borderRadius: "3px", cursor: "pointer", color: "var(--cream-2)", transition: "color 0.15s, border-color 0.15s", flexShrink: 0 }}
          onMouseEnter={e => { e.currentTarget.style.color = "var(--cream-1)"; e.currentTarget.style.borderColor = "rgba(240,233,214,0.25)"; }}
          onMouseLeave={e => { e.currentTarget.style.color = "var(--cream-2)"; e.currentTarget.style.borderColor = "rgba(240,233,214,0.1)"; }}
        >
          <Maximize2 style={{ width: "0.7rem", height: "0.7rem" }} />
        </button>
      </div>
      <div style={{ flex: 1, overflow: "hidden" }}>{iframe}</div>
    </div>
  );
}
