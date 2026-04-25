"use client";
import { useState } from "react";
import { ChevronDown, ChevronRight, BookOpen, ExternalLink, FileText, Image as ImageIcon } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeHighlight from "rehype-highlight";
import "katex/dist/katex.min.css";
import "highlight.js/styles/github.css";
import type { LessonImageMeta } from "@/lib/api";

function normalizeLatexDelimiters(text: string): string {
  return text
    .replace(/\\\[/g, "$$")
    .replace(/\\\]/g, "$$")
    .replace(/\\\(/g, "$")
    .replace(/\\\)/g, "$");
}

interface ReferenceSourcesProps {
  referenceKb: string | null;
  sourcesUsed: string[];
  imageMetadata: LessonImageMeta[];
}

function extractKbSections(kb: string): { title: string; body: string }[] {
  const sections: { title: string; body: string }[] = [];
  const lines = kb.split("\n");
  let currentTitle = "";
  let currentBody: string[] = [];

  for (const line of lines) {
    const heading = line.match(/^##\s+(.+)/);
    if (heading) {
      if (currentTitle) {
        sections.push({ title: currentTitle, body: currentBody.join("\n").trim() });
      }
      currentTitle = heading[1];
      currentBody = [];
    } else if (currentTitle) {
      currentBody.push(line);
    }
  }
  if (currentTitle) {
    sections.push({ title: currentTitle, body: currentBody.join("\n").trim() });
  }
  return sections;
}

function SourceUrl({ url }: { url: string }) {
  let display: string;
  try {
    const u = new URL(url);
    display = u.hostname.replace(/^www\./, "") + (u.pathname.length > 1 ? u.pathname.slice(0, 40) : "");
    if (u.pathname.length > 40) display += "…";
  } catch {
    display = url.slice(0, 50);
  }

  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      className="flex items-center gap-2 px-3 py-2 rounded-lg border border-border hover:bg-muted/50 transition-colors group text-sm"
    >
      <FileText className="h-3.5 w-3.5 text-muted-foreground flex-shrink-0" />
      <span className="text-muted-foreground group-hover:text-foreground truncate">
        {display}
      </span>
      <ExternalLink className="h-3 w-3 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity ml-auto flex-shrink-0" />
    </a>
  );
}

export function ReferenceSources({ referenceKb, sourcesUsed, imageMetadata }: ReferenceSourcesProps) {
  const [expanded, setExpanded] = useState(false);
  const [expandedSection, setExpandedSection] = useState<string | null>(null);

  const hasContent = referenceKb || sourcesUsed.length > 0 || imageMetadata.length > 0;
  if (!hasContent) return null;

  const kbSections = referenceKb ? extractKbSections(referenceKb) : [];

  return (
    <div className="border border-border rounded-xl overflow-hidden bg-card/50">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center gap-2 px-4 py-3 text-sm font-medium text-foreground hover:bg-muted/30 transition-colors"
      >
        {expanded ? (
          <ChevronDown className="h-4 w-4 text-muted-foreground" />
        ) : (
          <ChevronRight className="h-4 w-4 text-muted-foreground" />
        )}
        <BookOpen className="h-4 w-4 text-primary" />
        <span>Reference Sources</span>
        <span className="text-xs text-muted-foreground ml-auto">
          {sourcesUsed.length} sources · {imageMetadata.length} images
        </span>
      </button>

      {expanded && (
        <div className="border-t border-border px-4 py-3 space-y-4">
          {sourcesUsed.length > 0 && (
            <div className="space-y-1.5">
              <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                Sources
              </h4>
              <div className="space-y-1">
                {sourcesUsed.map((url, i) => (
                  <SourceUrl key={i} url={url} />
                ))}
              </div>
            </div>
          )}

          {imageMetadata.length > 0 && (
            <div className="space-y-1.5">
              <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                Educational Images
              </h4>
              <div className="grid grid-cols-2 gap-2">
                {imageMetadata.slice(0, 6).map((img, i) => {
                  const apiBase = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
                  const src = img.file.includes("/images/")
                    ? `${apiBase}/api/wiki-images/${img.file}`
                    : `${apiBase}/api/wiki-images/${img.topic}/images/${img.file}`;
                  return (
                    <div
                      key={i}
                      className="rounded-lg border border-border overflow-hidden bg-white/5"
                    >
                      <img
                        src={src}
                        alt={img.caption || img.description || ""}
                        className="w-full h-24 object-contain p-1"
                        loading="lazy"
                      />
                      {img.caption && (
                        <p className="text-[10px] text-muted-foreground px-2 py-1 border-t border-border truncate">
                          {img.caption}
                        </p>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {kbSections.length > 0 && (
            <div className="space-y-1.5">
              <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                Deep Dive
              </h4>
              <div className="space-y-1">
                {kbSections.map((section) => (
                  <div key={section.title} className="border border-border rounded-lg overflow-hidden">
                    <button
                      onClick={() =>
                        setExpandedSection(
                          expandedSection === section.title ? null : section.title
                        )
                      }
                      className="w-full flex items-center gap-2 px-3 py-2 text-sm text-foreground hover:bg-muted/30 transition-colors"
                    >
                      {expandedSection === section.title ? (
                        <ChevronDown className="h-3.5 w-3.5 text-muted-foreground" />
                      ) : (
                        <ChevronRight className="h-3.5 w-3.5 text-muted-foreground" />
                      )}
                      <span className="truncate">{section.title}</span>
                    </button>
                    {expandedSection === section.title && (
                      <div className="px-3 py-2 border-t border-border max-h-96 overflow-y-auto
                        prose dark:prose-invert prose-sm max-w-none
                        prose-p:text-muted-foreground prose-p:leading-relaxed prose-p:my-1.5
                        prose-headings:text-foreground prose-headings:font-semibold prose-headings:my-2 prose-headings:text-sm
                        prose-code:bg-muted prose-code:rounded prose-code:px-1 prose-code:py-0.5 prose-code:text-xs
                        prose-pre:bg-slate-100 dark:prose-pre:bg-slate-800 prose-pre:rounded-lg prose-pre:p-3 prose-pre:my-2
                        prose-strong:text-foreground
                        prose-a:text-primary
                        prose-li:text-muted-foreground prose-li:my-0.5
                        prose-ul:my-1.5 prose-ol:my-1.5
                        prose-table:text-xs
                        prose-th:bg-muted/50 prose-th:px-2 prose-th:py-1.5
                        prose-td:px-2 prose-td:py-1.5 prose-td:text-muted-foreground
                        prose-blockquote:border-primary/40 prose-blockquote:text-muted-foreground">
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm, remarkMath]}
                          rehypePlugins={[rehypeKatex, rehypeHighlight]}
                        >
                          {normalizeLatexDelimiters(section.body)}
                        </ReactMarkdown>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
