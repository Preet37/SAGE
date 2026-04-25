"use client";
import { useState, useEffect, useRef, useCallback } from "react";
import { Play, Loader2, RotateCcw, Terminal, Eye } from "lucide-react";
import { cn } from "@/lib/utils";

// ── Language config ──────────────────────────────────────────────────────────

type RunStrategy = "piston" | "iframe-js" | "iframe-html";

interface LangConfig {
  label: string;
  pistonLang?: string;   // language slug for Piston API
  strategy: RunStrategy;
  extension: string;
}

const LANG_MAP: Record<string, LangConfig> = {
  // Web
  javascript:  { label: "JavaScript", strategy: "iframe-js",   extension: "js"   },
  js:          { label: "JavaScript", strategy: "iframe-js",   extension: "js"   },
  typescript:  { label: "TypeScript", pistonLang: "typescript", strategy: "piston", extension: "ts" },
  ts:          { label: "TypeScript", pistonLang: "typescript", strategy: "piston", extension: "ts" },
  html:        { label: "HTML",       strategy: "iframe-html", extension: "html" },
  // Systems
  python:      { label: "Python",     pistonLang: "python",    strategy: "piston", extension: "py"  },
  py:          { label: "Python",     pistonLang: "python",    strategy: "piston", extension: "py"  },
  python3:     { label: "Python",     pistonLang: "python",    strategy: "piston", extension: "py"  },
  c:           { label: "C",          pistonLang: "c",         strategy: "piston", extension: "c"   },
  cpp:         { label: "C++",        pistonLang: "c++",       strategy: "piston", extension: "cpp" },
  "c++":       { label: "C++",        pistonLang: "c++",       strategy: "piston", extension: "cpp" },
  java:        { label: "Java",       pistonLang: "java",      strategy: "piston", extension: "java"},
  go:          { label: "Go",         pistonLang: "go",        strategy: "piston", extension: "go"  },
  rust:        { label: "Rust",       pistonLang: "rust",      strategy: "piston", extension: "rs"  },
  ruby:        { label: "Ruby",       pistonLang: "ruby",      strategy: "piston", extension: "rb"  },
  bash:        { label: "Bash",       pistonLang: "bash",      strategy: "piston", extension: "sh"  },
  sh:          { label: "Shell",      pistonLang: "bash",      strategy: "piston", extension: "sh"  },
  swift:       { label: "Swift",      pistonLang: "swift",     strategy: "piston", extension: "swift"},
  kotlin:      { label: "Kotlin",     pistonLang: "kotlin",    strategy: "piston", extension: "kt"  },
  csharp:      { label: "C#",         pistonLang: "csharp",    strategy: "piston", extension: "cs"  },
  "c#":        { label: "C#",         pistonLang: "csharp",    strategy: "piston", extension: "cs"  },
  php:         { label: "PHP",        pistonLang: "php",       strategy: "piston", extension: "php" },
  r:           { label: "R",          pistonLang: "r",         strategy: "piston", extension: "r"   },
  lua:         { label: "Lua",        pistonLang: "lua",       strategy: "piston", extension: "lua" },
};

const RUNNABLE_LANGS = new Set(Object.keys(LANG_MAP));

export function getCodeLang(classNames: (string | number)[] | null | undefined): LangConfig | null {
  if (!classNames) return null;
  for (const cls of classNames) {
    const s = String(cls);
    const match = s.match(/language-(\w+)/);
    if (!match) continue;
    const key = match[1].toLowerCase();
    if (RUNNABLE_LANGS.has(key)) return LANG_MAP[key];
  }
  return null;
}

// ── Piston API ───────────────────────────────────────────────────────────────

const PISTON_URL = "https://emkc.org/api/v2/piston/execute";

async function runViaPiston(pistonLang: string, code: string, extension: string): Promise<{ stdout: string; stderr: string }> {
  const res = await fetch(PISTON_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      language: pistonLang,
      version: "*",
      files: [{ name: `main.${extension}`, content: code }],
      stdin: "",
      args: [],
      compile_timeout: 15000,
      run_timeout: 10000,
    }),
  });
  if (!res.ok) throw new Error(`Piston API error: ${res.status}`);
  const data = await res.json();
  return {
    stdout: (data.run?.stdout || data.compile?.stdout || "").trim(),
    stderr: (data.run?.stderr || data.compile?.stderr || data.compile?.output || "").trim(),
  };
}

// ── JS iframe sandbox ────────────────────────────────────────────────────────

function buildJsSrcdoc(code: string): string {
  const safe = code.replace(/\\/g, "\\\\").replace(/`/g, "\\`").replace(/\$/g, "\\$");
  return `<!DOCTYPE html><html><body><script>
(function(){
  var out=[], err=[];
  var fmt=function(a){return Array.from(a).map(function(x){return typeof x==='object'?JSON.stringify(x,null,2):String(x);}).join(' ');};
  console.log=function(){out.push(fmt(arguments));};
  console.warn=function(){out.push('\u26a0 '+fmt(arguments));};
  console.info=function(){out.push('\u2139 '+fmt(arguments));};
  console.error=function(){err.push('\u2716 '+fmt(arguments));};
  try{eval(\`${safe}\`);}catch(e){err.push('\u2716 '+e.message);}
  window.parent.postMessage({type:'code-output',stdout:out.join('\\n'),stderr:err.join('\\n')},'*');
})();
<\/script></body></html>`;
}

// ── Component ────────────────────────────────────────────────────────────────

interface RunResult { stdout: string; stderr: string; error?: string }

export function CodeRunner({ code, langConfig }: { code: string; langConfig: LangConfig }) {
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<RunResult | null>(null);
  const [showPreview, setShowPreview] = useState(false);
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const previewRef = useRef<HTMLIFrameElement>(null);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const isHtml = langConfig.strategy === "iframe-html";
  const isJs  = langConfig.strategy === "iframe-js";

  // postMessage listener for JS iframe
  const onMessage = useCallback((e: MessageEvent) => {
    if (e.data?.type !== "code-output") return;
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    setResult({ stdout: e.data.stdout || "", stderr: e.data.stderr || "" });
    setRunning(false);
  }, []);

  useEffect(() => {
    window.addEventListener("message", onMessage);
    return () => window.removeEventListener("message", onMessage);
  }, [onMessage]);

  async function run() {
    setRunning(true);
    setResult(null);
    if (timeoutRef.current) clearTimeout(timeoutRef.current);

    try {
      if (isHtml) {
        // HTML: just show preview
        setShowPreview(true);
        if (previewRef.current) previewRef.current.srcdoc = code;
        setRunning(false);
        return;
      }

      if (isJs) {
        const srcdoc = buildJsSrcdoc(code);
        if (iframeRef.current) {
          iframeRef.current.srcdoc = "";
          setTimeout(() => { if (iframeRef.current) iframeRef.current.srcdoc = srcdoc; }, 10);
        }
        timeoutRef.current = setTimeout(() => {
          setResult({ stdout: "", stderr: "", error: "Timed out." });
          setRunning(false);
        }, 6000);
        return;
      }

      // Piston
      if (!langConfig.pistonLang) throw new Error("No execution backend for this language.");
      const r = await runViaPiston(langConfig.pistonLang, code, langConfig.extension);
      setResult(r);
    } catch (e) {
      setResult({ stdout: "", stderr: "", error: String(e) });
    } finally {
      if (!isJs) setRunning(false);
    }
  }

  function reset() {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    setResult(null);
    setRunning(false);
    setShowPreview(false);
    if (iframeRef.current) iframeRef.current.srcdoc = "";
  }

  const lines = result
    ? [result.error && `Error: ${result.error}`, result.stderr, result.stdout]
        .filter(Boolean).join("\n").trim() || "(no output)"
    : null;

  const hasErr = !!(result?.error || result?.stderr);

  return (
    <div className="not-prose my-3 rounded-xl overflow-hidden border border-zinc-200 dark:border-zinc-700 shadow-sm">
      {/* Top bar */}
      <div className="flex items-center justify-between px-4 py-2 bg-zinc-900 dark:bg-zinc-950">
        <div className="flex items-center gap-2">
          <div className="flex gap-1.5">
            <span className="w-3 h-3 rounded-full bg-red-500/70" />
            <span className="w-3 h-3 rounded-full bg-amber-500/70" />
            <span className="w-3 h-3 rounded-full bg-emerald-500/70" />
          </div>
          <span className="text-[11px] font-mono text-zinc-500 ml-1">{langConfig.label}</span>
        </div>
        <div className="flex items-center gap-2">
          {isHtml && result === null && !showPreview && (
            <button
              onClick={() => { setShowPreview(true); if (previewRef.current) previewRef.current.srcdoc = code; }}
              className="flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-md text-zinc-400 hover:text-zinc-200 border border-zinc-700 hover:border-zinc-500 transition-all"
            >
              <Eye className="h-3 w-3" /> Preview
            </button>
          )}
          {(result !== null || showPreview) && (
            <button onClick={reset} className="flex items-center gap-1 text-xs text-zinc-500 hover:text-zinc-300 transition-colors">
              <RotateCcw className="h-3 w-3" /> Reset
            </button>
          )}
          {!isHtml && (
            <button
              onClick={run}
              disabled={running}
              className={cn(
                "flex items-center gap-1.5 text-xs px-3 py-1 rounded-md font-medium transition-all",
                running
                  ? "bg-zinc-700 text-zinc-400 cursor-not-allowed"
                  : "bg-zinc-100 dark:bg-zinc-200 text-zinc-900 hover:bg-white dark:hover:bg-white"
              )}
            >
              {running
                ? <><Loader2 className="h-3 w-3 animate-spin" />Running…</>
                : <><Play className="h-3 w-3 fill-current" />Run</>}
            </button>
          )}
        </div>
      </div>

      {/* Code */}
      <pre className="bg-zinc-900 dark:bg-zinc-950 text-zinc-200 p-4 text-[13px] font-mono overflow-x-auto m-0 leading-relaxed border-t border-zinc-800">
        <code>{code}</code>
      </pre>

      {/* Hidden JS execution iframe */}
      {isJs && <iframe ref={iframeRef} sandbox="allow-scripts" title="js-runner" className="hidden" />}

      {/* HTML preview iframe */}
      {isHtml && showPreview && (
        <div className="border-t border-zinc-700">
          <div className="flex items-center gap-2 px-4 py-2 bg-zinc-800">
            <Eye className="h-3 w-3 text-blue-400" />
            <span className="text-[11px] text-blue-400 font-semibold uppercase tracking-wider">Preview</span>
          </div>
          <iframe
            ref={previewRef}
            sandbox="allow-scripts allow-same-origin"
            title="html-preview"
            className="w-full bg-white"
            style={{ height: "320px", border: "none" }}
          />
        </div>
      )}

      {/* Terminal output */}
      {lines !== null && (
        <div className="border-t border-zinc-800 bg-zinc-950">
          <div className="flex items-center gap-2 px-4 py-2 border-b border-zinc-800/60">
            <Terminal className="h-3 w-3 text-zinc-500" />
            <span className="text-[11px] text-zinc-500 font-medium uppercase tracking-wider">Output</span>
            {hasErr && <span className="text-[10px] px-1.5 py-0.5 rounded bg-red-900/50 text-red-400 font-medium">error</span>}
          </div>
          <pre className="px-4 py-3 text-[13px] font-mono leading-relaxed whitespace-pre-wrap text-zinc-200">
            {lines}
          </pre>
        </div>
      )}
    </div>
  );
}
