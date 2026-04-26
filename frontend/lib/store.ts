import { create } from "zustand";
import { getToken } from "@/lib/auth";
import type { LangCode } from "@/lib/i18n";

// ── Auth store ───────────────────────────────────────────────────────────────

interface AuthState {
  token: string | null;
  setToken: (t: string | null) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: typeof window !== "undefined" ? getToken() : null,
  setToken: (token) => set({ token }),
}));

// ── Tutor/UI prefs store ─────────────────────────────────────────────────────

interface TutorState {
  lowDataMode: boolean;
  setLowDataMode: (v: boolean) => void;
  language: LangCode;
  setLanguage: (l: LangCode) => void;
  crisisDetected: boolean;
  setCrisisDetected: (v: boolean) => void;
}

export const useTutorStore = create<TutorState>((set) => ({
  lowDataMode: false,
  setLowDataMode: (lowDataMode) => set({ lowDataMode }),
  language: "en" as LangCode,
  setLanguage: (language) => set({ language }),
  crisisDetected: false,
  setCrisisDetected: (crisisDetected) => set({ crisisDetected }),
}));
