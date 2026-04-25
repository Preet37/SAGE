'use client';
import { useEffect, useState } from 'react';

interface Props {
  onLowBattery?: () => void;
}

/**
 * Tier 3: Solar-charge / low-battery awareness.
 * If the device battery drops below 15%, fires onLowBattery callback
 * and shows a non-intrusive indicator.
 */
export default function SolarChargeGuard({ onLowBattery }: Props) {
  const [batteryLevel, setBatteryLevel] = useState<number | null>(null);
  const [isCharging, setIsCharging] = useState<boolean | null>(null);

  useEffect(() => {
    // Battery Status API — supported in Chrome/Android
    if (!('getBattery' in navigator)) return;

    let battery: BatteryManager | null = null;

    function update(b: BatteryManager) {
      setBatteryLevel(b.level);
      setIsCharging(b.charging);
      if (b.level < 0.15 && !b.charging) {
        onLowBattery?.();
      }
    }

    // @ts-expect-error getBattery is not in standard TS types
    (navigator.getBattery() as Promise<BatteryManager>).then((b) => {
      battery = b;
      update(b);
      b.addEventListener('levelchange', () => update(b));
      b.addEventListener('chargingchange', () => update(b));
    }).catch(() => {});

    return () => {
      if (battery) {
        battery.removeEventListener('levelchange', () => {});
        battery.removeEventListener('chargingchange', () => {});
      }
    };
  }, [onLowBattery]);

  if (batteryLevel === null || batteryLevel > 0.15 || isCharging) return null;

  const pct = Math.round(batteryLevel * 100);

  return (
    <div
      role="status"
      aria-live="polite"
      className="fixed bottom-4 right-4 z-40 flex items-center gap-2 px-3 py-2 bg-bg2 border border-yel/30 rounded-xl text-xs text-yel shadow-lg"
    >
      {/* Battery icon */}
      <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
        <rect x="2" y="7" width="16" height="10" rx="2" />
        <path d="M22 11v2" strokeLinecap="round" />
        <rect x="3" y="8" width={`${pct / 10}`} height="8" rx="1" fill="currentColor" opacity={0.7} />
      </svg>
      <span>
        <strong>{pct}% battery</strong> — data saver active
      </span>
    </div>
  );
}

// TypeScript shim for the Battery Status API
interface BatteryManager extends EventTarget {
  charging: boolean;
  chargingTime: number;
  dischargingTime: number;
  level: number;
}
