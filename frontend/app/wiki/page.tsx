"use client";
import { useRouter } from "next/navigation";
import { ArrowLeft, ExternalLink } from "lucide-react";

const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };

export default function WikiPage() {
  const router = useRouter();

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh", background: "var(--ink)", overflow: "hidden" }}>
      <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", padding: "0.5rem 1rem", borderBottom: "1px solid rgba(240,233,214,0.07)", background: "var(--ink-1)", flexShrink: 0 }}>
        <button
          onClick={() => router.back()}
          style={{ ...mono, display: "flex", alignItems: "center", gap: "0.35rem", fontSize: "0.52rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)", background: "none", border: "none", cursor: "pointer", padding: "0.3rem 0" }}
        >
          <ArrowLeft style={{ width: "0.8rem", height: "0.8rem" }} />
          Back
        </button>
        <div style={{ width: "1px", height: "1rem", background: "rgba(240,233,214,0.12)" }} />
        <span style={{ ...mono, fontSize: "0.55rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-0)" }}>Documentation</span>
        <span style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.08em", color: "var(--cream-2)" }}>— SAGE Knowledge Base</span>
        <div style={{ marginLeft: "auto" }}>
          <a
            href="https://socratic-tutor-pi.vercel.app"
            target="_blank"
            rel="noopener noreferrer"
            style={{ ...mono, display: "flex", alignItems: "center", gap: "0.35rem", fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)", textDecoration: "none" }}
          >
            <ExternalLink style={{ width: "0.75rem", height: "0.75rem" }} />
            Open in new tab
          </a>
        </div>
      </div>

      <iframe
        src="https://socratic-tutor-pi.vercel.app"
        style={{ flex: 1, width: "100%", border: "none" }}
        title="SAGE Documentation"
        sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-popups-to-escape-sandbox"
      />
    </div>
  );
}
