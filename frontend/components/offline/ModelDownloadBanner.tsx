'use client';

import { useCallback, useEffect, useState } from 'react';
import { isEngineLoaded, loadEngine, type ModelStatus } from '@/lib/offline/agent';

interface Props {
  autoLoad?: boolean;
}

export default function ModelDownloadBanner({ autoLoad = false }: Props) {
  const [status, setStatus] = useState<ModelStatus>(isEngineLoaded() ? 'ready' : 'idle');
  const [progress, setProgress] = useState(0);

  const handleProgress = useCallback((p: number, s: ModelStatus) => {
    setProgress(p);
    setStatus(s);
  }, []);

  const startLoad = useCallback(() => {
    setStatus('loading');
    loadEngine(handleProgress).catch(() => setStatus('error'));
  }, [handleProgress]);

  useEffect(() => {
    if (autoLoad && status === 'idle') startLoad();
  }, [autoLoad, startLoad, status]);

  if (status === 'ready') return null;

  return (
    <div className="rounded-xl border border-white/10 bg-bg2 p-3 text-xs">
      <div className="flex items-center justify-between gap-2">
        <div>
          <p className="font-semibold text-t0">Offline AI model</p>
          <p className="text-t3 mt-0.5">Phi-3.5-mini · runs in browser · ~2.4 GB</p>
        </div>
        {status === 'idle' && (
          <button
            type="button"
            onClick={startLoad}
            className="px-3 py-1 rounded-lg bg-acc text-white font-semibold text-[11px] hover:opacity-90 transition-opacity"
          >
            Download
          </button>
        )}
        {status === 'error' && (
          <button
            type="button"
            onClick={startLoad}
            className="px-3 py-1 rounded-lg bg-red-500 text-white font-semibold text-[11px] hover:opacity-90 transition-opacity"
          >
            Retry
          </button>
        )}
      </div>

      {status === 'loading' && (
        <div className="mt-2">
          <div className="h-1 w-full overflow-hidden rounded-full bg-white/5">
            <div
              className="h-full rounded-full bg-acc transition-all duration-300"
              style={{ width: `${Math.round(progress * 100)}%` }}
            />
          </div>
          <p className="mt-1 text-t3">{Math.round(progress * 100)}% — cached after first download</p>
        </div>
      )}

      {status === 'error' && (
        <p className="mt-1 text-red-400">
          Download failed — WebGPU may not be supported on this device.
        </p>
      )}
    </div>
  );
}
