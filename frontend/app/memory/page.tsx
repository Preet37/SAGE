"use client";

import { useEffect, useState, useCallback, useRef } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";
import { api } from "@/lib/api";
import type { DocumentOut, DocumentDetail } from "@/lib/api";
import { AppHeader } from "@/components/AppHeader";
import { Button } from "@/components/ui/button";
import {
  FolderOpen, Upload, Search, Trash2, Loader2, FileText,
  FileVideo, FileAudio, ChevronDown, ChevronUp, X, Brain,
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

function mimeIcon(mime: string) {
  if (mime.startsWith("video/") || mime.startsWith("audio/")) return FileVideo;
  if (mime.includes("audio")) return FileAudio;
  return FileText;
}

function mimeLabel(mime: string, filename: string): string {
  const ext = filename.split(".").pop()?.toUpperCase() ?? "";
  if (ext) return ext;
  if (mime.includes("pdf")) return "PDF";
  if (mime.includes("word")) return "DOCX";
  if (mime.includes("presentation")) return "PPTX";
  if (mime.startsWith("text/")) return "TXT";
  return mime.split("/")[1]?.toUpperCase() ?? "FILE";
}

const ACCEPTED = [
  ".pdf", ".docx", ".doc", ".pptx", ".ppt",
  ".txt", ".md", ".csv",
  ".mp4", ".mov", ".webm", ".mp3", ".wav", ".m4a",
].join(",");

// ── Main page ─────────────────────────────────────────────────────────────────

export default function MyDocumentsPage() {
  const router = useRouter();
  const [docs, setDocs] = useState<DocumentOut[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<string | null>(null);
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
      const data = await api.documents.list(token);
      setDocs(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load documents");
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
    const results: DocumentOut[] = [];
    for (const file of Array.from(files)) {
      setUploading(true);
      setUploadProgress(`Uploading ${file.name}…`);
      try {
        const doc = await api.documents.upload(file, token);
        results.push(doc);
      } catch (e) {
        setError(e instanceof Error ? e.message : `Failed to upload ${file.name}`);
      }
    }
    setUploading(false);
    setUploadProgress(null);
    if (results.length > 0) {
      setDocs((prev) => [...results, ...prev]);
    }
  }

  async function handleDelete(id: string) {
    if (!confirm("Remove this document from memory? This cannot be undone.")) return;
    const token = getToken();
    if (!token) return;
    await api.documents.delete(id, token);
    setDocs((prev) => prev.filter((d) => d.id !== id));
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
      const d = await api.documents.get(id, token);
      setDetail(d);
    } catch {
      // ignore
    } finally {
      setDetailLoading(false);
    }
  }

  const filtered = docs.filter((d) =>
    !searchQuery || d.filename.toLowerCase().includes(searchQuery.toLowerCase()) ||
    d.preview.toLowerCase().includes(searchQuery.toLowerCase())
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
                  Upload anything — SAGE will parse and remember it for your sessions.
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2 text-xs text-muted-foreground bg-muted/40 rounded-lg px-3 py-2">
              <Brain className="h-3.5 w-3.5" />
              <span>{docs.length} document{docs.length !== 1 ? "s" : ""} in memory</span>
            </div>
          </div>

          {/* Drop zone */}
          <div
            className={cn(
              "rounded-xl border-2 border-dashed transition-all mb-6 cursor-pointer",
              dragOver
                ? "border-primary bg-primary/5 scale-[1.01]"
                : "border-border hover:border-primary/50 hover:bg-muted/30",
            )}
            onClick={() => inputRef.current?.click()}
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={(e) => { e.preventDefault(); setDragOver(false); handleFiles(e.dataTransfer.files); }}
          >
            <div className="flex flex-col items-center justify-center py-10 gap-3">
              {uploading ? (
                <>
                  <Loader2 className="h-8 w-8 animate-spin text-primary" />
                  <p className="text-sm font-medium text-primary">{uploadProgress}</p>
                </>
              ) : (
                <>
                  <Upload className="h-8 w-8 text-muted-foreground" />
                  <p className="text-sm font-medium">Drop files here or click to upload</p>
                  <p className="text-xs text-muted-foreground">
                    PDF · DOCX · PPTX · TXT · MD · CSV · MP4 · MP3 · WAV (max 50 MB)
                  </p>
                </>
              )}
            </div>
            <input
              ref={inputRef}
              type="file"
              multiple
              accept={ACCEPTED}
              className="hidden"
              onChange={(e) => handleFiles(e.target.files)}
            />
          </div>

          {/* Search */}
          {docs.length > 0 && (
            <div className="relative mb-5">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search documents by name or content…"
                className="w-full pl-10 pr-4 py-2.5 rounded-lg border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary/40"
              />
              {searchQuery && (
                <button onClick={() => setSearchQuery("")} className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground">
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
                {searchQuery ? "No documents match your search." : "No documents yet. Upload your first file above."}
              </p>
            </div>
          ) : (
            <div className="space-y-2">
              {filtered.map((doc) => {
                const Icon = mimeIcon(doc.mime);
                const isOpen = expanded === doc.id;
                return (
                  <div
                    key={doc.id}
                    className="rounded-xl border border-border bg-card hover:border-primary/40 transition overflow-hidden"
                  >
                    {/* Row */}
                    <div className="flex items-center gap-3 px-4 py-3">
                      <div className="h-9 w-9 rounded-lg bg-primary/10 text-primary flex items-center justify-center flex-shrink-0">
                        <Icon className="h-4 w-4" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="font-medium text-sm truncate">{doc.filename}</span>
                          <span className="text-[10px] px-1.5 py-0.5 rounded bg-muted text-muted-foreground font-mono uppercase">
                            {mimeLabel(doc.mime, doc.filename)}
                          </span>
                        </div>
                        <div className="flex items-center gap-3 mt-0.5 text-xs text-muted-foreground">
                          <span>{fmtBytes(doc.size_bytes)}</span>
                          <span>·</span>
                          <span>{doc.chunk_count} chunk{doc.chunk_count !== 1 ? "s" : ""} in memory</span>
                          <span>·</span>
                          <span>{relTime(doc.created_at)}</span>
                        </div>
                      </div>
                      <div className="flex items-center gap-1 flex-shrink-0">
                        <Button
                          variant="ghost" size="sm"
                          className="text-muted-foreground hover:text-foreground h-8 w-8 p-0"
                          onClick={() => toggleExpand(doc.id)}
                          title={isOpen ? "Collapse" : "Preview chunks"}
                        >
                          {isOpen ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                        </Button>
                        <Button
                          variant="ghost" size="sm"
                          className="text-muted-foreground hover:text-destructive h-8 w-8 p-0"
                          onClick={() => handleDelete(doc.id)}
                          title="Delete document"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>

                    {/* Preview snippet */}
                    {doc.preview && (
                      <p className="px-4 pb-3 text-xs text-muted-foreground line-clamp-2 leading-relaxed">
                        {doc.preview}
                      </p>
                    )}

                    {/* Expanded chunks */}
                    {isOpen && (
                      <div className="border-t border-border bg-muted/20 px-4 py-3">
                        {detailLoading ? (
                          <div className="flex items-center gap-2 text-sm text-muted-foreground py-2">
                            <Loader2 className="h-4 w-4 animate-spin" /> Loading chunks…
                          </div>
                        ) : detail ? (
                          <div className="space-y-2 max-h-64 overflow-y-auto">
                            <p className="text-xs font-medium text-muted-foreground mb-2 uppercase tracking-wider">
                              Memory chunks ({detail.chunks.length})
                            </p>
                            {detail.chunks.map((chunk, i) => (
                              <div key={i} className="rounded-lg bg-background border border-border px-3 py-2">
                                <p className="text-xs text-muted-foreground mb-1">Chunk {i + 1}</p>
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
