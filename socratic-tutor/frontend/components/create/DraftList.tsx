"use client";
import { DraftSummaryResponse } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Trash2 } from "lucide-react";

interface DraftListProps {
  drafts: DraftSummaryResponse[];
  onResume: (draftId: string) => void;
  onDelete: (draftId: string) => void;
}

const PHASE_LABELS: Record<string, string> = {
  draft: "Draft",
  outline: "Outline",
  content: "Content",
  research: "Research",
  review: "Review",
  published: "Published",
};

const PHASE_COLORS: Record<string, string> = {
  draft: "bg-muted text-muted-foreground",
  outline: "bg-blue-500/15 text-blue-600",
  content: "bg-amber-500/15 text-amber-600",
  research: "bg-purple-500/15 text-purple-600",
  review: "bg-primary/15 text-primary",
  published: "bg-green-500/15 text-green-600",
};

function timeAgo(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

export function DraftList({ drafts, onResume, onDelete }: DraftListProps) {
  return (
    <div className="space-y-2">
      <h2 className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
        Recent Drafts
      </h2>
      <div className="divide-y divide-border rounded-lg border border-border overflow-hidden">
        {drafts.map((draft) => (
          <div
            key={draft.id}
            className="flex items-center gap-3 px-4 py-2.5 cursor-pointer hover:bg-accent/40 transition-colors group"
            onClick={() => onResume(draft.id)}
          >
            <div className="flex-1 min-w-0">
              <span className="text-sm text-primary hover:underline underline-offset-2 truncate block">
                {draft.title}
              </span>
            </div>
            <span className="text-[11px] text-muted-foreground shrink-0">
              {timeAgo(draft.updated_at)}
            </span>
            <Badge
              variant="secondary"
              className={`text-[10px] shrink-0 ${PHASE_COLORS[draft.phase] || ""}`}
            >
              {PHASE_LABELS[draft.phase] || draft.phase}
            </Badge>
            <button
              className="opacity-0 group-hover:opacity-100 transition-opacity p-1 rounded hover:bg-destructive/10 shrink-0"
              onClick={(e) => {
                e.stopPropagation();
                onDelete(draft.id);
              }}
            >
              <Trash2 className="h-3 w-3 text-muted-foreground hover:text-destructive" />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
