"use client";
import { useRouter } from "next/navigation";
import { ArrowLeft, ExternalLink } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function WikiPage() {
  const router = useRouter();

  return (
    <div className="flex flex-col h-screen bg-background overflow-hidden">
      {/* Toolbar */}
      <div className="flex items-center gap-3 px-4 py-2 border-b border-border bg-card/60 backdrop-blur-sm flex-shrink-0">
        <Button
          variant="ghost"
          size="sm"
          className="gap-1.5 text-muted-foreground hover:text-foreground"
          onClick={() => router.back()}
        >
          <ArrowLeft className="h-4 w-4" />
          Back
        </Button>
        <div className="h-4 w-px bg-border" />
        <span className="text-sm font-medium">Documentation</span>
        <span className="text-xs text-muted-foreground ml-1">— SAGE Knowledge Base</span>
        <div className="ml-auto">
          <a
            href="https://socratic-tutor-pi.vercel.app"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Button variant="ghost" size="sm" className="gap-1.5 text-muted-foreground hover:text-foreground text-xs">
              <ExternalLink className="h-3.5 w-3.5" />
              Open in new tab
            </Button>
          </a>
        </div>
      </div>

      {/* Embedded wiki */}
      <iframe
        src="https://socratic-tutor-pi.vercel.app"
        className="flex-1 w-full border-0"
        title="SAGE Documentation"
        sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-popups-to-escape-sandbox"
      />
    </div>
  );
}
