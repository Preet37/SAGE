"use client";
import { useEffect, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";
import { useCreatorState } from "@/lib/useCreatorState";
import { CreateCanvas } from "@/components/create/CreateCanvas";
import { Loader2 } from "lucide-react";

export default function CreateWorkspacePage() {
  const params = useParams();
  const router = useRouter();
  const draftId = params.draftId as string;
  const state = useCreatorState(draftId);
  const outlineAttempted = useRef(false);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }
    outlineAttempted.current = false;
    state.loadDraft();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [draftId]);

  // Auto-generate outline once on first load if draft has no outline
  useEffect(() => {
    if (
      !state.loading &&
      state.draft &&
      !state.outline &&
      !state.generating &&
      !outlineAttempted.current
    ) {
      outlineAttempted.current = true;
      state.generateOutline();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [state.loading, state.draft, state.outline]);

  if (state.loading) {
    return (
      <div className="flex items-center justify-center h-screen gap-3 text-muted-foreground">
        <Loader2 className="h-5 w-5 animate-spin" />
        <span>Loading workspace...</span>
      </div>
    );
  }

  if (!state.draft) {
    return (
      <div className="flex items-center justify-center h-screen text-muted-foreground">
        Draft not found.
      </div>
    );
  }

  return <CreateCanvas state={state} />;
}
