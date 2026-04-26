"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";
import {
  api,
  PeerOut,
  ResourceItem,
  ResourceRouterResponseT,
} from "@/lib/api";
import { AppHeader } from "@/components/AppHeader";
import { Button } from "@/components/ui/button";
import { usePresence } from "@/lib/usePresence";
import {
  Network,
  Loader2,
  Sparkles,
  Search,
  ExternalLink,
  Github,
  Youtube,
  FileText,
  Users,
  Hand,
  Bell,
  Wifi,
  Globe2,
} from "lucide-react";

type SourceFilter = "all" | "arxiv" | "github" | "youtube";

function StatusDot({ status }: { status: string }) {
  const color =
    status === "studying" ? "bg-emerald-500"
    : status === "stuck" ? "bg-amber-500"
    : status === "review" ? "bg-sky-500"
    : "bg-slate-400";
  return <span className={`inline-block h-2 w-2 rounded-full ${color}`} />;
}

function sourceIcon(src: string) {
  if (src === "github") return <Github className="h-4 w-4" />;
  if (src === "youtube") return <Youtube className="h-4 w-4" />;
  if (src === "arxiv") return <FileText className="h-4 w-4" />;
  return <Globe2 className="h-4 w-4" />;
}

export default function NetworkPage() {
  const router = useRouter();
  const [lookingForPair, setLookingForPair] = useState(false);
  const [note, setNote] = useState("");
  const [query, setQuery] = useState("");
  const [resources, setResources] = useState<ResourceRouterResponseT | null>(null);
  const [searching, setSearching] = useState(false);
  const [filter, setFilter] = useState<SourceFilter>("all");

  useEffect(() => {
    const token = getToken();
    if (!token) { router.push("/login"); return; }
  }, [router]);

  const { presence, livePeers, nudges, nudge, dismissNudge } = usePresence({
    status: lookingForPair ? "stuck" : "studying",
    lookingForPair,
    note,
  });

  async function handleSearch(e?: React.FormEvent) {
    e?.preventDefault();
    if (!query.trim()) return;
    const token = getToken();
    if (!token) return;
    setSearching(true);
    try {
      const data = await api.network.routeResources({ query }, token);
      setResources(data);
    } finally { setSearching(false); }
  }

  const filteredItems: ResourceItem[] = resources
    ? (filter === "all" ? resources.items : resources.items.filter((i) => i.source === filter))
    : [];

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      <AppHeader />
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-6xl mx-auto px-6 py-8 space-y-8">

          <header className="flex items-start justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
                <Network className="h-5 w-5" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">Connect the dots</h1>
                <p className="text-sm text-muted-foreground">
                  Live peer presence + a unified resource router pulling from arXiv, GitHub, and YouTube.
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <Wifi className="h-3.5 w-3.5 text-emerald-500" />
              <span>{livePeers.length} peer{livePeers.length === 1 ? "" : "s"} online</span>
            </div>
          </header>

          {/* Nudges */}
          {nudges.length > 0 && (
            <div className="space-y-2">
              {nudges
                .filter((n) => !presence || n.to === "" || n.to === presence.me.user_id)
                .slice(0, 3)
                .map((n) => (
                <div key={n.ts} className="flex items-center justify-between rounded-lg border border-primary/40 bg-primary/5 px-4 py-2 text-sm">
                  <span className="flex items-center gap-2">
                    <Bell className="h-4 w-4 text-primary" />
                    Nudge from a peer: “{n.message}”
                  </span>
                  <button onClick={() => dismissNudge(n.ts)} className="text-muted-foreground hover:text-foreground text-xs">
                    Dismiss
                  </button>
                </div>
              ))}
            </div>
          )}

          {/* Presence panel */}
          <section className="rounded-xl border border-border bg-card p-5">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Users className="h-4 w-4 text-primary" />
                <h2 className="font-semibold">Study peers</h2>
              </div>
              <label className="flex items-center gap-2 text-xs text-muted-foreground cursor-pointer">
                <input
                  type="checkbox"
                  checked={lookingForPair}
                  onChange={(e) => setLookingForPair(e.target.checked)}
                  className="rounded border-border"
                />
                <Hand className="h-3.5 w-3.5" /> I'm looking for a study buddy
              </label>
            </div>
            <input
              value={note}
              onChange={(e) => setNote(e.target.value)}
              placeholder="Optional public note (e.g. 'stuck on attention math')"
              maxLength={140}
              className="w-full px-3 py-2 mb-4 rounded-lg border border-border bg-background text-sm"
            />

            {livePeers.length === 0 ? (
              <p className="text-sm text-muted-foreground py-6 text-center">
                No peers online right now. Open a lesson and your presence will appear to others on the same lesson.
              </p>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {Array.from(
                  new Map(
                    livePeers
                      .filter((p) => !presence || p.user_id !== presence.me.user_id)
                      .map((p) => [p.user_id, p])
                  ).values()
                ).map((p) => <PeerCard key={p.user_id} peer={p}
                    onNudge={(msg) => nudge(p.user_id, msg)} />)}
              </div>
            )}
          </section>

          {/* Resource router */}
          <section className="rounded-xl border border-border bg-card p-5">
            <div className="flex items-center gap-2 mb-3">
              <Sparkles className="h-4 w-4 text-primary" />
              <h2 className="font-semibold">Resource router</h2>
            </div>
            <p className="text-sm text-muted-foreground mb-4">
              Pulls related papers, repos, and videos from public APIs and reranks them
              against your query — one click instead of three tabs.
            </p>
            <form onSubmit={handleSearch} className="flex gap-2 mb-4">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <input
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="e.g. 'low rank adaptation language models'"
                  className="w-full pl-10 pr-4 py-2.5 rounded-lg border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary/40"
                />
              </div>
              <Button type="submit" disabled={searching || !query.trim()}>
                {searching ? <Loader2 className="h-4 w-4 animate-spin" /> : "Route"}
              </Button>
            </form>

            {resources && (
              <>
                <div className="flex flex-wrap items-center gap-2 mb-4 text-xs">
                  <FilterChip active={filter === "all"} onClick={() => setFilter("all")}>
                    All ({resources.items.length})
                  </FilterChip>
                  {Object.entries(resources.by_source).map(([src, n]) => (
                    <FilterChip key={src} active={filter === src} onClick={() => setFilter(src as SourceFilter)}>
                      {src} ({n})
                    </FilterChip>
                  ))}
                  <span className="ml-auto text-muted-foreground">routed in {resources.elapsed_ms}ms</span>
                </div>

                {filteredItems.length === 0 ? (
                  <p className="text-sm text-muted-foreground py-6 text-center">No results for that filter.</p>
                ) : (
                  <ul className="space-y-3">
                    {filteredItems.map((item, i) => (
                      <li key={`${item.source}-${i}-${item.url}`} className="rounded-lg border border-border bg-background p-4 hover:border-primary/40 transition">
                        <div className="flex items-start justify-between gap-3">
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 text-xs text-muted-foreground mb-1">
                              {sourceIcon(item.source)}
                              <span className="capitalize">{item.source}</span>
                              {item.published && <span>· {item.published}</span>}
                              {item.stars !== undefined && <span>· {item.stars.toLocaleString()}★</span>}
                              {item.language && <span>· {item.language}</span>}
                              {item.channel && <span>· {item.channel}</span>}
                            </div>
                            <a href={item.url} target="_blank" rel="noopener noreferrer"
                               className="font-medium text-sm hover:text-primary inline-flex items-center gap-1">
                              {item.title}
                              <ExternalLink className="h-3 w-3 opacity-60" />
                            </a>
                            {item.snippet && <p className="text-xs text-muted-foreground mt-1.5 line-clamp-2">{item.snippet}</p>}
                            {item.authors && item.authors.length > 0 && (
                              <p className="text-xs text-muted-foreground mt-1">{item.authors.join(", ")}</p>
                            )}
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

function FilterChip({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button onClick={onClick}
      className={`rounded-full px-3 py-1 capitalize transition ${
        active
          ? "bg-primary text-primary-foreground"
          : "bg-muted text-muted-foreground hover:bg-muted/70"
      }`}>
      {children}
    </button>
  );
}

function PeerCard({ peer, onNudge }: { peer: PeerOut; onNudge: (msg: string) => void }) {
  const [showNudgeInput, setShowNudgeInput] = useState(false);
  const [draft, setDraft] = useState("Hey, want to tackle this together?");

  return (
    <div className="rounded-lg border border-border bg-background p-4">
      <div className="flex items-center gap-2 mb-2">
        <StatusDot status={peer.status} />
        <span className="font-medium text-sm truncate">{peer.display_name}</span>
        {peer.looking_for_pair && (
          <span className="ml-auto text-[10px] uppercase tracking-wide bg-amber-500/15 text-amber-700 dark:text-amber-300 rounded-full px-2 py-0.5">
            wants pair
          </span>
        )}
      </div>
      <div className="text-xs text-muted-foreground mb-2 truncate">
        {peer.lesson_id ? "studying a lesson" : "exploring"}
      </div>
      {peer.note && <p className="text-xs italic text-foreground/70 mb-3">“{peer.note}”</p>}
      {showNudgeInput ? (
        <div className="space-y-2">
          <input
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            className="w-full text-xs px-2 py-1.5 rounded border border-border bg-background"
            maxLength={140}
          />
          <div className="flex gap-1.5">
            <Button size="sm" variant="default" onClick={() => { onNudge(draft); setShowNudgeInput(false); }}>
              Send nudge
            </Button>
            <Button size="sm" variant="ghost" onClick={() => setShowNudgeInput(false)}>Cancel</Button>
          </div>
        </div>
      ) : (
        <Button size="sm" variant="outline" className="w-full" onClick={() => setShowNudgeInput(true)}>
          <Hand className="h-3 w-3 mr-1" /> Nudge
        </Button>
      )}
    </div>
  );
}
