"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";
import { AppHeader } from "@/components/AppHeader";
import { Button } from "@/components/ui/button";
import {
  Cpu,
  Cloud,
  Loader2,
  Send,
  Smartphone,
  ShieldCheck,
  AlertTriangle,
  Wifi,
  WifiOff,
  Sparkles,
  RotateCw,
} from "lucide-react";
import {
  isWebGPUAvailable,
  loadOnDeviceEngine,
  ON_DEVICE_MODELS,
  type InitProgress,
  type OnDeviceEngine,
  type OnDeviceModel,
} from "@/lib/onDeviceLLM";

interface DeviceMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  tokensPerSec?: number;
  latencyMs?: number;
}

const SYSTEM_PROMPT = `You are SAGE Pocket Tutor — running entirely on this user's device.

Your job:
- Answer ML / AI / computer science questions clearly and concisely.
- When you're not confident, say so plainly. Don't invent specifics.
- Use Socratic prompts when the user is exploring an idea: ask one
  pointed question that helps them think, rather than dumping a lecture.
- Keep responses under ~250 words unless asked for more.

You have NO internet access. If a question requires fresh information,
suggest the user switch to the Cloud Tutor.`;

export default function PocketTutorPage() {
  const router = useRouter();
  const [hasWebGPU, setHasWebGPU] = useState<boolean | null>(null);
  const [model, setModel] = useState<OnDeviceModel>(ON_DEVICE_MODELS[0]);
  const [engine, setEngine] = useState<OnDeviceEngine | null>(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState<InitProgress | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<DeviceMessage[]>([]);
  const [generating, setGenerating] = useState(false);
  const abortRef = useRef<AbortController | null>(null);
  const scrollRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!getToken()) router.push("/login");
    isWebGPUAvailable().then(setHasWebGPU);
  }, [router]);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, generating]);

  async function handleLoad(target: OnDeviceModel) {
    setError(null);
    setLoading(true);
    setProgress({ progress: 0, text: "Initializing WebGPU…" });
    try {
      const e = await loadOnDeviceEngine(target.id, setProgress);
      setEngine(e);
      setModel(target);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load model");
    } finally {
      setLoading(false);
      setProgress(null);
    }
  }

  async function handleSend(e?: React.FormEvent) {
    e?.preventDefault();
    if (!engine || !input.trim() || generating) return;

    const userMsg: DeviceMessage = { id: crypto.randomUUID(), role: "user", content: input.trim() };
    const assistantId = crypto.randomUUID();
    setMessages((p) => [...p, userMsg, { id: assistantId, role: "assistant", content: "" }]);
    setInput("");
    setGenerating(true);
    abortRef.current = new AbortController();

    const history = [{ role: "system" as const, content: SYSTEM_PROMPT }];
    for (const m of [...messages, userMsg]) {
      history.push({ role: m.role, content: m.content });
    }

    try {
      const { tokensPerSec, latencyMs } = await engine.generate(history, (delta) => {
        setMessages((prev) =>
          prev.map((m) => m.id === assistantId ? { ...m, content: m.content + delta } : m),
        );
      }, abortRef.current.signal);
      setMessages((prev) =>
        prev.map((m) => m.id === assistantId ? { ...m, tokensPerSec, latencyMs } : m),
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Generation failed");
    } finally {
      setGenerating(false);
      abortRef.current = null;
    }
  }

  function handleStop() {
    abortRef.current?.abort();
  }

  function handleClear() {
    setMessages([]);
  }

  const isOffline = typeof navigator !== "undefined" && navigator.onLine === false;

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      <AppHeader />
      <main className="flex-1 overflow-hidden flex flex-col">
        <div className="max-w-4xl w-full mx-auto flex-1 flex flex-col px-6 py-6 gap-4">

          <header className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
                <Smartphone className="h-5 w-5" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">Pocket Tutor</h1>
                <p className="text-sm text-muted-foreground flex items-center gap-2 flex-wrap">
                  Runs entirely on your device · zero tokens leave your browser
                  {isOffline ? <span className="inline-flex items-center gap-1 text-emerald-600"><WifiOff className="h-3 w-3" /> offline</span>
                              : <span className="inline-flex items-center gap-1 text-muted-foreground"><Wifi className="h-3 w-3" /> online (still local)</span>}
                </p>
              </div>
            </div>
            <a href="/learn" className="text-xs text-muted-foreground hover:text-foreground inline-flex items-center gap-1">
              <Cloud className="h-3.5 w-3.5" /> use Cloud Tutor instead
            </a>
          </header>

          {hasWebGPU === false && (
            <div className="rounded-lg border border-amber-500/40 bg-amber-50 dark:bg-amber-950/20 px-4 py-3 text-sm text-amber-700 dark:text-amber-300 flex items-start gap-2">
              <AlertTriangle className="h-4 w-4 mt-0.5 flex-shrink-0" />
              <div>
                Your browser doesn't expose WebGPU, which is required for on-device inference.
                Try Chrome 121+ or Edge on a desktop. Mobile path: build a Melange-deployed
                app variant per docs/MELANGE-DEPLOYMENT.md.
              </div>
            </div>
          )}

          {error && (
            <div className="rounded-lg border border-destructive/40 bg-destructive/10 px-4 py-3 text-sm text-destructive">
              {error}
            </div>
          )}

          <div className="rounded-xl border border-border bg-card p-4">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-semibold flex items-center gap-2">
                <Cpu className="h-4 w-4 text-primary" /> Pick a model
              </h2>
              <span className="text-xs text-muted-foreground inline-flex items-center gap-1">
                <ShieldCheck className="h-3 w-3" /> private inference
              </span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {ON_DEVICE_MODELS.map((m) => (
                <button key={m.id}
                  onClick={() => handleLoad(m)}
                  disabled={loading || hasWebGPU === false}
                  className={`text-left rounded-lg border p-3 transition ${
                    engine?.modelId === m.id
                      ? "border-primary bg-primary/5"
                      : "border-border hover:border-primary/40"
                  } ${loading ? "opacity-60 cursor-wait" : ""}`}
                >
                  <div className="text-sm font-medium">{m.label}</div>
                  <div className="text-[11px] text-muted-foreground mt-0.5">{m.approxSizeMb} MB · cached after first load</div>
                  <div className="text-xs text-muted-foreground mt-1.5 line-clamp-2">{m.description}</div>
                </button>
              ))}
            </div>
            {loading && progress && (
              <div className="mt-3">
                <div className="h-1.5 bg-muted rounded-full overflow-hidden">
                  <div className="h-full bg-primary transition-all" style={{ width: `${Math.round(progress.progress * 100)}%` }} />
                </div>
                <p className="text-xs text-muted-foreground mt-1.5">{progress.text}</p>
              </div>
            )}
          </div>

          {/* Chat */}
          <div className="flex-1 rounded-xl border border-border bg-card flex flex-col overflow-hidden">
            <div ref={scrollRef} className="flex-1 overflow-y-auto p-5 space-y-4">
              {!engine ? (
                <div className="h-full flex items-center justify-center text-center text-sm text-muted-foreground py-10">
                  Pick a model above to start chatting offline.
                </div>
              ) : messages.length === 0 ? (
                <div className="h-full flex flex-col items-center justify-center text-center text-sm text-muted-foreground gap-3 py-10">
                  <Sparkles className="h-6 w-6 text-primary" />
                  <p>Ready. Ask anything — runs entirely on your device.</p>
                  <div className="flex flex-wrap gap-2 justify-center">
                    {[
                      "Explain LoRA in three sentences.",
                      "What's the intuition behind self-attention?",
                      "Give me a quick comprehension check on transformers.",
                    ].map((s) => (
                      <button key={s} onClick={() => setInput(s)}
                        className="text-xs rounded-full border border-border bg-background px-3 py-1 hover:bg-muted/50">
                        {s}
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                messages.map((m) => (
                  <div key={m.id} className={m.role === "user" ? "flex justify-end" : ""}>
                    <div className={
                      m.role === "user"
                        ? "max-w-[75%] rounded-2xl rounded-tr-sm bg-primary text-primary-foreground px-4 py-2 text-sm whitespace-pre-wrap"
                        : "max-w-[85%] text-sm whitespace-pre-wrap leading-relaxed"
                    }>
                      {m.content || (generating ? <span className="text-muted-foreground italic">thinking…</span> : null)}
                      {m.role === "assistant" && m.tokensPerSec && (
                        <div className="mt-2 inline-flex items-center gap-1 text-[11px] text-muted-foreground">
                          <Cpu className="h-3 w-3" />
                          {m.tokensPerSec.toFixed(1)} tok/s · {(m.latencyMs! / 1000).toFixed(1)}s · on-device
                        </div>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>

            <form onSubmit={handleSend} className="border-t border-border p-3 flex gap-2">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={engine ? "Ask the Pocket Tutor…" : "Load a model to start"}
                disabled={!engine || generating}
                className="flex-1 px-3 py-2 rounded-lg border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary/40 disabled:opacity-60"
              />
              {generating ? (
                <Button type="button" variant="outline" onClick={handleStop}>
                  Stop
                </Button>
              ) : (
                <>
                  <Button type="submit" disabled={!engine || !input.trim()}>
                    <Send className="h-4 w-4" />
                  </Button>
                  {messages.length > 0 && (
                    <Button type="button" variant="ghost" onClick={handleClear} title="Clear">
                      <RotateCw className="h-4 w-4" />
                    </Button>
                  )}
                </>
              )}
            </form>
          </div>
        </div>
      </main>
    </div>
  );
}
