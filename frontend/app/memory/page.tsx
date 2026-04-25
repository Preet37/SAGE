"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";
import { api, MemoryHitResponse, MemoryItemResponse } from "@/lib/api";
import { AppHeader } from "@/components/AppHeader";
import { Button } from "@/components/ui/button";
import { Brain, Search, Trash2, Loader2, Sparkles } from "lucide-react";

function relTime(iso: string | null | undefined): string {
  if (!iso) return "";
  const d = new Date(iso);
  const diff = (Date.now() - d.getTime()) / 1000;
  if (diff < 60) return "just now";
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`;
  return d.toLocaleDateString();
}

export default function MemoryPage() {
  const router = useRouter();
  const [items, setItems] = useState<MemoryItemResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [enabled, setEnabled] = useState(true);
  const [query, setQuery] = useState("");
  const [hits, setHits] = useState<MemoryHitResponse[] | null>(null);
  const [searching, setSearching] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    const token = getToken();
    if (!token) { router.push("/login"); return; }
    setLoading(true);
    try {
      const data = await api.cognition.listMemory(token, undefined, 100);
      setItems(data.items);
      setEnabled(data.enabled);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load memory");
    } finally {
      setLoading(false);
    }
  }, [router]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  async function handleSearch(e?: React.FormEvent) {
    e?.preventDefault();
    if (!query.trim()) { setHits(null); return; }
    const token = getToken();
    if (!token) return;
    setSearching(true);
    try {
      const data = await api.cognition.recall(query, token, { k: 8 });
      setHits(data.hits);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Search failed");
    } finally {
      setSearching(false);
    }
  }

  async function handleDelete(id: string) {
    const token = getToken();
    if (!token) return;
    await api.cognition.deleteMemory(id, token);
    setItems((prev) => prev.filter((i) => i.id !== id));
    if (hits) setHits(hits.filter((h) => h.id !== id));
  }

  async function handleClearAll() {
    if (!confirm("Erase all stored memory? This cannot be undone.")) return;
    const token = getToken();
    if (!token) return;
    await api.cognition.clearMemory(token);
    setItems([]);
    setHits(null);
  }

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      <AppHeader />
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-6 py-8">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
                <Brain className="h-5 w-5" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">Memory</h1>
                <p className="text-sm text-muted-foreground">
                  Cross-session context the tutor recalls automatically.
                </p>
              </div>
            </div>
            {items.length > 0 && (
              <Button variant="outline" size="sm" onClick={handleClearAll}>
                <Trash2 className="h-4 w-4 mr-1.5" /> Clear all
              </Button>
            )}
          </div>

          {!enabled && (
            <div className="rounded-lg border border-amber-500/40 bg-amber-50 dark:bg-amber-950/20 px-4 py-3 text-sm text-amber-700 dark:text-amber-300 mb-6">
              Semantic memory is currently disabled in <code>settings.yaml</code>.
            </div>
          )}

          <form onSubmit={handleSearch} className="flex gap-2 mb-6">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Recall a topic, concept, or question you discussed before..."
                className="w-full pl-10 pr-4 py-2.5 rounded-lg border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary/40"
              />
            </div>
            <Button type="submit" disabled={searching || !query.trim()}>
              {searching ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4 mr-1.5" />}
              Recall
            </Button>
            {hits && (
              <Button type="button" variant="ghost" onClick={() => { setHits(null); setQuery(""); }}>
                Clear
              </Button>
            )}
          </form>

          {error && (
            <div className="rounded-lg border border-destructive/40 bg-destructive/10 px-4 py-3 text-sm text-destructive mb-6">
              {error}
            </div>
          )}

          {loading ? (
            <div className="flex items-center justify-center py-20 text-muted-foreground">
              <Loader2 className="h-5 w-5 animate-spin" />
            </div>
          ) : (
            <div className="space-y-3">
              {hits ? (
                hits.length === 0 ? (
                  <p className="text-sm text-muted-foreground py-8 text-center">
                    No matching memories. Try a different phrasing.
                  </p>
                ) : (
                  hits.map((h) => (
                    <MemoryCard key={h.id}
                      role={h.role} content={h.content}
                      created_at={h.created_at} score={h.score}
                      onDelete={() => handleDelete(h.id)}
                    />
                  ))
                )
              ) : items.length === 0 ? (
                <div className="rounded-xl border border-dashed border-border bg-muted/30 p-10 text-center">
                  <Brain className="h-8 w-8 text-muted-foreground mx-auto mb-3" />
                  <p className="text-sm text-muted-foreground">
                    No memories yet. Chat with the tutor and significant turns
                    will be saved here automatically.
                  </p>
                </div>
              ) : (
                items.map((m) => (
                  <MemoryCard key={m.id}
                    role={m.role} content={m.content}
                    created_at={m.created_at} importance={m.importance}
                    onDelete={() => handleDelete(m.id)}
                  />
                ))
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

interface CardProps {
  role: string;
  content: string;
  created_at: string | null;
  score?: number;
  importance?: number;
  onDelete: () => void;
}

function MemoryCard({ role, content, created_at, score, importance, onDelete }: CardProps) {
  return (
    <div className="rounded-xl border border-border bg-card p-4 hover:border-primary/40 transition">
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1.5 text-xs">
            <span className={`rounded-full px-2 py-0.5 font-medium ${
              role === "user"
                ? "bg-primary/10 text-primary"
                : "bg-emerald-500/10 text-emerald-700 dark:text-emerald-300"
            }`}>
              {role === "user" ? "You" : "Tutor"}
            </span>
            <span className="text-muted-foreground">{relTime(created_at)}</span>
            {score !== undefined && (
              <span className="text-muted-foreground">· match {Math.round(score * 100)}%</span>
            )}
            {importance !== undefined && score === undefined && (
              <span className="text-muted-foreground">· importance {Math.round(importance * 100)}%</span>
            )}
          </div>
          <p className="text-sm text-foreground/90 whitespace-pre-wrap leading-relaxed line-clamp-5">
            {content}
          </p>
        </div>
        <button
          onClick={onDelete}
          className="text-muted-foreground hover:text-destructive transition"
          aria-label="Delete memory"
        >
          <Trash2 className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}
