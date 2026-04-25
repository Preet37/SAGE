'use client';
import { useEffect, useState, useCallback, useRef } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { useAuthStore, useTutorStore } from '@/lib/store';
import { getLesson, createSession, streamChat, getConceptMap, updateTeachingMode } from '@/lib/api';
import TutorChat from '@/components/tutor/TutorChat';
import ConceptMap from '@/components/concept-map/ConceptMap';
import AgentPanel from '@/components/agents/AgentPanel';
import VoiceAgent from '@/components/voice/VoiceAgent';
import NetworkPanel from '@/components/network/NetworkPanel';
import NotesPanel from '@/components/notes/NotesPanel';
import ReplayPanel from '@/components/replay/ReplayPanel';
import ModelDownloadBanner from '@/components/offline/ModelDownloadBanner';
import OfflineBadge from '@/components/offline/OfflineBadge';
import AccessibilityModal from '@/components/accessibility/AccessibilityModal';
import MaterialsGallery from '@/components/cloudinary/MaterialsGallery';
import DiagramLibrary from '@/components/cloudinary/DiagramLibrary';
import ZeticAgent from '@/components/zetic/ZeticAgent';
import type { CognitionData, FetchAiBadge } from '@/lib/store';
import Link from 'next/link';
import { useConnectivity } from '@/lib/offline/connectivity';
import { runOfflineChat } from '@/lib/offline/agent';
import { lessonCache, sessionStore } from '@/lib/offline/store';
import { splitIntoChunks } from '@/lib/offline/retriever';

interface Lesson {
  id: number; course_id: number; slug: string; title: string; summary: string;
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
  const { sessionId: activeSessionId, setSessionId, setTeachingMode, teachingMode, clearMessages, addAgentEvent, addMessage, appendToLast, setStreaming, updateLastVerification, updateLastCognition, setFetchAiBadge } = useTutorStore();

  const { isOnline } = useConnectivity();
  const wasOnlineRef = useRef(true);
  const [syncedCount, setSyncedCount] = useState(0);

  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [conceptMap, setConceptMap] = useState<{ nodes: unknown[]; edges: unknown[] } | null>(null);
  const [activePanel, setActivePanel] = useState<'chat' | 'map' | 'network' | 'notes' | 'replay' | 'materials'>('chat');
  const [showAccessibility, setShowAccessibility] = useState(false);
  const [loading, setLoading] = useState(true);
  const [uiHints, setUiHints] = useState<string[]>([]);

  useEffect(() => {
    if (!token) { router.push('/login'); return; }
    init();
  }, [token, courseId, lessonId]);

  useEffect(() => {
    if (isOnline && !wasOnlineRef.current) {
      import('@/lib/offline/sync').then(({ runSync }) =>
        runSync().then((n) => { if (n > 0) setSyncedCount(n); })
      );
    }
    wasOnlineRef.current = isOnline;
  }, [isOnline]);

  async function init() {
    try {
      const l = await getLesson(courseId, lessonId);
      setLesson(l);

      // pre-cache lesson content for offline RAG
      lessonCache.save({
        lessonId: l.id,
        title: l.title,
        chunks: splitIntoChunks(l.content_md),
        cachedAt: Date.now(),
      }).catch(() => {});

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
        const map = await getConceptMap(token!, l.course_id);
        setConceptMap(map);
      } catch {}

      // fetch accessibility profile and apply ui_hints
      try {
        const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const accRes = await fetch(`${BASE}/accessibility/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (accRes.ok) {
          const accData = await accRes.json();
          setUiHints(accData.ui_hints || []);
        }
      } catch {}
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  async function handleModeChange(mode: string) {
    setTeachingMode(mode);
    if (token) {
      try {
        await updateTeachingMode(token, mode);
      } catch {}
    }
  }

  const handleSend = useCallback(async (text: string, imageUrl?: string, extractedText?: string) => {
    if (!lesson || !token) return;
    const { messages, sessionId } = useTutorStore.getState();

    addMessage({ id: Date.now().toString(), role: 'user', content: text, image_url: imageUrl });
    addMessage({ id: Date.now().toString() + '-a', role: 'assistant', content: '' });
    setStreaming(true);

    const history = messages
      .filter(m => m.id !== 'welcome')
      .map(m => ({ role: m.role as 'user' | 'assistant', content: m.content }));

    if (!isOnline) {
      const stop = runOfflineChat(
        lesson.id,
        text,
        history,
        lesson.key_concepts,
        {
          onToken: (t) => appendToLast(t),
          onDone: () => setStreaming(false),
          onError: (err) => {
            setStreaming(false);
            appendToLast('\n\n_Offline AI error: ' + String(err) + '_');
          },
        },
      );
      if (sessionId) {
        sessionStore.appendMessage(sessionId, lesson.id, { role: 'user', content: text, timestamp: Date.now() }).catch(() => {});
      }
      return stop;
    }

    const stop = streamChat(
      token,
      {
        lesson_id: lesson.id,
        message: text,
        history,
        session_id: sessionId ?? undefined,
        teaching_mode: teachingMode,
        voice_enabled: false,
        image_url: imageUrl,
        extracted_text: extractedText,
      },
      (event, data: unknown) => {
        const d = data as Record<string, unknown>;
        if (event === 'token') appendToLast((d.content as string) || '');
        else if (event === 'agent_event') addAgentEvent(d.type as string, d);
        else if (event === 'verification') updateLastVerification({ passed: d.passed as boolean, flags: d.flags as string[] });
        else if (event === 'fetchai_badge') setFetchAiBadge(d as unknown as FetchAiBadge);
        else if (event === 'judge_result') updateLastCognition(d as unknown as CognitionData);
        else if (event === 'done') setStreaming(false);
        else if (event === 'error') { setStreaming(false); appendToLast('\n\n_Error: ' + d.message + '_'); }
      }
    );

    return () => stop();
  }, [lesson, token, teachingMode, isOnline, addMessage, appendToLast, setStreaming, addAgentEvent, updateLastVerification, setFetchAiBadge, updateLastCognition]);

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-8 h-8 border-2 border-white/10 border-t-acc rounded-full animate-spin-slow" />
    </div>
  );

  if (!lesson) return <div className="min-h-screen flex items-center justify-center text-t2">Lesson not found</div>;

  const accessibilityClass = [
    uiHints.includes('large_font') ? 'text-base' : '',
    uiHints.includes('high_contrast') ? 'contrast-more' : '',
    uiHints.includes('focus_mode') ? 'sage-focus-mode' : '',
  ].filter(Boolean).join(' ');

  const wrapperStyle = uiHints.includes('large_font') ? { fontSize: '110%' } : undefined;

  return (
    <div
      className={`h-screen flex flex-col overflow-hidden bg-bg${accessibilityClass ? ` ${accessibilityClass}` : ''}`}
      style={wrapperStyle}
    >
      {/* Topbar */}
      <header className="flex-shrink-0 h-12 border-b border-white/5 bg-bg/90 backdrop-blur-md flex items-center gap-3 px-4 z-20">
        <Link href="/learn" className="text-t2 hover:text-t0 transition-colors text-sm">← Courses</Link>
        <div className="w-px h-4 bg-white/10" />
        <span className="font-black text-base">S<span className="text-acc">AGE</span></span>
        <div className="w-px h-4 bg-white/10" />
        <span className="text-t1 text-sm font-medium truncate max-w-xs">{lesson.title}</span>
        <OfflineBadge isOnline={isOnline} syncedCount={syncedCount} />

        {/* Mode selector */}
        <div className="ml-auto flex items-center gap-1">
          <span className="text-[9px] text-t3 font-semibold uppercase tracking-wider mr-1">Teaching Mode</span>
          {MODES.map(m => (
            <button
              key={m.id}
              onClick={() => handleModeChange(m.id)}
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
      <div
        className="flex-1 flex overflow-hidden"
        aria-live={uiHints.includes('screen_reader') ? 'polite' : undefined}
      >
        {/* LEFT: Agent panel */}
        <div
          className="w-64 flex-shrink-0 border-r border-white/5 overflow-y-auto bg-bg1"
          style={uiHints.includes('focus_mode') ? { display: 'none' } : undefined}
        >
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
              ['materials', '◫ Materials'],
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
            {activePanel === 'map' && <ConceptMap data={conceptMap} courseId={lesson.course_id} />}
            {activePanel === 'network' && <NetworkPanel lessonId={lesson.id} />}
            {activePanel === 'materials' && (
              <div className="p-6 h-full overflow-y-auto space-y-6">
                <div>
                  <div className="text-[9.5px] font-bold uppercase tracking-widest text-t3 mb-3">
                    Cloudinary · uploaded materials
                  </div>
                  <MaterialsGallery lessonId={lesson.id} />
                </div>
                <div>
                  <div className="text-[9.5px] font-bold uppercase tracking-widest text-t3 mb-3">
                    Diagram library · {lesson.title}
                  </div>
                  <DiagramLibrary
                    courseId={lesson.course_id}
                    lessonId={lesson.id}
                    conceptSlug={(lesson.key_concepts[0] || lesson.slug || 'main')
                      .toLowerCase()
                      .replace(/[^a-z0-9]+/g, '-')
                      .replace(/^-|-$/g, '')}
                  />
                </div>
              </div>
            )}
            {activePanel === 'notes' && <NotesPanel lessonId={lesson.id} />}
            {activePanel === 'replay' && <ReplayPanel activeSessionId={activeSessionId} />}
          </div>
        </div>

        {/* RIGHT: Key concepts + voice + ZETIC */}
        <div className="w-72 flex-shrink-0 border-l border-white/5 bg-bg1 flex flex-col overflow-hidden">
          {!uiHints.includes('no_voice_ui') && <VoiceAgent onTranscript={handleSend} />}
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

            <ModelDownloadBanner autoLoad={!isOnline} />

            <ZeticAgent context={lesson.summary} />

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
