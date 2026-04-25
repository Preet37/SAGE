"use client";

import { useCallback, useRef, useState } from "react";

import { API_BASE } from "@/lib/api";

interface UploadedPdf {
  url: string;
  publicId: string;
}

interface CropResult {
  cropped_url: string;
  page: number;
  topic: string;
}

export default function PdfViewer({ token }: { token: string }) {
  const [pdf, setPdf] = useState<UploadedPdf | null>(null);
  const [crop, setCrop] = useState<CropResult | null>(null);
  const [topic, setTopic] = useState("");
  const [busy, setBusy] = useState<"idle" | "upload" | "crop">("idle");
  const [zoom, setZoom] = useState(1);
  const [error, setError] = useState<string | null>(null);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const draggingRef = useRef<{ startX: number; startY: number; baseX: number; baseY: number } | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const onUpload = useCallback(
    async (file: File) => {
      setBusy("upload");
      setError(null);
      try {
        const fd = new FormData();
        fd.append("file", file);
        const res = await fetch(`${API_BASE}/notes/upload-pdf`, {
          method: "POST",
          headers: { Authorization: `Bearer ${token}` },
          body: fd,
        });
        if (!res.ok) throw new Error(`upload failed (${res.status})`);
        const data = (await res.json()) as { url: string; public_id: string };
        setPdf({ url: data.url, publicId: data.public_id });
        setCrop(null);
        setZoom(1);
        setPan({ x: 0, y: 0 });
      } catch (err) {
        setError(err instanceof Error ? err.message : "upload failed");
      } finally {
        setBusy("idle");
      }
    },
    [token],
  );

  const onCrop = useCallback(async () => {
    if (!pdf || !topic.trim()) return;
    setBusy("crop");
    setError(null);
    try {
      const url = `${API_BASE}/notes/fetch-crop?public_id=${encodeURIComponent(pdf.publicId)}&topic=${encodeURIComponent(topic)}`;
      const res = await fetch(url, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error(`crop failed (${res.status})`);
      setCrop((await res.json()) as CropResult);
      setZoom(1);
      setPan({ x: 0, y: 0 });
    } catch (err) {
      setError(err instanceof Error ? err.message : "crop failed");
    } finally {
      setBusy("idle");
    }
  }, [pdf, token, topic]);

  const startDrag = (e: React.PointerEvent) => {
    if (zoom === 1) return;
    (e.target as HTMLElement).setPointerCapture(e.pointerId);
    draggingRef.current = { startX: e.clientX, startY: e.clientY, baseX: pan.x, baseY: pan.y };
  };
  const onDrag = (e: React.PointerEvent) => {
    const d = draggingRef.current;
    if (!d) return;
    setPan({ x: d.baseX + (e.clientX - d.startX), y: d.baseY + (e.clientY - d.startY) });
  };
  const endDrag = () => { draggingRef.current = null; };

  const displayUrl = crop?.cropped_url ?? pdf?.url;

  return (
    <div className="card flex h-full min-h-0 flex-col overflow-hidden p-5">
      <div className="flex items-center justify-between gap-3">
        <div>
          <h2 className="text-lg">PDF Notes</h2>
          <p className="text-sm" style={{ opacity: 0.6 }}>
            Upload, then crop a page to a topic.
          </p>
        </div>
        {pdf && (
          <button className="btn-ghost" onClick={() => { setPdf(null); setCrop(null); }}>
            Reset
          </button>
        )}
      </div>

      {!pdf ? (
        <Dropzone busy={busy === "upload"} onPick={() => fileInputRef.current?.click()} />
      ) : (
        <>
          <TopicBar
            topic={topic}
            setTopic={setTopic}
            onCrop={onCrop}
            cropping={busy === "crop"}
            page={crop?.page}
          />
          <div
            className="relative mt-3 flex-1 overflow-hidden rounded-2xl"
            style={{ background: "var(--color-surface-tint)", border: "1px solid var(--glass-border)" }}
            onPointerDown={startDrag}
            onPointerMove={onDrag}
            onPointerUp={endDrag}
            onPointerCancel={endDrag}
          >
            {displayUrl && (
              // eslint-disable-next-line @next/next/no-img-element
              <img
                src={displayUrl}
                alt={crop ? `Page ${crop.page} cropped to ${crop.topic}` : "Uploaded document"}
                draggable={false}
                style={{
                  position: "absolute",
                  top: "50%", left: "50%",
                  transform: `translate(calc(-50% + ${pan.x}px), calc(-50% + ${pan.y}px)) scale(${zoom})`,
                  transformOrigin: "center",
                  transition: draggingRef.current ? "none" : "transform 200ms ease",
                  maxWidth: "100%",
                  maxHeight: "100%",
                  cursor: zoom > 1 ? (draggingRef.current ? "grabbing" : "grab") : "default",
                  userSelect: "none",
                }}
              />
            )}
            <ZoomControls zoom={zoom} setZoom={setZoom} reset={() => { setZoom(1); setPan({x:0,y:0}); }} />
          </div>
        </>
      )}

      <input
        ref={fileInputRef}
        type="file"
        accept="application/pdf"
        className="hidden"
        onChange={(e) => {
          const f = e.target.files?.[0];
          if (f) onUpload(f);
        }}
      />

      {error && (
        <p className="mt-2 text-xs" style={{ color: "var(--color-destructive)" }}>
          {error}
        </p>
      )}
    </div>
  );
}

function Dropzone({ busy, onPick }: { busy: boolean; onPick: () => void }) {
  return (
    <button
      onClick={onPick}
      disabled={busy}
      className="mt-4 flex flex-1 flex-col items-center justify-center gap-3 rounded-2xl text-sm"
      style={{
        background: "rgba(255,255,255,0.4)",
        border: "2px dashed var(--glass-border)",
        cursor: busy ? "wait" : "pointer",
      }}
    >
      <div
        className="grid h-12 w-12 place-items-center rounded-2xl"
        style={{
          background: "linear-gradient(135deg, var(--color-ring), var(--color-secondary))",
          color: "white",
          boxShadow: "var(--shadow-md)",
        }}
        aria-hidden
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <path d="M12 19V5" /><path d="m5 12 7-7 7 7" />
        </svg>
      </div>
      <p className="font-semibold">{busy ? "Uploading…" : "Click to upload a PDF"}</p>
      <p className="text-xs" style={{ opacity: 0.6 }}>Backed by Cloudinary · cropped per topic via Gemini</p>
    </button>
  );
}

function TopicBar({
  topic, setTopic, onCrop, cropping, page,
}: {
  topic: string; setTopic: (s: string) => void;
  onCrop: () => void; cropping: boolean; page?: number;
}) {
  return (
    <div className="mt-3 flex items-center gap-2">
      <input
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && onCrop()}
        placeholder="Topic to crop to (e.g. mitochondria)"
        className="flex-1 rounded-xl px-3 py-2 text-sm outline-none"
        style={{
          background: "rgba(255,255,255,0.6)",
          border: "1px solid var(--glass-border)",
        }}
      />
      <button onClick={onCrop} disabled={cropping || !topic.trim()} className="btn-primary disabled:opacity-50">
        {cropping ? "…" : "Crop"}
      </button>
      {page !== undefined && (
        <span className="rounded-full px-2.5 py-1 text-xs font-semibold"
          style={{ background: "rgba(255,255,255,0.6)", border: "1px solid var(--glass-border)" }}>
          p. {page}
        </span>
      )}
    </div>
  );
}

function ZoomControls({
  zoom, setZoom, reset,
}: {
  zoom: number; setZoom: (n: number) => void; reset: () => void;
}) {
  return (
    <div
      className="absolute bottom-3 right-3 flex items-center gap-1 rounded-full p-1"
      style={{
        background: "rgba(255,255,255,0.85)",
        border: "1px solid var(--glass-border)",
        boxShadow: "var(--shadow-sm)",
        backdropFilter: "blur(8px)",
      }}
    >
      <ZoomBtn onClick={() => setZoom(Math.max(0.5, +(zoom - 0.25).toFixed(2)))} aria="Zoom out">−</ZoomBtn>
      <button
        onClick={reset}
        className="px-2 text-xs font-semibold tabular-nums"
        style={{ color: "var(--color-foreground)", cursor: "pointer" }}
        aria-label="Reset zoom"
      >
        {Math.round(zoom * 100)}%
      </button>
      <ZoomBtn onClick={() => setZoom(Math.min(3, +(zoom + 0.25).toFixed(2)))} aria="Zoom in">+</ZoomBtn>
    </div>
  );
}

function ZoomBtn({ onClick, aria, children }: { onClick: () => void; aria: string; children: React.ReactNode }) {
  return (
    <button
      onClick={onClick}
      aria-label={aria}
      className="grid h-7 w-7 place-items-center rounded-full text-base font-bold"
      style={{ color: "var(--color-foreground)", cursor: "pointer" }}
    >
      {children}
    </button>
  );
}
