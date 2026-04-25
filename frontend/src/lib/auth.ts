"use client";

/**
 * Lightweight auth store.
 *
 * Persists token + user in localStorage under `sage-auth`. Subscribers are
 * notified via a `storage` event so multiple tabs stay in sync.
 */

import { useEffect, useState } from "react";

import { getMe, type User } from "./api";

const STORAGE_KEY = "sage-auth";

interface Persisted {
  token: string;
  user: User;
}

function read(): Persisted | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    return raw ? (JSON.parse(raw) as Persisted) : null;
  } catch {
    return null;
  }
}

function write(value: Persisted | null): void {
  if (typeof window === "undefined") return;
  if (value) {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(value));
  } else {
    window.localStorage.removeItem(STORAGE_KEY);
  }
  // Trigger same-tab listeners.
  window.dispatchEvent(new Event("sage-auth-change"));
}

export function setAuth(token: string, user: User): void {
  write({ token, user });
}

export function clearAuth(): void {
  write(null);
}

export function getToken(): string | null {
  return read()?.token ?? null;
}

export interface AuthState {
  token: string | null;
  user: User | null;
  ready: boolean;
}

export function useAuth(): AuthState {
  const [state, setState] = useState<AuthState>({ token: null, user: null, ready: false });

  useEffect(() => {
    const sync = () => {
      const v = read();
      setState({ token: v?.token ?? null, user: v?.user ?? null, ready: true });
    };
    sync();
    window.addEventListener("storage", sync);
    window.addEventListener("sage-auth-change", sync);
    return () => {
      window.removeEventListener("storage", sync);
      window.removeEventListener("sage-auth-change", sync);
    };
  }, []);

  // Best-effort token validation: if token is present but /auth/me fails, clear.
  useEffect(() => {
    if (!state.token) return;
    let cancelled = false;
    getMe(state.token)
      .then((user) => {
        if (cancelled) return;
        const cur = read();
        // Only write if anything actually changed — avoids a re-fired
        // sage-auth-change event and the corresponding render churn.
        if (!cur || !sameUser(cur.user, user)) {
          setAuth(state.token!, user);
        }
      })
      .catch(() => {
        if (!cancelled) clearAuth();
      });
    return () => {
      cancelled = true;
    };
    // Only re-validate when the token itself changes.
  }, [state.token]);

  return state;
}

function sameUser(a: User, b: User): boolean {
  return (
    a.id === b.id &&
    a.email === b.email &&
    a.name === b.name &&
    a.teaching_mode === b.teaching_mode
  );
}
