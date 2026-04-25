'use client';
import { useState, useRef } from 'react';

interface Props {
  beforeUrl: string;
  afterUrl: string;
  beforeLabel?: string;
  afterLabel?: string;
}

export default function BeforeAfter({
  beforeUrl,
  afterUrl,
  beforeLabel = 'Before',
  afterLabel = 'After',
}: Props) {
  const [split, setSplit] = useState(50);
  const containerRef = useRef<HTMLDivElement>(null);
  const dragging = useRef(false);

  function handleMouseMove(e: React.MouseEvent) {
    if (!dragging.current || !containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const pct = ((e.clientX - rect.left) / rect.width) * 100;
    setSplit(Math.max(5, Math.min(95, pct)));
  }

  return (
    <div
      ref={containerRef}
      className="relative overflow-hidden rounded-xl border border-orange-400/20 cursor-col-resize select-none"
      style={{ height: 200 }}
      onMouseMove={handleMouseMove}
      onMouseUp={() => {
        dragging.current = false;
      }}
      onMouseLeave={() => {
        dragging.current = false;
      }}
    >
      <img src={afterUrl} alt={afterLabel} className="absolute inset-0 w-full h-full object-cover" />

      <div className="absolute inset-0 overflow-hidden" style={{ width: `${split}%` }}>
        <img
          src={beforeUrl}
          alt={beforeLabel}
          className="absolute inset-0 h-full object-cover"
          style={{ width: containerRef.current?.offsetWidth ?? 400 }}
        />
      </div>

      <div
        className="absolute top-0 bottom-0 w-0.5 bg-orange-400/80"
        style={{ left: `${split}%` }}
        onMouseDown={(e) => {
          e.preventDefault();
          dragging.current = true;
        }}
      >
        <div className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-6 h-6 rounded-full bg-orange-400 border-2 border-white flex items-center justify-center shadow-lg">
          <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 9l-3 3 3 3M16 9l3 3-3 3" />
          </svg>
        </div>
      </div>

      <div className="absolute bottom-2 left-2 text-[9px] font-bold text-white bg-black/50 px-2 py-0.5 rounded">
        {beforeLabel}
      </div>
      <div className="absolute bottom-2 right-2 text-[9px] font-bold text-white bg-black/50 px-2 py-0.5 rounded">
        {afterLabel}
      </div>

      <div className="absolute top-2 right-2">
        <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-orange-500/80 text-white border border-orange-400">
          cloudinary
        </span>
      </div>
    </div>
  );
}
