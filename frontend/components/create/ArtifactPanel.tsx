"use client";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { OutlineView } from "./OutlineView";
import { ResearchView } from "./ResearchView";
import { EnrichmentView } from "./EnrichmentView";
import { ProgressView } from "./ProgressView";
import { LessonsView } from "./LessonsView";
import { PublishView } from "./PublishView";
import { List, Search, Zap, Activity, BookOpen, Rocket } from "lucide-react";
import type { useCreatorState } from "@/lib/useCreatorState";
import type { ArtifactView } from "@/lib/useCreatorState";

interface ArtifactPanelProps {
  state: ReturnType<typeof useCreatorState>;
}

const TAB_CONFIG: { value: ArtifactView; label: string; icon: React.ElementType }[] = [
  { value: "outline", label: "Outline", icon: List },
  { value: "research", label: "Research", icon: Search },
  { value: "enrichment", label: "Enrich", icon: Zap },
  { value: "progress", label: "Build", icon: Activity },
  { value: "lessons", label: "Lessons", icon: BookOpen },
  { value: "publish", label: "Publish", icon: Rocket },
];

export function ArtifactPanel({ state }: ArtifactPanelProps) {
  return (
    <div className="flex flex-col h-full min-h-0 bg-background">
      <Tabs
        value={state.activeView}
        onValueChange={(v) => state.setActiveView(v as ArtifactView)}
        className="flex flex-col h-full min-h-0"
      >
        {/* Tab bar */}
        <div className="border-b border-border px-4 shrink-0">
          <TabsList className="h-10 bg-transparent gap-1 p-0">
            {TAB_CONFIG.map(({ value, label, icon: Icon }) => (
              <TabsTrigger
                key={value}
                value={value}
                className="gap-1.5 text-xs data-[state=active]:bg-muted data-[state=active]:shadow-none rounded-md px-3 py-1.5"
              >
                <Icon className="h-3.5 w-3.5" />
                {label}
              </TabsTrigger>
            ))}
          </TabsList>
        </div>

        {/* Tab content — each TabsContent must be a flex container so children
             can size via flex-1 instead of h-full (height:100% doesn't resolve
             against a flex-derived size). */}
        <TabsContent value="outline" className="flex-1 mt-0 min-h-0 overflow-hidden flex flex-col">
          <OutlineView state={state} />
        </TabsContent>
        <TabsContent value="research" className="flex-1 mt-0 min-h-0 overflow-hidden flex flex-col">
          <ResearchView state={state} />
        </TabsContent>
        <TabsContent value="enrichment" className="flex-1 mt-0 min-h-0 overflow-hidden flex flex-col">
          <EnrichmentView state={state} />
        </TabsContent>
        <TabsContent value="progress" className="flex-1 mt-0 min-h-0 overflow-hidden flex flex-col">
          <ProgressView state={state} />
        </TabsContent>
        <TabsContent value="lessons" className="flex-1 mt-0 min-h-0 overflow-hidden flex flex-col">
          <LessonsView state={state} />
        </TabsContent>
        <TabsContent value="publish" className="flex-1 mt-0 min-h-0 overflow-hidden flex flex-col">
          <PublishView state={state} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
