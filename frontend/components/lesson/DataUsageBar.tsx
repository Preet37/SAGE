'use client';
import { useTutorStore } from '@/lib/store';

interface Props {
  bytesThisSession: number;
}

function formatBytes(b: number): string {
  if (b < 1024) return `${b}B`;
  if (b < 1024 * 1024) return `${(b / 1024).toFixed(1)}KB`;
  return `${(b / (1024 * 1024)).toFixed(2)}MB`;
}

export default function DataUsageBar({ bytesThisSession }: Props) {
  const { lowDataMode, setLowDataMode } = useTutorStore();

  return (
    <div className={`flex items-center gap-2 px-2 py-1 rounded-lg border transition-all text-[10px] font-semibold ${
      lowDataMode
        ? 'bg-grn/10 border-grn/30 text-grn'
        : 'bg-white/5 border-white/10 text-t3 hover:text-t2'
    }`}>
      <button
        onClick={() => setLowDataMode(!lowDataMode)}
        title={lowDataMode ? 'Data Saver ON — click to disable' : 'Enable Data Saver (2G mode)'}
        className="flex items-center gap-1.5"
        aria-pressed={lowDataMode}
      >
        {/* Signal bars icon */}
        <svg className="w-3 h-3" viewBox="0 0 24 24" fill="currentColor">
          <rect x="1" y="16" width="4" height="7" rx="1" opacity={lowDataMode ? 1 : 0.3} />
          <rect x="7" y="11" width="4" height="12" rx="1" opacity={lowDataMode ? 1 : 0.5} />
          <rect x="13" y="6"  width="4" height="17" rx="1" opacity={lowDataMode ? 0.5 : 1} />
          <rect x="19" y="1"  width="4" height="22" rx="1" opacity={lowDataMode ? 0.3 : 1} />
        </svg>
        {lowDataMode ? '2G' : 'Data'}
      </button>
      {bytesThisSession > 0 && (
        <span className="text-t3 font-normal">~{formatBytes(bytesThisSession)}</span>
      )}
    </div>
  );
}
