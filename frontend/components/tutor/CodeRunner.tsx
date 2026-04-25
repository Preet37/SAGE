"use client";
import { useState, useEffect, useRef, useCallback } from "react";
import { Play, Loader2, RotateCcw, X, Terminal } from "lucide-react";
import { cn } from "@/lib/utils";

type Lang = "javascript" | "typescript" | "python" | "js" | "ts" | "py";

const RUNNABLE: Set<string> = new Set([
  "javascript", "js", "typescript", "ts", "python", "py", "python3",
]);

function isRunnable(className: string | undefined): Lang | null {
  if (!className) return null;
  const match = className.match(/language-(\w+)/);
  if (!match) return null;
  const lang = match[1].toLowerCase() as Lang;
  return RUNNABLE.has(lang) ? lang : null;
}

function buildJsSandbox(code: string): string {
  const escaped = code.replace(/\\/g, "\\\\").replace(/`/g, "\\`");
  return `<!DOCTYPE html><html><body><script>
(function(){
  var out=[], err=[];
  var _log=console.log, _warn=console.warn, _err=console.error, _info=console.info;
  var fmt=function(args){ return Array.from(args).map(function(a){ return typeof a==='object'?JSON.stringify(a,null,2):String(a); }).join(' '); };
  console.log=function(){ out.push(fmt(arguments)); _log.apply(console,arguments); };
  console.warn=function(){ out.push('⚠ '+fmt(arguments)); _warn.apply(console,arguments); };
  console.info=function(){ out.push('ℹ '+fmt(arguments)); _info.apply(console,arguments); };
  console.error=function(){ err.push('✖ '+fmt(arguments)); _err.apply(console,arguments); };
  try{
    eval(\`${escaped}\`);
  }catch(e){ err.push('✖ '+e.message); }
  window.parent.postMessage({type:'run-output',stdout:out.join('\\n'),stderr:err.join('\\n')},'*');
})();
<\/script></body></html>`;
}

function buildPySandbox(code: string): string {
  const escaped = JSON.stringify(code);
  return `<!DOCTYPE html><html><body>
<div id="s" style="font:12px monospace;padding:8px;white-space:pre-wrap">Loading Python (Pyodide)...</div>
<script src="https://cdn.jsdelivr.net/pyodide/v0.26.2/full/pyodide.js"><\/script>
<script>
(async()=>{
  var out=[], err=[];
  try{
    var pyodide=await loadPyodide({indexURL:'https://cdn.jsdelivr.net/pyodide/v0.26.2/full/'});
    pyodide.setStdout({batched:function(t){ out.push(t); }});
    pyodide.setStderr({batched:function(t){ err.push('✖ '+t); }});
    await pyodide.runPythonAsync(${escaped});
  }catch(e){
    err.push('✖ '+e.message);
  }
  var combined=(out.join('\\n')+(err.length?'\\n'+err.join('\\n'):'')).trim();
  document.getElementById('s').textContent=combined||'(no output)';
  window.parent.postMessage({type:'run-output',stdout:out.join('\\n'),stderr:err.join('\\n')},'*');
})();
<\/script></body></html>`;
}

interface CodeRunnerProps {
  code: string;
  lang: Lang;
  className?: string;
}

export function CodeRunner({ code, lang, className }: CodeRunnerProps) {
  const [running, setRunning] = useState(false);
  const [output, setOutput] = useState<string | null>(null);
  const [hasError, setHasError] = useState(false);
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const isPython = lang === "python" || lang === "py" || (lang as string) === "python3";

  const handleMessage = useCallback((e: MessageEvent) => {
    if (e.data?.type !== "run-output") return;
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    const stdout = (e.data.stdout || "").trim();
    const stderr = (e.data.stderr || "").trim();
    const combined = [stdout, stderr].filter(Boolean).join("\n");
    setOutput(combined || "(no output)");
    setHasError(!!stderr);
    setRunning(false);
  }, []);

  useEffect(() => {
    window.addEventListener("message", handleMessage);
    return () => window.removeEventListener("message", handleMessage);
  }, [handleMessage]);

  function run() {
    setRunning(true);
    setOutput(null);
    setHasError(false);

    const srcdoc = isPython ? buildPySandbox(code) : buildJsSandbox(code);

    if (iframeRef.current) {
      iframeRef.current.srcdoc = srcdoc;
    }

    // Timeout — Python/Pyodide can take up to 30s to load; JS should be near-instant
    const maxMs = isPython ? 35000 : 5000;
    timeoutRef.current = setTimeout(() => {
      setOutput(isPython ? "Timed out — Pyodide may still be loading. Try again." : "Timed out.");
      setRunning(false);
    }, maxMs);
  }

  function reset() {
    setOutput(null);
    setHasError(false);
    setRunning(false);
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    if (iframeRef.current) iframeRef.current.srcdoc = "";
  }

  return (
    <div className={cn("not-prose my-3", className)}>
      {/* Code header bar */}
      <div className="flex items-center justify-between px-3 py-1.5 rounded-t-xl bg-slate-800 dark:bg-slate-900 border border-border border-b-0">
        <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">
          {isPython ? "python" : "javascript"}
        </span>
        <div className="flex items-center gap-1">
          {output !== null && (
            <button
              onClick={reset}
              className="flex items-center gap-1 text-[10px] px-2 py-0.5 rounded text-slate-400 hover:text-slate-200 transition-colors"
            >
              <RotateCcw className="h-2.5 w-2.5" /> Clear
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
            {running ? (
              <><Loader2 className="h-3 w-3 animate-spin" /> {isPython ? "Loading..." : "Running..."}</>
            ) : (
              <><Play className="h-3 w-3" /> Run</>
            )}
          </button>
        </div>
      </div>

      {/* Code body — pass through children from the pre block */}
      <div className="rounded-b-xl overflow-hidden border border-border border-t-0">
        <pre className="bg-slate-50 dark:bg-slate-900 p-4 text-sm overflow-x-auto m-0 rounded-none">
          <code className="font-mono text-xs">{code}</code>
        </pre>

        {/* Hidden iframe for execution */}
        <iframe
          ref={iframeRef}
          sandbox="allow-scripts"
          className="hidden"
          title="code-runner"
        />

        {/* Output panel */}
        {output !== null && (
          <div
            className={cn(
              "border-t border-border px-4 py-3",
              hasError
                ? "bg-red-950/30"
                : "bg-emerald-950/20"
            )}
          >
            <div className="flex items-center gap-1.5 mb-2">
              <Terminal className={cn("h-3 w-3", hasError ? "text-red-400" : "text-emerald-400")} />
              <span className={cn("text-[10px] font-semibold uppercase tracking-wider", hasError ? "text-red-400" : "text-emerald-400")}>
                Output
              </span>
            </div>
            <pre className={cn(
              "text-xs font-mono leading-relaxed whitespace-pre-wrap",
              hasError ? "text-red-300" : "text-emerald-300"
            )}>
              {output}
            </pre>
          </div>
        )}

        {/* Loading indicator for Python */}
        {running && isPython && (
          <div className="border-t border-border px-4 py-3 bg-amber-950/20">
            <div className="flex items-center gap-2 text-xs text-amber-400">
              <Loader2 className="h-3 w-3 animate-spin" />
              Loading Pyodide (Python runtime)... first run takes ~10s
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── Helper: parse language from rehype className list ──────────────────────────
export function getCodeLang(classNames: (string | number)[] | null | undefined): Lang | null {
  if (!classNames) return null;
  for (const cls of classNames) {
    const lang = isRunnable(String(cls));
    if (lang) return lang;
  }
  return null;
}
