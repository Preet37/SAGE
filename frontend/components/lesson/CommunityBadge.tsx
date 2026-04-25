'use client';

/**
 * Tier 3: Community tutor certification badge.
 * Awarded to users who have completed ≥ 3 lessons and helped a peer.
 * Stored in localStorage for demo purposes.
 */

import { useEffect, useState } from 'react';

const BADGE_KEY = 'sage-community-tutor';

export interface BadgeState {
  earned: boolean;
  lessonCount: number;
  peerSessions: number;
}

function loadBadge(): BadgeState {
  if (typeof window === 'undefined') return { earned: false, lessonCount: 0, peerSessions: 0 };
  try {
    return JSON.parse(localStorage.getItem(BADGE_KEY) || '{}');
  } catch {
    return { earned: false, lessonCount: 0, peerSessions: 0 };
  }
}

export function recordLessonComplete() {
  const state = loadBadge();
  state.lessonCount = (state.lessonCount || 0) + 1;
  if (!state.earned && state.lessonCount >= 3 && (state.peerSessions || 0) >= 1) {
    state.earned = true;
  }
  localStorage.setItem(BADGE_KEY, JSON.stringify(state));
}

export function recordPeerSession() {
  const state = loadBadge();
  state.peerSessions = (state.peerSessions || 0) + 1;
  if (!state.earned && (state.lessonCount || 0) >= 3 && state.peerSessions >= 1) {
    state.earned = true;
  }
  localStorage.setItem(BADGE_KEY, JSON.stringify(state));
}

export default function CommunityBadge() {
  const [badge, setBadge] = useState<BadgeState>({ earned: false, lessonCount: 0, peerSessions: 0 });
  const [showTooltip, setShowTooltip] = useState(false);

  useEffect(() => {
    setBadge(loadBadge());
  }, []);

  if (!badge.earned) return null;

  return (
    <div className="relative">
      <button
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
        onFocus={() => setShowTooltip(true)}
        onBlur={() => setShowTooltip(false)}
        aria-label="Community Tutor badge — you've helped others learn"
        className="flex items-center gap-1.5 text-[11px] px-2.5 py-1 rounded-lg bg-yel/10 border border-yel/30 text-yel hover:bg-yel/20 transition-all"
      >
        <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
        </svg>
        Community Tutor
      </button>
      {showTooltip && (
        <div className="absolute bottom-full right-0 mb-2 w-56 bg-bg2 border border-white/10 rounded-xl p-3 text-xs text-t1 shadow-2xl z-50">
          <p className="font-semibold text-yel mb-1">🌍 Community Tutor</p>
          <p>You've completed {badge.lessonCount} lessons and helped a peer learn. SAGE recognises your contribution to community learning.</p>
        </div>
      )}
    </div>
  );
}
