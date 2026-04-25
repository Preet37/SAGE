"use client";
import { useState, useEffect, useRef, useCallback } from "react";
import { Play, Loader2, RotateCcw, Terminal } from "lucide-react";
import { cn } from "@/lib/utils";

type Lang = "javascript" | "typescript" | "python" | "js" | "ts" | "py";

const RUNNABLE: Set<string> = new Set([
  "javascript", "js", "typescript", "ts", "python", "py", "python3",
]);

const PYTHON_LANGS = new Set(["python", "py", "python3"]);

function detectLangFromClass(className: string | undefined): Lang | null {
  if (!className) return null;
  const match = className.match(/language-(\w+)/);
  if (!match) return null;
  const lang = match[1].toLowerCase();
  return RUNNABLE.has(lang) ? (lang as Lang) : null;
}

// ── JS sandbox via sandboxed iframe ──────────────────────────────────────────
function buildJsSandbox(code: string): string {
  // Escape for use inside a JS template literal inside an HTML string
  const safe = code
    .replace(/\\/g, "\\\\")
    .replace(/`/g, "\\`")
    .replace(/\$/g, "\\$");
  return `<!DOCTYPE html><html><body><script>
(function(){
  var out=[], errs=[];
  var _fmt=function(a){ return Array.from(a).map(function(x){ return typeof x==='object'?JSON.stringify(x,null,2):String(x); }).join(' '); };
  console.log=function(){ out.push(_fmt(arguments)); };
  console.warn=function(){ out.push('\u26a0 '+_fmt(arguments)); };
  console.info=function(){ out.push('\u2139 '+_fmt(arguments)); };
  console.error=function(){ errs.push('\u2716 '+_fmt(arguments)); };
  try{ eval(\`${safe}\`); }
  catch(e){ errs.push('\u2716 '+e.message); }
  window.parent.postMessage({type:'code-output',stdout:out.join('\\n'),stderr:errs.join('\\n')},'*');
})();
<\/script></body></html>`;
}

interface RunResult {
  stdout: string;
  stderr: string;
  error?: string | null;
}

interface CodeRunnerProps {
  code: string;
  lang: Lang;
}

export function CodeRunner({ code, lang }: CodeRunnerProps) {
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<RunResult | null>(null);
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const isPython = PYTHON_LANGS.has(lang as string);
  const label = isPython ? "Python" : "JavaScript";

  // ── Listen for postMessage from JS iframe ───────────────────────────────
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

  // ── Run ─────────────────────────────────────────────────────────────────
  async function run() {
    setRunning(true);
    setResult(null);

    if (isPython) {
      // Python: use backend sandbox endpoint
      try {
        const apiBase = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const res = await fetch(`${apiBase}/sandbox/run`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ language: "python", code }),
        });
        const data: RunResult = await res.json();
        setResult(data);
      } catch (e) {
        setResult({ stdout: "", stderr: "", error: String(e) });
      } finally {
        setRunning(false);
      }
    } else {
      // JavaScript: run in sandboxed iframe
      const srcdoc = buildJsSandbox(code);
      if (iframeRef.current) {
        iframeRef.current.srcdoc = "";
        setTimeout(() => {
          if (iframeRef.current) iframeRef.current.srcdoc = srcdoc;
        }, 10);
      }
      timeoutRef.current = setTimeout(() => {
        setResult({ stdout: "", stderr: "", error: "Execution timed out." });
        setRunning(false);
      }, 6000);
    }
  }

  function reset() {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    setResult(null);
    setRunning(false);
    if (iframeRef.current) iframeRef.current.srcdoc = "";
  }

  // Combine output lines for display
  const displayOutput = result
    ? [result.error && `⚠ ${result.error}`, result.stderr, result.stdout]
        .filter(Boolean)
        .join("\n")
        .trim() || "(no output)"
    : null;

  const hasError = !!(result?.error || result?.stderr);

  return (
    <div className="not-prose my-3 rounded-xl border border-border overflow-hidden">
      {/* Header bar */}
      <div className="flex items-center justify-between px-3 py-1.5 bg-slate-800 dark:bg-slate-900">
        <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">{label}</span>
        <div className="flex items-center gap-1.5">
          {result !== null && (
            <button
              onClick={reset}
              className="text-[10px] px-2 py-0.5 rounded text-slate-400 hover:text-slate-200 transition-colors"
            >
              <RotateCcw className="h-2.5 w-2.5 inline mr-1" />Clear
            </button>
          )}
          <button
            onClick={run}
            disabled={running}
            className={cn(
              "flex items-center gap-1.5 text-xs px-2.5 py-0.5 rounded font-medium transition-all",
              running
                ? "bg-emerald-700/40 text-emerald-300 cursor-not-allowed"
                : "bg-emerald-600 hover:bg-emerald-500 text-white"
            )}
          >
            {running
              ? <><Loader2 className="h-3 w-3 animate-spin" /> Running…</>
              : <><Play className="h-3 w-3" /> Run</>}
          </button>
        </div>
      </div>

      {/* Code */}
      <pre className="bg-slate-50 dark:bg-slate-900 p-4 text-xs font-mono overflow-x-auto m-0 leading-relaxed">
        <code>{code}</code>
      </pre>

      {/* Hidden iframe for JS */}
      <iframe
        ref={iframeRef}
        sandbox="allow-scripts"
        title="code-runner"
        className="hidden"
      />

      {/* Output */}
      {displayOutput !== null && (
        <div className={cn(
          "border-t border-border px-4 py-3",
          hasError ? "bg-red-950/30" : "bg-emerald-950/20"
        )}>
          <div className="flex items-center gap-1.5 mb-1.5">
            <Terminal className={cn("h-3 w-3", hasError ? "text-red-400" : "text-emerald-400")} />
            <span className={cn("text-[10px] font-semibold uppercase tracking-wider",
              hasError ? "text-red-400" : "text-emerald-400")}>
              Output
            </span>
          </div>
          <pre className={cn(
            "text-xs font-mono leading-relaxed whitespace-pre-wrap",
            hasError ? "text-red-300" : "text-emerald-300"
          )}>
            {displayOutput}
          </pre>
        </div>
      )}
    </div>
  );
}

// ── Export lang detector for MessageBubble ────────────────────────────────────
export function getCodeLang(classNames: (string | number)[] | null | undefined): Lang | null {
  if (!classNames) return null;
  for (const cls of classNames) {
    const lang = detectLangFromClass(String(cls));
    if (lang) return lang;
  }
  return null;
}
