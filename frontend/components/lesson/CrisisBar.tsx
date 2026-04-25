'use client';
import { useTutorStore } from '@/lib/store';
import { t } from '@/lib/i18n';

export default function CrisisBar() {
  const { language, crisisDetected, setCrisisDetected } = useTutorStore();

  if (!crisisDetected) return null;

  return (
    <div
      role="status"
      aria-live="polite"
      className="flex-shrink-0 flex items-center gap-3 px-4 py-2 bg-pur/10 border-b border-pur/20 text-xs"
    >
      <div className="w-1.5 h-1.5 rounded-full bg-pur animate-pulse flex-shrink-0" />
      <span className="text-pur font-semibold">{t(language, 'crisis')}</span>
      <span className="text-t2 flex-1">{t(language, 'crisisMessage')}</span>
      <button
        onClick={() => setCrisisDetected(false)}
        className="text-t3 hover:text-t1 ml-auto flex-shrink-0"
        aria-label="Dismiss crisis support bar"
      >
        ✕
      </button>
    </div>
  );
}
