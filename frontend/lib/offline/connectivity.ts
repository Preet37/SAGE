"use client";

import { useCallback, useEffect, useState } from "react";

const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const PROBE_INTERVAL_MS = 30_000;

async function probeOnline(): Promise<boolean> {
  try {
    const res = await fetch(`${BASE}/health`, {
      method: "HEAD",
      cache: "no-store",
      signal: AbortSignal.timeout(5_000),
    });
    return res.ok;
  } catch {
    return false;
  }
}

export function useConnectivity(): { isOnline: boolean } {
  const [isOnline, setIsOnline] = useState(
    typeof navigator !== "undefined" ? navigator.onLine : true,
  );

  const check = useCallback(async () => {
    if (typeof navigator === "undefined") return;
    if (!navigator.onLine) {
      setIsOnline(false);
      return;
    }
    setIsOnline(await probeOnline());
  }, []);

  useEffect(() => {
    const onOnline = () => void check();
    const onOffline = () => setIsOnline(false);

    window.addEventListener("online", onOnline);
    window.addEventListener("offline", onOffline);
    const timer = setInterval(() => void check(), PROBE_INTERVAL_MS);
    void check();

    return () => {
      window.removeEventListener("online", onOnline);
      window.removeEventListener("offline", onOffline);
      clearInterval(timer);
    };
  }, [check]);

  return { isOnline };
}
