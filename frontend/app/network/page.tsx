"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";
import { api, PeerOut, ResourceItem, ResourceRouterResponseT } from "@/lib/api";
import { AppHeader } from "@/components/AppHeader";
import { usePresence } from "@/lib/usePresence";
import { Loader2, Sparkles, Search, ExternalLink, Github, Youtube, FileText, Users, Hand, Bell, Wifi, Globe2 } from "lucide-react";

const mono: React.CSSProperties  = { fontFamily: "var(--font-dm-mono)" };
const serif: React.CSSProperties = { fontFamily: "var(--font-cormorant)" };
const body: React.CSSProperties  = { fontFamily: "var(--font-crimson)" };

type SourceFilter = "all" | "arxiv" | "github" | "youtube";

function StatusDot({ status }: { status: string }) {
  const color = status === "studying" ? "var(--sage-c)" : status === "stuck" ? "var(--gold)" : status === "review" ? "#60a5fa" : "var(--cream-2)";
  return <span style={{ display: "inline-block", width: "0.5rem", height: "0.5rem", borderRadius: "50%", background: color, flexShrink: 0 }} />;
}

function sourceIcon(src: string) {
  const s = { width: "0.85rem", height: "0.85rem", color: "var(--cream-2)" };
  if (src === "github") return <Github style={s} />;
  if (src === "youtube") return <Youtube style={s} />;
  if (src === "arxiv") return <FileText style={s} />;
  return <Globe2 style={s} />;
}

function FilterChip({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button onClick={onClick} style={{
      ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase",
      padding: "0.25rem 0.65rem", background: active ? "var(--gold)" : "none", color: active ? "var(--ink)" : "var(--cream-2)",
      border: `1px solid ${active ? "var(--gold)" : "rgba(240,233,214,0.12)"}`, cursor: "pointer", transition: "all 0.2s",
    }}>{children}</button>
  );
}

export default function NetworkPage() {
  const router = useRouter();
  const [lookingForPair, setLookingForPair] = useState(false);
  const [note, setNote] = useState("");
  const [query, setQuery] = useState("");
  const [resources, setResources] = useState<ResourceRouterResponseT | null>(null);
  const [searching, setSearching] = useState(false);
  const [filter, setFilter] = useState<SourceFilter>("all");

  useEffect(() => { const token = getToken(); if (!token) { router.push("/login"); return; } }, [router]);
  const { presence, livePeers, nudges, nudge, dismissNudge } = usePresence({ status: lookingForPair ? "stuck" : "studying", lookingForPair, note });

  async function handleSearch(e?: React.FormEvent) {
    e?.preventDefault();
    if (!query.trim()) return;
    const token = getToken(); if (!token) return;
    setSearching(true);
    try { const data = await api.network.routeResources({ query }, token); setResources(data); } finally { setSearching(false); }
  }

  const filteredItems: ResourceItem[] = resources ? (filter === "all" ? resources.items : resources.items.filter((i) => i.source === filter)) : [];

  return (
    <div className="flex flex-col h-screen overflow-hidden" style={{ background: "var(--ink)", color: "var(--cream-0)" }}>
      <AppHeader />
      <main className="flex-1 overflow-y-auto thin-scrollbar">
        <div style={{ maxWidth: "64rem", margin: "0 auto", padding: "2.5rem 1.5rem 4rem" }}>

          {/* Header */}
          <div style={{ marginBottom: "2.5rem" }}>
            <p style={{ ...mono, fontSize: "0.58rem", letterSpacing: "0.16em", textTransform: "uppercase", color: "var(--gold)", marginBottom: "0.5rem" }}>Network</p>
            <h1 style={{ ...serif, fontWeight: 700, fontStyle: "italic", fontSize: "clamp(2rem,5vw,3rem)", color: "var(--cream-0)", lineHeight: 1.1, marginBottom: "0.4rem" }}>
              Connect the dots<span style={{ color: "var(--gold)" }}>.</span>
            </h1>
            <p style={{ ...body, fontSize: "1rem", color: "var(--cream-1)", lineHeight: 1.6 }}>
              Live peer presence + a unified resource router pulling from arXiv, GitHub, and YouTube.
            </p>
          </div>

          {/* Nudges */}
          {nudges.filter((n) => !presence || n.to === "" || n.to === presence.me.user_id).slice(0, 3).map((n) => (
            <div key={n.ts} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", background: "rgba(196,152,90,0.07)", border: "1px solid rgba(196,152,90,0.3)", padding: "0.65rem 1rem", marginBottom: "0.75rem" }}>
              <span style={{ ...body, fontSize: "0.9rem", color: "var(--cream-1)", display: "flex", alignItems: "center", gap: "0.5rem" }}>
                <Bell style={{ width: "0.8rem", height: "0.8rem", color: "var(--gold)" }} />
                Nudge from a peer: "{n.message}"
              </span>
              <button onClick={() => dismissNudge(n.ts)} style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", background: "none", border: "none", cursor: "pointer", color: "var(--cream-2)" }}>Dismiss</button>
            </div>
          ))}

          {/* Study peers */}
          <section style={{ background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.07)", padding: "1.5rem", marginBottom: "1.5rem" }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "1rem" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                <Users style={{ width: "0.85rem", height: "0.85rem", color: "var(--gold)" }} />
                <span style={{ ...mono, fontSize: "0.58rem", letterSpacing: "0.14em", textTransform: "uppercase", color: "var(--cream-1)" }}>Study Peers</span>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                <Wifi style={{ width: "0.7rem", height: "0.7rem", color: "var(--sage-c)" }} />
                <span style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", color: "var(--cream-2)" }}>{livePeers.length} online</span>
              </div>
            </div>

            <label style={{ display: "flex", alignItems: "center", gap: "0.5rem", cursor: "pointer", marginBottom: "0.75rem" }}>
              <input type="checkbox" checked={lookingForPair} onChange={(e) => setLookingForPair(e.target.checked)} style={{ accentColor: "var(--gold)" }} />
              <Hand style={{ width: "0.7rem", height: "0.7rem", color: "var(--cream-2)" }} />
              <span style={{ ...mono, fontSize: "0.52rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)" }}>I'm looking for a study buddy</span>
            </label>

            <input value={note} onChange={(e) => setNote(e.target.value)} placeholder="Optional public note (e.g. 'stuck on attention math')" maxLength={140}
              style={{ width: "100%", padding: "0.6rem 0.85rem", background: "var(--ink-2)", border: "1px solid rgba(240,233,214,0.08)", outline: "none", ...body, fontSize: "0.9rem", color: "var(--cream-0)", marginBottom: "1rem", boxSizing: "border-box" }} />

            {livePeers.length === 0 ? (
              <p style={{ ...body, fontSize: "0.9rem", color: "var(--cream-2)", textAlign: "center", padding: "1.5rem 0" }}>
                No peers online right now. Open a lesson and your presence will appear to others.
              </p>
            ) : (
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(14rem, 1fr))", gap: "0.75rem" }}>
                {Array.from(new Map(livePeers.filter((p) => !presence || p.user_id !== presence.me.user_id).map((p) => [p.user_id, p])).values()).map((p) => (
                  <PeerCard key={p.user_id} peer={p} onNudge={(msg) => nudge(p.user_id, msg)} />
                ))}
              </div>
            )}
          </section>

          {/* Resource router */}
          <section style={{ background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.07)", padding: "1.5rem" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.5rem" }}>
              <Sparkles style={{ width: "0.8rem", height: "0.8rem", color: "var(--gold)" }} />
              <span style={{ ...mono, fontSize: "0.58rem", letterSpacing: "0.14em", textTransform: "uppercase", color: "var(--cream-1)" }}>Resource Router</span>
            </div>
            <p style={{ ...body, fontSize: "0.9rem", color: "var(--cream-2)", marginBottom: "1rem", lineHeight: 1.6 }}>
              Pulls related papers, repos, and videos from public APIs — one click instead of three tabs.
            </p>
            <form onSubmit={handleSearch} style={{ display: "flex", gap: "0.75rem", marginBottom: "1rem" }}>
              <div style={{ position: "relative", flex: 1 }}>
                <Search style={{ position: "absolute", left: "0.75rem", top: "50%", transform: "translateY(-50%)", width: "0.8rem", height: "0.8rem", color: "var(--cream-2)" }} />
                <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="e.g. 'low rank adaptation language models'"
                  style={{ width: "100%", paddingLeft: "2.2rem", paddingRight: "0.85rem", paddingTop: "0.6rem", paddingBottom: "0.6rem", background: "var(--ink-2)", border: "1px solid rgba(240,233,214,0.08)", outline: "none", ...body, fontSize: "0.9rem", color: "var(--cream-0)", boxSizing: "border-box" }} />
              </div>
              <button type="submit" disabled={searching || !query.trim()} style={{ ...mono, fontSize: "0.58rem", letterSpacing: "0.13em", textTransform: "uppercase", padding: "0 1.25rem", background: searching || !query.trim() ? "rgba(196,152,90,0.3)" : "var(--gold)", color: searching || !query.trim() ? "var(--cream-2)" : "var(--ink)", border: "none", cursor: searching || !query.trim() ? "not-allowed" : "pointer", display: "flex", alignItems: "center", gap: "0.4rem", flexShrink: 0 }}>
                {searching ? <Loader2 style={{ width: "0.8rem", height: "0.8rem" }} className="animate-spin" /> : "Route"}
              </button>
            </form>

            {resources && (
              <>
                <div style={{ display: "flex", flexWrap: "wrap", gap: "0.4rem", marginBottom: "1rem", alignItems: "center" }}>
                  <FilterChip active={filter === "all"} onClick={() => setFilter("all")}>All ({resources.items.length})</FilterChip>
                  {Object.entries(resources.by_source).map(([src, n]) => (
                    <FilterChip key={src} active={filter === src as SourceFilter} onClick={() => setFilter(src as SourceFilter)}>{src} ({n})</FilterChip>
                  ))}
                  <span style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", color: "var(--cream-2)", marginLeft: "auto" }}>routed in {resources.elapsed_ms}ms</span>
                </div>
                {filteredItems.length === 0 ? (
                  <p style={{ ...body, fontSize: "0.9rem", color: "var(--cream-2)", textAlign: "center", padding: "1.5rem 0" }}>No results for that filter.</p>
                ) : (
                  <ul style={{ display: "flex", flexDirection: "column", gap: "0.5rem", listStyle: "none", padding: 0, margin: 0 }}>
                    {filteredItems.map((item, i) => (
                      <li key={`${item.source}-${i}-${item.url}`} style={{ padding: "0.9rem 1rem", background: "var(--ink-2)", border: "1px solid rgba(240,233,214,0.06)", transition: "border-color 0.2s" }}
                        onMouseEnter={e => (e.currentTarget as HTMLLIElement).style.borderColor = "rgba(196,152,90,0.3)"}
                        onMouseLeave={e => (e.currentTarget as HTMLLIElement).style.borderColor = "rgba(240,233,214,0.06)"}>
                        <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: "1rem" }}>
                          <div style={{ flex: 1, minWidth: 0 }}>
                            <div style={{ display: "flex", alignItems: "center", gap: "0.4rem", marginBottom: "0.35rem" }}>
                              {sourceIcon(item.source)}
                              <span style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)" }}>{item.source}</span>
                              {item.published && <span style={{ ...mono, fontSize: "0.5rem", color: "var(--cream-2)" }}>· {item.published}</span>}
                              {item.stars !== undefined && <span style={{ ...mono, fontSize: "0.5rem", color: "var(--cream-2)" }}>· {item.stars.toLocaleString()}★</span>}
                            </div>
                            <a href={item.url} target="_blank" rel="noopener noreferrer" style={{ ...body, fontSize: "0.95rem", color: "var(--cream-0)", textDecoration: "none", display: "inline-flex", alignItems: "center", gap: "0.3rem", transition: "color 0.2s" }}
                              onMouseEnter={e => (e.currentTarget as HTMLAnchorElement).style.color = "var(--gold)"}
                              onMouseLeave={e => (e.currentTarget as HTMLAnchorElement).style.color = "var(--cream-0)"}>
                              {item.title}
                              <ExternalLink style={{ width: "0.65rem", height: "0.65rem", opacity: 0.6 }} />
                            </a>
                            {item.snippet && <p style={{ ...body, fontSize: "0.82rem", color: "var(--cream-2)", marginTop: "0.3rem", lineHeight: 1.5, display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical", overflow: "hidden" }}>{item.snippet}</p>}
                            {item.authors && item.authors.length > 0 && <p style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.08em", color: "var(--cream-2)", marginTop: "0.25rem" }}>{item.authors.join(", ")}</p>}
                          </div>
                        </div>
                      </li>
                    ))}
                  </ul>
                )}
              </>
            )}
          </section>
        </div>
      </main>
    </div>
  );
}

function PeerCard({ peer, onNudge }: { peer: PeerOut; onNudge: (msg: string) => void }) {
  const [showNudge, setShowNudge] = useState(false);
  const [draft, setDraft] = useState("Hey, want to tackle this together?");
  const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };
  const body: React.CSSProperties = { fontFamily: "var(--font-crimson)" };
  return (
    <div style={{ padding: "0.9rem", background: "var(--ink-2)", border: "1px solid rgba(240,233,214,0.06)" }}>
      <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.4rem" }}>
        <StatusDot status={peer.status} />
        <span style={{ ...body, fontSize: "0.95rem", color: "var(--cream-0)", flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{peer.display_name}</span>
        {peer.looking_for_pair && <span style={{ ...mono, fontSize: "0.45rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--gold)", border: "1px solid rgba(196,152,90,0.4)", padding: "0.1rem 0.35rem" }}>wants pair</span>}
      </div>
      <p style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.08em", color: "var(--cream-2)", marginBottom: peer.note ? "0.4rem" : "0.75rem" }}>{peer.lesson_id ? "studying a lesson" : "exploring"}</p>
      {peer.note && <p style={{ ...body, fontSize: "0.82rem", fontStyle: "italic", color: "var(--cream-1)", marginBottom: "0.75rem" }}>"{peer.note}"</p>}
      {showNudge ? (
        <div style={{ display: "flex", flexDirection: "column", gap: "0.4rem" }}>
          <input value={draft} onChange={(e) => setDraft(e.target.value)} maxLength={140}
            style={{ padding: "0.4rem 0.6rem", background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.1)", outline: "none", ...body, fontSize: "0.82rem", color: "var(--cream-0)" }} />
          <div style={{ display: "flex", gap: "0.4rem" }}>
            <button onClick={() => { onNudge(draft); setShowNudge(false); }} style={{ flex: 1, padding: "0.35rem", background: "var(--gold)", border: "none", cursor: "pointer", ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--ink)" }}>Send</button>
            <button onClick={() => setShowNudge(false)} style={{ padding: "0.35rem 0.65rem", background: "none", border: "1px solid rgba(240,233,214,0.1)", cursor: "pointer", ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)" }}>Cancel</button>
          </div>
        </div>
      ) : (
        <button onClick={() => setShowNudge(true)} style={{ width: "100%", padding: "0.4rem", background: "none", border: "1px solid rgba(240,233,214,0.12)", cursor: "pointer", ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)", display: "flex", alignItems: "center", justifyContent: "center", gap: "0.35rem", transition: "border-color 0.2s, color 0.2s" }}
          onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(196,152,90,0.4)"; (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-1)"; }}
          onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(240,233,214,0.12)"; (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-2)"; }}>
          <Hand style={{ width: "0.65rem", height: "0.65rem" }} /> Nudge
        </button>
      )}
    </div>
  );
}
