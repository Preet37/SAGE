"use client";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { AppHeader } from "@/components/AppHeader";
import { getToken } from "@/lib/auth";
import { API_URL } from "@/lib/api";
import { Loader2, Upload, Search, Trash2, FileText, Film, Image as ImageIcon, Sparkles, X } from "lucide-react";

const mono: React.CSSProperties  = { fontFamily: "var(--font-dm-mono)" };
const serif: React.CSSProperties = { fontFamily: "var(--font-cormorant)" };
const body: React.CSSProperties  = { fontFamily: "var(--font-crimson)" };

interface DocumentOut { id: string; public_id: string; resource_type: "image" | "video" | "raw"; format: string | null; bytes: number; pages: number | null; duration: number | null; category: string; original_filename: string; tags: string[]; preview_url: string; download_url: string; streaming_url: string | null; }
interface SignResponse { cloud_name: string; api_key: string; timestamp: number; folder: string; signature: string; resource_type: string; extra_params: Record<string, string>; }

function classifyFile(file: File): "image" | "video" | "raw" { if (file.type.startsWith("video/")) return "video"; if (file.type.startsWith("image/")) return "image"; if (file.type === "application/pdf") return "image"; return "raw"; }
function formatBytes(b: number): string { if (!b) return "—"; const units = ["B","KB","MB","GB"]; let i = 0, n = b; while (n > 1024 && i < units.length - 1) { n /= 1024; i++; } return `${n.toFixed(n < 10 && i > 0 ? 1 : 0)} ${units[i]}`; }
function authHeaders(): HeadersInit { const t = getToken(); return t ? { Authorization: `Bearer ${t}` } : {}; }

function GoldBtn({ onClick, disabled, children }: { onClick?: () => void; disabled?: boolean; children: React.ReactNode }) {
  return (
    <button onClick={onClick} disabled={disabled} style={{ ...mono, fontSize: "0.52rem", letterSpacing: "0.12em", textTransform: "uppercase", padding: "0.45rem 0.85rem", background: disabled ? "rgba(196,152,90,0.3)" : "var(--gold)", color: disabled ? "var(--cream-2)" : "var(--ink)", border: "none", cursor: disabled ? "not-allowed" : "pointer", display: "inline-flex", alignItems: "center", gap: "0.4rem", transition: "opacity 0.2s" }}>
      {children}
    </button>
  );
}
function OutlineBtn({ onClick, disabled, children }: { onClick?: () => void; disabled?: boolean; children: React.ReactNode }) {
  return (
    <button onClick={onClick} disabled={disabled} style={{ ...mono, fontSize: "0.52rem", letterSpacing: "0.12em", textTransform: "uppercase", padding: "0.4rem 0.75rem", background: "none", color: disabled ? "var(--cream-2)" : "var(--cream-1)", border: "1px solid rgba(240,233,214,0.15)", cursor: disabled ? "not-allowed" : "pointer", display: "inline-flex", alignItems: "center", gap: "0.4rem", transition: "border-color 0.2s, color 0.2s" }}>
      {children}
    </button>
  );
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
    if (!t) { router.push("/login?returnTo=/documents"); return; }
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/documents`, { headers: authHeaders() });
      if (res.status === 401) { router.push("/login?returnTo=/documents"); return; }
      if (res.ok) setDocs(await res.json());
    } catch { }
    finally { setLoading(false); }
  }, [router]);

  useEffect(() => { refresh(); }, [refresh]);

  const handleSearch = useCallback(async () => {
    if (!query.trim()) { refresh(); return; }
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/documents/search?q=${encodeURIComponent(query)}`, { headers: authHeaders() });
      if (!res.ok) throw new Error(await res.text());
      setDocs(await res.json());
    } catch (e: any) { setError(e?.message ?? "Search failed"); }
    finally { setLoading(false); }
  }, [query, refresh]);

  const handleUpload = useCallback(async (file: File) => {
    setError(null); setUploading(true); setUploadProgress(0);
    try {
      const resourceType = classifyFile(file);
      const signRes = await fetch(`${API_URL}/documents/sign`, { method: "POST", headers: { "Content-Type": "application/json", ...authHeaders() }, body: JSON.stringify({ resource_type: resourceType }) });
      if (!signRes.ok) {
        if (signRes.status === 401 || signRes.status === 403) throw new Error("Not logged in — please sign in and try again.");
        const detail = await signRes.json().catch(() => null);
        throw new Error(detail?.detail || "Couldn't get upload signature — check server configuration.");
      }
      const sign = await signRes.json() as SignResponse;
      const form = new FormData();
      form.append("file", file); form.append("api_key", sign.api_key); form.append("timestamp", String(sign.timestamp)); form.append("folder", sign.folder); form.append("signature", sign.signature);
      for (const [k, v] of Object.entries(sign.extra_params || {})) form.append(k, v);
      const result = await new Promise<any>((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open("POST", `https://api.cloudinary.com/v1_1/${sign.cloud_name}/${sign.resource_type}/upload`);
        xhr.upload.onprogress = (e) => { if (e.lengthComputable) setUploadProgress(Math.round((e.loaded / e.total) * 100)); };
        xhr.onload = () => xhr.status >= 200 && xhr.status < 300 ? resolve(JSON.parse(xhr.responseText)) : reject(new Error(xhr.responseText || "Upload failed"));
        xhr.onerror = () => reject(new Error("Upload failed"));
        xhr.send(form);
      });
      const importRes = await fetch(`${API_URL}/documents/import`, { method: "POST", headers: { "Content-Type": "application/json", ...authHeaders() }, body: JSON.stringify({ public_id: result.public_id, resource_type: resourceType, format: result.format, bytes: result.bytes, pages: result.pages, duration: result.duration, original_filename: file.name, tags: Array.isArray(result.tags) ? result.tags : [] }) });
      if (!importRes.ok) throw new Error("Couldn't save document");
      const imported = await importRes.json();
      setDocs((prev) => [imported, ...prev]);
    } catch (e: any) { setError(e?.message ?? "Upload failed"); }
    finally { setUploading(false); setUploadProgress(0); }
  }, []);

  const handleDelete = useCallback(async (doc: DocumentOut) => {
    if (!confirm(`Delete "${doc.original_filename}"?`)) return;
    const res = await fetch(`${API_URL}/documents/${doc.id}`, { method: "DELETE", headers: authHeaders() });
    if (res.ok) { setDocs((prev) => prev.filter((d) => d.id !== doc.id)); if (viewing?.id === doc.id) setViewing(null); }
  }, [viewing]);

  return (
    <div className="flex flex-col h-screen" style={{ background: "var(--ink)", color: "var(--cream-0)" }}>
      <AppHeader />
      <div className="flex-1 overflow-y-auto thin-scrollbar">
        <div style={{ maxWidth: "64rem", margin: "0 auto", padding: "2.5rem 1.5rem 4rem" }}>
          <div style={{ marginBottom: "2rem" }}>
            <p style={{ ...mono, fontSize: "0.58rem", letterSpacing: "0.16em", textTransform: "uppercase", color: "var(--gold)", marginBottom: "0.5rem" }}>Documents</p>
            <h1 style={{ ...serif, fontWeight: 700, fontStyle: "italic", fontSize: "clamp(2rem,5vw,3rem)", color: "var(--cream-0)", lineHeight: 1.1, marginBottom: "0.4rem" }}>
              My Documents<span style={{ color: "var(--gold)" }}>.</span>
            </h1>
            <p style={{ ...body, fontSize: "0.95rem", color: "var(--cream-1)", lineHeight: 1.6 }}>
              Upload lecture videos, PDFs, and notes. Cloudinary handles streaming, multi-page rendering, and on-the-fly enhancements.
            </p>
          </div>

          {/* Upload */}
          <div style={{ background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.07)", padding: "1.25rem", marginBottom: "1.25rem" }}>
            <input ref={fileInputRef} type="file" hidden accept="image/*,video/*,application/pdf" onChange={(e) => { const f = e.target.files?.[0]; if (f) handleUpload(f); e.target.value = ""; }} />
            <div style={{ display: "flex", alignItems: "center", gap: "1rem", flexWrap: "wrap" }}>
              <GoldBtn onClick={() => fileInputRef.current?.click()} disabled={uploading}>
                {uploading ? <><Loader2 style={{ width: "0.75rem", height: "0.75rem" }} className="animate-spin" />Uploading {uploadProgress}%</> : <><Upload style={{ width: "0.75rem", height: "0.75rem" }} />Choose file</>}
              </GoldBtn>
              <span style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.08em", color: "var(--cream-2)" }}>Images, videos, or PDFs · auto-tagged for search</span>
            </div>
            {uploading && uploadProgress > 0 && (
              <div style={{ marginTop: "0.75rem", height: "2px", background: "rgba(240,233,214,0.08)", overflow: "hidden" }}>
                <div style={{ height: "100%", background: "var(--gold)", transition: "width 0.3s", width: `${uploadProgress}%` }} />
              </div>
            )}
          </div>

          {/* Search */}
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "1.5rem" }}>
            <div style={{ position: "relative", flex: 1 }}>
              <Search style={{ position: "absolute", left: "0.75rem", top: "50%", transform: "translateY(-50%)", width: "0.8rem", height: "0.8rem", color: "var(--cream-2)" }} />
              <input placeholder='Search by filename or content…' value={query} onChange={(e) => setQuery(e.target.value)} onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                style={{ width: "100%", paddingLeft: "2.2rem", paddingRight: "0.85rem", paddingTop: "0.6rem", paddingBottom: "0.6rem", background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.08)", outline: "none", ...body, fontSize: "0.9rem", color: "var(--cream-0)", boxSizing: "border-box" }} />
            </div>
            <OutlineBtn onClick={handleSearch}>Search</OutlineBtn>
          </div>

          {error && (
            <div style={{ background: "rgba(201,124,104,0.08)", border: "1px solid rgba(201,124,104,0.3)", padding: "0.65rem 1rem", marginBottom: "1rem" }}>
              <p style={{ ...body, fontSize: "0.9rem", color: "var(--rose)" }}>{error}</p>
            </div>
          )}

          {loading ? (
            <div style={{ display: "flex", justifyContent: "center", padding: "5rem 0" }}>
              <Loader2 style={{ width: "1.5rem", height: "1.5rem", color: "var(--gold)" }} className="animate-spin" />
            </div>
          ) : docs.length === 0 ? (
            <div style={{ textAlign: "center", padding: "5rem 0" }}>
              <p style={{ ...mono, fontSize: "0.58rem", letterSpacing: "0.12em", textTransform: "uppercase", color: "var(--cream-2)" }}>No documents yet. Upload one above to get started.</p>
            </div>
          ) : (
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(18rem, 1fr))", gap: "0.75rem" }}>
              {docs.map((doc) => <DocCard key={doc.id} doc={doc} onView={() => setViewing(doc)} onDelete={() => handleDelete(doc)} />)}
            </div>
          )}
        </div>
      </div>

      {viewing && <ViewerOverlay doc={viewing} onClose={() => setViewing(null)} />}
    </div>
  );
}

function DocCard({ doc, onView, onDelete }: { doc: DocumentOut; onView: () => void; onDelete: () => void }) {
  const Icon = doc.resource_type === "video" ? Film : doc.format === "pdf" ? FileText : ImageIcon;
  const [imgFailed, setImgFailed] = useState(false);
  return (
    <div style={{ background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.07)", overflow: "hidden", display: "flex", flexDirection: "column", transition: "border-color 0.2s" }}
      onMouseEnter={e => (e.currentTarget as HTMLDivElement).style.borderColor = "rgba(196,152,90,0.3)"}
      onMouseLeave={e => (e.currentTarget as HTMLDivElement).style.borderColor = "rgba(240,233,214,0.07)"}>
      <button type="button" onClick={onView} style={{ aspectRatio: "16/9", background: "var(--ink-2)", position: "relative", display: "flex", alignItems: "center", justifyContent: "center", overflow: "hidden", border: "none", cursor: "pointer", width: "100%" }}>
        {!imgFailed && <img src={doc.preview_url} alt={doc.original_filename} style={{ width: "100%", height: "100%", objectFit: "cover" }} onError={() => setImgFailed(true)} />}
        {imgFailed && <Icon style={{ width: "1.5rem", height: "1.5rem", color: "var(--cream-2)" }} />}
      </button>
      <div style={{ padding: "0.85rem", flex: 1, display: "flex", flexDirection: "column", gap: "0.4rem" }}>
        <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: "0.5rem" }}>
          <span style={{ ...body, fontSize: "0.9rem", color: "var(--cream-0)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", flex: 1 }}>{doc.original_filename}</span>
          <span style={{ ...mono, fontSize: "0.48rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--gold)", border: "1px solid rgba(196,152,90,0.3)", padding: "0.1rem 0.35rem", flexShrink: 0 }}>{doc.category}</span>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: "0.35rem", ...mono, fontSize: "0.5rem", letterSpacing: "0.08em", color: "var(--cream-2)" }}>
          <span>{doc.resource_type}</span><span>·</span><span>{formatBytes(doc.bytes)}</span>
          {doc.pages && <><span>·</span><span>{doc.pages}p</span></>}
          {doc.duration && <><span>·</span><span>{Math.round(doc.duration)}s</span></>}
        </div>
        <div style={{ display: "flex", gap: "0.4rem", marginTop: "auto" }}>
          <button onClick={onView} style={{ flex: 1, padding: "0.4rem", background: "none", border: "1px solid rgba(240,233,214,0.12)", cursor: "pointer", ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-1)", transition: "border-color 0.2s" }}>View</button>
          <button onClick={onDelete} style={{ padding: "0.4rem 0.6rem", background: "none", border: "1px solid rgba(240,233,214,0.08)", cursor: "pointer", color: "var(--cream-2)", display: "flex", alignItems: "center", transition: "color 0.2s, border-color 0.2s" }}
            onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.color = "var(--rose)"; (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(201,124,104,0.4)"; }}
            onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-2)"; (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(240,233,214,0.08)"; }}>
            <Trash2 style={{ width: "0.75rem", height: "0.75rem" }} />
          </button>
        </div>
      </div>
    </div>
  );
}

function ViewerOverlay({ doc, onClose }: { doc: DocumentOut; onClose: () => void }) {
  const [enhancedUrl, setEnhancedUrl] = useState<string | null>(null);
  const [enhanceNote, setEnhanceNote] = useState<string | null>(null);
  const [enhanceError, setEnhanceError] = useState<string | null>(null);
  const [pageIndex, setPageIndex] = useState(1);
  const [ocrText, setOcrText] = useState<string | null>(null);
  const [ocrLoading, setOcrLoading] = useState(false);
  const [transcript, setTranscript] = useState<string | null>(null);
  const [transcriptStatus, setTranscriptStatus] = useState<string | null>(null);
  const [transcriptLoading, setTranscriptLoading] = useState(false);

  async function runOcr() {
    setOcrLoading(true); setOcrText(null); setEnhanceError(null);
    try { const res = await fetch(`${API_URL}/documents/${doc.id}/ocr`, { method: "POST", headers: authHeaders() }); if (!res.ok) { const j = await res.json().catch(() => ({})); setEnhanceError(j.detail || "OCR failed"); return; } const j = await res.json(); setOcrText(j.text || "(no text detected)"); }
    finally { setOcrLoading(false); }
  }
  async function runTranscribe() {
    setTranscriptLoading(true); setTranscript(null); setTranscriptStatus("processing"); setEnhanceError(null);
    const maxAttempts = 60; const intervalMs = 5000; let lastStatus: string | null = null;
    try {
      for (let attempt = 0; attempt < maxAttempts; attempt++) {
        const res = await fetch(`${API_URL}/documents/${doc.id}/transcribe`, { method: "POST", headers: authHeaders() });
        if (!res.ok) { const j = await res.json().catch(() => ({})); setEnhanceError(j.detail || "Transcription failed"); return; }
        const j = await res.json(); lastStatus = j.status;
        if (j.status === "ready" && j.text) { setTranscriptStatus("ready"); setTranscript(j.text); return; }
        setTranscript(`Transcribing… (~${Math.round(((attempt + 1) * intervalMs) / 1000)}s elapsed)`);
        await new Promise((r) => setTimeout(r, intervalMs));
      }
      setTranscript(lastStatus === "processing" ? "Still processing — click Transcribe again to keep waiting." : "(no speech detected)");
    } finally { setTranscriptLoading(false); }
  }
  async function runEnhance(op: string) {
    setEnhanceNote(null); setEnhanceError(null);
    const res = await fetch(`${API_URL}/documents/enhance`, { method: "POST", headers: { "Content-Type": "application/json", ...authHeaders() }, body: JSON.stringify({ document_id: doc.id, op }) });
    if (res.ok) { const j = await res.json(); setEnhancedUrl(j.url); setEnhanceNote(j.note ?? null); }
  }

  const isPdf = doc.resource_type === "image" && doc.format === "pdf";
  const previewSrc = isPdf ? doc.preview_url.replace(/\/pg_\d+\//, `/pg_${pageIndex}/`) : doc.preview_url;

  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.85)", zIndex: 50, display: "flex", alignItems: "center", justifyContent: "center", padding: "1rem" }}>
      <div style={{ background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.1)", maxWidth: "64rem", width: "100%", maxHeight: "90vh", overflow: "hidden", display: "flex", flexDirection: "column" }}>
        {/* Header */}
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0.75rem 1rem", borderBottom: "1px solid rgba(240,233,214,0.07)", gap: "1rem" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", minWidth: 0 }}>
            <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--gold)", border: "1px solid rgba(196,152,90,0.3)", padding: "0.1rem 0.4rem", flexShrink: 0 }}>{doc.category}</span>
            <span style={{ fontFamily: "var(--font-crimson)", fontSize: "0.95rem", color: "var(--cream-0)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{doc.original_filename}</span>
          </div>
          <button onClick={onClose} style={{ background: "none", border: "none", cursor: "pointer", color: "var(--cream-2)", display: "flex", padding: "0.25rem", transition: "color 0.2s" }} onMouseEnter={e => (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-1)"} onMouseLeave={e => (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-2)"}>
            <X style={{ width: "0.9rem", height: "0.9rem" }} />
          </button>
        </div>

        {doc.tags.length > 0 && (
          <div style={{ padding: "0.5rem 1rem", borderBottom: "1px solid rgba(240,233,214,0.07)", display: "flex", flexWrap: "wrap", alignItems: "center", gap: "0.4rem" }}>
            <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: "0.48rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)", marginRight: "0.25rem" }}>AI tags:</span>
            {doc.tags.slice(0, 12).map((t) => <span key={t} style={{ fontFamily: "var(--font-dm-mono)", fontSize: "0.48rem", letterSpacing: "0.08em", color: "var(--cream-2)", border: "1px solid rgba(240,233,214,0.1)", padding: "0.1rem 0.35rem" }}>{t}</span>)}
          </div>
        )}

        <div style={{ flex: 1, overflow: "auto", background: "rgba(0,0,0,0.4)", padding: "1rem", minHeight: "18rem", display: "flex", alignItems: "center", justifyContent: "center" }}>
          {doc.resource_type === "video" && doc.streaming_url
            ? <VideoPlayer src={doc.streaming_url} poster={doc.preview_url} />
            : <img src={enhancedUrl ?? previewSrc} alt={doc.original_filename} style={{ maxWidth: "100%", height: "auto" }} onError={() => { if (enhancedUrl) setEnhanceError("Add-on unavailable or out of free transformations."); }} />}
        </div>

        <div style={{ padding: "0.75rem 1rem", borderTop: "1px solid rgba(240,233,214,0.07)", display: "flex", flexWrap: "wrap", alignItems: "center", gap: "0.5rem" }}>
          {isPdf && doc.pages && doc.pages > 1 && (
            <div style={{ display: "flex", alignItems: "center", gap: "0.4rem" }}>
              <OutlineBtn onClick={() => setPageIndex((p) => Math.max(1, p - 1))} disabled={pageIndex <= 1}>Prev</OutlineBtn>
              <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: "0.5rem", letterSpacing: "0.08em", color: "var(--cream-2)", padding: "0 0.25rem" }}>{pageIndex} / {doc.pages}</span>
              <OutlineBtn onClick={() => setPageIndex((p) => Math.min(doc.pages || 1, p + 1))} disabled={pageIndex >= (doc.pages || 1)}>Next</OutlineBtn>
            </div>
          )}
          {doc.resource_type === "image" && (
            <>
              <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)", display: "inline-flex", alignItems: "center", gap: "0.25rem" }}><Sparkles style={{ width: "0.65rem", height: "0.65rem" }} />Enhance:</span>
              <OutlineBtn onClick={() => runEnhance("bg_remove")}>Remove BG</OutlineBtn>
              <OutlineBtn onClick={() => runEnhance("auto_enhance")}>Auto-enhance</OutlineBtn>
              <OutlineBtn onClick={runOcr} disabled={ocrLoading}>{ocrLoading ? <Loader2 style={{ width: "0.7rem", height: "0.7rem" }} className="animate-spin" /> : "Extract text"}</OutlineBtn>
              {enhancedUrl && <OutlineBtn onClick={() => setEnhancedUrl(null)}>Reset</OutlineBtn>}
            </>
          )}
          {doc.resource_type === "video" && <OutlineBtn onClick={runTranscribe} disabled={transcriptLoading}>{transcriptLoading ? <Loader2 style={{ width: "0.7rem", height: "0.7rem" }} className="animate-spin" /> : "Transcribe"}</OutlineBtn>}
          <a href={doc.download_url} target="_blank" rel="noopener noreferrer" style={{ marginLeft: "auto" }}><OutlineBtn>Download</OutlineBtn></a>
        </div>

        {enhanceError && <div style={{ padding: "0 1rem 0.75rem" }}><p style={{ fontFamily: "var(--font-dm-mono)", fontSize: "0.5rem", letterSpacing: "0.08em", color: "var(--rose)" }}>{enhanceError}</p></div>}
        {ocrText !== null && (
          <div style={{ padding: "0 1rem 0.75rem" }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "0.4rem" }}>
              <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)" }}>OCR result</span>
              <button onClick={() => setOcrText(null)} style={{ fontFamily: "var(--font-dm-mono)", fontSize: "0.48rem", letterSpacing: "0.1em", textTransform: "uppercase", background: "none", border: "none", cursor: "pointer", color: "var(--cream-2)" }}>Dismiss</button>
            </div>
            <pre style={{ fontFamily: "var(--font-dm-mono)", fontSize: "0.55rem", background: "rgba(240,233,214,0.04)", border: "1px solid rgba(240,233,214,0.08)", padding: "0.75rem", maxHeight: "12rem", overflowY: "auto", whiteSpace: "pre-wrap", wordBreak: "break-word", color: "var(--cream-1)" }}>{ocrText}</pre>
          </div>
        )}
        {transcript !== null && (
          <div style={{ padding: "0 1rem 0.75rem" }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "0.4rem" }}>
              <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)" }}>Transcript {transcriptStatus === "processing" && "(processing…)"}</span>
              <button onClick={() => setTranscript(null)} style={{ fontFamily: "var(--font-dm-mono)", fontSize: "0.48rem", letterSpacing: "0.1em", textTransform: "uppercase", background: "none", border: "none", cursor: "pointer", color: "var(--cream-2)" }}>Dismiss</button>
            </div>
            <pre style={{ fontFamily: "var(--font-dm-mono)", fontSize: "0.55rem", background: "rgba(240,233,214,0.04)", border: "1px solid rgba(240,233,214,0.08)", padding: "0.75rem", maxHeight: "12rem", overflowY: "auto", whiteSpace: "pre-wrap", wordBreak: "break-word", color: "var(--cream-1)" }}>{transcript}</pre>
          </div>
        )}
      </div>
    </div>
  );
}

function VideoPlayer({ src, poster }: { src: string; poster: string }) {
  const videoRef = useRef<HTMLVideoElement>(null);
  useEffect(() => {
    const video = videoRef.current; if (!video) return;
    if (video.canPlayType("application/vnd.apple.mpegurl")) { video.src = src; return; }
    let hls: any, cancelled = false;
    (async () => { const Hls = (await import("hls.js")).default; if (cancelled) return; if (Hls.isSupported()) { hls = new Hls(); hls.loadSource(src); hls.attachMedia(video); } else { video.src = src; } })();
    return () => { cancelled = true; if (hls) hls.destroy(); };
  }, [src]);
  return <video ref={videoRef} controls poster={poster} style={{ maxHeight: "100%", maxWidth: "100%" }} />;
}
