'use client';
import { useEffect, useState } from 'react';
import { useAuthStore } from '@/lib/store';
import { getMaterials } from '@/lib/api';

interface Material {
  public_id: string;
  url: string;
  thumb_url: string;
  width: number;
  height: number;
  bytes: number;
  format: string;
}

interface Props {
  lessonId: number;
}

function formatBytes(b: number): string {
  if (b < 1024) return `${b} B`;
  if (b < 1024 * 1024) return `${(b / 1024).toFixed(0)} kB`;
  return `${(b / (1024 * 1024)).toFixed(1)} MB`;
}

export default function MaterialsGallery({ lessonId }: Props) {
  const { token } = useAuthStore();
  const [items, setItems] = useState<Material[]>([]);
  const [mock, setMock] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) return;
    let alive = true;
    setLoading(true);
    getMaterials(token, lessonId)
      .then((res) => {
        if (!alive) return;
        setItems(res.items);
        setMock(res.mock);
      })
      .catch(() => alive && setMock(true))
      .finally(() => alive && setLoading(false));
    return () => { alive = false; };
  }, [token, lessonId]);

  if (loading) {
    return <div className="text-[10px] text-t3 italic">Loading materials…</div>;
  }

  if (mock) {
    return (
      <div className="text-[10px] text-t3 bg-bg2 border border-white/5 rounded-lg p-3">
        Cloudinary not configured. Upload an image in chat to start a personal library.
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="text-[10px] text-t3 bg-bg2 border border-white/5 rounded-lg p-3">
        Nothing uploaded yet. Drop an image in chat — SAGE will OCR and remember it.
      </div>
    );
  }

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2">
        <div className="text-[10px] font-bold uppercase tracking-widest text-ora">
          Your Materials · {items.length}
        </div>
        <span className="text-[9px] text-t3 ml-auto">stored on cloudinary</span>
      </div>
      <div className="grid grid-cols-3 gap-2">
        {items.map((m) => (
          <a
            key={m.public_id}
            href={m.url}
            target="_blank"
            rel="noopener noreferrer"
            className="group relative aspect-video bg-bg2 border border-white/5 rounded-lg overflow-hidden hover:border-ora/40 transition-colors"
          >
            <img
              src={m.thumb_url}
              alt={m.public_id}
              loading="lazy"
              className="w-full h-full object-cover"
              onError={(e) => {
                (e.currentTarget as HTMLImageElement).style.display = 'none';
              }}
            />
            <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/80 to-transparent px-1.5 py-1 flex items-center justify-between">
              <span className="text-[8px] font-bold text-white uppercase">{m.format}</span>
              <span className="text-[8px] font-bold text-white/70">{formatBytes(m.bytes)}</span>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
}
