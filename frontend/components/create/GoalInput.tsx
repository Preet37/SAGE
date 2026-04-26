"use client";
import { useState, useRef, useEffect } from "react";
import { ArrowRight, Loader2 } from "lucide-react";

const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };
const body: React.CSSProperties = { fontFamily: "var(--font-crimson)" };

interface GoalInputProps {
  onSubmit: (goal: string) => void;
  loading?: boolean;
}

export function GoalInput({ onSubmit, loading }: GoalInputProps) {
  const [value, setValue] = useState("");
  const [focused, setFocused] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    textareaRef.current?.focus();
  }, []);

  function handleSubmit() {
    const trimmed = value.trim();
    if (!trimmed || loading) return;
    onSubmit(trimmed);
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }

  return (
    <div style={{ position: "relative" }}>
      <div style={{ background: "var(--ink-1)", border: `1px solid ${focused ? "rgba(196,152,90,0.45)" : "rgba(240,233,214,0.12)"}`, overflow: "hidden", transition: "border-color 0.2s" }}>
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          placeholder="e.g. How LLMs work, from tokenization to RLHF…"
          rows={4}
          disabled={loading}
          style={{ width: "100%", resize: "none", background: "transparent", padding: "1.25rem 1.25rem 3.5rem", ...body, fontSize: "1rem", color: "var(--cream-0)", outline: "none", boxSizing: "border-box", lineHeight: 1.6 }}
        />
        <div style={{ position: "absolute", bottom: "0.75rem", right: "0.75rem" }}>
          <button
            onClick={handleSubmit}
            disabled={!value.trim() || loading}
            style={{ ...mono, display: "flex", alignItems: "center", gap: "0.4rem", fontSize: "0.52rem", letterSpacing: "0.12em", textTransform: "uppercase", padding: "0.5rem 0.9rem", background: (!value.trim() || loading) ? "var(--ink-3)" : "var(--gold)", color: (!value.trim() || loading) ? "var(--cream-2)" : "var(--ink)", border: `1px solid ${(!value.trim() || loading) ? "rgba(240,233,214,0.12)" : "transparent"}`, cursor: (!value.trim() || loading) ? "not-allowed" : "pointer", transition: "background 0.2s, color 0.2s" }}
          >
            {loading ? <><Loader2 style={{ width: "0.75rem", height: "0.75rem" }} className="animate-spin" />Creating…</> : <>Build Course <ArrowRight style={{ width: "0.75rem", height: "0.75rem" }} /></>}
          </button>
        </div>
      </div>
      <p style={{ ...mono, fontSize: "0.48rem", letterSpacing: "0.1em", color: "var(--cream-2)", marginTop: "0.6rem", textAlign: "center", textTransform: "uppercase" }}>
        Press Enter to submit · Shift+Enter for new line
      </p>
    </div>
  );
}
