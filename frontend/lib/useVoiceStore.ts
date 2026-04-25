import { create } from "zustand";

export type PageType = "lesson" | "explore" | "learn" | "create" | "other";

export interface VoicePageContext {
  pageType: PageType;
  /** Human-readable title of current page/lesson */
  title: string;
  /** What the page contains — visible text summary */
  description: string;
  /** The active topic / lesson content the user is looking at */
  currentTopic?: string;
  /** Last few chat messages (text form) for the voice agent to have context */
  recentMessages?: string;
  /** Callback: send a message to the current tutor panel */
  sendToTutor?: (msg: string) => void;
}

interface VoiceStore {
  context: VoicePageContext;
  setContext: (ctx: Partial<VoicePageContext>) => void;
  clearContext: () => void;
}

const DEFAULT_CONTEXT: VoicePageContext = {
  pageType: "other",
  title: "SAGE",
  description: "AI-powered adaptive learning platform",
};

export const useVoiceStore = create<VoiceStore>((set) => ({
  context: DEFAULT_CONTEXT,
  setContext: (ctx) =>
    set((state) => ({
      context: { ...state.context, ...ctx },
    })),
  clearContext: () => set({ context: DEFAULT_CONTEXT }),
}));
