"use client";

import { useCallback, useEffect, useState } from "react";

import AppHeader from "@/components/AppHeader";
import BrainGraph from "@/components/BrainGraph";
import LessonPlayer from "@/components/LessonPlayer";
import TutorChat from "@/components/TutorChat";
import { MasteredTopic, addMastered, listMastered, slugify } from "@/lib/mastery";

export default function LearnDashboard() {
  const [mastered, setMastered] = useState<MasteredTopic[]>([]);
  const [activeTopic, setActiveTopic] = useState<string | null>(null);
  const [highlightId, setHighlightId] = useState<string | null>(null);
  const [token, setToken] = useState("");
  const [showGraph, setShowGraph] = useState(false);

  useEffect(() => {
    setMastered(listMastered());
    setToken(typeof window !== "undefined" ? localStorage.getItem("sage_token") ?? "" : "");
    const onChange = () => setMastered(listMastered());
    window.addEventListener("sage:mastery-changed", onChange);
    window.addEventListener("storage", onChange);
    return () => {
      window.removeEventListener("sage:mastery-changed", onChange);
      window.removeEventListener("storage", onChange);
    };
  }, []);

  const onTopicRequest = useCallback((topic: string) => {
    setActiveTopic(topic);
  }, []);

  const onComplete = useCallback((topic: string) => {
    const t = addMastered(topic);
    setHighlightId(t.id);
    setActiveTopic(null);
    setTimeout(() => setHighlightId(null), 4000);
  }, []);

  return (
    <main className="bg-blobs flex h-screen flex-col gap-4 p-4">
      <AppHeader onToggleGraph={() => setShowGraph(!showGraph)} isGraphOpen={showGraph} />
      <div className="relative flex min-h-0 flex-1 gap-4 overflow-hidden">
        <section className={`min-h-0 flex-1 transition-all duration-500 ${showGraph ? "max-w-[45%]" : "max-w-full"}`}>
          {activeTopic ? (
            <LessonPlayer
              topic={activeTopic}
              onComplete={onComplete}
              onClose={() => setActiveTopic(null)}
            />
          ) : (
            <TutorChat sessionId={1} token={token} onTopicRequest={onTopicRequest} />
          )}
        </section>

        <section 
          className={`min-h-0 flex-[1.5] transition-all duration-500 ${showGraph ? "translate-x-0 opacity-100" : "absolute right-0 top-0 h-full translate-x-full opacity-0 pointer-events-none"}`}
        >
          <div className="card h-full overflow-hidden">
            <BrainGraph mastered={mastered} highlightId={highlightId} />
          </div>
        </section>
      </div>

      {mastered.length > 0 && (
        <MasteryFooter mastered={mastered} onJump={(id) => {
          setHighlightId(id);
          setTimeout(() => setHighlightId(null), 2500);
        }} />
      )}
    </main>
  );
}

function MasteryFooter({
  mastered, onJump,
}: { mastered: MasteredTopic[]; onJump: (id: string) => void }) {
  return (
    <footer className="glass flex items-center gap-3 overflow-x-auto px-4 py-2">
      <span className="shrink-0 text-xs font-semibold uppercase tracking-wider" style={{ opacity: 0.55 }}>
        Mastered
      </span>
      {mastered.slice().reverse().map((t) => (
        <button
          key={t.id}
          onClick={() => onJump(slugify(t.label))}
          className="shrink-0 rounded-full px-3 py-1 text-xs font-semibold"
          style={{
            background: "rgba(108,92,231,0.12)",
            color: "var(--color-ring)",
            border: "1px solid rgba(108,92,231,0.25)",
            cursor: "pointer",
          }}
        >
          {t.label}
        </button>
      ))}
    </footer>
  );
}
