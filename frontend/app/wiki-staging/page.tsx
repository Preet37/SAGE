"use client";
import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Check, X, FileQuestion, RefreshCw, Loader2 } from "lucide-react";
import { api, WikiStagingItemResponse } from "@/lib/api";
import { getToken } from "@/lib/auth";

export default function WikiStagingPage() {
  const router = useRouter();
  const [items, setItems] = useState<WikiStagingItemResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await api.wikiStaging.list(token);
      setItems(res.items);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load staging queue");
    } finally {
      setLoading(false);
    }
  }, [router]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  async function handleAct(filename: string, action: "approve" | "reject") {
    const token = getToken();
    if (!token) return;
    setBusy(filename);
    try {
      if (action === "approve") {
        await api.wikiStaging.approve(filename, token);
      } else {
        await api.wikiStaging.reject(filename, token);
      }
      setItems((prev) => prev.filter((i) => i.filename !== filename));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Action failed");
    } finally {
      setBusy(null);
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-8">
      <div className="flex items-start justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Wiki staging</h1>
          <p className="text-sm text-muted-foreground mt-1">
            Review wiki changes proposed by the enrichment pipeline before they
            land in the canonical wiki.
          </p>
        </div>
        <button
          onClick={refresh}
          disabled={loading}
          aria-label="Refresh staging queue"
          className="inline-flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg border border-border text-muted-foreground hover:text-foreground hover:bg-muted transition-colors disabled:opacity-50"
        >
          <RefreshCw className={`h-3 w-3 ${loading ? "animate-spin" : ""}`} />
          Refresh
        </button>
      </div>

      {error && (
        <div className="mb-4 rounded-lg border border-rose-200 bg-rose-50 dark:border-rose-900 dark:bg-rose-950/40 px-4 py-3 text-sm text-rose-700 dark:text-rose-300">
          {error}
        </div>
      )}

      {loading && items.length === 0 ? (
        <div className="flex items-center gap-2 text-sm text-muted-foreground py-12 justify-center">
          <Loader2 className="h-4 w-4 animate-spin" />
          Loading staging queue...
        </div>
      ) : items.length === 0 ? (
        <div className="text-center py-16 text-muted-foreground">
          <FileQuestion className="h-10 w-10 mx-auto mb-3 opacity-50" />
          <p className="text-sm">Nothing pending review.</p>
        </div>
      ) : (
        <ul className="space-y-3">
          {items.map((item) => (
            <li
              key={item.filename}
              className="rounded-xl border border-border bg-card/60 p-4"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2 text-xs text-muted-foreground mb-1">
                    <span className="font-mono px-1.5 py-0.5 rounded bg-muted">
                      {item.type}
                    </span>
                    <span>{item.timestamp}</span>
                    {item.course && <span>· {item.course}</span>}
                  </div>
                  <h2 className="text-sm font-semibold text-foreground truncate">
                    {item.topic_slug || "(no slug)"}
                  </h2>
                  <p className="text-xs text-muted-foreground mt-1">{item.summary}</p>
                </div>
                <div className="flex items-center gap-1.5 flex-shrink-0">
                  <button
                    onClick={() => handleAct(item.filename, "reject")}
                    disabled={busy === item.filename}
                    aria-label={`Reject ${item.topic_slug}`}
                    className="inline-flex items-center gap-1 text-xs px-3 py-1.5 rounded-lg border border-border text-muted-foreground hover:text-rose-600 hover:border-rose-300 transition-colors disabled:opacity-50"
                  >
                    <X className="h-3 w-3" /> Reject
                  </button>
                  <button
                    onClick={() => handleAct(item.filename, "approve")}
                    disabled={busy === item.filename}
                    aria-label={`Approve ${item.topic_slug}`}
                    className="inline-flex items-center gap-1 text-xs px-3 py-1.5 rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 transition-colors disabled:opacity-50"
                  >
                    {busy === item.filename ? (
                      <Loader2 className="h-3 w-3 animate-spin" />
                    ) : (
                      <Check className="h-3 w-3" />
                    )}
                    Approve
                  </button>
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
