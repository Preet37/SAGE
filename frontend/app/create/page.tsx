"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, DraftSummaryResponse } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { GoalInput } from "@/components/create/GoalInput";
import { DraftList } from "@/components/create/DraftList";
import { Sparkles } from "lucide-react";
import { AppHeader } from "@/components/AppHeader";

export default function CreateLandingPage() {
  const router = useRouter();
  const [drafts, setDrafts] = useState<DraftSummaryResponse[]>([]);
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    const token = getToken();
    if (!token) return;
    api.courseCreator.listDrafts(token).then(setDrafts).catch(() => {
      // Token may be expired — redirect to login
      router.push("/login");
    });
  }, [router]);

  async function handleCreate(goal: string) {
    const token = getToken();
    if (!token) return;
    setCreating(true);
    try {
      const draft = await api.courseCreator.createDraft(goal, goal, token);
      router.push(`/create/${draft.id}`);
    } catch (err) {
      console.error("Failed to create draft:", err);
      setCreating(false);
    }
  }

  function handleResume(draftId: string) {
    router.push(`/create/${draftId}`);
  }

  async function handleDelete(draftId: string) {
    const draft = drafts.find((d) => d.id === draftId);
    const title = draft?.title || "this draft";
    if (!window.confirm(`Delete "${title}"? This cannot be undone.`)) return;

    const token = getToken();
    if (!token) return;
    try {
      await api.courseCreator.deleteDraft(draftId, token);
      setDrafts((prev) => prev.filter((d) => d.id !== draftId));
    } catch (err) {
      console.error("Failed to delete draft:", err);
    }
  }

  return (
    <div className="flex flex-col min-h-screen bg-background">
      <AppHeader
        leftSlot={
          <>
            <Sparkles className="h-5 w-5 text-primary" />
            <span className="font-semibold text-sm">Create</span>
          </>
        }
      />

      <div className="flex flex-col items-center flex-1 px-4 py-12">
      <div className="w-full max-w-2xl space-y-12">
        {/* Hero */}
        <div className="text-center space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-primary/10 text-primary text-sm font-medium">
            <Sparkles className="h-4 w-4" />
            AI-Powered Course Builder
          </div>
          <h1 className="text-4xl font-bold tracking-tight">
            What do you want to learn?
          </h1>
          <p className="text-muted-foreground text-lg max-w-md mx-auto">
            Describe a topic and we&apos;ll build a structured course from our
            curated knowledge base.
          </p>
        </div>

        {/* Goal Input */}
        <GoalInput onSubmit={handleCreate} loading={creating} />

        {/* Recent Drafts */}
        {drafts.length > 0 && (
          <DraftList
            drafts={drafts}
            onResume={handleResume}
            onDelete={handleDelete}
          />
        )}
      </div>
      </div>
    </div>
  );
}
