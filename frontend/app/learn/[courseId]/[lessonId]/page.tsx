'use client';
import { useEffect, useState, useCallback } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { useAuthStore, useTutorStore } from '@/lib/store';
import { getLesson, createSession, streamChat, getConceptMap } from '@/lib/api';
import TutorChat from '@/components/tutor/TutorChat';
import ConceptMap from '@/components/concept-map/ConceptMap';
import AgentPanel from '@/components/agents/AgentPanel';
import VoiceAgent from '@/components/voice/VoiceAgent';
import NetworkPanel from '@/components/network/NetworkPanel';
import NotesPanel from '@/components/notes/NotesPanel';
import ZeticAgent from '@/components/zetic/ZeticAgent';
import AccessibilityModal from '@/components/accessibility/AccessibilityModal';
import Link from 'next/link';

interface Lesson {
  id: number; slug: string; title: string; summary: string;
  key_concepts: string[]; estimated_minutes: number; content_md: string;
}

const MODES = [
  { id: 'default',   label: 'Socratic',  icon: '◎', tip: 'Guided questioning — SAGE never just gives the answer' },
  { id: 'eli5',      label: 'Simple',    icon: '◉', tip: 'Explain like I\'m 10 — everyday analogies, no jargon' },
  { id: 'analogy',   label: 'Analogy',   icon: '≈',  tip: 'Build intuition through real-world comparisons first' },
  { id: 'code',      label: 'Code',      icon: '{ }', tip: 'Show working code examples, then explain the concept' },
  { id: 'deep_dive', label: 'Deep Dive', icon: '∞',  tip: 'Math-heavy, formal notation, assumes strong background' },
];

export default function LessonPage() {
  const params = useParams();
  const courseId = params.courseId as string;
  const lessonId = params.lessonId as string;

  const { token } = useAuthStore();
  const router = useRouter();
  const { setSessionId, setTeachingMode, teachingMode, clearMessages, addAgentEvent, addMessage, appendToLast, setStreaming, updateLastVerification } = useTutorStore();

  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [conceptMap, setConceptMap] = useState<{ nodes: unknown[]; edges: unknown[] } | null>(null);
  const [activePanel, setActivePanel] = useState<'chat' | 'map' | 'network' | 'notes' | 'replay'>('chat');
  const [showAccessibility, setShowAccessibility] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) { router.push('/login'); return; }
    init();
  }, [token, courseId, lessonId]);

  async function init() {
    try {
      const [l, _session] = await Promise.all([
        getLesson(courseId, lessonId),
        (async () => {
          const s = await createSession(token!, 0, teachingMode);
          return s;
        })(),
      ]);
      setLesson(l);

      // create real session now that we have lesson id
      const sess = await createSession(token!, l.id, teachingMode);
      setSessionId(sess.session_id);

      clearMessages();
      addMessage({
        id: 'welcome',
        role: 'assistant',
        content: `Hello! I'm SAGE, your Socratic tutor. We're working on **${l.title}**.\n\nTell me — what do you already know about this topic? Or jump right in with a question.`,
      });

      // load concept map
      try {
        const map = await getConceptMap(token!, 1); // course id 1 for demo
        setConceptMap(map);
      } catch {}
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  const handleSend = useCallback(async (text: string) => {
    if (!lesson || !token) return;
    const { messages, sessionId } = useTutorStore.getState();

    addMessage({ id: Date.now().toString(), role: 'user', content: text });
    addMessage({ id: Date.now().toString() + '-a', role: 'assistant', content: '' });
    setStreaming(true);

    const history = messages
      .filter(m => m.id !== 'welcome')
      .map(m => ({ role: m.role, content: m.content }));

    const stop = streamChat(
      token,
      {
        lesson_id: lesson.id,
        message: text,
        history,
        session_id: sessionId ?? undefined,
        teaching_mode: teachingMode,
        voice_enabled: false,
      },
      (event, data: unknown) => {
        const d = data as Record<string, unknown>;
        if (event === 'token') appendToLast((d.content as string) || '');
        else if (event === 'agent_event') addAgentEvent(d.type as string, d);
        else if (event === 'verification') updateLastVerification({ passed: d.passed as boolean, flags: d.flags as string[] });
        else if (event === 'done') setStreaming(false);
        else if (event === 'error') { setStreaming(false); appendToLast('\n\n_Error: ' + d.message + '_'); }
      }
    );

    return () => stop();
  }, [lesson, token, teachingMode]);

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-8 h-8 border-2 border-white/10 border-t-acc rounded-full animate-spin-slow" />
    </div>
  );

  if (!lesson) return <div className="min-h-screen flex items-center justify-center text-t2">Lesson not found</div>;

  return (
    <div className="h-screen flex flex-col overflow-hidden bg-bg">
      {/* Topbar */}
      <header className="flex-shrink-0 h-12 border-b border-white/5 bg-bg/90 backdrop-blur-md flex items-center gap-3 px-4 z-20">
        <Link href="/learn" className="text-t2 hover:text-t0 transition-colors text-sm">← Courses</Link>
        <div className="w-px h-4 bg-white/10" />
        <span className="font-black text-base">S<span className="text-acc">AGE</span></span>
        <div className="w-px h-4 bg-white/10" />
        <span className="text-t1 text-sm font-medium truncate max-w-xs">{lesson.title}</span>

        {/* Mode selector */}
        <div className="ml-auto flex items-center gap-1">
          <span className="text-[9px] text-t3 font-semibold uppercase tracking-wider mr-1">Teaching Mode</span>
          {MODES.map(m => (
            <button
              key={m.id}
              onClick={() => setTeachingMode(m.id)}
              title={m.tip}
              className={`text-[11px] font-semibold px-2.5 py-1 rounded-lg transition-all ${
                teachingMode === m.id
                  ? 'bg-acc text-white shadow-sm'
                  : 'text-t2 hover:text-t0 hover:bg-white/5'
              }`}
            >
              <span className="mr-1 opacity-70">{m.icon}</span>{m.label}
            </button>
          ))}
          <div className="w-px h-4 bg-white/10 mx-2" />
          <Link href="/dashboard" title="Your learning dashboard" className="text-[11px] text-t2 hover:text-t0 px-2 py-1 rounded-lg hover:bg-white/5 transition-all flex items-center gap-1">
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
            Dashboard
          </Link>
          <button
            onClick={() => setShowAccessibility(true)}
            title="Set learning accessibility preferences (dyslexia, ADHD, etc.)"
            className="text-[11px] text-t2 hover:text-pur px-2 py-1 rounded-lg hover:bg-pur/10 transition-all flex items-center gap-1"
          >
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 4a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" /></svg>
            Accessibility
          </button>
        </div>
      </header>

      {/* Main 3-column layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* LEFT: Agent panel */}
        <div className="w-64 flex-shrink-0 border-r border-white/5 overflow-y-auto bg-bg1">
          <AgentPanel />
        </div>

        {/* CENTER: Chat + panels */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Panel tabs */}
          <div className="flex-shrink-0 flex gap-0 border-b border-white/5 bg-bg1/50 overflow-x-auto">
            {([
              ['chat', '◎ Chat'],
              ['map', '⬡ Concepts'],
              ['network', '◈ Peers'],
              ['notes', '✎ Notes'],
              ['replay', '↩ Replay'],
            ] as const).map(([p, label]) => (
              <button
                key={p}
                onClick={() => setActivePanel(p)}
                className={`px-4 py-2.5 text-xs font-semibold uppercase tracking-wider transition-all border-b-2 whitespace-nowrap ${
                  activePanel === p
                    ? 'text-acc border-acc'
                    : 'text-t2 border-transparent hover:text-t0'
                }`}
              >
                {label}
              </button>
            ))}
          </div>

          <div className="flex-1 overflow-hidden">
            {activePanel === 'chat' && <TutorChat onSend={handleSend} lesson={lesson} />}
            {activePanel === 'map' && <ConceptMap data={conceptMap} courseId={1} />}
            {activePanel === 'network' && <NetworkPanel lessonId={lesson.id} />}
            {activePanel === 'notes' && <NotesPanel lessonId={lesson.id} />}
            {activePanel === 'replay' && (
              <div className="p-6 text-t2 text-sm">Session replay available after completing the session.</div>
            )}
          </div>
        </div>

        {/* RIGHT: Key concepts + voice + ZETIC */}
        <div className="w-72 flex-shrink-0 border-l border-white/5 bg-bg1 flex flex-col overflow-hidden">
          <VoiceAgent onTranscript={handleSend} />
          <div className="border-t border-white/5 p-4 flex-1 overflow-y-auto space-y-5">
            <div>
              <div className="text-[10px] font-bold uppercase tracking-widest text-t3 mb-3">Key Concepts</div>
              <div className="space-y-2">
                {lesson.key_concepts.map(c => (
                  <div key={c} className="flex items-center gap-2 text-xs text-t1">
                    <div className="w-1.5 h-1.5 rounded-full bg-acc/60 flex-shrink-0" />
                    {c}
                  </div>
                ))}
              </div>
            </div>

            {/* ZETIC on-device AI */}
            <ZeticAgent
              context={lesson.key_concepts.join(', ')}
              onResponse={(text) => {
                // inject ZETIC response as an assistant message
                useTutorStore.getState().addMessage({
                  id: 'zetic-' + Date.now(),
                  role: 'assistant',
                  content: `**[On-Device ZETIC]** ${text}`,
                });
              }}
            />

            <div>
              <div className="text-[10px] font-bold uppercase tracking-widest text-t3 mb-3">About This Lesson</div>
              <p className="text-xs text-t1 leading-relaxed">{lesson.summary}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Accessibility modal */}
      <AccessibilityModal isOpen={showAccessibility} onClose={() => setShowAccessibility(false)} />
    </div>
  );
}
