"use client";
import React, { useState, useCallback } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeHighlight from "rehype-highlight";
import "katex/dist/katex.min.css";
import "highlight.js/styles/github.css";
import { Badge } from "@/components/ui/badge";
import { ZoomIn, X, ExternalLink, BookOpen } from "lucide-react";

interface LessonContentProps {
  title: string;
  content: string;
  concepts: string[];
}

function ImageLightbox({
  src,
  alt,
  onClose,
}: {
  src: string;
  alt: string;
  onClose: () => void;
}) {
  return (
    <div
      className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <button
        onClick={onClose}
        className="absolute top-4 right-4 text-white/70 hover:text-white transition-colors"
      >
        <X className="h-6 w-6" />
      </button>
      <img
        src={src}
        alt={alt}
        className="max-w-[90vw] max-h-[90vh] object-contain rounded-lg"
        onClick={(e) => e.stopPropagation()}
      />
    </div>
  );
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

export function LessonContent({ title, content, concepts }: LessonContentProps) {
  const [lightboxSrc, setLightboxSrc] = useState<{
    src: string;
    alt: string;
  } | null>(null);

  const closeLightbox = useCallback(() => setLightboxSrc(null), []);

  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-2xl font-bold mb-3">{title}</h1>
        <div className="flex flex-wrap gap-1.5">
          {concepts.map((c) => (
            <Badge key={c} variant="secondary" className="text-xs">
              {c}
            </Badge>
          ))}
        </div>
      </div>
      <div
        className="prose dark:prose-invert max-w-none
          prose-headings:font-semibold prose-headings:text-foreground
          prose-h2:text-xl prose-h2:mt-8 prose-h2:mb-3 prose-h2:border-b prose-h2:border-border prose-h2:pb-2
          prose-h3:text-lg prose-h3:mt-6 prose-h3:mb-2
          prose-h4:text-base prose-h4:mt-4 prose-h4:mb-1
          prose-p:text-foreground/85 prose-p:leading-[1.8]
          prose-code:bg-muted prose-code:rounded-md prose-code:px-1.5 prose-code:py-0.5 prose-code:text-sm prose-code:font-medium
          prose-pre:bg-slate-50 dark:prose-pre:bg-slate-900 prose-pre:rounded-xl prose-pre:p-5 prose-pre:border prose-pre:border-border
          prose-strong:text-foreground prose-strong:font-semibold
          prose-a:text-primary prose-a:font-medium
          prose-li:text-foreground/85 prose-li:leading-[1.8]
          prose-ul:my-3 prose-ol:my-3
          prose-table:text-sm prose-table:rounded-lg prose-table:overflow-hidden
          prose-th:bg-muted/60 prose-th:px-4 prose-th:py-2.5 prose-th:text-left prose-th:font-semibold prose-th:text-foreground
          prose-td:px-4 prose-td:py-2.5 prose-td:text-foreground/80
          prose-img:rounded-xl"
      >
        <ReactMarkdown
          remarkPlugins={remarkPlugins}
          rehypePlugins={rehypePlugins}
          components={{
            img({ src, alt }) {
              if (!src || typeof src !== "string") return null;
              const resolvedSrc = src.startsWith("/api/")
                ? `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}${src}`
                : src;

              return (
                <figure className="my-4 not-prose">
                  <div
                    className="relative group cursor-pointer rounded-xl border border-border overflow-hidden bg-card/60"
                    onClick={() =>
                      setLightboxSrc({ src: resolvedSrc, alt: alt || "" })
                    }
                  >
                    <img
                      src={resolvedSrc}
                      alt={alt || ""}
                      className="w-full max-h-80 object-contain bg-white/5 p-2"
                      loading="lazy"
                    />
                    <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors flex items-center justify-center">
                      <ZoomIn className="h-6 w-6 text-white opacity-0 group-hover:opacity-70 transition-opacity drop-shadow-lg" />
                    </div>
                  </div>
                  {alt && (
                    <figcaption className="text-xs text-muted-foreground mt-1.5 px-1 leading-snug">
                      {alt}
                    </figcaption>
                  )}
                </figure>
              );
            },
            p({ children }) {
              // Block-level custom renderers (figure, etc.) can't live inside <p>
              const kids = React.Children.toArray(children);
              const hasBlock = kids.some(
                (c) =>
                  React.isValidElement(c) &&
                  typeof c.type === "string" &&
                  ["figure", "div", "table", "ul", "ol", "section"].includes(c.type),
              );
              if (hasBlock) return <div className="my-2">{children}</div>;
              return <p>{children}</p>;
            },
            a({ href, children }) {
              const isExternal =
                href && (href.startsWith("http://") || href.startsWith("https://"));
              return (
                <a
                  href={href}
                  target={isExternal ? "_blank" : undefined}
                  rel={isExternal ? "noopener noreferrer" : undefined}
                  className="inline-flex items-center gap-0.5"
                >
                  {children}
                  {isExternal && (
                    <ExternalLink className="inline h-3 w-3 ml-0.5 flex-shrink-0" />
                  )}
                </a>
              );
            },
          }}
        >
          {normalizeLatexDelimiters(content)}
        </ReactMarkdown>
      </div>

      {lightboxSrc && (
        <ImageLightbox
          src={lightboxSrc.src}
          alt={lightboxSrc.alt}
          onClose={closeLightbox}
        />
      )}
    </div>
  );
}
