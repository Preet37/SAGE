"use client";
import { useEffect, useMemo, useRef, useState } from "react";
import { Code2, Eye, RefreshCw } from "lucide-react";

interface ArtifactBlockProps {
  /** The raw inner text of an `<artifact>` tag — may be a JSON envelope or raw HTML. */
  content: string;
}

interface ParsedArtifact {
  title: string;
  html: string;
  /** Whether the original payload was JSON (vs. raw HTML fallback). */
  structured: boolean;
}

function parseArtifact(content: string): ParsedArtifact {
  const trimmed = content.trim();
  // Prefer JSON envelopes for explicit title + html separation.
  if (trimmed.startsWith("{")) {
    try {
      const data = JSON.parse(trimmed);
      const html = typeof data.html === "string" ? data.html : "";
      const title = typeof data.title === "string" ? data.title : "Interactive artifact";
      if (html) {
        return { title, html, structured: true };
      }
    } catch {
      // fall through to raw-HTML interpretation
    }
  }
  return { title: "Interactive artifact", html: trimmed, structured: false };
}

/**
 * Wrap the artifact HTML in a complete document so srcdoc gets a clean root.
 * The sandboxed iframe blocks navigation, top-frame access, and same-origin
 * privileges — only allow-scripts so the embedded JS can run.
 */
function buildSrcDoc(html: string): string {
  // If the artifact already includes <html>/<!doctype>, use it verbatim.
  if (/^\s*(<!doctype|<html)/i.test(html)) {
    return html;
  }
  return `<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<style>
  html,body{margin:0;padding:12px;font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#0f172a;background:transparent;}
  *{box-sizing:border-box;}
</style>
</head>
<body>
${html}
</body>
</html>`;
}

export function ArtifactBlock({ content }: ArtifactBlockProps) {
  const parsed = useMemo(() => parseArtifact(content), [content]);
  const srcDoc = useMemo(() => buildSrcDoc(parsed.html), [parsed.html]);
  const [view, setView] = useState<"preview" | "code">("preview");
  const [reloadKey, setReloadKey] = useState(0);
  const iframeRef = useRef<HTMLIFrameElement>(null);

  // Auto-resize the iframe to its content (up to a reasonable max).
  useEffect(() => {
    if (view !== "preview") return;
    const iframe = iframeRef.current;
    if (!iframe) return;
    function resize() {
      try {
        const doc = iframe?.contentDocument;
        if (!doc) return;
        const h = Math.min(
          Math.max(doc.documentElement.scrollHeight, doc.body?.scrollHeight ?? 0),
          800,
        );
        if (iframe) iframe.style.height = `${h + 4}px`;
      } catch {
        // cross-origin if the artifact navigated; leave default height.
      }
    }
    iframe.addEventListener("load", resize);
    const timer = window.setInterval(resize, 1000);
    return () => {
      iframe.removeEventListener("load", resize);
      window.clearInterval(timer);
    };
  }, [view, reloadKey]);

  return (
    <figure className="my-3 not-prose rounded-xl border border-border overflow-hidden bg-card/60">
      <div className="flex items-center justify-between gap-2 px-3 py-2 border-b border-border bg-muted/40">
        <span className="text-xs font-medium text-foreground truncate">
          {parsed.title}
        </span>
        <div className="flex items-center gap-1">
          <button
            type="button"
            onClick={() => setView("preview")}
            aria-pressed={view === "preview"}
            aria-label="Show preview"
            className={`inline-flex items-center gap-1 text-[11px] px-2 py-1 rounded-md transition-colors ${
              view === "preview"
                ? "bg-background text-foreground shadow-sm"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <Eye className="h-3 w-3" /> Preview
          </button>
          <button
            type="button"
            onClick={() => setView("code")}
            aria-pressed={view === "code"}
            aria-label="Show source"
            className={`inline-flex items-center gap-1 text-[11px] px-2 py-1 rounded-md transition-colors ${
              view === "code"
                ? "bg-background text-foreground shadow-sm"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <Code2 className="h-3 w-3" /> Source
          </button>
          {view === "preview" && (
            <button
              type="button"
              onClick={() => setReloadKey((k) => k + 1)}
              aria-label="Reload artifact"
              className="inline-flex items-center text-[11px] px-2 py-1 rounded-md text-muted-foreground hover:text-foreground transition-colors"
            >
              <RefreshCw className="h-3 w-3" />
            </button>
          )}
        </div>
      </div>
      {view === "preview" ? (
        <iframe
          key={reloadKey}
          ref={iframeRef}
          title={parsed.title}
          srcDoc={srcDoc}
          // allow-scripts only — no allow-same-origin so the iframe cannot
          // read the parent's cookies, localStorage, or DOM.
          sandbox="allow-scripts"
          className="w-full bg-white"
          style={{ height: 280, border: 0 }}
        />
      ) : (
        <pre className="text-xs p-3 max-h-[400px] overflow-auto bg-slate-50 dark:bg-slate-900 m-0">
          <code>{parsed.html}</code>
        </pre>
      )}
    </figure>
  );
}
