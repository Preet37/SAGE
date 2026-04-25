"use client";

import { useCallback, useEffect, useState } from "react";

import { isEngineLoaded, loadEngine, type ModelStatus } from "@/lib/offline/agent";

interface Props {
  autoLoad?: boolean;
}

export default function ModelDownloadBanner({ autoLoad = false }: Props) {
  const [status, setStatus] = useState<ModelStatus>(isEngineLoaded() ? "ready" : "idle");
  const [progress, setProgress] = useState(0);

  const handleProgress = useCallback((p: number, s: ModelStatus) => {
    setProgress(p);
    setStatus(s);
  }, []);

  const startLoad = useCallback(() => {
    setStatus("loading");
    loadEngine(handleProgress).catch(() => setStatus("error"));
  }, [handleProgress]);

  useEffect(() => {
    if (autoLoad && status === "idle") startLoad();
  }, [autoLoad, startLoad, status]);

  if (status === "ready") return null;

  return (
    <div
      role="status"
      aria-live="polite"
      className="rounded-2xl p-3"
      style={{
        background: "var(--color-muted)",
        border: "1px solid var(--color-border)",
        fontSize: 13,
      }}
    >
      <div className="flex items-center justify-between gap-2">
        <div>
          <p className="font-semibold" style={{ fontFamily: "var(--font-heading)" }}>
            Offline AI model
          </p>
          <p className="opacity-60" style={{ fontSize: 11 }}>
            Phi-3.5-mini · runs in your browser · ~2.4 GB
          </p>
        </div>
        {status === "idle" && (
          <button
            type="button"
            onClick={startLoad}
            className="btn-primary"
            style={{ fontSize: 12, padding: "4px 12px" }}
          >
            Download
          </button>
        )}
        {status === "error" && (
          <button
            type="button"
            onClick={startLoad}
            className="btn-primary"
            style={{ fontSize: 12, padding: "4px 12px", background: "var(--color-destructive)" }}
          >
            Retry
          </button>
        )}
      </div>

      {status === "loading" && (
        <div className="mt-2">
          <div
            className="h-1.5 w-full overflow-hidden rounded-full"
            style={{ background: "var(--color-border)" }}
          >
            <div
              className="h-full rounded-full transition-all duration-300"
              style={{
                width: `${Math.round(progress * 100)}%`,
                background: "var(--color-primary)",
              }}
            />
          </div>
          <p className="mt-1 opacity-60" style={{ fontSize: 11 }}>
            {Math.round(progress * 100)}% — cached after first download
          </p>
        </div>
      )}

      {status === "error" && (
        <p className="mt-1 opacity-70" style={{ fontSize: 11, color: "var(--color-destructive)" }}>
          Download failed — WebGPU may not be supported on this device.
        </p>
      )}
    </div>
  );
}
