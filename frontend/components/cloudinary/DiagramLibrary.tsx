'use client';
import { useEffect, useState } from 'react';
import { getDiagramLibrary } from '@/lib/api';

interface DiagramItem {
  label: string;
  url: string;
  thumb_url: string;
}

interface Props {
  courseId: number;
  lessonId: number;
  conceptSlug: string;
}

export default function DiagramLibrary({ courseId, lessonId, conceptSlug }: Props) {
  const [items, setItems] = useState<DiagramItem[]>([]);
  const [mock, setMock] = useState(false);
  const [expanded, setExpanded] = useState<DiagramItem | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    setLoading(true);
    getDiagramLibrary(courseId, lessonId, conceptSlug)
      .then((res) => {
        if (!alive) return;
        setItems(res.items);
        setMock(res.mock);
      })
      .catch(() => alive && setMock(true))
      .finally(() => alive && setLoading(false));
    return () => { alive = false; };
  }, [courseId, lessonId, conceptSlug]);

  if (loading) {
    return <div className="text-[10px] text-t3 italic">Loading diagrams…</div>;
  }

  if (mock || items.length === 0) {
    return (
      <div className="text-[10px] text-t3 bg-bg2 border border-white/5 rounded-lg p-3">
        No diagram library configured for this concept yet.
        <span className="block mt-1 text-ora/70">Cloudinary cloud not set.</span>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2">
        <div className="text-[10px] font-bold uppercase tracking-widest text-ora">
          Diagram Library · {items.length}
        </div>
        <span className="text-[9px] text-t3 ml-auto">cloudinary transformations</span>
      </div>
      <div className="grid grid-cols-4 gap-1.5">
        {items.map((item) => (
          <button
            key={item.label}
            onClick={() => setExpanded(item)}
            className="group relative aspect-video bg-bg2 border border-white/5 rounded-lg overflow-hidden hover:border-ora/40 transition-colors"
          >
            <img
              src={item.thumb_url}
              alt={item.label}
              loading="lazy"
              className="w-full h-full object-cover"
              onError={(e) => {
                (e.currentTarget as HTMLImageElement).style.display = 'none';
              }}
            />
            <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/80 to-transparent px-1.5 py-1">
              <span className="text-[9px] font-bold text-white">{item.label}</span>
            </div>
          </button>
        ))}
      </div>

      {expanded && (
        <div
          className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-8"
          onClick={() => setExpanded(null)}
        >
          <div className="max-w-4xl w-full" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-bold text-ora uppercase tracking-widest">
                {expanded.label}
              </span>
              <button
                onClick={() => setExpanded(null)}
                className="w-7 h-7 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white"
              >
                ×
              </button>
            </div>
            <img
              src={expanded.url}
              alt={expanded.label}
              className="w-full rounded-2xl border border-white/10"
              onError={(e) => {
                (e.currentTarget as HTMLImageElement).style.display = 'none';
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
