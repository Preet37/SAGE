"use client";

import { useCallback, useEffect, useState } from "react";

import { applyPrefsToDom, cachePrefs } from "@/lib/a11y";
import {
  getAccessibility,
  saveAccessibility,
  type AccessibilityPrefs,
} from "@/lib/api";

interface AccessibilityModalProps {
  token: string;
  open: boolean;
  onClose: () => void;
  onChange?: (prefs: AccessibilityPrefs) => void;
}

const DEFAULTS: AccessibilityPrefs = {
  dyslexia_font: false,
  high_contrast: false,
  reduce_motion: false,
  tts_voice: "default",
};

export default function AccessibilityModal({
  token,
  open,
  onClose,
  onChange,
}: AccessibilityModalProps) {
  const [prefs, setPrefs] = useState<AccessibilityPrefs>(DEFAULTS);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (!open || !token) return;
    getAccessibility(token).then(setPrefs).catch(() => setPrefs(DEFAULTS));
  }, [open, token]);

  const save = useCallback(async () => {
    setBusy(true);
    try {
      const saved = await saveAccessibility(prefs, token);
      cachePrefs(saved);
      applyPrefsToDom(saved);
      onChange?.(saved);
      onClose();
    } finally {
      setBusy(false);
    }
  }, [onChange, onClose, prefs, token]);

  if (!open) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="a11y-title"
      className="fixed inset-0 z-50 grid place-items-center p-4"
      style={{ background: "rgba(15, 23, 42, 0.45)" }}
      onClick={onClose}
    >
      <div
        className="card w-full max-w-md p-6"
        onClick={(e) => e.stopPropagation()}
      >
        <header className="flex items-center justify-between">
          <h2 id="a11y-title" className="text-xl" style={{ fontFamily: "var(--font-heading)", fontWeight: 700 }}>
            Accessibility
          </h2>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close"
            className="grid h-7 w-7 place-items-center rounded-full text-sm"
            style={{ background: "var(--color-muted)", cursor: "pointer" }}
          >
            ✕
          </button>
        </header>
        <p className="mt-1 text-xs opacity-70">
          These preferences shape SAGE&apos;s tone, length, and motion.
        </p>

        <fieldset className="mt-4 space-y-2">
          <Toggle
            label="Use simpler sentences (dyslexia-friendly)"
            checked={prefs.dyslexia_font}
            onChange={(v) => setPrefs({ ...prefs, dyslexia_font: v })}
          />
          <Toggle
            label="High contrast emphasis"
            checked={prefs.high_contrast}
            onChange={(v) => setPrefs({ ...prefs, high_contrast: v })}
          />
          <Toggle
            label="Reduce motion in answers"
            checked={prefs.reduce_motion}
            onChange={(v) => setPrefs({ ...prefs, reduce_motion: v })}
          />
        </fieldset>

        <label className="mt-4 block">
          <span className="text-xs font-semibold opacity-80">Voice</span>
          <select
            value={prefs.tts_voice}
            onChange={(e) => setPrefs({ ...prefs, tts_voice: e.target.value })}
            className="mt-1 w-full rounded-xl border bg-white px-3 py-2 text-sm"
            style={{ borderColor: "var(--color-border)" }}
          >
            <option value="default">Default</option>
            <option value="warm">Warm</option>
            <option value="precise">Precise</option>
          </select>
        </label>

        <footer className="mt-5 flex justify-end gap-2">
          <button
            type="button"
            onClick={onClose}
            className="rounded-full px-4 py-2 text-sm font-semibold"
            style={{ background: "var(--color-muted)", color: "var(--color-foreground)", cursor: "pointer" }}
          >
            Cancel
          </button>
          <button type="button" onClick={save} disabled={busy} className="btn-primary disabled:opacity-50">
            {busy ? "Saving…" : "Save"}
          </button>
        </footer>
      </div>
    </div>
  );
}

function Toggle({
  label,
  checked,
  onChange,
}: {
  label: string;
  checked: boolean;
  onChange: (v: boolean) => void;
}) {
  return (
    <label className="flex cursor-pointer items-center justify-between rounded-xl border px-3 py-2 text-sm"
      style={{ borderColor: "var(--color-border)", background: "var(--color-muted)" }}>
      <span>{label}</span>
      <input
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        className="h-4 w-4 cursor-pointer"
      />
    </label>
  );
}
