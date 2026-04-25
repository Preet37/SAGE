"use client";

import { useEffect, useRef, useState } from "react";

import { TEACHING_MODES, type TeachingMode } from "@/lib/api";

interface TeachingModeSelectorProps {
  value: TeachingMode;
  onChange: (mode: TeachingMode) => void;
  disabled?: boolean;
}

export default function TeachingModeSelector({
  value,
  onChange,
  disabled,
}: TeachingModeSelectorProps) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!open) return;
    const close = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", close);
    return () => document.removeEventListener("mousedown", close);
  }, [open]);

  const current = TEACHING_MODES.find((m) => m.id === value) ?? TEACHING_MODES[0];

  return (
    <div ref={ref} className="relative">
      <button
        type="button"
        disabled={disabled}
        onClick={() => setOpen((o) => !o)}
        aria-haspopup="listbox"
        aria-expanded={open}
        className="rounded-full px-3 py-1.5 text-xs font-semibold disabled:opacity-50"
        style={{
          background: "var(--color-muted)",
          color: "var(--color-primary)",
          border: "1px solid var(--color-border)",
          cursor: disabled ? "not-allowed" : "pointer",
        }}
      >
        Mode: {current.label}
        <span aria-hidden style={{ marginLeft: 6, opacity: 0.7 }}>
          ▾
        </span>
      </button>

      {open && (
        <ul
          role="listbox"
          className="absolute right-0 z-30 mt-2 w-64 overflow-hidden rounded-2xl"
          style={{
            background: "white",
            border: "1px solid var(--color-border)",
            boxShadow: "var(--shadow-md)",
          }}
        >
          {TEACHING_MODES.map((m) => {
            const active = m.id === value;
            return (
              <li key={m.id}>
                <button
                  type="button"
                  role="option"
                  aria-selected={active}
                  onClick={() => {
                    onChange(m.id);
                    setOpen(false);
                  }}
                  className="block w-full px-3 py-2 text-left text-sm"
                  style={{
                    background: active ? "var(--color-muted)" : "white",
                    cursor: "pointer",
                  }}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-semibold">{m.label}</span>
                    {active && (
                      <span style={{ color: "var(--color-primary)", fontSize: 11 }}>active</span>
                    )}
                  </div>
                  <p className="text-xs opacity-70">{m.description}</p>
                </button>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
