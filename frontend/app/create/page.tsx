"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, DraftSummaryResponse } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { GoalInput } from "@/components/create/GoalInput";
import { DraftList } from "@/components/create/DraftList";
import { Sparkles } from "lucide-react";
import { AppHeader } from "@/components/AppHeader";

const mono: React.CSSProperties  = { fontFamily: "var(--font-dm-mono)" };
const serif: React.CSSProperties = { fontFamily: "var(--font-cormorant)" };
const body: React.CSSProperties  = { fontFamily: "var(--font-crimson)" };

export default function CreateLandingPage() {
  const router = useRouter();
  const [drafts, setDrafts] = useState<DraftSummaryResponse[]>([]);
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    const token = getToken();
    if (!token) return;
    // Silently show empty state if API unavailable
    api.courseCreator.listDrafts(token).then(setDrafts).catch(() => {});
  }, []);

  async function handleCreate(goal: string) {
    const token = getToken(); if (!token) return;
    setCreating(true);
    try { const draft = await api.courseCreator.createDraft(goal, goal, token); router.push(`/create/${draft.id}`); }
    catch { setCreating(false); }
  }

  function handleResume(draftId: string) { router.push(`/create/${draftId}`); }

  async function handleDelete(draftId: string) {
    const draft = drafts.find((d) => d.id === draftId);
    if (!window.confirm(`Delete "${draft?.title || "this draft"}"?`)) return;
    const token = getToken(); if (!token) return;
    try { await api.courseCreator.deleteDraft(draftId, token); setDrafts((prev) => prev.filter((d) => d.id !== draftId)); } catch {}
  }

  return (
    <div className="flex flex-col min-h-screen" style={{ background: "var(--ink)", color: "var(--cream-0)" }}>
      <AppHeader leftSlot={
        <div style={{ display: "flex", alignItems: "center", gap: "0.4rem" }}>
          <Sparkles style={{ width: "0.85rem", height: "0.85rem", color: "var(--gold)" }} />
          <span style={{ ...mono, fontSize: "0.55rem", letterSpacing: "0.13em", textTransform: "uppercase", color: "var(--cream-1)" }}>Create</span>
        </div>
      } />

      <div style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", padding: "3.5rem 1.5rem" }}>
        <div style={{ width: "100%", maxWidth: "38rem" }}>
          {/* Hero */}
          <div style={{ textAlign: "center", marginBottom: "3rem" }}>
            <div style={{ display: "inline-flex", alignItems: "center", gap: "0.4rem", ...mono, fontSize: "0.52rem", letterSpacing: "0.14em", textTransform: "uppercase", color: "var(--gold)", border: "1px solid rgba(196,152,90,0.3)", padding: "0.3rem 0.75rem", marginBottom: "1.25rem" }}>
              <Sparkles style={{ width: "0.7rem", height: "0.7rem" }} /> AI-Powered Course Builder
            </div>
            <h1 style={{ ...serif, fontWeight: 700, fontStyle: "italic", fontSize: "clamp(2rem,5vw,3rem)", color: "var(--cream-0)", lineHeight: 1.1, marginBottom: "0.6rem" }}>
              What do you want to learn<span style={{ color: "var(--gold)" }}>?</span>
            </h1>
            <p style={{ ...body, fontSize: "1.05rem", color: "var(--cream-1)", lineHeight: 1.7 }}>
              Describe a topic and we'll build a structured course from our curated knowledge base.
            </p>
          </div>

          <GoalInput onSubmit={handleCreate} loading={creating} />

          {drafts.length > 0 && (
            <div style={{ marginTop: "3rem" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", marginBottom: "1.25rem" }}>
                <div style={{ height: "1px", width: "1.5rem", background: "var(--gold)" }} />
                <span style={{ ...mono, fontSize: "0.55rem", letterSpacing: "0.15em", textTransform: "uppercase", color: "var(--cream-2)" }}>Recent Drafts</span>
                <div style={{ flex: 1, height: "1px", background: "rgba(240,233,214,0.07)" }} />
              </div>
              <DraftList drafts={drafts} onResume={handleResume} onDelete={handleDelete} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
