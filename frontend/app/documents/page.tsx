"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { AppHeader } from "@/components/AppHeader";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { getToken } from "@/lib/auth";
import { API_URL } from "@/lib/api";
import {
  Loader2,
  Upload,
  Search,
  Trash2,
  FileText,
  Film,
  Image as ImageIcon,
  Sparkles,
  X,
} from "lucide-react";

interface DocumentOut {
  id: string;
  public_id: string;
  resource_type: "image" | "video" | "raw";
  format: string | null;
  bytes: number;
  pages: number | null;
  duration: number | null;
  category: string;
  original_filename: string;
  tags: string[];
  preview_url: string;
  download_url: string;
  streaming_url: string | null;
}

interface SignResponse {
  cloud_name: string;
  api_key: string;
  timestamp: number;
  folder: string;
  signature: string;
  resource_type: string;
  extra_params: Record<string, string>;
}

function classifyFile(file: File): "image" | "video" | "raw" {
  if (file.type.startsWith("video/")) return "video";
  if (file.type.startsWith("image/")) return "image";
  // PDFs go through `image` to unlock multi-page rendering on Cloudinary.
  if (file.type === "application/pdf") return "image";
  return "raw";
}

function formatBytes(b: number): string {
  if (!b) return "—";
  const units = ["B", "KB", "MB", "GB"];
  let i = 0;
  let n = b;
  while (n > 1024 && i < units.length - 1) {
    n /= 1024;
    i++;
  }
  return `${n.toFixed(n < 10 && i > 0 ? 1 : 0)} ${units[i]}`;
}

function authHeaders(): HeadersInit {
  const t = getToken();
  return t ? { Authorization: `Bearer ${t}` } : {};
}

export default function DocumentsPage() {
  const router = useRouter();
  const [docs, setDocs] = useState<DocumentOut[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [viewing, setViewing] = useState<DocumentOut | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const refresh = useCallback(async () => {
    const t = getToken();
    if (!t) {
      router.push("/login?returnTo=/documents");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/documents`, {
        headers: authHeaders(),
      });
      if (res.status === 401) {
        router.push("/login?returnTo=/documents");
        return;
      }
      if (!res.ok) throw new Error(await res.text());
      const data = (await res.json()) as DocumentOut[];
      setDocs(data);
    } catch (e: any) {
      setError(e?.message ?? "Failed to load documents");
    } finally {
      setLoading(false);
    }
  }, [router]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const handleSearch = useCallback(async () => {
    if (!query.trim()) {
      refresh();
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(
        `${API_URL}/documents/search?q=${encodeURIComponent(query)}`,
        { headers: authHeaders() }
      );
      if (!res.ok) throw new Error(await res.text());
      setDocs(await res.json());
    } catch (e: any) {
      setError(e?.message ?? "Search failed");
    } finally {
      setLoading(false);
    }
  }, [query, refresh]);

  const handleUpload = useCallback(
    async (file: File) => {
      setError(null);
      setUploading(true);
      setUploadProgress(0);
      try {
        const resourceType = classifyFile(file);

        const signRes = await fetch(`${API_URL}/documents/sign`, {
          method: "POST",
          headers: { "Content-Type": "application/json", ...authHeaders() },
          body: JSON.stringify({ resource_type: resourceType }),
        });
        if (!signRes.ok) throw new Error("Couldn't get upload signature");
        const sign = (await signRes.json()) as SignResponse;

        const form = new FormData();
        form.append("file", file);
        form.append("api_key", sign.api_key);
        form.append("timestamp", String(sign.timestamp));
        form.append("folder", sign.folder);
        form.append("signature", sign.signature);
        // Extra params (auto_tagging, categorization) must match what the
        // backend signed, otherwise Cloudinary rejects the upload.
        for (const [k, v] of Object.entries(sign.extra_params || {})) {
          form.append(k, v);
        }

        const uploadEndpoint = `https://api.cloudinary.com/v1_1/${sign.cloud_name}/${sign.resource_type}/upload`;

        const xhr = new XMLHttpRequest();
        const result = await new Promise<any>((resolve, reject) => {
          xhr.open("POST", uploadEndpoint);
          xhr.upload.onprogress = (e) => {
            if (e.lengthComputable) {
              setUploadProgress(Math.round((e.loaded / e.total) * 100));
            }
          };
          xhr.onload = () => {
            if (xhr.status >= 200 && xhr.status < 300) {
              resolve(JSON.parse(xhr.responseText));
            } else {
              reject(new Error(xhr.responseText || "Upload failed"));
            }
          };
          xhr.onerror = () => reject(new Error("Upload failed"));
          xhr.send(form);
        });

        const importRes = await fetch(`${API_URL}/documents/import`, {
          method: "POST",
          headers: { "Content-Type": "application/json", ...authHeaders() },
          body: JSON.stringify({
            public_id: result.public_id,
            resource_type: resourceType,
            format: result.format,
            bytes: result.bytes,
            pages: result.pages,
            duration: result.duration,
            // category omitted — backend derives it from the AI tags
            original_filename: file.name,
            tags: Array.isArray(result.tags) ? result.tags : [],
          }),
        });
        if (!importRes.ok) throw new Error("Couldn't save document");
        const doc = (await importRes.json()) as DocumentOut;
        setDocs((prev) => [doc, ...prev]);
      } catch (e: any) {
        setError(e?.message ?? "Upload failed");
      } finally {
        setUploading(false);
        setUploadProgress(0);
      }
    },
    []
  );

  const handleDelete = useCallback(
    async (doc: DocumentOut) => {
      if (!confirm(`Delete "${doc.original_filename}"?`)) return;
      const res = await fetch(`${API_URL}/documents/${doc.id}`, {
        method: "DELETE",
        headers: authHeaders(),
      });
      if (res.ok) {
        setDocs((prev) => prev.filter((d) => d.id !== doc.id));
        if (viewing?.id === doc.id) setViewing(null);
      }
    },
    [viewing]
  );

  const visibleDocs = useMemo(() => docs, [docs]);

  return (
    <div className="flex flex-col h-screen">
      <AppHeader />

      <div className="flex-1 overflow-y-auto">
        <div className="max-w-6xl mx-auto p-6 space-y-6">
          <header>
            <h1 className="text-2xl font-semibold">My Documents</h1>
            <p className="text-sm text-muted-foreground mt-1">
              Upload lecture videos, PDFs, and notes. Cloudinary handles streaming,
              multi-page rendering, and on-the-fly enhancements.
            </p>
          </header>

          <Card className="p-4 space-y-3">
            <div className="flex items-center gap-3">
              <input
                ref={fileInputRef}
                type="file"
                hidden
                accept="image/*,video/*,application/pdf"
                onChange={(e) => {
                  const f = e.target.files?.[0];
                  if (f) handleUpload(f);
                  e.target.value = "";
                }}
              />
              <Button
                onClick={() => fileInputRef.current?.click()}
                disabled={uploading}
              >
                {uploading ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Uploading {uploadProgress}%
                  </>
                ) : (
                  <>
                    <Upload className="h-4 w-4 mr-2" />
                    Choose file
                  </>
                )}
              </Button>
              <span className="text-xs text-muted-foreground">
                Images, videos, or PDFs. Cloudinary auto-detects what's in the
                file and tags it for search.
              </span>
            </div>
            {uploading && uploadProgress > 0 && (
              <div className="h-1 bg-muted rounded overflow-hidden">
                <div
                  className="h-full bg-primary transition-all"
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
            )}
          </Card>

          <div className="flex items-center gap-2">
            <Search className="h-4 w-4 text-muted-foreground" />
            <Input
              placeholder='Search by filename or content (e.g. "hat", "whiteboard")…'
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            />
            <Button variant="outline" size="sm" onClick={handleSearch}>
              Search
            </Button>
          </div>

          {error && (
            <div className="text-sm text-red-500 bg-red-500/10 border border-red-500/30 rounded p-3">
              {error}
            </div>
          )}

          {loading ? (
            <div className="flex items-center justify-center py-16">
              <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
            </div>
          ) : visibleDocs.length === 0 ? (
            <div className="text-center py-16 text-muted-foreground text-sm">
              No documents yet. Upload one above to get started.
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {visibleDocs.map((doc) => (
                <DocCard
                  key={doc.id}
                  doc={doc}
                  onView={() => setViewing(doc)}
                  onDelete={() => handleDelete(doc)}
                />
              ))}
            </div>
          )}
        </div>
      </div>

      {viewing && (
        <ViewerOverlay doc={viewing} onClose={() => setViewing(null)} />
      )}
    </div>
  );
}

function DocCard({
  doc,
  onView,
  onDelete,
}: {
  doc: DocumentOut;
  onView: () => void;
  onDelete: () => void;
}) {
  const Icon =
    doc.resource_type === "video"
      ? Film
      : doc.format === "pdf"
      ? FileText
      : ImageIcon;
  const [imgFailed, setImgFailed] = useState(false);

  return (
    <Card className="overflow-hidden flex flex-col">
      <button
        type="button"
        onClick={onView}
        className="aspect-video bg-muted relative group flex items-center justify-center overflow-hidden"
      >
        {!imgFailed && (
          <img
            src={doc.preview_url}
            alt={doc.original_filename}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform"
            onError={() => setImgFailed(true)}
          />
        )}
        {imgFailed && <Icon className="h-8 w-8 text-muted-foreground" />}
      </button>
      <div className="p-3 flex-1 flex flex-col gap-2">
        <div className="flex items-start justify-between gap-2">
          <div className="text-sm font-medium truncate" title={doc.original_filename}>
            {doc.original_filename}
          </div>
          <Badge variant="outline" className="shrink-0 text-xs">
            {doc.category}
          </Badge>
        </div>
        <div className="text-xs text-muted-foreground flex items-center gap-2">
          <span>{doc.resource_type}</span>
          <span>·</span>
          <span>{formatBytes(doc.bytes)}</span>
          {doc.pages ? (
            <>
              <span>·</span>
              <span>{doc.pages}p</span>
            </>
          ) : null}
          {doc.duration ? (
            <>
              <span>·</span>
              <span>{Math.round(doc.duration)}s</span>
            </>
          ) : null}
        </div>
        <div className="flex gap-1 mt-auto">
          <Button size="sm" variant="outline" className="flex-1" onClick={onView}>
            View
          </Button>
          <Button
            size="sm"
            variant="ghost"
            onClick={onDelete}
            className="text-muted-foreground hover:text-red-500"
          >
            <Trash2 className="h-3.5 w-3.5" />
          </Button>
        </div>
      </div>
    </Card>
  );
}

function ViewerOverlay({
  doc,
  onClose,
}: {
  doc: DocumentOut;
  onClose: () => void;
}) {
  const [enhancedUrl, setEnhancedUrl] = useState<string | null>(null);
  const [enhanceNote, setEnhanceNote] = useState<string | null>(null);
  const [enhanceError, setEnhanceError] = useState<string | null>(null);
  const [pageIndex, setPageIndex] = useState(1);
  const [ocrText, setOcrText] = useState<string | null>(null);
  const [ocrLoading, setOcrLoading] = useState(false);
  const [transcript, setTranscript] = useState<string | null>(null);
  const [transcriptStatus, setTranscriptStatus] = useState<string | null>(null);
  const [transcriptLoading, setTranscriptLoading] = useState(false);

  async function runTranscribe() {
    setTranscriptLoading(true);
    setTranscript(null);
    setTranscriptStatus("processing");
    setEnhanceError(null);

    // Poll until the transcript file is ready or we hit the cap. Cloudinary's
    // Google Speech transcription typically takes 30–90s for short clips.
    const maxAttempts = 60; // ~5 minutes at 5s intervals
    const intervalMs = 5000;
    let lastStatus: string | null = null;
    try {
      for (let attempt = 0; attempt < maxAttempts; attempt++) {
        const res = await fetch(`${API_URL}/documents/${doc.id}/transcribe`, {
          method: "POST",
          headers: authHeaders(),
        });
        if (!res.ok) {
          const j = await res.json().catch(() => ({}));
          setEnhanceError(j.detail || "Transcription failed");
          return;
        }
        const j = await res.json();
        lastStatus = j.status;
        if (j.status === "ready" && j.text) {
          setTranscriptStatus("ready");
          setTranscript(j.text);
          return;
        }
        // Still processing — show progress and wait.
        setTranscript(
          `Transcribing… (~${Math.round(((attempt + 1) * intervalMs) / 1000)}s elapsed)`
        );
        await new Promise((r) => setTimeout(r, intervalMs));
      }
      setTranscript(
        lastStatus === "processing"
          ? "Still processing on Cloudinary's side — click Transcribe again to keep waiting."
          : "(no speech detected)"
      );
    } finally {
      setTranscriptLoading(false);
    }
  }

  async function runOcr() {
    setOcrLoading(true);
    setOcrText(null);
    setEnhanceError(null);
    try {
      const res = await fetch(`${API_URL}/documents/${doc.id}/ocr`, {
        method: "POST",
        headers: authHeaders(),
      });
      if (!res.ok) {
        const j = await res.json().catch(() => ({}));
        setEnhanceError(j.detail || "OCR failed");
        return;
      }
      const j = await res.json();
      setOcrText(j.text || "(no text detected)");
    } finally {
      setOcrLoading(false);
    }
  }

  async function runEnhance(op: string, prompt?: string) {
    setEnhanceNote(null);
    setEnhanceError(null);
    const res = await fetch(`${API_URL}/documents/enhance`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeaders() },
      body: JSON.stringify({ document_id: doc.id, op, prompt }),
    });
    if (res.ok) {
      const j = await res.json();
      setEnhancedUrl(j.url);
      setEnhanceNote(j.note ?? null);
    }
  }

  const isPdf = doc.resource_type === "image" && doc.format === "pdf";
  // Backend already injects pg_1 for PDFs; swap to the requested page for the viewer.
  const previewSrc = isPdf
    ? doc.preview_url.replace(/\/pg_\d+\//, `/pg_${pageIndex}/`)
    : doc.preview_url;

  return (
    <div className="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4">
      <div className="bg-card border border-border rounded-lg max-w-5xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        <div className="flex items-center justify-between px-4 py-3 border-b border-border gap-3">
          <div className="flex items-center gap-2 min-w-0">
            <Badge variant="outline">{doc.category}</Badge>
            <span className="text-sm font-medium truncate">{doc.original_filename}</span>
          </div>
          <Button size="icon" variant="ghost" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </div>
        {doc.tags.length > 0 && (
          <div className="px-4 py-2 border-b border-border flex flex-wrap items-center gap-1.5 text-xs">
            <span className="text-muted-foreground mr-1">AI tags:</span>
            {doc.tags.slice(0, 12).map((t) => (
              <Badge key={t} variant="outline" className="text-[10px] py-0 h-5">
                {t}
              </Badge>
            ))}
          </div>
        )}

        <div className="flex-1 overflow-auto bg-black/50 p-4 min-h-[300px]">
          {doc.resource_type === "video" && doc.streaming_url ? (
            <div className="min-h-full flex items-center justify-center">
              <VideoPlayer src={doc.streaming_url} poster={doc.preview_url} />
            </div>
          ) : (
            <div className="min-h-full flex items-start justify-center">
              <img
                src={enhancedUrl ?? previewSrc}
                alt={doc.original_filename}
                className="max-w-full h-auto"
                onLoad={() => setEnhanceError(null)}
                onError={() => {
                  if (enhancedUrl) {
                    setEnhanceError(
                      "This add-on returned an error — the corresponding Cloudinary add-on may not be enabled or has run out of free transformations."
                    );
                  }
                }}
              />
            </div>
          )}
        </div>

        <div className="px-4 py-3 border-t border-border flex flex-wrap items-center gap-2">
          {isPdf && doc.pages && doc.pages > 1 && (
            <div className="flex items-center gap-1">
              <Button
                size="sm"
                variant="outline"
                onClick={() => setPageIndex((p) => Math.max(1, p - 1))}
                disabled={pageIndex <= 1}
              >
                Prev
              </Button>
              <span className="text-xs text-muted-foreground px-2">
                {pageIndex} / {doc.pages}
              </span>
              <Button
                size="sm"
                variant="outline"
                onClick={() => setPageIndex((p) => Math.min(doc.pages || 1, p + 1))}
                disabled={pageIndex >= (doc.pages || 1)}
              >
                Next
              </Button>
            </div>
          )}

          {doc.resource_type === "image" && (
            <>
              <span className="text-xs text-muted-foreground mr-1">
                <Sparkles className="h-3 w-3 inline mr-1" />
                Enhance:
              </span>
              <Button size="sm" variant="outline" onClick={() => runEnhance("bg_remove")}>
                Remove BG
              </Button>
              <Button size="sm" variant="outline" onClick={() => runEnhance("auto_enhance")}>
                Auto-enhance
              </Button>
              <Button size="sm" variant="outline" onClick={runOcr} disabled={ocrLoading}>
                {ocrLoading ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : "Extract text"}
              </Button>
              {enhancedUrl && (
                <Button size="sm" variant="ghost" onClick={() => setEnhancedUrl(null)}>
                  Reset
                </Button>
              )}
            </>
          )}
          {doc.resource_type === "video" && (
            <Button
              size="sm"
              variant="outline"
              onClick={runTranscribe}
              disabled={transcriptLoading}
            >
              {transcriptLoading ? (
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
              ) : (
                "Transcribe"
              )}
            </Button>
          )}

          <a
            href={doc.download_url}
            target="_blank"
            rel="noopener noreferrer"
            className="ml-auto"
          >
            <Button size="sm" variant="outline">Download</Button>
          </a>
        </div>

        {enhanceError && (
          <div className="px-4 pb-3 text-xs text-red-500">{enhanceError}</div>
        )}
        {ocrText !== null && (
          <div className="px-4 pb-3">
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs font-medium text-muted-foreground">
                OCR result
              </span>
              <Button
                size="sm"
                variant="ghost"
                onClick={() => setOcrText(null)}
                className="h-6 px-2 text-xs"
              >
                Dismiss
              </Button>
            </div>
            <pre className="text-xs bg-muted/50 rounded p-3 max-h-48 overflow-auto whitespace-pre-wrap break-words">
              {ocrText}
            </pre>
          </div>
        )}
        {transcript !== null && (
          <div className="px-4 pb-3">
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs font-medium text-muted-foreground">
                Transcript {transcriptStatus === "processing" && "(processing…)"}
              </span>
              <Button
                size="sm"
                variant="ghost"
                onClick={() => setTranscript(null)}
                className="h-6 px-2 text-xs"
              >
                Dismiss
              </Button>
            </div>
            <pre className="text-xs bg-muted/50 rounded p-3 max-h-48 overflow-auto whitespace-pre-wrap break-words">
              {transcript}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}

function VideoPlayer({ src, poster }: { src: string; poster: string }) {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    // Native HLS (Safari)
    if (video.canPlayType("application/vnd.apple.mpegurl")) {
      video.src = src;
      return;
    }

    // hls.js for everyone else
    let hls: any;
    let cancelled = false;
    (async () => {
      const Hls = (await import("hls.js")).default;
      if (cancelled) return;
      if (Hls.isSupported()) {
        hls = new Hls();
        hls.loadSource(src);
        hls.attachMedia(video);
      } else {
        video.src = src;
      }
    })();
    return () => {
      cancelled = true;
      if (hls) hls.destroy();
    };
  }, [src]);

  return (
    <video
      ref={videoRef}
      controls
      poster={poster}
      className="max-h-full max-w-full"
    />
  );
}
