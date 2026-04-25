"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";
import {
  api,
  MediaAssetResponse,
  SketchExplainResponseT,
} from "@/lib/api";
import { cloudinaryUrl, uploadToCloudinary } from "@/lib/cloudinary";
import { AppHeader } from "@/components/AppHeader";
import { Button } from "@/components/ui/button";
import {
  Loader2,
  UploadCloud,
  Sparkles,
  Trash2,
  ImageIcon,
  Wand2,
  Scissors,
  Crop,
  Tag as TagIcon,
} from "lucide-react";

type Variant = "original" | "removed_bg" | "smart_crop" | "auto_color";

const VARIANTS: { id: Variant; label: string; icon: React.ReactNode; transformations: string[] }[] = [
  { id: "original",    label: "Original",       icon: <ImageIcon className="h-3.5 w-3.5" />, transformations: ["q_auto", "f_auto"] },
  { id: "removed_bg",  label: "Background-free", icon: <Scissors className="h-3.5 w-3.5" />,  transformations: ["e_background_removal", "f_auto"] },
  { id: "smart_crop",  label: "Smart-cropped",   icon: <Crop className="h-3.5 w-3.5" />,      transformations: ["c_thumb,w_512,h_512,g_auto", "f_auto"] },
  { id: "auto_color",  label: "Auto-balanced",   icon: <Wand2 className="h-3.5 w-3.5" />,     transformations: ["e_improve:outdoor", "f_auto"] },
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
      // Cloudinary's secure_url contains cloud name as the segment after /upload prefix.
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
      const res = await api.media.sketchExplain({
        asset_id: selected.id, note: explainNote || undefined,
      }, token);
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
    if (selected?.id === asset.id) {
      setSelected(null);
      setExplanation(null);
    }
  }

  const currentTransformation = VARIANTS.find((v) => v.id === variant)!;
  const previewUrl = selected && cloudName
    ? cloudinaryUrl(cloudName, selected.public_id, currentTransformation.transformations)
    : selected?.secure_url || "";

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      <AppHeader />
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-6xl mx-auto px-6 py-8">

          <header className="flex items-start justify-between gap-4 mb-6">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
                <Sparkles className="h-5 w-5" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">Sketch Studio</h1>
                <p className="text-sm text-muted-foreground">
                  Upload diagrams, equations, or screenshots. Cloudinary AI cleans them up;
                  the tutor explains what they show.
                </p>
              </div>
            </div>
            <input
              ref={inputRef} type="file" accept="image/*"
              onChange={(e) => { const f = e.target.files?.[0]; if (f) handleFile(f); }}
              className="hidden"
            />
            <Button onClick={() => inputRef.current?.click()} disabled={uploading}>
              {uploading ? <Loader2 className="h-4 w-4 mr-1.5 animate-spin" /> : <UploadCloud className="h-4 w-4 mr-1.5" />}
              {uploading ? `Uploading ${progress}%` : "Upload sketch"}
            </Button>
          </header>

          {error && (
            <div className="rounded-lg border border-destructive/40 bg-destructive/10 px-4 py-3 text-sm text-destructive mb-4">
              {error}
            </div>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Library */}
            <aside className="rounded-xl border border-border bg-card p-4">
              <h2 className="text-sm font-semibold mb-3">Your sketches</h2>
              {assets.length === 0 ? (
                <div className="rounded-lg border border-dashed border-border p-6 text-center text-xs text-muted-foreground">
                  No sketches yet. Upload one to begin.
                </div>
              ) : (
                <ul className="space-y-2 max-h-[60vh] overflow-y-auto pr-1">
                  {assets.map((a) => (
                    <li key={a.id}>
                      <button
                        onClick={() => { setSelected(a); setExplanation(null); const m = a.secure_url.match(/res\.cloudinary\.com\/([^/]+)\//); if (m) setCloudName(m[1]); }}
                        className={`w-full flex items-center gap-3 rounded-lg border px-2 py-2 text-left transition ${
                          selected?.id === a.id
                            ? "border-primary/60 bg-primary/5"
                            : "border-border hover:bg-muted/40"
                        }`}
                      >
                        <img src={a.secure_url} alt="" className="h-12 w-12 object-cover rounded-md flex-shrink-0" loading="lazy" />
                        <div className="min-w-0 flex-1">
                          <div className="text-xs font-medium truncate">{a.public_id.split("/").pop()}</div>
                          <div className="text-[11px] text-muted-foreground">{a.width}×{a.height} · {(a.bytes / 1024).toFixed(0)}kb</div>
                        </div>
                        <button
                          onClick={(ev) => { ev.stopPropagation(); handleDelete(a); }}
                          className="text-muted-foreground hover:text-destructive"
                          aria-label="Delete"
                        >
                          <Trash2 className="h-3.5 w-3.5" />
                        </button>
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </aside>

            {/* Detail */}
            <section className="lg:col-span-2 space-y-4">
              {!selected ? (
                <div className="rounded-xl border border-dashed border-border bg-muted/30 p-12 text-center">
                  <ImageIcon className="h-10 w-10 text-muted-foreground mx-auto mb-3" />
                  <p className="text-sm text-muted-foreground">
                    Upload a sketch to see Cloudinary AI transformations and tutor explanations.
                  </p>
                </div>
              ) : (
                <>
                  <div className="rounded-xl border border-border bg-card p-4">
                    <div className="flex items-center justify-between mb-3">
                      <h2 className="text-sm font-semibold">Cloudinary AI variants</h2>
                      <span className="text-xs text-muted-foreground">delivered via CDN</span>
                    </div>
                    <div className="flex flex-wrap gap-2 mb-4">
                      {VARIANTS.map((v) => (
                        <button
                          key={v.id}
                          onClick={() => setVariant(v.id)}
                          className={`inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs transition ${
                            variant === v.id
                              ? "bg-primary text-primary-foreground border-primary"
                              : "bg-background hover:bg-muted/50"
                          }`}
                        >
                          {v.icon}
                          {v.label}
                        </button>
                      ))}
                    </div>
                    <div className="rounded-lg overflow-hidden bg-checker">
                      {/* eslint-disable-next-line @next/next/no-img-element */}
                      <img src={previewUrl} alt="" className="w-full max-h-[460px] object-contain bg-muted/30" />
                    </div>
                  </div>

                  <div className="rounded-xl border border-border bg-card p-4">
                    <h2 className="text-sm font-semibold mb-3 flex items-center gap-2">
                      <Sparkles className="h-4 w-4 text-primary" /> Explain with the tutor
                    </h2>
                    <textarea
                      value={explainNote}
                      onChange={(e) => setExplainNote(e.target.value)}
                      placeholder="What's confusing about this image? (optional — leave blank for a general explanation)"
                      rows={2}
                      className="w-full px-3 py-2 mb-3 rounded-lg border border-border bg-background text-sm"
                    />
                    <Button onClick={handleExplain} disabled={explaining}>
                      {explaining ? <Loader2 className="h-4 w-4 mr-1.5 animate-spin" /> : <Wand2 className="h-4 w-4 mr-1.5" />}
                      Explain this sketch
                    </Button>

                    {explanation && (
                      <div className="mt-4 space-y-3">
                        <p className="text-sm text-foreground/90 leading-relaxed whitespace-pre-wrap">
                          {explanation.explanation}
                        </p>
                        {explanation.detected_concepts.length > 0 && (
                          <div className="flex flex-wrap items-center gap-1.5">
                            <TagIcon className="h-3.5 w-3.5 text-muted-foreground" />
                            {explanation.detected_concepts.map((c) => (
                              <span key={c} className="text-[11px] bg-muted text-foreground/80 rounded-full px-2 py-0.5">
                                {c}
                              </span>
                            ))}
                          </div>
                        )}
                        {explanation.suggested_prompt && (
                          <div className="rounded-lg border border-primary/40 bg-primary/5 px-3 py-2 text-sm">
                            <div className="text-[11px] uppercase tracking-wide text-primary font-semibold mb-1">
                              Try asking the tutor
                            </div>
                            <p className="text-foreground/90 italic">{explanation.suggested_prompt}</p>
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
