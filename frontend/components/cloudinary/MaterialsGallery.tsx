'use client';
import { useEffect, useState } from 'react';
import { useAuthStore } from '@/lib/store';
import { buildThumbnailUrl, buildEnhancedUrl } from '@/lib/cloudinary';

interface MaterialEntry {
  public_id: string;
  secure_url: string;
  format: string;
  created_at: string;
  bytes: number;
  width?: number;
  height?: number;
}

interface Props {
  lessonId: number;
}

export default function MaterialsGallery({ lessonId }: Props) {
  const { token } = useAuthStore();
  const [materials, setMaterials] = useState<MaterialEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<MaterialEntry | null>(null);

  useEffect(() => {
    if (!token) return;
    fetch(`/api/media/materials/${lessonId}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then((data) => setMaterials((data.materials as MaterialEntry[]) ?? []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [token, lessonId]);

  if (loading) {
    return <div className="text-xs text-t3 py-4 text-center">Loading materials…</div>;
  }

  if (materials.length === 0) {
    return (
      <div className="text-center py-6 text-t3 text-xs">
        <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-orange-500/15 text-orange-400 border border-orange-500/20 block mb-2 w-fit mx-auto">
          cloudinary
        </span>
        No materials uploaded yet — use the image button in chat to share diagrams or notes
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-[10px] font-bold uppercase tracking-widest text-orange-400">
          Lesson Materials
        </span>
        <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-orange-500/15 text-orange-400 border border-orange-500/20">
          cloudinary ↗
        </span>
      </div>

      <div className="grid grid-cols-3 gap-2">
        {materials.map((m) => (
          <button
            key={m.public_id}
            onClick={() => setSelected(selected?.public_id === m.public_id ? null : m)}
            className="rounded-lg overflow-hidden border border-white/5 hover:border-orange-400/30 transition-all group relative"
          >
            <img
              src={buildThumbnailUrl(m.public_id)}
              alt={m.public_id.split('/').pop()}
              className="w-full h-16 object-cover"
            />
            <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-all flex items-center justify-center">
              <span className="text-[9px] text-white font-semibold">View</span>
            </div>
          </button>
        ))}
      </div>

      {selected && (
        <div className="rounded-xl border border-orange-400/20 overflow-hidden">
          <img
            src={buildEnhancedUrl(selected.public_id, 800)}
            alt={selected.public_id.split('/').pop()}
            className="w-full object-contain max-h-64"
          />
          <div className="px-3 py-1.5 bg-orange-500/5 flex items-center justify-between text-[9px] text-orange-400">
            <span>{selected.public_id.split('/').pop()}</span>
            <span>{(selected.bytes / 1024).toFixed(0)} KB</span>
          </div>
        </div>
      )}
    </div>
  );
}
