"use client";

import { useEffect, useState, useCallback, useRef } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";
import { api } from "@/lib/api";
import type { DocumentOut, DocumentDetail } from "@/lib/api";
import { AppHeader } from "@/components/AppHeader";
import { Button } from "@/components/ui/button";
import {
  FolderOpen, Upload, Search, Trash2, Loader2, FileText, FileVideo,
  ChevronDown, ChevronUp, X, Brain, Sparkles, Eraser, Zap, Tag,
} from "lucide-react";
import { cn } from "@/lib/utils";

// ── Helpers ──────────────────────────────────────────────────────────────────

function relTime(iso: string): string {
  const diff = (Date.now() - new Date(iso).getTime()) / 1000;
  if (diff < 60) return "just now";
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return new Date(iso).toLocaleDateString();
}

function fmtBytes(n: number): string {
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / (1024 * 1024)).toFixed(1)} MB`;
}

function extOf(filename: string): string {
  return filename.split(".").pop()?.toUpperCase() ?? "FILE";
}

// Color palette for doc_type badges
const DOC_TYPE_COLORS: Record<string, string> = {
  "Research Paper":      "bg-violet-500/15 text-violet-700 dark:text-violet-300",
  "Lecture Notes":       "bg-blue-500/15 text-blue-700 dark:text-blue-300",
  "Textbook Chapter":    "bg-emerald-500/15 text-emerald-700 dark:text-emerald-300",
  "Presentation":        "bg-amber-500/15 text-amber-700 dark:text-amber-300",
  "Study Guide":         "bg-cyan-500/15 text-cyan-700 dark:text-cyan-300",
  "Code/Technical":      "bg-pink-500/15 text-pink-700 dark:text-pink-300",
  "Image/Diagram":       "bg-orange-500/15 text-orange-700 dark:text-orange-300",
  "Video Transcript":    "bg-red-500/15 text-red-700 dark:text-red-300",
  "General Notes":       "bg-zinc-500/15 text-zinc-700 dark:text-zinc-300",
  "Other":               "bg-zinc-500/15 text-zinc-600 dark:text-zinc-400",
};
function docTypeColor(t: string) {
  return DOC_TYPE_COLORS[t] ?? DOC_TYPE_COLORS["Other"];
}

const ACCEPTED = [
  ".pdf", ".docx", ".doc", ".pptx", ".ppt",
  ".txt", ".md", ".csv",
  ".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif",
  ".mp4", ".mov", ".webm", ".mp3", ".wav", ".m4a",
].join(",");

// ── Image viewer ─────────────────────────────────────────────────────────────

type ImgTab = "original" | "enhanced" | "nobg";

function ImageViewer({ doc }: { doc: DocumentOut }) {
  const [tab, setTab] = useState<ImgTab>("original");
  const src =
    tab === "enhanced" ? doc.enhanced_url :
    tab === "nobg"     ? doc.nobg_url :
    doc.thumbnail_url;
  if (!src) return null;

  const tabs: { key: ImgTab; label: string; available: boolean }[] = [
    { key: "original",  label: "Original",  available: !!doc.thumbnail_url },
    { key: "enhanced",  label: "Enhanced",  available: !!doc.enhanced_url },
    { key: "nobg",      label: "No BG",     available: !!doc.nobg_url },
  ];

  return (
    <div className="mt-3">
      <div className="flex gap-1 mb-2">
        {tabs.filter(t => t.available).map(t => (
          <button
            key={t.key}
            onClick={() => setTab(t.key)}
            className={cn(
              "text-[11px] px-2.5 py-1 rounded-full border font-medium transition-all",
              tab === t.key
                ? "bg-primary text-primary-foreground border-primary"
                : "border-border text-muted-foreground hover:border-primary/50"
            )}
          >
            {t.label}
          </button>
        ))}
      </div>
      {/* checkerboard bg for transparent images */}
      <div className="rounded-xl overflow-hidden border border-border"
           style={{ background: "repeating-conic-gradient(#ddd 0% 25%, #fff 0% 50%) 0 0 / 16px 16px" }}>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={src} alt={tab} className="max-h-64 mx-auto object-contain block" />
      </div>
    </div>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────────

export default function MyDocumentsPage() {
  const router = useRouter();
  const [docs, setDocs] = useState<DocumentOut[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [uploadMsg, setUploadMsg] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<string | null>(null);
  const [detail, setDetail] = useState<DocumentDetail | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const refresh = useCallback(async () => {
    const token = getToken();
    if (!token) { router.push("/login"); return; }
    setLoading(true);
    try {
      setDocs(await api.documents.list(token));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load");
    } finally {
      setLoading(false);
    }
  }, [router]);

  useEffect(() => { refresh(); }, [refresh]);

  async function handleFiles(files: FileList | null) {
    if (!files || files.length === 0) return;
    const token = getToken();
    if (!token) return;
    setError(null);
    const arr = Array.from(files);
    for (const file of arr) {
      setUploading(true);
      setUploadMsg(`Parsing & classifying "${file.name}"…`);
      try {
        const doc = await api.documents.upload(file, token);
        setDocs(prev => [doc, ...prev]);
      } catch (e) {
        setError(e instanceof Error ? e.message : `Failed: ${file.name}`);
      }
    }
    setUploading(false);
    setUploadMsg(null);
  }

  async function handleDelete(id: string) {
    if (!confirm("Remove this document from memory?")) return;
    const token = getToken();
    if (!token) return;
    await api.documents.delete(id, token);
    setDocs(prev => prev.filter(d => d.id !== id));
    if (expanded === id) { setExpanded(null); setDetail(null); }
  }

  async function toggleExpand(id: string) {
    if (expanded === id) { setExpanded(null); setDetail(null); return; }
    setExpanded(id);
    setDetail(null);
    const token = getToken();
    if (!token) return;
    setDetailLoading(true);
    try {
      setDetail(await api.documents.get(id, token));
    } catch { /* ignore */ }
    finally { setDetailLoading(false); }
  }

  const filtered = docs.filter(d =>
    !searchQuery ||
    d.filename.toLowerCase().includes(searchQuery.toLowerCase()) ||
    d.subject.toLowerCase().includes(searchQuery.toLowerCase()) ||
    d.summary.toLowerCase().includes(searchQuery.toLowerCase()) ||
    d.key_topics.some(t => t.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      <AppHeader />
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-6 py-8">

          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
                <FolderOpen className="h-5 w-5" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">My Documents</h1>
                <p className="text-sm text-muted-foreground">
                  Upload anything — SAGE parses, classifies, and remembers it for your sessions.
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2 text-xs text-muted-foreground bg-muted/40 rounded-lg px-3 py-2">
              <Brain className="h-3.5 w-3.5" />
              <span>{docs.length} doc{docs.length !== 1 ? "s" : ""} in memory</span>
            </div>
          </div>

          {/* Drop zone */}
          <div
            className={cn(
              "rounded-xl border-2 border-dashed transition-all mb-6 cursor-pointer select-none",
              dragOver ? "border-primary bg-primary/5 scale-[1.01]"
                       : "border-border hover:border-primary/50 hover:bg-muted/20",
            )}
            onClick={() => !uploading && inputRef.current?.click()}
            onDragOver={e => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={e => { e.preventDefault(); setDragOver(false); handleFiles(e.dataTransfer.files); }}
          >
            <div className="flex flex-col items-center justify-center py-10 gap-2">
              {uploading ? (
                <>
                  <Loader2 className="h-8 w-8 animate-spin text-primary" />
                  <p className="text-sm font-medium text-primary">{uploadMsg}</p>
                  <p className="text-xs text-muted-foreground">Extracting text · Classifying · Processing images…</p>
                </>
              ) : (
                <>
                  <Upload className="h-8 w-8 text-muted-foreground" />
                  <p className="text-sm font-semibold">Drop files here or click to upload</p>
                  <div className="flex flex-wrap justify-center gap-1.5 mt-1">
                    {["PDF","DOCX","PPTX","TXT","MD","CSV","PNG","JPG","WEBP","MP4","MP3"].map(f => (
                      <span key={f} className="text-[10px] px-1.5 py-0.5 rounded bg-muted text-muted-foreground font-mono">{f}</span>
                    ))}
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">Max 50 MB · Images get auto-enhanced &amp; background removed</p>
                </>
              )}
            </div>
            <input ref={inputRef} type="file" multiple accept={ACCEPTED}
              className="hidden" onChange={e => handleFiles(e.target.files)} />
          </div>

          {/* Search */}
          {docs.length > 0 && (
            <div className="relative mb-5">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                placeholder="Search by name, subject, or topic…"
                className="w-full pl-10 pr-10 py-2.5 rounded-lg border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary/40"
              />
              {searchQuery && (
                <button onClick={() => setSearchQuery("")}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground">
                  <X className="h-4 w-4" />
                </button>
              )}
            </div>
          )}

          {error && (
            <div className="rounded-lg border border-destructive/40 bg-destructive/10 px-4 py-3 text-sm text-destructive mb-5 flex items-center justify-between">
              <span>{error}</span>
              <button onClick={() => setError(null)}><X className="h-4 w-4" /></button>
            </div>
          )}

          {/* Document list */}
          {loading ? (
            <div className="flex items-center justify-center py-20 text-muted-foreground">
              <Loader2 className="h-5 w-5 animate-spin" />
            </div>
          ) : filtered.length === 0 ? (
            <div className="rounded-xl border border-dashed border-border bg-muted/30 p-10 text-center">
              <FolderOpen className="h-8 w-8 text-muted-foreground mx-auto mb-3" />
              <p className="text-sm text-muted-foreground">
                {searchQuery ? "No documents match your search." : "No documents yet — upload your first file above."}
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {filtered.map(doc => {
                const Icon = doc.mime.startsWith("video/") || doc.mime.startsWith("audio/") ? FileVideo : FileText;
                const isOpen = expanded === doc.id;
                return (
                  <div key={doc.id}
                    className="rounded-xl border border-border bg-card hover:border-primary/30 transition overflow-hidden">

                    {/* Main row */}
                    <div className="flex gap-3 px-4 py-3">
                      {/* Thumbnail or icon */}
                      {doc.is_image && doc.thumbnail_url ? (
                        // eslint-disable-next-line @next/next/no-img-element
                        <img src={doc.thumbnail_url} alt={doc.filename}
                          className="h-12 w-12 rounded-lg object-cover flex-shrink-0 border border-border" />
                      ) : (
                        <div className="h-12 w-12 rounded-lg bg-primary/10 text-primary flex items-center justify-center flex-shrink-0">
                          <Icon className="h-5 w-5" />
                        </div>
                      )}

                      <div className="flex-1 min-w-0">
                        {/* Filename + badges */}
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="font-semibold text-sm truncate max-w-[240px]">{doc.filename}</span>
                          <span className="text-[10px] px-1.5 py-0.5 rounded bg-muted text-muted-foreground font-mono uppercase">
                            {extOf(doc.filename)}
                          </span>
                          {doc.doc_type && doc.doc_type !== "Other" && (
                            <span className={cn("text-[10px] px-2 py-0.5 rounded-full font-medium", docTypeColor(doc.doc_type))}>
                              {doc.doc_type}
                            </span>
                          )}
                          {doc.subject && (
                            <span className="text-[10px] px-2 py-0.5 rounded-full bg-muted text-muted-foreground font-medium">
                              {doc.subject}
                            </span>
                          )}
                        </div>

                        {/* Meta row */}
                        <div className="flex items-center gap-2 mt-0.5 text-xs text-muted-foreground flex-wrap">
                          <span>{fmtBytes(doc.size_bytes)}</span>
                          <span>·</span>
                          <span>{doc.chunk_count} chunk{doc.chunk_count !== 1 ? "s" : ""}</span>
                          <span>·</span>
                          <span>{relTime(doc.created_at)}</span>
                        </div>

                        {/* AI Summary */}
                        {doc.summary && (
                          <p className="text-xs text-muted-foreground mt-1.5 leading-relaxed line-clamp-2">
                            <Sparkles className="inline h-3 w-3 mr-1 text-primary/60" />
                            {doc.summary}
                          </p>
                        )}

                        {/* Key topics */}
                        {doc.key_topics.length > 0 && (
                          <div className="flex items-center gap-1 mt-1.5 flex-wrap">
                            <Tag className="h-3 w-3 text-muted-foreground" />
                            {doc.key_topics.slice(0, 4).map(t => (
                              <span key={t} className="text-[10px] px-1.5 py-0.5 rounded-full border border-border text-muted-foreground">
                                {t}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>

                      {/* Actions */}
                      <div className="flex flex-col items-end gap-1 flex-shrink-0">
                        <div className="flex items-center gap-1">
                          <Button variant="ghost" size="sm"
                            className="text-muted-foreground hover:text-foreground h-7 w-7 p-0"
                            onClick={() => toggleExpand(doc.id)}
                            title={isOpen ? "Collapse" : "Expand"}>
                            {isOpen ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
                          </Button>
                          <Button variant="ghost" size="sm"
                            className="text-muted-foreground hover:text-destructive h-7 w-7 p-0"
                            onClick={() => handleDelete(doc.id)}>
                            <Trash2 className="h-3.5 w-3.5" />
                          </Button>
                        </div>
                        {/* Image action badges */}
                        {doc.is_image && (
                          <div className="flex gap-1 mt-1">
                            {doc.enhanced_url && (
                              <span className="text-[9px] px-1.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 font-medium flex items-center gap-0.5">
                                <Zap className="h-2.5 w-2.5" />Enhanced
                              </span>
                            )}
                            {doc.nobg_url && (
                              <span className="text-[9px] px-1.5 py-0.5 rounded-full bg-blue-500/15 text-blue-700 dark:text-blue-300 font-medium flex items-center gap-0.5">
                                <Eraser className="h-2.5 w-2.5" />No BG
                              </span>
                            )}
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Image viewer tabs */}
                    {doc.is_image && (
                      <div className="px-4 pb-3">
                        <ImageViewer doc={doc} />
                      </div>
                    )}

                    {/* Expanded chunks */}
                    {isOpen && (
                      <div className="border-t border-border bg-muted/20 px-4 py-3">
                        {detailLoading ? (
                          <div className="flex items-center gap-2 text-sm text-muted-foreground py-2">
                            <Loader2 className="h-4 w-4 animate-spin" /> Loading chunks…
                          </div>
                        ) : detail ? (
                          <div className="space-y-2 max-h-60 overflow-y-auto">
                            <p className="text-[11px] font-medium text-muted-foreground uppercase tracking-wider mb-2">
                              Memory chunks ({detail.chunks.length})
                            </p>
                            {detail.chunks.map((chunk, i) => (
                              <div key={i} className="rounded-lg bg-background border border-border px-3 py-2">
                                <p className="text-[10px] text-muted-foreground mb-1">Chunk {i + 1}</p>
                                <p className="text-xs text-foreground/80 font-mono whitespace-pre-wrap leading-relaxed line-clamp-4">
                                  {chunk}
                                </p>
                              </div>
                            ))}
                          </div>
                        ) : null}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
