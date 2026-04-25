"use client";

interface Props {
  isOnline: boolean;
  syncedCount?: number;
}

export default function OfflineBadge({ isOnline, syncedCount }: Props) {
  if (isOnline && !syncedCount) return null;

  if (!isOnline) {
    return (
      <div
        role="status"
        aria-live="polite"
        className="flex items-center gap-1.5 rounded-full px-3 py-1"
        style={{
          background: "oklch(85% 0.12 60)",
          color: "oklch(30% 0.12 60)",
          border: "1px solid oklch(70% 0.12 60)",
          fontSize: 12,
          fontWeight: 600,
        }}
      >
        <span
          className="inline-block h-2 w-2 rounded-full"
          style={{ background: "oklch(55% 0.18 50)" }}
          aria-hidden
        />
        Offline — AI running locally
      </div>
    );
  }

  if (syncedCount) {
    return (
      <div
        role="status"
        aria-live="polite"
        className="flex items-center gap-1.5 rounded-full px-3 py-1"
        style={{
          background: "oklch(90% 0.1 145)",
          color: "oklch(30% 0.12 145)",
          border: "1px solid oklch(70% 0.1 145)",
          fontSize: 12,
          fontWeight: 600,
        }}
      >
        <span
          className="inline-block h-2 w-2 rounded-full"
          style={{ background: "oklch(55% 0.18 145)" }}
          aria-hidden
        />
        {syncedCount} item{syncedCount !== 1 ? "s" : ""} synced
      </div>
    );
  }

  return null;
}
