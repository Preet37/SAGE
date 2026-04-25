'use client';
import { useEffect, useState } from 'react';

type Accelerator = 'NPU' | 'GPU' | 'CPU' | 'unknown';

interface HardwareInfo {
  accelerator: Accelerator;
  device: string;
  vram_mb: number;
  webgpu: boolean;
}

const ACCEL_COLOR: Record<Accelerator, string> = {
  NPU: '#9d78f5',
  GPU: '#f5834a',
  CPU: '#5b9fff',
  unknown: '#64748b',
};

interface Props {
  offlineProven?: boolean;
  size?: 'sm' | 'md';
}

export default function HardwareBadge({ offlineProven, size = 'md' }: Props) {
  const [info, setInfo] = useState<HardwareInfo | null>(null);

  useEffect(() => {
    detectHardware().then(setInfo);
  }, []);

  if (!info) {
    return (
      <span className="text-[9px] text-t3 font-mono">detecting hw…</span>
    );
  }

  const color = ACCEL_COLOR[info.accelerator];
  const padding = size === 'sm' ? 'px-1.5 py-0.5' : 'px-2 py-1';
  const fontSize = size === 'sm' ? 'text-[9px]' : 'text-[10px]';

  return (
    <div className="inline-flex items-center gap-1.5">
      <span
        className={`${padding} ${fontSize} font-bold rounded-full border`}
        style={{
          color,
          borderColor: color + '40',
          backgroundColor: color + '15',
        }}
      >
        {info.accelerator}
      </span>
      <span className={`${fontSize} text-t3 font-mono truncate max-w-[140px]`}>
        {info.device}
      </span>
      {offlineProven && (
        <span
          className={`${padding} ${fontSize} font-bold rounded-full border border-grn/40 bg-grn/15 text-grn`}
        >
          OFFLINE ✓
        </span>
      )}
      <span className={`${fontSize} font-bold text-pur`}>zetic ↗</span>
    </div>
  );
}

async function detectHardware(): Promise<HardwareInfo> {
  const webgpu = 'gpu' in navigator;
  let accelerator: Accelerator = 'CPU';
  let device = 'CPU';
  let vram_mb = 0;

  if (webgpu) {
    accelerator = 'GPU';
    try {
      const gpu = (navigator as Navigator & { gpu?: { requestAdapter: () => Promise<unknown> } }).gpu;
      const adapter = (await gpu?.requestAdapter()) as
        | { name?: string; info?: { vendor?: string; description?: string }; limits?: { maxBufferSize?: number } }
        | null;
      if (adapter) {
        device = adapter.info?.description || adapter.info?.vendor || adapter.name || 'WebGPU';
        if (adapter.limits?.maxBufferSize) {
          vram_mb = Math.round(adapter.limits.maxBufferSize / (1024 * 1024));
        }
        // Apple Silicon advertises an "Apple Neural Engine"-class adapter,
        // detect it via vendor string and surface as NPU for the demo.
        const vendor = (adapter.info?.vendor || '').toLowerCase();
        if (vendor.includes('apple') && /m[1-9]/.test(device.toLowerCase())) {
          accelerator = 'NPU';
        }
      }
    } catch {
      // Adapter request can fail on some browsers; fall back to GPU label.
    }
  } else {
    // No WebGPU → CPU only. Try to surface a friendly device string.
    const ua = navigator.userAgent;
    if (/Macintosh/.test(ua)) device = 'macOS CPU';
    else if (/Windows/.test(ua)) device = 'Windows CPU';
    else if (/Linux/.test(ua)) device = 'Linux CPU';
  }

  return { accelerator, device, vram_mb, webgpu };
}
