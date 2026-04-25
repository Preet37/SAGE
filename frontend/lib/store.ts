'use client';
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: number;
  email: string;
  username: string;
  display_name: string;
  teaching_mode: string;
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
}

export const useTutorStore = create<TutorStore>((set) => ({
  messages: [],
  sessionId: null,
  teachingMode: 'default',
  isStreaming: false,
  agentEvents: [],
  fetchAiBadge: null,
  addMessage: (msg) => set((s) => ({ messages: [...s.messages, msg] })),
  appendToLast: (content) =>
    set((s) => {
      const msgs = [...s.messages];
      if (msgs.length > 0) msgs[msgs.length - 1].content += content;
      return { messages: msgs };
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
      const msgs = [...s.messages];
      if (msgs.length > 0) msgs[msgs.length - 1].verification = v;
      return { messages: msgs };
    }),
  updateLastCognition: (c) =>
    set((s) => {
      const msgs = [...s.messages];
      if (msgs.length > 0) msgs[msgs.length - 1].cognition = c;
      return { messages: msgs };
    }),
  setFetchAiBadge: (b) => set({ fetchAiBadge: b }),
}));
