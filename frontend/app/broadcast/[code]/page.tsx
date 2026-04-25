'use client';
import { useEffect, useRef, useState } from 'react';
import { useParams } from 'next/navigation';
import { getBroadcastStreamUrl } from '@/lib/api';
import Link from 'next/link';

interface LessonContent {
  type: string;
  lesson_id: number;
  title: string;
  content_md: string;
  key_concepts: string[];
}

export default function BroadcastJoinPage() {
  const params = useParams();
  const code = (params.code as string)?.toUpperCase();
  const wsRef = useRef<WebSocket | null>(null);
  const [status, setStatus] = useState<'connecting' | 'waiting' | 'live' | 'closed' | 'error'>('connecting');
  const [lesson, setLesson] = useState<LessonContent | null>(null);

  useEffect(() => {
    if (!code) return;
    const url = getBroadcastStreamUrl(code);
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => setStatus('waiting');
    ws.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data);
        if (data.type === 'lesson_content') {
          setLesson(data as LessonContent);
          setStatus('live');
        } else if (data.type === 'room_closed') {
          setStatus('closed');
        }
      } catch {}
    };
    ws.onerror = () => setStatus('error');
    ws.onclose = (e) => {
      if (e.code === 4004) setStatus('error');
      else if (status !== 'closed') setStatus('closed');
    };

    return () => ws.close();
  }, [code]);

  return (
    <div className="min-h-screen bg-bg flex flex-col items-center justify-center px-4">
      <div className="w-full max-w-2xl space-y-6">
        <div className="text-center space-y-1">
          <div className="font-black text-2xl">S<span className="text-acc">AGE</span></div>
          <div className="text-t2 text-sm">Classroom · Room <span className="font-mono text-t0">{code}</span></div>
        </div>

        {status === 'connecting' && (
          <div className="text-center text-t2">
            <div className="w-6 h-6 border-2 border-white/10 border-t-acc rounded-full animate-spin mx-auto mb-3" />
            Connecting…
          </div>
        )}

        {status === 'waiting' && (
          <div className="text-center text-t2 space-y-2">
            <div className="w-2 h-2 bg-grn rounded-full animate-pulse mx-auto" />
            <p>You're in the room. Waiting for your teacher to share the lesson…</p>
          </div>
        )}

        {status === 'error' && (
          <div className="text-center text-ora space-y-3">
            <p>Room not found or has been closed.</p>
            <Link href="/learn" className="text-acc hover:underline text-sm">Go to courses →</Link>
          </div>
        )}

        {status === 'closed' && (
          <div className="text-center text-t2 space-y-3">
            <p>The teacher has ended this session.</p>
            <Link href="/learn" className="text-acc hover:underline text-sm">Go to courses →</Link>
          </div>
        )}

        {status === 'live' && lesson && (
          <div className="space-y-5">
            <div className="bg-bg2 border border-white/10 rounded-2xl p-5 space-y-3">
              <div className="flex items-center gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-grn animate-pulse" />
                <span className="text-grn text-xs font-semibold">LIVE</span>
              </div>
              <h1 className="text-xl font-bold text-t0">{lesson.title}</h1>
              {lesson.key_concepts.length > 0 && (
                <div className="flex flex-wrap gap-1.5">
                  {lesson.key_concepts.map((c) => (
                    <span key={c} className="text-[11px] px-2 py-0.5 bg-acc/10 text-acc rounded-full border border-acc/20">
                      {c}
                    </span>
                  ))}
                </div>
              )}
            </div>

            <div className="bg-bg2 border border-white/10 rounded-2xl p-5">
              <div className="text-[10px] font-bold uppercase tracking-widest text-t3 mb-3">Lesson Content</div>
              <div className="prose prose-sm prose-invert max-w-none text-t1 leading-relaxed whitespace-pre-wrap text-sm">
                {lesson.content_md}
              </div>
            </div>

            <Link
              href={`/learn`}
              className="block text-center bg-acc hover:bg-acc/90 text-white font-semibold py-3 rounded-xl transition-all text-sm"
            >
              Open in SAGE tutor →
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
