"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import mermaid from "mermaid";

let lastTheme: string | null = null;

function initMermaid(isDark: boolean) {
  const theme = isDark ? "dark" : "default";
  if (lastTheme === theme) return;
  mermaid.initialize({
    startOnLoad: false,
    theme,
    fontFamily: "inherit",
    securityLevel: "loose",
    suppressErrorRendering: true,
    flowchart: { curve: "monotoneX", padding: 16 },
  });
  lastTheme = theme;
}

function stripStyleDirectives(code: string): string {
  return code
    .split("\n")
    .filter((line) => !line.trim().startsWith("style ") && !line.trim().startsWith("classDef "))
    .join("\n");
}

interface MermaidBlockProps {
  code: string;
}

let renderCounter = 0;

export function MermaidBlock({ code }: MermaidBlockProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [error, setError] = useState<string | null>(null);
  const [rendered, setRendered] = useState(false);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const doRender = useCallback(async (source: string) => {
    const isDark = document.documentElement.classList.contains("dark");
    initMermaid(isDark);
    const id = `mermaid-${renderCounter++}`;
    const cleaned = stripStyleDirectives(source).trim();
    if (!cleaned) return;

    try {
      const { svg } = await mermaid.render(id, cleaned);
      if (containerRef.current) {
        containerRef.current.innerHTML = svg;
        setError(null);
        setRendered(true);
      }
    } catch {
      const errEl = document.getElementById(`d${id}`);
      errEl?.remove();
    }
  }, []);

  useEffect(() => {
    if (timerRef.current) clearTimeout(timerRef.current);

    timerRef.current = setTimeout(() => {
      doRender(code);
    }, 400);

    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, [code, doRender]);

  // Re-render when theme changes
  useEffect(() => {
    const observer = new MutationObserver(() => {
      setRendered(false);
      lastTheme = null;
      doRender(code);
    });
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["class"],
    });
    return () => observer.disconnect();
  }, [code, doRender]);

  if (error) {
    return (
      <div className="rounded-lg bg-muted p-4 my-3">
        <p className="text-xs text-muted-foreground mb-2">Diagram could not be rendered:</p>
        <pre className="text-xs overflow-x-auto whitespace-pre-wrap">{code}</pre>
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className={`my-3 flex justify-center [&_svg]:max-w-full [&_svg]:h-auto transition-opacity duration-300 ${rendered ? "opacity-100" : "opacity-0"}`}
    />
  );
}
