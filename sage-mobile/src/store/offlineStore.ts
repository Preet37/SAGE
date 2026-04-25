import { create } from 'zustand';

export type ModelStatus = 'idle' | 'downloading' | 'ready' | 'error';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  inferenceMs?: number;
  accelerator?: string;
  offlineProven?: boolean;
}

interface OfflineStore {
  modelStatus: ModelStatus;
  modelProgress: number;
  modelError: string | null;
  accelerator: string;
  messages: Message[];
  isInferring: boolean;
  benchmarkResult: { tokensPerSecond: number; accelerator: string } | null;
  privacyMode: boolean;

  setModelStatus: (s: ModelStatus) => void;
  setModelProgress: (p: number) => void;
  setModelError: (e: string | null) => void;
  setAccelerator: (a: string) => void;
  addMessage: (m: Message) => void;
  appendToLast: (text: string) => void;
  setIsInferring: (v: boolean) => void;
  setBenchmarkResult: (r: { tokensPerSecond: number; accelerator: string } | null) => void;
  togglePrivacyMode: () => void;
  clearMessages: () => void;
}

export const useOfflineStore = create<OfflineStore>((set) => ({
  modelStatus: 'idle',
  modelProgress: 0,
  modelError: null,
  accelerator: 'CPU',
  messages: [],
  isInferring: false,
  benchmarkResult: null,
  privacyMode: true,

  setModelStatus: (s) => set({ modelStatus: s }),
  setModelProgress: (p) => set({ modelProgress: p }),
  setModelError: (e) => set({ modelError: e }),
  setAccelerator: (a) => set({ accelerator: a }),
  addMessage: (m) => set((s) => ({ messages: [...s.messages, m] })),
  appendToLast: (text) =>
    set((s) => {
      const msgs = [...s.messages];
      if (msgs.length > 0) msgs[msgs.length - 1].content += text;
      return { messages: msgs };
    }),
  setIsInferring: (v) => set({ isInferring: v }),
  setBenchmarkResult: (r) => set({ benchmarkResult: r }),
  togglePrivacyMode: () => set((s) => ({ privacyMode: !s.privacyMode })),
  clearMessages: () => set({ messages: [] }),
}));
