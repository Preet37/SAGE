"use client";
import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";
import { AppHeader } from "@/components/AppHeader";
import { Cpu, Cloud, Loader2, Send, Smartphone, ShieldCheck, AlertTriangle, Wifi, WifiOff, Sparkles, RotateCw } from "lucide-react";
import { isWebGPUAvailable, loadOnDeviceEngine, ON_DEVICE_MODELS, type InitProgress, type OnDeviceEngine, type OnDeviceModel } from "@/lib/onDeviceLLM";

const mono: React.CSSProperties  = { fontFamily: "var(--font-dm-mono)" };
const serif: React.CSSProperties = { fontFamily: "var(--font-cormorant)" };
const body: React.CSSProperties  = { fontFamily: "var(--font-crimson)" };

const SYSTEM_PROMPT = `You are SAGE Pocket Tutor — running entirely on this user's device.\n\nYour job:\n- Answer ML / AI / computer science questions clearly and concisely.\n- When you're not confident, say so plainly. Don't invent specifics.\n- Use Socratic prompts when the user is exploring an idea: ask one pointed question that helps them think, rather than dumping a lecture.\n- Keep responses under ~250 words unless asked for more.\n\nYou have NO internet access. If a question requires fresh information, suggest the user switch to the Cloud Tutor.`;

interface DeviceMessage { id: string; role: "user" | "assistant"; content: string; tokensPerSec?: number; latencyMs?: number; }

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

  useEffect(() => { if (!getToken()) router.push("/login"); isWebGPUAvailable().then(setHasWebGPU); }, [router]);
  useEffect(() => { scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" }); }, [messages, generating]);

  async function handleLoad(target: OnDeviceModel) {
    setError(null); setLoading(true); setProgress({ progress: 0, text: "Initializing WebGPU…" });
    try { const e = await loadOnDeviceEngine(target.id, setProgress); setEngine(e); setModel(target); }
    catch (err) { setError(err instanceof Error ? err.message : "Failed to load model"); }
    finally { setLoading(false); setProgress(null); }
  }

  async function handleSend(e?: React.FormEvent) {
    e?.preventDefault();
    if (!engine || !input.trim() || generating) return;
    const userMsg: DeviceMessage = { id: crypto.randomUUID(), role: "user", content: input.trim() };
    const assistantId = crypto.randomUUID();
    setMessages((p) => [...p, userMsg, { id: assistantId, role: "assistant", content: "" }]);
    setInput(""); setGenerating(true);
    abortRef.current = new AbortController();
    const history: { role: "system" | "user" | "assistant"; content: string }[] = [{ role: "system", content: SYSTEM_PROMPT }];
    for (const m of [...messages, userMsg]) history.push({ role: m.role, content: m.content });
    try {
      const { tokensPerSec, latencyMs } = await engine.generate(history, (delta) => { setMessages((prev) => prev.map((m) => m.id === assistantId ? { ...m, content: m.content + delta } : m)); }, abortRef.current.signal);
      setMessages((prev) => prev.map((m) => m.id === assistantId ? { ...m, tokensPerSec, latencyMs } : m));
    } catch (err) { setError(err instanceof Error ? err.message : "Generation failed"); }
    finally { setGenerating(false); abortRef.current = null; }
  }

  const isOffline = typeof navigator !== "undefined" && navigator.onLine === false;

  return (
    <div className="flex flex-col h-screen overflow-hidden" style={{ background: "var(--ink)", color: "var(--cream-0)" }}>
      <AppHeader />
      <main className="flex-1 overflow-hidden flex flex-col">
        <div style={{ maxWidth: "52rem", width: "100%", margin: "0 auto", flex: 1, display: "flex", flexDirection: "column", padding: "2rem 1.5rem", gap: "1.25rem" }}>

          {/* Header */}
          <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between" }}>
            <div>
              <p style={{ ...mono, fontSize: "0.58rem", letterSpacing: "0.16em", textTransform: "uppercase", color: "var(--gold)", marginBottom: "0.4rem" }}>Pocket</p>
              <h1 style={{ ...serif, fontWeight: 700, fontStyle: "italic", fontSize: "clamp(1.8rem,4vw,2.5rem)", color: "var(--cream-0)", lineHeight: 1.1, marginBottom: "0.3rem" }}>
                Pocket Tutor<span style={{ color: "var(--gold)" }}>.</span>
              </h1>
              <p style={{ ...body, fontSize: "0.9rem", color: "var(--cream-1)", display: "flex", alignItems: "center", gap: "0.5rem", flexWrap: "wrap" }}>
                Runs entirely on your device · zero tokens leave your browser
                {isOffline
                  ? <span style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", color: "var(--sage-c)", display: "inline-flex", alignItems: "center", gap: "0.25rem" }}><WifiOff style={{ width: "0.7rem", height: "0.7rem" }} />offline</span>
                  : <span style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", color: "var(--cream-2)", display: "inline-flex", alignItems: "center", gap: "0.25rem" }}><Wifi style={{ width: "0.7rem", height: "0.7rem" }} />online (still local)</span>}
              </p>
            </div>
            <a href="/learn" style={{ ...mono, fontSize: "0.52rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)", textDecoration: "none", display: "inline-flex", alignItems: "center", gap: "0.3rem", transition: "color 0.2s" }}
              onMouseEnter={e => (e.currentTarget as HTMLAnchorElement).style.color = "var(--cream-1)"}
              onMouseLeave={e => (e.currentTarget as HTMLAnchorElement).style.color = "var(--cream-2)"}>
              <Cloud style={{ width: "0.7rem", height: "0.7rem" }} /> Cloud Tutor
            </a>
          </div>

          {hasWebGPU === false && (
            <div style={{ background: "rgba(201,124,104,0.08)", border: "1px solid rgba(201,124,104,0.3)", padding: "0.75rem 1rem", display: "flex", alignItems: "flex-start", gap: "0.5rem" }}>
              <AlertTriangle style={{ width: "0.85rem", height: "0.85rem", color: "var(--rose)", flexShrink: 0, marginTop: "0.1rem" }} />
              <p style={{ ...body, fontSize: "0.9rem", color: "var(--rose)", lineHeight: 1.5 }}>Your browser doesn't expose WebGPU. Try Chrome 121+ or Edge on a desktop.</p>
            </div>
          )}
          {error && (
            <div style={{ background: "rgba(201,124,104,0.08)", border: "1px solid rgba(201,124,104,0.3)", padding: "0.65rem 0.9rem" }}>
              <p style={{ ...body, fontSize: "0.9rem", color: "var(--rose)" }}>{error}</p>
            </div>
          )}

          {/* Model picker */}
          <div style={{ background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.07)", padding: "1.25rem" }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "1rem" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "0.4rem" }}>
                <Cpu style={{ width: "0.8rem", height: "0.8rem", color: "var(--gold)" }} />
                <span style={{ ...mono, fontSize: "0.55rem", letterSpacing: "0.13em", textTransform: "uppercase", color: "var(--cream-1)" }}>Pick a model</span>
              </div>
              <span style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", color: "var(--cream-2)", display: "inline-flex", alignItems: "center", gap: "0.25rem" }}>
                <ShieldCheck style={{ width: "0.65rem", height: "0.65rem" }} /> private inference
              </span>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(13rem, 1fr))", gap: "0.65rem" }}>
              {ON_DEVICE_MODELS.map((m) => (
                <button key={m.id} onClick={() => handleLoad(m)} disabled={loading || hasWebGPU === false} style={{
                  textAlign: "left", padding: "0.85rem 1rem", background: engine?.modelId === m.id ? "rgba(196,152,90,0.07)" : "var(--ink-2)",
                  border: `1px solid ${engine?.modelId === m.id ? "var(--gold)" : "rgba(240,233,214,0.08)"}`,
                  cursor: loading || hasWebGPU === false ? "not-allowed" : "pointer", opacity: loading ? 0.6 : 1, transition: "all 0.2s",
                }}>
                  <div style={{ ...body, fontSize: "0.95rem", color: "var(--cream-0)", marginBottom: "0.2rem" }}>{m.label}</div>
                  <div style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.08em", color: "var(--cream-2)", marginBottom: "0.4rem" }}>{m.approxSizeMb} MB · cached after first load</div>
                  <div style={{ ...body, fontSize: "0.82rem", color: "var(--cream-2)", lineHeight: 1.4, display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical", overflow: "hidden" }}>{m.description}</div>
                </button>
              ))}
            </div>
            {loading && progress && (
              <div style={{ marginTop: "1rem" }}>
                <div style={{ height: "2px", background: "rgba(240,233,214,0.08)", overflow: "hidden" }}>
                  <div style={{ height: "100%", background: "var(--gold)", transition: "width 0.3s", width: `${Math.round(progress.progress * 100)}%` }} />
                </div>
                <p style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", color: "var(--cream-2)", marginTop: "0.5rem" }}>{progress.text}</p>
              </div>
            )}
          </div>

          {/* Chat */}
          <div style={{ flex: 1, background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.07)", display: "flex", flexDirection: "column", overflow: "hidden", minHeight: 0 }}>
            <div ref={scrollRef} className="thin-scrollbar" style={{ flex: 1, overflowY: "auto", padding: "1.25rem" }}>
              {!engine ? (
                <div style={{ height: "100%", display: "flex", alignItems: "center", justifyContent: "center", textAlign: "center" }}>
                  <p style={{ ...body, fontSize: "0.95rem", color: "var(--cream-2)" }}>Pick a model above to start chatting offline.</p>
                </div>
              ) : messages.length === 0 ? (
                <div style={{ height: "100%", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: "1rem", textAlign: "center" }}>
                  <Sparkles style={{ width: "1.4rem", height: "1.4rem", color: "var(--gold)" }} />
                  <p style={{ ...body, fontSize: "0.95rem", color: "var(--cream-1)" }}>Ready. Ask anything — runs entirely on your device.</p>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem", justifyContent: "center" }}>
                    {["Explain LoRA in three sentences.", "What's the intuition behind self-attention?", "Give me a quick comprehension check on transformers."].map((s) => (
                      <button key={s} onClick={() => setInput(s)} style={{ ...body, fontSize: "0.82rem", color: "var(--cream-1)", background: "none", border: "1px solid rgba(240,233,214,0.1)", padding: "0.35rem 0.75rem", cursor: "pointer", transition: "border-color 0.2s" }}
                        onMouseEnter={e => (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(196,152,90,0.4)"}
                        onMouseLeave={e => (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(240,233,214,0.1)"}>
                        {s}
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
                  {messages.map((m) => (
                    <div key={m.id} style={{ display: "flex", justifyContent: m.role === "user" ? "flex-end" : "flex-start" }}>
                      <div style={{
                        maxWidth: m.role === "user" ? "75%" : "85%",
                        background: m.role === "user" ? "rgba(196,152,90,0.15)" : "none",
                        border: m.role === "user" ? "1px solid rgba(196,152,90,0.25)" : "none",
                        padding: m.role === "user" ? "0.6rem 0.9rem" : "0",
                        ...body, fontSize: "0.95rem", color: "var(--cream-0)", lineHeight: 1.6, whiteSpace: "pre-wrap",
                      }}>
                        {m.content || (generating ? <span style={{ color: "var(--cream-2)", fontStyle: "italic" }}>thinking…</span> : null)}
                        {m.role === "assistant" && m.tokensPerSec && (
                          <div style={{ marginTop: "0.5rem", display: "inline-flex", alignItems: "center", gap: "0.3rem", ...mono, fontSize: "0.48rem", letterSpacing: "0.08em", color: "var(--cream-2)" }}>
                            <Cpu style={{ width: "0.65rem", height: "0.65rem" }} />
                            {m.tokensPerSec.toFixed(1)} tok/s · {(m.latencyMs! / 1000).toFixed(1)}s · on-device
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <form onSubmit={handleSend} style={{ borderTop: "1px solid rgba(240,233,214,0.07)", padding: "0.75rem", display: "flex", gap: "0.5rem" }}>
              <input value={input} onChange={(e) => setInput(e.target.value)} placeholder={engine ? "Ask the Pocket Tutor…" : "Load a model to start"} disabled={!engine || generating}
                style={{ flex: 1, padding: "0.6rem 0.85rem", background: "var(--ink-2)", border: "1px solid rgba(240,233,214,0.08)", outline: "none", ...body, fontSize: "0.9rem", color: "var(--cream-0)", opacity: (!engine || generating) ? 0.5 : 1 }} />
              {generating ? (
                <button type="button" onClick={() => abortRef.current?.abort()} style={{ ...mono, fontSize: "0.52rem", letterSpacing: "0.1em", textTransform: "uppercase", padding: "0 1rem", background: "none", border: "1px solid rgba(240,233,214,0.15)", cursor: "pointer", color: "var(--cream-1)" }}>Stop</button>
              ) : (
                <>
                  <button type="submit" disabled={!engine || !input.trim()} style={{ background: !engine || !input.trim() ? "rgba(196,152,90,0.3)" : "var(--gold)", border: "none", cursor: !engine || !input.trim() ? "not-allowed" : "pointer", color: "var(--ink)", padding: "0.6rem 0.85rem", display: "flex", alignItems: "center" }}>
                    <Send style={{ width: "0.9rem", height: "0.9rem" }} />
                  </button>
                  {messages.length > 0 && (
                    <button type="button" onClick={() => setMessages([])} style={{ background: "none", border: "1px solid rgba(240,233,214,0.1)", cursor: "pointer", color: "var(--cream-2)", padding: "0.6rem 0.75rem", display: "flex", alignItems: "center" }}>
                      <RotateCw style={{ width: "0.85rem", height: "0.85rem" }} />
                    </button>
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
