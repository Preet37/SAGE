'use client';
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { LangCode } from './i18n';

interface User {
  id: number;
  email: string;
  username: string;
  display_name: string;
  teaching_mode: string;
  preferred_language?: string;
}

interface AuthStore {
  token: string | null;
  user: User | null;
  setAuth: (token: string, user: User) => void;
  clearAuth: () => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      setAuth: (token, user) => set({ token, user }),
      clearAuth: () => set({ token: null, user: null }),
    }),
    { name: 'sage-auth' }
  )
);

export interface CognitionData {
  hyde_query?: string;
  retrieved: { id: string; preview: string; cosine: number; rerank?: number }[];
  rerank_used: boolean;
  judge?: { score: number; grounded: boolean; reasoning: string; citations: number[] };
  latency_ms: number;
}

export interface FetchAiBadge {
  director_address: string;
  agentverse_url: string;
  deep_dive_cost_micro_asi: number;
  agents: { name: string; port: number; role: string }[];
  payment?: { amount_micro_asi: number; token: string; ts: string };
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  agent_trace?: Record<string, unknown>;
  verification?: { passed: boolean; flags: string[] };
  quiz?: { question: string; options: string[]; answer: string; explanation: string };
  audio?: string;
  cognition?: CognitionData;
  image_url?: string;
}

interface TutorStore {
  messages: Message[];
  sessionId: number | null;
  teachingMode: string;
  isStreaming: boolean;
  agentEvents: { type: string; data: unknown; ts: number }[];
  fetchAiBadge: FetchAiBadge | null;
  // Accessibility / context flags
  language: LangCode;
  lowDataMode: boolean;
  voiceOnlyMode: boolean;
  crisisDetected: boolean;
  // Actions
  addMessage: (msg: Message) => void;
  appendToLast: (content: string) => void;
  setSessionId: (id: number) => void;
  setTeachingMode: (mode: string) => void;
  setStreaming: (v: boolean) => void;
  addAgentEvent: (type: string, data: unknown) => void;
  clearMessages: () => void;
  updateLastVerification: (v: { passed: boolean; flags: string[] }) => void;
  updateLastCognition: (c: CognitionData) => void;
  setFetchAiBadge: (b: FetchAiBadge) => void;
  setLanguage: (lang: LangCode) => void;
  setLowDataMode: (v: boolean) => void;
  setVoiceOnlyMode: (v: boolean) => void;
  setCrisisDetected: (v: boolean) => void;
}

export const useTutorStore = create<TutorStore>((set) => ({
  messages: [],
  sessionId: null,
  teachingMode: 'default',
  isStreaming: false,
  agentEvents: [],
  fetchAiBadge: null,
  language: 'en',
  lowDataMode: false,
  voiceOnlyMode: false,
  crisisDetected: false,
  addMessage: (msg) => set((s) => ({ messages: [...s.messages, msg] })),
  appendToLast: (content) =>
    set((s) => {
      if (s.messages.length === 0) return {};
      const last = s.messages[s.messages.length - 1];
      return {
        messages: [
          ...s.messages.slice(0, -1),
          { ...last, content: last.content + content },
        ],
      };
    }),
  setSessionId: (id) => set({ sessionId: id }),
  setTeachingMode: (mode) => set({ teachingMode: mode }),
  setStreaming: (v) => set({ isStreaming: v }),
  addAgentEvent: (type, data) =>
    set((s) => ({
      agentEvents: [{ type, data, ts: Date.now() }, ...s.agentEvents].slice(0, 50),
    })),
  clearMessages: () => set({ messages: [], agentEvents: [] }),
  updateLastVerification: (v) =>
    set((s) => {
      if (s.messages.length === 0) return {};
      const last = s.messages[s.messages.length - 1];
      return {
        messages: [
          ...s.messages.slice(0, -1),
          { ...last, verification: v },
        ],
      };
    }),
  updateLastCognition: (c) =>
    set((s) => {
      if (s.messages.length === 0) return {};
      const last = s.messages[s.messages.length - 1];
      return {
        messages: [
          ...s.messages.slice(0, -1),
          { ...last, cognition: c },
        ],
      };
    }),
  setFetchAiBadge: (b) => set({ fetchAiBadge: b }),
  setLanguage: (lang) => set({ language: lang }),
  setLowDataMode: (v) => set({ lowDataMode: v }),
  setVoiceOnlyMode: (v) => set({ voiceOnlyMode: v }),
  setCrisisDetected: (v) => set({ crisisDetected: v }),
}));
