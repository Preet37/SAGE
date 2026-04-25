'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store';
import { createBroadcastRoom, getBroadcastQrUrl, getCourses, getLessons, pushBroadcastContent } from '@/lib/api';
import Link from 'next/link';
import Image from 'next/image';

interface Course { id: number; slug: string; title: string; }
interface Lesson { id: number; slug: string; title: string; content_md: string; key_concepts: string[]; }
interface Room { code: string; join_url: string; qr_url: string; }

export default function BroadcastPage() {
  const router = useRouter();
  const { token } = useAuthStore();
  const [courses, setCourses] = useState<Course[]>([]);
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);
  const [selectedLesson, setSelectedLesson] = useState<Lesson | null>(null);
  const [room, setRoom] = useState<Room | null>(null);
  const [loading, setLoading] = useState(false);
  const [pushed, setPushed] = useState(false);

  useEffect(() => {
    if (!token) { router.push('/login'); return; }
    getCourses().then(setCourses).catch(() => {});
  }, [token]);

  async function handleCourseSelect(c: Course) {
    setSelectedCourse(c);
    setSelectedLesson(null);
    setLessons([]);
    const ls = await getLessons(c.slug);
    setLessons(Array.isArray(ls) ? ls : []);
  }

  async function createRoom() {
    if (!token || !selectedLesson) return;
    setLoading(true);
    try {
      const r = await createBroadcastRoom(token, selectedLesson.id);
      setRoom(r);
    } finally {
      setLoading(false);
    }
  }

  async function pushLesson() {
    if (!token || !room || !selectedLesson) return;
    setLoading(true);
    try {
      await pushBroadcastContent(token, room.code, {
        lesson_id: selectedLesson.id,
        content_md: selectedLesson.content_md,
        title: selectedLesson.title,
        key_concepts: selectedLesson.key_concepts,
      });
      setPushed(true);
      setTimeout(() => setPushed(false), 3000);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-bg flex flex-col">
      {/* Header */}
      <header className="h-12 border-b border-white/5 flex items-center gap-3 px-4">
        <Link href="/learn" className="text-t2 hover:text-t0 text-sm">← Courses</Link>
        <div className="w-px h-4 bg-white/10" />
        <span className="font-black">S<span className="text-acc">AGE</span></span>
        <div className="w-px h-4 bg-white/10" />
        <span className="text-t2 text-sm">Classroom Broadcast</span>
      </header>

      <div className="flex-1 max-w-3xl mx-auto w-full px-4 py-8 space-y-8">
        <div className="space-y-1">
          <h1 className="text-2xl font-bold text-t0">Broadcast to Your Class</h1>
          <p className="text-t2 text-sm">
            Push a lesson to up to 40 students instantly. Students scan the QR code to join — no account needed.
          </p>
        </div>

        {!room ? (
          <div className="space-y-6">
            {/* Course picker */}
            <div>
              <label className="block text-[10px] font-bold uppercase tracking-widest text-t3 mb-2">
                1. Select a course
              </label>
              <div className="grid grid-cols-2 gap-2">
                {courses.map((c) => (
                  <button
                    key={c.id}
                    onClick={() => handleCourseSelect(c)}
                    className={`text-left px-4 py-3 rounded-xl border text-sm transition-all ${
                      selectedCourse?.id === c.id
                        ? 'border-acc bg-acc/10 text-t0'
                        : 'border-white/10 text-t1 hover:border-white/20 hover:bg-white/5'
                    }`}
                  >
                    {c.title}
                  </button>
                ))}
              </div>
            </div>

            {/* Lesson picker */}
            {lessons.length > 0 && (
              <div>
                <label className="block text-[10px] font-bold uppercase tracking-widest text-t3 mb-2">
                  2. Select a lesson
                </label>
                <div className="space-y-1.5 max-h-60 overflow-y-auto pr-1">
                  {lessons.map((l) => (
                    <button
                      key={l.id}
                      onClick={() => setSelectedLesson(l)}
                      className={`w-full text-left px-4 py-3 rounded-xl border text-sm transition-all ${
                        selectedLesson?.id === l.id
                          ? 'border-acc bg-acc/10 text-t0'
                          : 'border-white/10 text-t1 hover:border-white/20 hover:bg-white/5'
                      }`}
                    >
                      {l.title}
                    </button>
                  ))}
                </div>
              </div>
            )}

            <button
              onClick={createRoom}
              disabled={!selectedLesson || loading}
              className="w-full bg-acc hover:bg-acc/90 disabled:opacity-40 text-white font-semibold py-3 rounded-xl transition-all"
            >
              {loading ? 'Creating room…' : 'Create broadcast room'}
            </button>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Room code */}
            <div className="bg-bg2 border border-white/10 rounded-2xl p-6 flex flex-col md:flex-row gap-6 items-center">
              <div className="flex-1 space-y-4">
                <div>
                  <div className="text-[10px] font-bold uppercase tracking-widest text-t3 mb-1">Room code</div>
                  <div className="text-5xl font-black tracking-widest text-acc">{room.code}</div>
                </div>
                <div>
                  <div className="text-[10px] font-bold uppercase tracking-widest text-t3 mb-1">Student join URL</div>
                  <div className="text-xs text-t2 font-mono bg-bg border border-white/5 rounded-lg px-3 py-2 break-all">
                    {room.join_url}
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => navigator.clipboard?.writeText(room.join_url)}
                    className="text-xs px-3 py-1.5 border border-white/10 rounded-lg text-t2 hover:text-t0 hover:border-white/20 transition-all"
                  >
                    Copy link
                  </button>
                  {typeof navigator !== 'undefined' && 'share' in navigator && (
                    <button
                      onClick={() => navigator.share?.({ url: room.join_url, title: 'Join SAGE classroom' })}
                      className="text-xs px-3 py-1.5 border border-white/10 rounded-lg text-t2 hover:text-t0 hover:border-white/20 transition-all"
                    >
                      Share
                    </button>
                  )}
                </div>
              </div>

              {/* QR code */}
              <div className="flex-shrink-0 bg-white p-3 rounded-xl">
                <img
                  src={getBroadcastQrUrl(room.code)}
                  alt={`QR code for room ${room.code}`}
                  width={160}
                  height={160}
                  className="block"
                />
              </div>
            </div>

            {/* Push lesson */}
            <div className="bg-bg2 border border-white/10 rounded-2xl p-5 space-y-3">
              <div>
                <div className="text-[10px] font-bold uppercase tracking-widest text-t3 mb-0.5">Lesson to broadcast</div>
                <div className="text-t0 font-semibold">{selectedLesson?.title}</div>
              </div>
              <button
                onClick={pushLesson}
                disabled={loading}
                className={`w-full font-semibold py-3 rounded-xl transition-all text-sm ${
                  pushed
                    ? 'bg-grn/20 text-grn border border-grn/30'
                    : 'bg-acc hover:bg-acc/90 text-white disabled:opacity-40'
                }`}
              >
                {loading ? 'Pushing…' : pushed ? '✓ Pushed to all students' : 'Push lesson to all students'}
              </button>
              <p className="text-t3 text-xs">
                Students currently in the room will receive the lesson content immediately.
                New students who join will also get it automatically.
              </p>
            </div>

            <button
              onClick={() => { setRoom(null); setPushed(false); }}
              className="text-sm text-t2 hover:text-t0 transition-colors"
            >
              ← Create a new room
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
