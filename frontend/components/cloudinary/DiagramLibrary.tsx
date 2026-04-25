'use client';
import { useEffect, useState } from 'react';
import { useAuthStore } from '@/lib/store';
import { buildDiagramUrl, buildThumbnailUrl } from '@/lib/cloudinary';

interface DiagramEntry {
  public_id: string;
  url: string;
  format: string;
}

interface Props {
  courseId: number;
  lessonId: number;
  conceptSlug?: string;
}

export default function DiagramLibrary({ courseId, lessonId, conceptSlug = 'overview' }: Props) {
  const { token } = useAuthStore();
  const [diagrams, setDiagrams] = useState<DiagramEntry[]>([]);
  const [selected, setSelected] = useState<DiagramEntry | null>(null);

  useEffect(() => {
    if (!token) return;
    fetch(`/api/media/diagram/${courseId}/${lessonId}/${conceptSlug}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then((data) => {
        if (Array.isArray(data)) setDiagrams(data);
        else if (data?.url) setDiagrams([data as DiagramEntry]);
      })
      .catch(() => {});
  }, [token, courseId, lessonId, conceptSlug]);

  if (diagrams.length === 0) {
    return (
      <div className="text-center py-6 text-t3 text-xs">
        <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-orange-500/15 text-orange-400 border border-orange-500/20 block mb-2 w-fit mx-auto">
          cloudinary
        </span>
        No diagrams available yet
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-[10px] font-bold uppercase tracking-widest text-orange-400">
          Concept Diagrams
        </span>
        <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-orange-500/15 text-orange-400 border border-orange-500/20">
          cloudinary ↗
        </span>
      </div>

      <div className="grid grid-cols-2 gap-2">
        {diagrams.map((d) => (
          <button
            key={d.public_id}
            onClick={() => setSelected(selected?.public_id === d.public_id ? null : d)}
            className="rounded-lg overflow-hidden border border-white/5 hover:border-orange-400/30 transition-all"
          >
            <img
              src={buildThumbnailUrl(d.public_id)}
              alt={d.public_id.split('/').pop()}
              className="w-full h-24 object-cover"
            />
          </button>
        ))}
      </div>

      {selected && (
        <div className="rounded-xl border border-orange-400/20 overflow-hidden">
          <img
            src={buildDiagramUrl(selected.public_id, 800)}
            alt={selected.public_id.split('/').pop()}
            className="w-full object-contain max-h-64"
          />
          <div className="px-3 py-1.5 bg-orange-500/5 text-[9px] text-orange-400">
            {selected.public_id.split('/').pop()}
          </div>
        </div>
      )}
    </div>
  );
}
