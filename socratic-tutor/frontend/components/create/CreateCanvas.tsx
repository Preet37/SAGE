"use client";
import { Panel, Group as PanelGroup, Separator as PanelResizeHandle } from "react-resizable-panels";
import { ChatPanel } from "./ChatPanel";
import { ArtifactPanel } from "./ArtifactPanel";
import { Button } from "@/components/ui/button";
import { ArrowLeft, GripVertical } from "lucide-react";
import Link from "next/link";
import type { useCreatorState } from "@/lib/useCreatorState";

interface CreateCanvasProps {
  state: ReturnType<typeof useCreatorState>;
}

export function CreateCanvas({ state }: CreateCanvasProps) {
  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden">
      {/* Top bar */}
      <div className="flex items-center gap-3 px-4 py-2.5 border-b border-border bg-card/50 shrink-0">
        <Button variant="ghost" size="sm" className="h-8 w-8 p-0" asChild>
          <Link href="/create">
            <ArrowLeft className="h-4 w-4" />
          </Link>
        </Button>
        <div className="h-4 w-px bg-border" />
        <h1 className="text-sm font-medium truncate flex-1 min-w-0">
          {state.draft?.title || "Untitled Course"}
        </h1>
        <PhaseIndicator phase={state.phase} />
      </div>

      {/* Canvas — two resizable panels */}
      <div className="flex-1 min-h-0">
        <PanelGroup orientation="horizontal" style={{ height: "100%" }}>
          <Panel defaultSize={35} minSize={25}>
            <div className="h-full overflow-hidden">
              <ChatPanel state={state} />
            </div>
          </Panel>
          <PanelResizeHandle className="w-2 bg-border hover:bg-primary/30 active:bg-primary/50 transition-colors flex items-center justify-center group cursor-col-resize">
            <GripVertical className="h-4 w-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
          </PanelResizeHandle>
          <Panel defaultSize={65} minSize={30}>
            <div className="h-full overflow-hidden">
              <ArtifactPanel state={state} />
            </div>
          </Panel>
        </PanelGroup>
      </div>
    </div>
  );
}

function PhaseIndicator({ phase }: { phase: string }) {
  const labels: Record<string, { label: string; color: string }> = {
    shaping: { label: "Shaping", color: "bg-blue-500/15 text-blue-400" },
    researching: { label: "Researching", color: "bg-purple-500/15 text-purple-400" },
    building: { label: "Building", color: "bg-amber-500/15 text-amber-400" },
    reviewing: { label: "Reviewing", color: "bg-primary/15 text-primary" },
    published: { label: "Published", color: "bg-green-500/15 text-green-400" },
  };
  const info = labels[phase] || labels.shaping;
  return (
    <span className={`ml-auto text-xs font-medium px-2.5 py-1 rounded-full ${info.color}`}>
      {info.label}
    </span>
  );
}
