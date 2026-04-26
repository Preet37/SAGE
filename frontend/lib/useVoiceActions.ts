"use client";
/**
 * Voice Action Registry — lets the voice agent trigger real UI actions.
 *
 * Pages register their available actions here; the voice conversation hook
 * reads them and exposes them as ElevenLabs clientTools so the agent can
 * actually DO things on screen.
 */
import { create } from "zustand";

export interface VoiceAction {
  /** Unique key, passed by the agent */
  key: string;
  /** Human description sent to the agent in the system prompt */
  description: string;
  /** Called when the agent invokes this action */
  handler: (params?: Record<string, unknown>) => void | Promise<void>;
}

interface VoiceActionsState {
  actions: VoiceAction[];
  register: (actions: VoiceAction[]) => void;
  unregister: (keys: string[]) => void;
  invoke: (key: string, params?: Record<string, unknown>) => Promise<void>;
}

export const useVoiceActions = create<VoiceActionsState>((set, get) => ({
  actions: [],
  register(newActions) {
    set((s) => {
      const existing = s.actions.filter(
        (a) => !newActions.find((n) => n.key === a.key),
      );
      return { actions: [...existing, ...newActions] };
    });
  },
  unregister(keys) {
    set((s) => ({ actions: s.actions.filter((a) => !keys.includes(a.key)) }));
  },
  async invoke(key, params) {
    const action = get().actions.find((a) => a.key === key);
    if (action) await action.handler(params);
  },
}));
