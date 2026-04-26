"use client";
import { memo, useState, useCallback } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeHighlight from "rehype-highlight";
import "katex/dist/katex.min.css";
import "highlight.js/styles/github-dark.css";
import { InlineQuiz } from "./InlineQuiz";
import { MermaidBlock } from "./MermaidBlock";
import { AnimatedFlowBlock } from "./AnimatedFlowBlock";
import { ArchitectureBlock } from "./ArchitectureBlock";
import { VisualPlotRenderer } from "@/components/visual/VisualPlotRenderer";
import { CodeRunner, getCodeLang } from "@/components/tutor/CodeRunner";
import { parseFlowDiagram } from "@/lib/schemas/flow";
import { parseArchitectureDiagram } from "@/lib/schemas/architecture";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Loader2, Play, ExternalLink, BookOpen, ImageIcon, ZoomIn, X, BarChart2, Microscope, ShieldCheck, ShieldAlert, ShieldQuestion } from "lucide-react";
import { useRouter } from "next/navigation";
import type { Verification } from "@/lib/useTutorStream";

interface MessageBubbleProps {
  role: "user" | "assistant";
  content: string;
  isStreaming?: boolean;
  onSendMessage?: (msg: string) => void;
  verification?: Verification;
  lessonTitle?: string;
}

type BlockPart =
  | { type: "text"; content: string }
  | { type: "quiz"; content: string }
  | { type: "flow"; content: string }
  | { type: "architecture"; content: string }
  | { type: "resource"; content: string }
  | { type: "image"; content: string };

function parseStructuredBlocks(content: string): BlockPart[] {
  const parts: BlockPart[] = [];
  const blockRegex = /<(quiz|flow|architecture|resource|image)>([\s\S]*?)<\/\1>/g;
  let lastIndex = 0;
  let match;

  while ((match = blockRegex.exec(content)) !== null) {
    if (match.index > lastIndex) {
      parts.push({ type: "text", content: content.slice(lastIndex, match.index) });
    }
    parts.push({ type: match[1] as "quiz" | "flow" | "architecture" | "resource" | "image", content: match[2].trim() });
    lastIndex = match.index + match[0].length;
  }
  if (lastIndex < content.length) {
    parts.push({ type: "text", content: content.slice(lastIndex) });
  }
  return parts;
}

const remarkPlugins = [remarkGfm, remarkMath];
const rehypePlugins = [rehypeKatex, rehypeHighlight];

function normalizeLatexDelimiters(text: string): string {
  return text
    .replace(/\\\[/g, "$$")
    .replace(/\\\]/g, "$$")
    .replace(/\\\(/g, "$")
    .replace(/\\\)/g, "$");
}

function ResourceRecommendation({
  data,
  onSendMessage,
}: {
  data: { type?: string; title?: string; youtube_id?: string; educator?: string; why?: string; url?: string };
  onSendMessage?: (msg: string) => void;
}) {
  const isVideo = data.type === "video";
  // Prefer an explicit URL; for videos fall back to a YouTube search (never embed a hallucinated ID)
  const resolvedUrl =
    data.url ||
    (isVideo && data.title
      ? `https://www.youtube.com/results?search_query=${encodeURIComponent(
          [data.title, data.educator].filter(Boolean).join(" ")
        )}`
      : null);

  return (
    <div className="rounded-xl border border-border bg-card/60 overflow-hidden my-2">
      <div className="flex gap-3 p-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-1.5 text-xs text-muted-foreground mb-1">
            {isVideo ? <Play className="h-3 w-3" /> : <BookOpen className="h-3 w-3" />}
            <span>{isVideo ? "Video" : "Article"}</span>
            {data.educator && (
              <>
                <span className="mx-1">·</span>
                <span className="font-medium text-foreground">{data.educator}</span>
              </>
            )}
          </div>
          {resolvedUrl ? (
            <a
              href={resolvedUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm font-medium text-foreground leading-snug hover:text-primary transition-colors inline-flex items-center gap-1"
            >
              {data.title} <ExternalLink className="h-3 w-3 flex-shrink-0 opacity-50" />
            </a>
          ) : (
            <p className="text-sm font-medium text-foreground leading-snug">{data.title}</p>
          )}
          {data.why && (
            <p className="text-xs text-muted-foreground mt-1">{data.why}</p>
          )}
          <div className="flex gap-2 mt-2">
            {resolvedUrl && (
              <a
                href={resolvedUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs px-3 py-1 rounded-md bg-primary text-primary-foreground font-medium hover:bg-primary/90 transition-colors inline-flex items-center gap-1"
              >
                {isVideo ? "Search on YouTube" : "Read"} <ExternalLink className="h-3 w-3" />
              </a>
            )}
            {onSendMessage && (
              <button
                onClick={() =>
                  onSendMessage(`Summarize "${data.title}" for me instead`)
                }
                className="text-xs px-3 py-1 rounded-md border border-border text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
              >
                Skip — tell me what it says
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function resolveImageUrl(path: string): string {
  if (path.startsWith("/api/")) {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    return `${apiBase}${path}`;
  }
  return path;
}

function ImageCard({
  data,
}: {
  data: { path?: string; caption?: string; description?: string };
}) {
  const [expanded, setExpanded] = useState(false);

  if (!data.path) return null;
  const imgSrc = resolveImageUrl(data.path);

  return (
    <>
      <figure className="my-3 not-prose">
        <div
          className="relative group cursor-pointer rounded-xl border border-border overflow-hidden bg-card/60"
          onClick={() => setExpanded(true)}
        >
          <img
            src={imgSrc}
            alt={data.caption || "Educational diagram"}
            className="w-full max-h-96 object-contain p-3 bg-white dark:bg-white/5"
            loading="lazy"
          />
          <div className="absolute inset-0 bg-black/0 group-hover:bg-black/5 dark:group-hover:bg-black/10 transition-colors flex items-center justify-center">
            <ZoomIn className="h-6 w-6 text-white opacity-0 group-hover:opacity-70 transition-opacity drop-shadow-lg" />
          </div>
        </div>
        {(data.caption || data.description) && (
          <figcaption className="mt-2 px-1 space-y-0.5">
            {data.caption && (
              <p className="text-sm font-medium text-foreground/90 leading-snug">
                {data.caption}
              </p>
            )}
            {data.description && (
              <p className="text-xs text-muted-foreground leading-relaxed">
                {data.description}
              </p>
            )}
          </figcaption>
        )}
      </figure>

      {expanded && (
        <div
          className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4"
          onClick={() => setExpanded(false)}
        >
          <button
            onClick={() => setExpanded(false)}
            className="absolute top-4 right-4 text-white/70 hover:text-white transition-colors"
          >
            <X className="h-6 w-6" />
          </button>
          <img
            src={imgSrc}
            alt={data.caption || "Educational diagram"}
            className="max-w-[90vw] max-h-[90vh] object-contain rounded-lg"
            onClick={(e) => e.stopPropagation()}
          />
        </div>
      )}
    </>
  );
}

function VerificationChip({ v }: { v: Verification }) {
  const [open, setOpen] = useState(false);
  const config =
    v.label === "grounded"
      ? { Icon: ShieldCheck, cls: "text-emerald-700 bg-emerald-50 border-emerald-200 dark:text-emerald-300 dark:bg-emerald-950/40 dark:border-emerald-900", text: "Grounded" }
      : v.label === "partial"
        ? { Icon: ShieldQuestion, cls: "text-amber-700 bg-amber-50 border-amber-200 dark:text-amber-300 dark:bg-amber-950/40 dark:border-amber-900", text: "Partially grounded" }
        : { Icon: ShieldAlert, cls: "text-rose-700 bg-rose-50 border-rose-200 dark:text-rose-300 dark:bg-rose-950/40 dark:border-rose-900", text: "Unverified" };
  const pct = Math.round((v.score ?? 0) * 100);
  return (
    <div className="mt-2">
      <button
        type="button"
        onClick={() => setOpen((s) => !s)}
        className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-[11px] font-medium transition hover:opacity-90 ${config.cls}`}
        title="Click for verification details"
      >
        <config.Icon className="h-3 w-3" />
        <span>{config.text}</span>
        <span className="opacity-70">· {pct}%</span>
      </button>
      {open && (
        <div className="mt-2 rounded-lg border border-border bg-muted/40 p-3 text-xs space-y-2">
          {v.rationale && <div className="text-foreground/90">{v.rationale}</div>}
          {v.grounded_claims.length > 0 && (
            <div>
              <div className="font-semibold text-emerald-700 dark:text-emerald-300 mb-1">Supported by lesson:</div>
              <ul className="list-disc list-inside text-foreground/80 space-y-0.5">
                {v.grounded_claims.map((c, i) => <li key={i}>{c}</li>)}
              </ul>
            </div>
          )}
          {v.unsupported_claims.length > 0 && (
            <div>
              <div className="font-semibold text-amber-700 dark:text-amber-300 mb-1">Not found in lesson material:</div>
              <ul className="list-disc list-inside text-foreground/80 space-y-0.5">
                {v.unsupported_claims.map((c, i) => <li key={i}>{c}</li>)}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function MessageBubbleInner({ role, content, isStreaming, onSendMessage, verification, lessonTitle }: MessageBubbleProps) {
  const router = useRouter();
  const [plotHtml, setPlotHtml] = useState<string | null>(null);
  const [plotTopic, setPlotTopic] = useState<string>("");
  const [plotLoading, setPlotLoading] = useState(false);
  const [plotError, setPlotError] = useState<string | null>(null);

  const handleVisualize = useCallback(async () => {
    const token = getToken();
    if (!token) return;
    setPlotLoading(true);
    setPlotError(null);
    try {
      const topic = lessonTitle || content.slice(0, 120);
      const result = await api.visual.generatePlot(topic, content.slice(0, 1500), token);
      if (result.error) {
        setPlotError(result.error);
      } else if (result.html) {
        setPlotHtml(result.html);
        setPlotTopic(result.topic || topic);
      }
    } catch (e) {
      console.error("Plot generation failed:", e);
      setPlotError("Failed to generate visualization. Please try again.");
    } finally {
      setPlotLoading(false);
    }
  }, [content, lessonTitle]);

  if (role === "user") {
    return (
      <div className="flex justify-end">
        <div style={{ maxWidth: "75%", background: "var(--ink-3)", border: "1px solid rgba(196,152,90,0.2)", padding: "0.65rem 1rem", fontFamily: "var(--font-crimson)", fontSize: "0.95rem", color: "var(--cream-0)", lineHeight: 1.6, whiteSpace: "pre-wrap" }}>
          {content}
        </div>
      </div>
    );
  }

  const parts = parseStructuredBlocks(content);

  return (
    <div className="max-w-none">
      <div className="space-y-1">
        {parts.map((part, i) => {
          if (part.type === "quiz") {
            try {
              const data = JSON.parse(part.content);
              return <InlineQuiz key={i} data={data} onSendMessage={onSendMessage} />;
            } catch {
              return null;
            }
          }

          if (part.type === "flow") {
            if (isStreaming) {
              return (
                <div
                  key={i}
                  className="flex items-center gap-2 text-sm text-muted-foreground py-3 px-4 bg-muted/30 rounded-lg border border-border my-2"
                >
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>Building diagram...</span>
                </div>
              );
            }
            const diagram = parseFlowDiagram(part.content);
            if (!diagram) return null;
            return <AnimatedFlowBlock key={i} diagram={diagram} />;
          }

          if (part.type === "resource") {
            try {
              const data = JSON.parse(part.content);
              return <ResourceRecommendation key={i} data={data} onSendMessage={onSendMessage} />;
            } catch {
              return null;
            }
          }

          if (part.type === "image") {
            try {
              const data = JSON.parse(part.content);
              return <ImageCard key={i} data={data} />;
            } catch {
              return null;
            }
          }

          if (part.type === "architecture") {
            if (isStreaming) {
              return (
                <div
                  key={i}
                  className="flex items-center gap-2 text-sm text-muted-foreground py-3 px-4 bg-muted/30 rounded-lg border border-border my-2"
                >
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>Building architecture diagram...</span>
                </div>
              );
            }
            const arch = parseArchitectureDiagram(part.content);
            if (!arch) return null;
            return <ArchitectureBlock key={i} diagram={arch} />;
          }

          return (
            <div
              key={i}
              className="prose prose-invert prose-sm max-w-none
                prose-p:my-2 prose-p:leading-[1.75]
                prose-headings:font-semibold prose-headings:mt-4 prose-headings:mb-2
                prose-strong:font-semibold
                prose-a:no-underline hover:prose-a:underline
                prose-li:my-0.5 prose-li:leading-[1.75]
                prose-ul:my-2 prose-ol:my-2
                prose-table:text-sm prose-table:rounded-lg prose-table:overflow-hidden
                prose-th:px-3 prose-th:py-2 prose-th:text-left prose-th:font-semibold
                prose-td:px-3 prose-td:py-2"
              style={{ fontFamily: "var(--font-crimson)", fontSize: "0.95rem", color: "rgba(210,208,220,0.88)" }}
            >
              <ReactMarkdown
                remarkPlugins={remarkPlugins}
                rehypePlugins={rehypePlugins}
                components={{
                  img({ src, alt }) {
                    if (!src) return null;
                    const resolved = resolveImageUrl(src as string);
                    return <img src={resolved} alt={alt || ""} className="rounded-xl max-h-80 object-contain my-3" loading="lazy" />;
                  },
                  pre({ node, children, ...props }) {
                    // Check if this is a runnable code block
                    if (node && node.children) {
                      for (const child of node.children) {
                        if (
                          child.type === "element" &&
                          child.tagName === "code"
                        ) {
                          const classes = Array.isArray(child.properties?.className)
                            ? child.properties.className
                            : [];

                          // Mermaid diagrams
                          if (classes.some((c: string | number) => typeof c === "string" && c.includes("mermaid"))) {
                            // eslint-disable-next-line @typescript-eslint/no-explicit-any
                            function extractText(nodes: any[]): string {
                              return nodes.map((n) => {
                                if ("value" in n) return n.value as string;
                                if ("children" in n) return extractText(n.children);
                                return "";
                              }).join("");
                            }
                            const text = extractText(child.children);
                            if (isStreaming) {
                              return <pre className="text-xs text-muted-foreground opacity-60"><code>{text.trim()}</code></pre>;
                            }
                            return <MermaidBlock code={text.trim()} />;
                          }

                          // Runnable code blocks
                          const langConfig = getCodeLang(classes as (string | number)[]);
                          if (langConfig && !isStreaming) {
                            // eslint-disable-next-line @typescript-eslint/no-explicit-any
                            function extractCode(nodes: any[]): string {
                              return nodes.map((n) => {
                                if ("value" in n) return n.value as string;
                                if ("children" in n) return extractCode(n.children);
                                return "";
                              }).join("");
                            }
                            const code = extractCode(child.children).trimEnd();
                            return <CodeRunner key={code.slice(0, 20)} code={code} langConfig={langConfig} />;
                          }                        }
                      }
                    }
                    return <pre {...props}>{children}</pre>;
                  },
                }}
              >
                {normalizeLatexDelimiters(part.content)}
              </ReactMarkdown>
            </div>
          );
        })}
      </div>
      {verification && !isStreaming && <VerificationChip v={verification} />}

      {/* Action buttons — only for non-streaming assistant messages */}
      {!isStreaming && content.length > 80 && (
        <div className="mt-3 flex items-center gap-2 flex-wrap">
          {plotHtml ? (
            <button
              onClick={() => { setPlotHtml(null); setPlotError(null); }}
              style={{ display: "inline-flex", alignItems: "center", gap: "0.375rem", fontFamily: "var(--font-dm-mono)", fontSize: "0.6rem", letterSpacing: "0.1em", textTransform: "uppercase", padding: "0.375rem 0.75rem", border: "1px solid rgba(240,233,214,0.12)", color: "var(--cream-2)", background: "none", cursor: "pointer", transition: "border-color 0.15s, color 0.15s" }}
              onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(240,233,214,0.25)"; (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-1)"; }}
              onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(240,233,214,0.12)"; (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-2)"; }}
            >
              <X style={{ width: "0.7rem", height: "0.7rem" }} /> Close Plot
            </button>
          ) : (
            <button
              onClick={handleVisualize}
              disabled={plotLoading}
              style={{ display: "inline-flex", alignItems: "center", gap: "0.375rem", fontFamily: "var(--font-dm-mono)", fontSize: "0.6rem", letterSpacing: "0.1em", textTransform: "uppercase", padding: "0.375rem 0.75rem", border: "1px solid rgba(196,152,90,0.3)", color: "var(--gold)", background: "rgba(196,152,90,0.06)", cursor: "pointer", transition: "border-color 0.15s, background 0.15s", opacity: plotLoading ? 0.5 : 1 }}
              onMouseEnter={e => { if (!plotLoading) { (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(196,152,90,0.55)"; (e.currentTarget as HTMLButtonElement).style.background = "rgba(196,152,90,0.12)"; } }}
              onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(196,152,90,0.3)"; (e.currentTarget as HTMLButtonElement).style.background = "rgba(196,152,90,0.06)"; }}
            >
              {plotLoading ? (
                <><Loader2 style={{ width: "0.7rem", height: "0.7rem", animation: "spin 1s linear infinite" }} /> Generating...</>
              ) : (
                <><BarChart2 style={{ width: "0.7rem", height: "0.7rem" }} /> Plot Interactive Graph</>
              )}
            </button>
          )}
          <button
            onClick={() => {
              const topic = lessonTitle || content.slice(0, 60).replace(/\n/g, " ").trim();
              router.push(`/explore?q=${encodeURIComponent(topic)}`);
            }}
            style={{ display: "inline-flex", alignItems: "center", gap: "0.375rem", fontFamily: "var(--font-dm-mono)", fontSize: "0.6rem", letterSpacing: "0.1em", textTransform: "uppercase", padding: "0.375rem 0.75rem", border: "1px solid rgba(240,233,214,0.12)", color: "var(--cream-2)", background: "none", cursor: "pointer", transition: "border-color 0.15s, color 0.15s" }}
            onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(240,233,214,0.25)"; (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-1)"; }}
            onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(240,233,214,0.12)"; (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-2)"; }}
          >
            <Microscope style={{ width: "0.7rem", height: "0.7rem" }} /> Deep Dive
          </button>
        </div>
      )}

      {/* Rendered plot */}
      {plotHtml && <VisualPlotRenderer html={plotHtml} topic={plotTopic} />}

      {/* Plot generation error */}
      {plotError && !plotHtml && (
        <div style={{ marginTop: "0.75rem", background: "var(--ink-2)", border: "1px solid rgba(196,90,90,0.25)", padding: "0.75rem 1rem", fontFamily: "var(--font-crimson)", fontSize: "0.88rem", color: "var(--rose)" }}>
          {plotError}
        </div>
      )}
    </div>
  );
}

export const MessageBubble = memo(MessageBubbleInner);
