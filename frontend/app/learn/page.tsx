'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuthStore } from '@/lib/store';
import { getCourses, getLessons } from '@/lib/api';

interface Course { id: number; slug: string; title: string; description: string; level: string; tags: string[] }
interface Lesson { id: number; slug: string; title: string; order: number; summary: string; estimated_minutes: number }

const LEVEL_COLOR: Record<string, string> = {
  beginner: 'text-grn border-grn/30 bg-grn/10',
  intermediate: 'text-acc border-acc/30 bg-acc/10',
  advanced: 'text-pur border-pur/30 bg-pur/10',
};

export default function LearnPage() {
  const { token, user, clearAuth } = useAuthStore();
  const router = useRouter();
  const [courses, setCourses] = useState<Course[]>([]);
  const [expanded, setExpanded] = useState<string | null>(null);
  const [lessons, setLessons] = useState<Record<string, Lesson[]>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) { router.push('/login'); return; }
    getCourses().then(c => { setCourses(c); setLoading(false); });
  }, [token, router]);

  async function toggleCourse(slug: string) {
    if (expanded === slug) { setExpanded(null); return; }
    setExpanded(slug);
    if (!lessons[slug]) {
      const ls = await getLessons(slug);
      setLessons(p => ({ ...p, [slug]: ls }));
    }
  }

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-8 h-8 border-2 border-white/10 border-t-acc rounded-full animate-spin-slow" />
    </div>
  );

  return (
    <div className="min-h-screen flex flex-col">
      {/* Topbar */}
      <header className="border-b border-white/5 bg-bg/80 backdrop-blur-md sticky top-0 z-20">
        <div className="max-w-5xl mx-auto px-6 h-14 flex items-center justify-between">
          <div className="text-xl font-black">S<span className="text-acc">AGE</span></div>
          <div className="flex items-center gap-4">
            <span className="text-t2 text-sm hidden sm:block">Hey, {user?.display_name} 👋</span>
            <button onClick={() => { clearAuth(); router.push('/'); }} className="text-t2 text-sm hover:text-t0 transition-colors">Sign out</button>
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-5xl mx-auto px-6 py-12 w-full">
        <div className="mb-10">
          <h2 className="text-3xl font-bold mb-2">Your Courses</h2>
          <p className="text-t2 text-sm">Select a lesson to start a Socratic tutoring session.</p>
        </div>

        <div className="space-y-4">
          {courses.map(course => (
            <div key={course.slug} className="bg-bg1 border border-white/5 rounded-2xl overflow-hidden transition-all hover:border-white/10">
              <button
                className="w-full flex items-center gap-4 p-6 text-left"
                onClick={() => toggleCourse(course.slug)}
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1 flex-wrap">
                    <span className="text-lg font-bold text-t0">{course.title}</span>
                    <span className={`text-[10px] font-bold uppercase tracking-wider border rounded-full px-2 py-0.5 ${LEVEL_COLOR[course.level] || 'text-t2'}`}>
                      {course.level}
                    </span>
                  </div>
                  <p className="text-t1 text-sm leading-relaxed line-clamp-2">{course.description}</p>
                  <div className="flex gap-2 mt-2 flex-wrap">
                    {course.tags.slice(0, 4).map(t => (
                      <span key={t} className="text-[10px] text-t3 bg-bg2 border border-white/5 rounded px-2 py-0.5">{t}</span>
                    ))}
                  </div>
                </div>
                <span className="text-t2 text-lg ml-4 flex-shrink-0">{expanded === course.slug ? '↑' : '↓'}</span>
              </button>

              {expanded === course.slug && lessons[course.slug] && (
                <div className="border-t border-white/5 px-6 py-4 space-y-2">
                  {lessons[course.slug].map(lesson => (
                    <Link
                      key={lesson.slug}
                      href={`/learn/${course.slug}/${lesson.slug}`}
                      className="flex items-center gap-4 p-4 rounded-xl bg-bg2 hover:bg-bg3 border border-white/5 hover:border-acc/25 transition-all group"
                    >
                      <div className="w-8 h-8 rounded-lg bg-acc/10 text-acc flex items-center justify-center text-sm font-bold flex-shrink-0">
                        {lesson.order}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="text-sm font-semibold text-t0 group-hover:text-acc transition-colors">{lesson.title}</div>
                        <div className="text-xs text-t2 line-clamp-1">{lesson.summary}</div>
                      </div>
                      <span className="text-t3 text-xs flex-shrink-0">{lesson.estimated_minutes}m</span>
                      <span className="text-t2 group-hover:text-acc transition-colors">→</span>
                    </Link>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
