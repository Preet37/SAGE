"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";
import { api, MediaAssetResponse, SketchExplainResponseT } from "@/lib/api";
import { cloudinaryUrl, uploadToCloudinary } from "@/lib/cloudinary";
import { AppHeader } from "@/components/AppHeader";
import { Loader2, UploadCloud, Sparkles, Trash2, ImageIcon, Wand2, Scissors, Crop, Tag as TagIcon } from "lucide-react";

const mono: React.CSSProperties  = { fontFamily: "var(--font-dm-mono)" };
const serif: React.CSSProperties = { fontFamily: "var(--font-cormorant)" };
const body: React.CSSProperties  = { fontFamily: "var(--font-crimson)" };

type Variant = "original" | "removed_bg" | "smart_crop" | "auto_color";

const VARIANTS: { id: Variant; label: string; icon: React.ReactNode; transformations: string[] }[] = [
  { id: "original",   label: "Original",       icon: <ImageIcon style={{ width: "0.75rem", height: "0.75rem" }} />, transformations: ["q_auto", "f_auto"] },
  { id: "removed_bg", label: "No Background",  icon: <Scissors style={{ width: "0.75rem", height: "0.75rem" }} />,  transformations: ["e_background_removal", "f_auto"] },
  { id: "smart_crop", label: "Smart Crop",     icon: <Crop style={{ width: "0.75rem", height: "0.75rem" }} />,      transformations: ["c_thumb,w_512,h_512,g_auto", "f_auto"] },
  { id: "auto_color", label: "Auto Balance",   icon: <Wand2 style={{ width: "0.75rem", height: "0.75rem" }} />,     transformations: ["e_improve:outdoor", "f_auto"] },
];

export default function SketchPage() {
  const router = useRouter();
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [assets, setAssets] = useState<MediaAssetResponse[]>([]);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [selected, setSelected] = useState<MediaAssetResponse | null>(null);
  const [variant, setVariant] = useState<Variant>("original");
  const [explainNote, setExplainNote] = useState("");
  const [explanation, setExplanation] = useState<SketchExplainResponseT | null>(null);
  const [explaining, setExplaining] = useState(false);
  const [cloudName, setCloudName] = useState<string>("");

  useEffect(() => {
    const token = getToken();
    if (!token) { router.push("/login"); return; }
    api.media.listAssets(token, undefined, "sketch").then(setAssets).catch(() => {});
  }, [router]);

  async function handleFile(file: File) {
    setError(null);
    setUploading(true);
    setProgress(0);
    try {
      const asset = await uploadToCloudinary(file, {
        kind: "sketch",
        tags: ["sage_sketch"],
        onProgress: (p) => setProgress(p),
      });
      setAssets((prev) => [asset, ...prev]);
      setSelected(asset);
      setExplanation(null);
      const m = asset.secure_url.match(/res\.cloudinary\.com\/([^/]+)\//);
      if (m) setCloudName(m[1]);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Upload failed");
    } finally {
      setUploading(false);
      setProgress(0);
    }
  }

  async function handleExplain() {
    if (!selected) return;
    const token = getToken();
    if (!token) return;
    setExplaining(true);
    setError(null);
    try {
      const res = await api.media.sketchExplain({ asset_id: selected.id, note: explainNote || undefined }, token);
      setExplanation(res);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Explain failed");
    } finally {
      setExplaining(false);
    }
  }

  async function handleDelete(asset: MediaAssetResponse) {
    const token = getToken();
    if (!token) return;
    await api.media.deleteAsset(asset.id, token);
    setAssets((prev) => prev.filter((a) => a.id !== asset.id));
    if (selected?.id === asset.id) { setSelected(null); setExplanation(null); }
  }

  const currentTransformation = VARIANTS.find((v) => v.id === variant)!;
  const previewUrl = selected && cloudName
    ? cloudinaryUrl(cloudName, selected.public_id, currentTransformation.transformations)
    : selected?.secure_url || "";

  return (
    <div className="flex flex-col h-screen overflow-hidden" style={{ background: "var(--ink)", color: "var(--cream-0)" }}>
      <AppHeader />
      <main className="flex-1 overflow-y-auto thin-scrollbar">
        <div style={{ maxWidth: "72rem", margin: "0 auto", padding: "2.5rem 1.5rem 4rem" }}>

          <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: "1rem", marginBottom: "2rem" }}>
            <div>
              <p style={{ ...mono, fontSize: "0.58rem", letterSpacing: "0.16em", textTransform: "uppercase", color: "var(--gold)", marginBottom: "0.5rem" }}>Sketch Studio</p>
              <h1 style={{ ...serif, fontWeight: 700, fontStyle: "italic", fontSize: "clamp(1.75rem,4vw,2.5rem)", color: "var(--cream-0)", lineHeight: 1.1, marginBottom: "0.4rem" }}>
                See what you drew<span style={{ color: "var(--gold)" }}>.</span>
              </h1>
              <p style={{ ...body, fontSize: "0.95rem", color: "var(--cream-1)", lineHeight: 1.6 }}>
                Upload diagrams, equations, or screenshots. Cloudinary AI cleans them up; the tutor explains what they show.
              </p>
            </div>
            <input ref={inputRef} type="file" accept="image/*" onChange={(e) => { const f = e.target.files?.[0]; if (f) handleFile(f); }} style={{ display: "none" }} />
            <button
              onClick={() => inputRef.current?.click()}
              disabled={uploading}
              style={{ ...mono, display: "flex", alignItems: "center", gap: "0.4rem", fontSize: "0.52rem", letterSpacing: "0.12em", textTransform: "uppercase", padding: "0.55rem 1rem", background: uploading ? "rgba(196,152,90,0.3)" : "var(--gold)", color: uploading ? "var(--cream-2)" : "var(--ink)", border: "none", cursor: uploading ? "not-allowed" : "pointer", flexShrink: 0 }}
            >
              {uploading ? <Loader2 style={{ width: "0.75rem", height: "0.75rem" }} className="animate-spin" /> : <UploadCloud style={{ width: "0.75rem", height: "0.75rem" }} />}
              {uploading ? `Uploading ${progress}%` : "Upload sketch"}
            </button>
          </div>

          {uploading && progress > 0 && (
            <div style={{ height: "2px", background: "rgba(240,233,214,0.08)", marginBottom: "1.5rem", overflow: "hidden" }}>
              <div style={{ height: "100%", background: "var(--gold)", transition: "width 0.3s", width: `${progress}%` }} />
            </div>
          )}

          {error && (
            <div style={{ background: "rgba(201,124,104,0.08)", border: "1px solid rgba(201,124,104,0.3)", padding: "0.65rem 1rem", marginBottom: "1rem" }}>
              <p style={{ ...body, fontSize: "0.9rem", color: "var(--rose)" }}>{error}</p>
            </div>
          )}

          <div style={{ display: "grid", gridTemplateColumns: "1fr 2fr", gap: "1rem" }}>
            {/* Library */}
            <aside style={{ background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.07)", padding: "1.25rem" }}>
              <p style={{ ...mono, fontSize: "0.52rem", letterSpacing: "0.12em", textTransform: "uppercase", color: "var(--cream-2)", marginBottom: "0.85rem" }}>Your sketches</p>
              {assets.length === 0 ? (
                <div style={{ border: "1px dashed rgba(240,233,214,0.1)", padding: "2rem 1rem", textAlign: "center" }}>
                  <p style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.08em", textTransform: "uppercase", color: "var(--cream-2)" }}>No sketches yet. Upload one to begin.</p>
                </div>
              ) : (
                <ul style={{ listStyle: "none", padding: 0, margin: 0, maxHeight: "60vh", overflowY: "auto" }} className="thin-scrollbar">
                  {assets.map((a) => (
                    <li key={a.id} style={{ marginBottom: "0.5rem" }}>
                      <button
                        onClick={() => { setSelected(a); setExplanation(null); const m = a.secure_url.match(/res\.cloudinary\.com\/([^/]+)\//); if (m) setCloudName(m[1]); }}
                        style={{ width: "100%", display: "flex", alignItems: "center", gap: "0.65rem", padding: "0.5rem", background: selected?.id === a.id ? "rgba(196,152,90,0.08)" : "transparent", border: `1px solid ${selected?.id === a.id ? "rgba(196,152,90,0.4)" : "rgba(240,233,214,0.06)"}`, cursor: "pointer", textAlign: "left", transition: "border-color 0.15s" }}
                      >
                        {/* eslint-disable-next-line @next/next/no-img-element */}
                        <img src={a.secure_url} alt="" style={{ width: "3rem", height: "3rem", objectFit: "cover", flexShrink: 0 }} loading="lazy" />
                        <div style={{ minWidth: 0, flex: 1 }}>
                          <div style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.06em", color: "var(--cream-1)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{a.public_id.split("/").pop()}</div>
                          <div style={{ ...mono, fontSize: "0.45rem", color: "var(--cream-2)", marginTop: "0.2rem" }}>{a.width}×{a.height} · {(a.bytes / 1024).toFixed(0)}kb</div>
                        </div>
                        <button
                          onClick={(ev) => { ev.stopPropagation(); handleDelete(a); }}
                          style={{ background: "none", border: "none", cursor: "pointer", color: "var(--cream-2)", padding: "0.2rem", flexShrink: 0 }}
                          aria-label="Delete"
                        >
                          <Trash2 style={{ width: "0.75rem", height: "0.75rem" }} />
                        </button>
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </aside>

            {/* Detail */}
            <section style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
              {!selected ? (
                <div style={{ border: "1px dashed rgba(240,233,214,0.1)", padding: "4rem 1rem", textAlign: "center", background: "var(--ink-1)" }}>
                  <ImageIcon style={{ width: "2.5rem", height: "2.5rem", color: "var(--cream-2)", margin: "0 auto 0.75rem", opacity: 0.4 }} />
                  <p style={{ ...mono, fontSize: "0.52rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)" }}>
                    Upload a sketch to see Cloudinary AI transformations and tutor explanations.
                  </p>
                </div>
              ) : (
                <>
                  {/* Variants */}
                  <div style={{ background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.07)", padding: "1.25rem" }}>
                    <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "0.85rem" }}>
                      <p style={{ ...mono, fontSize: "0.52rem", letterSpacing: "0.12em", textTransform: "uppercase", color: "var(--cream-2)" }}>Cloudinary AI variants</p>
                      <span style={{ ...mono, fontSize: "0.45rem", letterSpacing: "0.06em", color: "var(--cream-2)" }}>delivered via CDN</span>
                    </div>
                    <div style={{ display: "flex", flexWrap: "wrap", gap: "0.4rem", marginBottom: "1rem" }}>
                      {VARIANTS.map((v) => (
                        <button
                          key={v.id}
                          onClick={() => setVariant(v.id)}
                          style={{ ...mono, display: "flex", alignItems: "center", gap: "0.35rem", fontSize: "0.48rem", letterSpacing: "0.1em", textTransform: "uppercase", padding: "0.3rem 0.65rem", background: variant === v.id ? "var(--gold)" : "transparent", color: variant === v.id ? "var(--ink)" : "var(--cream-2)", border: `1px solid ${variant === v.id ? "var(--gold)" : "rgba(240,233,214,0.12)"}`, cursor: "pointer", transition: "all 0.15s" }}
                        >
                          {v.icon} {v.label}
                        </button>
                      ))}
                    </div>
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img src={previewUrl} alt="" style={{ width: "100%", maxHeight: "460px", objectFit: "contain", background: "rgba(240,233,214,0.03)", display: "block" }} />
                  </div>

                  {/* Explain */}
                  <div style={{ background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.07)", padding: "1.25rem" }}>
                    <p style={{ ...mono, fontSize: "0.52rem", letterSpacing: "0.12em", textTransform: "uppercase", color: "var(--cream-2)", marginBottom: "0.75rem", display: "flex", alignItems: "center", gap: "0.4rem" }}>
                      <Sparkles style={{ width: "0.7rem", height: "0.7rem", color: "var(--gold)" }} /> Explain with the tutor
                    </p>
                    <textarea
                      value={explainNote}
                      onChange={(e) => setExplainNote(e.target.value)}
                      placeholder="What's confusing about this image? (optional)"
                      rows={2}
                      style={{ width: "100%", padding: "0.6rem 0.85rem", marginBottom: "0.75rem", background: "var(--ink-2)", border: "1px solid rgba(240,233,214,0.08)", outline: "none", ...body, fontSize: "0.9rem", color: "var(--cream-0)", resize: "vertical", boxSizing: "border-box" }}
                    />
                    <button
                      onClick={handleExplain}
                      disabled={explaining}
                      style={{ ...mono, display: "flex", alignItems: "center", gap: "0.4rem", fontSize: "0.52rem", letterSpacing: "0.12em", textTransform: "uppercase", padding: "0.5rem 0.9rem", background: explaining ? "rgba(196,152,90,0.3)" : "var(--gold)", color: explaining ? "var(--cream-2)" : "var(--ink)", border: "none", cursor: explaining ? "not-allowed" : "pointer" }}
                    >
                      {explaining ? <Loader2 style={{ width: "0.75rem", height: "0.75rem" }} className="animate-spin" /> : <Wand2 style={{ width: "0.75rem", height: "0.75rem" }} />}
                      Explain this sketch
                    </button>

                    {explanation && (
                      <div style={{ marginTop: "1.25rem" }}>
                        <p style={{ ...body, fontSize: "0.95rem", color: "var(--cream-1)", lineHeight: 1.7, whiteSpace: "pre-wrap", marginBottom: "1rem" }}>{explanation.explanation}</p>
                        {explanation.detected_concepts.length > 0 && (
                          <div style={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: "0.4rem", marginBottom: "0.75rem" }}>
                            <TagIcon style={{ width: "0.7rem", height: "0.7rem", color: "var(--cream-2)" }} />
                            {explanation.detected_concepts.map((c) => (
                              <span key={c} style={{ ...mono, fontSize: "0.45rem", letterSpacing: "0.08em", textTransform: "uppercase", color: "var(--gold)", border: "1px solid rgba(196,152,90,0.3)", padding: "0.1rem 0.4rem" }}>{c}</span>
                            ))}
                          </div>
                        )}
                        {explanation.suggested_prompt && (
                          <div style={{ border: "1px solid rgba(196,152,90,0.25)", background: "rgba(196,152,90,0.05)", padding: "0.75rem 1rem" }}>
                            <p style={{ ...mono, fontSize: "0.48rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--gold)", marginBottom: "0.4rem" }}>Try asking the tutor</p>
                            <p style={{ ...body, fontStyle: "italic", fontSize: "0.9rem", color: "var(--cream-1)" }}>{explanation.suggested_prompt}</p>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </>
              )}
            </section>
          </div>
        </div>
      </main>
    </div>
  );
}
