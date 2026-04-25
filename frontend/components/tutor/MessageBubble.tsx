"use client";
import { memo, useState, useCallback } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeHighlight from "rehype-highlight";
import "katex/dist/katex.min.css";
import "highlight.js/styles/github.css";
import { InlineQuiz } from "./InlineQuiz";
import { MermaidBlock } from "./MermaidBlock";
import { AnimatedFlowBlock } from "./AnimatedFlowBlock";
import { ArchitectureBlock } from "./ArchitectureBlock";
import { VisualPlotRenderer } from "@/components/visual/VisualPlotRenderer";
import { parseFlowDiagram } from "@/lib/schemas/flow";
import { parseArchitectureDiagram } from "@/lib/schemas/architecture";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Loader2, Play, ExternalLink, BookOpen, ImageIcon, ZoomIn, X, BarChart2 } from "lucide-react";

interface MessageBubbleProps {
  role: "user" | "assistant";
  content: string;
  isStreaming?: boolean;
  onSendMessage?: (msg: string) => void;
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
  const [expanded, setExpanded] = useState(false);
  const isVideo = !!(data.type === "video" && data.youtube_id);
  const resolvedUrl =
    data.url ||
    (data.youtube_id ? `https://www.youtube.com/watch?v=${data.youtube_id}` : null);
  const thumbnail = isVideo
    ? `https://img.youtube.com/vi/${data.youtube_id}/mqdefault.jpg`
    : null;

  return (
    <div className="rounded-xl border border-border bg-card/60 overflow-hidden my-2">
      <div className="flex gap-3 p-3">
        {thumbnail && !expanded && (
          <img
            src={thumbnail}
            alt=""
            className="w-32 h-20 rounded-lg object-cover flex-shrink-0 cursor-pointer"
            onClick={() => setExpanded(true)}
          />
        )}
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
            {isVideo && !expanded && (
              <button
                onClick={() => setExpanded(true)}
                className="text-xs px-3 py-1 rounded-md bg-primary text-primary-foreground font-medium hover:bg-primary/90 transition-colors"
              >
                Watch inline
              </button>
            )}
            {isVideo && resolvedUrl && (
              <a
                href={resolvedUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs px-3 py-1 rounded-md border border-border text-muted-foreground hover:text-foreground hover:bg-muted transition-colors inline-flex items-center gap-1"
              >
                Open on YouTube <ExternalLink className="h-3 w-3" />
              </a>
            )}
            {!isVideo && resolvedUrl && (
              <a
                href={resolvedUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs px-3 py-1 rounded-md bg-primary text-primary-foreground font-medium hover:bg-primary/90 transition-colors inline-flex items-center gap-1"
              >
                Read <ExternalLink className="h-3 w-3" />
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
      {expanded && isVideo && (
        <div className="aspect-video w-full">
          <iframe
            src={`https://www.youtube.com/embed/${data.youtube_id}`}
            title={data.title || "Video"}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            className="w-full h-full"
          />
        </div>
      )}
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

function MessageBubbleInner({ role, content, isStreaming, onSendMessage, lessonTitle }: MessageBubbleProps) {
  const [plotHtml, setPlotHtml] = useState<string | null>(null);
  const [plotTopic, setPlotTopic] = useState<string>("");
  const [plotLoading, setPlotLoading] = useState(false);

  const handleVisualize = useCallback(async () => {
    const token = getToken();
    if (!token) return;
    setPlotLoading(true);
    try {
      const topic = lessonTitle || content.slice(0, 120);
      const result = await api.visual.generatePlot(topic, content.slice(0, 1500), token);
      if (result.html) {
        setPlotHtml(result.html);
        setPlotTopic(result.topic || topic);
      }
    } catch (e) {
      console.error("Plot generation failed:", e);
    } finally {
      setPlotLoading(false);
    }
  }, [content, lessonTitle]);

  if (role === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-[75%] rounded-2xl rounded-tr-sm bg-primary text-primary-foreground px-5 py-3 text-sm leading-relaxed whitespace-pre-wrap">
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
              className="text-sm
                prose dark:prose-invert prose-sm max-w-none
                prose-p:my-2 prose-p:text-foreground prose-p:leading-[1.75]
                prose-headings:text-foreground prose-headings:font-semibold prose-headings:mt-4 prose-headings:mb-2
                prose-code:bg-muted prose-code:rounded-md prose-code:px-1.5 prose-code:py-0.5 prose-code:text-xs prose-code:font-medium
                prose-pre:bg-slate-50 dark:prose-pre:bg-slate-900 prose-pre:rounded-xl prose-pre:p-4 prose-pre:my-3 prose-pre:border prose-pre:border-border
                prose-strong:text-foreground prose-strong:font-semibold
                prose-a:text-primary prose-a:no-underline hover:prose-a:underline
                prose-li:my-0.5 prose-li:text-foreground prose-li:leading-[1.75]
                prose-ul:my-2 prose-ol:my-2
                prose-table:text-sm prose-table:rounded-lg prose-table:overflow-hidden
                prose-th:bg-muted/60 prose-th:px-3 prose-th:py-2 prose-th:text-left prose-th:font-semibold prose-th:text-foreground
                prose-td:px-3 prose-td:py-2 prose-td:text-foreground/80
                prose-blockquote:border-l-primary/50 prose-blockquote:text-foreground/80"
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
                    if (node && node.children) {
                      for (const child of node.children) {
                        if (
                          child.type === "element" &&
                          child.tagName === "code" &&
                          Array.isArray(child.properties?.className) &&
                          child.properties.className.some(
                            (c: string | number) => typeof c === "string" && c.includes("mermaid")
                          )
                        ) {
                          // eslint-disable-next-line @typescript-eslint/no-explicit-any
                          function extractText(nodes: any[]): string {
                            return nodes
                              .map((n) => {
                                if ("value" in n) return n.value as string;
                                if ("children" in n) return extractText(n.children);
                                return "";
                              })
                              .join("");
                          }
                          const text = extractText(child.children);
                          if (isStreaming) {
                            return (
                              <pre className="text-xs text-muted-foreground opacity-60">
                                <code>{text.trim()}</code>
                              </pre>
                            );
                          }
                          return <MermaidBlock code={text.trim()} />;
                        }
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

      {/* Visualize button — only for non-streaming assistant messages */}
      {!isStreaming && content.length > 80 && (
        <div className="mt-3 flex items-center gap-2 flex-wrap">
          {plotHtml ? (
            <button
              onClick={() => setPlotHtml(null)}
              className="inline-flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg border border-border text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
            >
              <X className="h-3 w-3" /> Close Plot
            </button>
          ) : (
            <button
              onClick={handleVisualize}
              disabled={plotLoading}
              className="inline-flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg border border-primary/30 text-primary bg-primary/5 hover:bg-primary/10 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {plotLoading ? (
                <><Loader2 className="h-3 w-3 animate-spin" /> Generating simulation...</>
              ) : (
                <><BarChart2 className="h-3 w-3" /> Plot Interactive Graph</>
              )}
            </button>
          )}
        </div>
      )}

      {/* Rendered plot */}
      {plotHtml && <VisualPlotRenderer html={plotHtml} topic={plotTopic} />}
    </div>
  );
}

export const MessageBubble = memo(MessageBubbleInner);
