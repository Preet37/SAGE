'use client';

interface Props {
  isOnline: boolean;
  syncedCount?: number;
}

export default function OfflineBadge({ isOnline, syncedCount }: Props) {
  if (isOnline && !syncedCount) return null;

  if (!isOnline) {
    return (
      <span
        role="status"
        aria-live="polite"
        className="flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-[11px] font-semibold"
        style={{
          background: 'rgba(234,179,8,0.1)',
          borderColor: 'rgba(234,179,8,0.3)',
          color: 'rgb(234,179,8)',
        }}
      >
        <span className="h-1.5 w-1.5 rounded-full bg-yellow-400" aria-hidden />
        Offline — AI running locally
      </span>
    );
  }

  if (syncedCount) {
    return (
      <span
        role="status"
        aria-live="polite"
        className="flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-[11px] font-semibold"
        style={{
          background: 'rgba(34,197,94,0.1)',
          borderColor: 'rgba(34,197,94,0.3)',
          color: 'rgb(34,197,94)',
        }}
      >
        <span className="h-1.5 w-1.5 rounded-full bg-green-400" aria-hidden />
        {syncedCount} item{syncedCount !== 1 ? 's' : ''} synced
      </span>
    );
  }

  return null;
}
