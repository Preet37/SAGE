"use client";

/**
 * Apply accessibility preferences to <body> as CSS classes.
 *
 * Caches in localStorage so the classes are applied before the first
 * authenticated fetch returns (no flash of default styling).
 */

import { useEffect } from "react";

import { getAccessibility, type AccessibilityPrefs } from "./api";

const CACHE_KEY = "sage-a11y";

const CLASSES = {
  dyslexia: "a11y-dyslexia",
  contrast: "a11y-high-contrast",
  motion: "a11y-reduce-motion",
} as const;

export function applyPrefsToDom(prefs: AccessibilityPrefs): void {
  if (typeof document === "undefined") return;
  const body = document.body;
  body.classList.toggle(CLASSES.dyslexia, prefs.dyslexia_font);
  body.classList.toggle(CLASSES.contrast, prefs.high_contrast);
  body.classList.toggle(CLASSES.motion, prefs.reduce_motion);
}

export function cachePrefs(prefs: AccessibilityPrefs): void {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.setItem(CACHE_KEY, JSON.stringify(prefs));
  } catch {
    /* ignore */
  }
}

export function readCachedPrefs(): AccessibilityPrefs | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.localStorage.getItem(CACHE_KEY);
    return raw ? (JSON.parse(raw) as AccessibilityPrefs) : null;
  } catch {
    return null;
  }
}

/** Read cache immediately; refresh from server when token is present. */
export function useAccessibility(token: string | null): void {
  useEffect(() => {
    const cached = readCachedPrefs();
    if (cached) applyPrefsToDom(cached);
    if (!token) return;
    let cancelled = false;
    getAccessibility(token)
      .then((prefs) => {
        if (cancelled) return;
        cachePrefs(prefs);
        applyPrefsToDom(prefs);
      })
      .catch(() => {
        /* fall back to cached values */
      });
    return () => {
      cancelled = true;
    };
  }, [token]);
}
