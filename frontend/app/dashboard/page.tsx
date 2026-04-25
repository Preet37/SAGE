'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuthStore } from '@/lib/store';

const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface DashData {
  user: { display_name: string; subscription_tier: string; teaching_mode: string; member_since: string };
  stats: { sessions_30d: number; total_messages: number; time_spent_minutes: number; streak_days: number; concepts_mastered: number; concepts_in_progress: number; verification_fail_rate: number };
  mastery: { mastered: { id: number; label: string }[]; in_progress: { id: number; label: string; score: number }[]; weak_areas: { id: number; label: string; score: number; attempts: number }[] };
  recent_sessions: { id: number; lesson_id: number; started_at: string; teaching_mode: string }[];
  courses_active: { id: number; title: string }[];
  cognition_metrics: { semantic_retrievals: number; verification_checks: number; verification_pass_rate: number };
}

export default function DashboardPage() {
  const { token, user, clearAuth } = useAuthStore();
  const router = useRouter();
  const [data, setData] = useState<DashData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) { router.push('/login'); return; }
    fetch(`${BASE}/dashboard/overview`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.json()).then(d => { setData(d); setLoading(false); });
  }, [token, router]);

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-8 h-8 border-2 border-white/10 border-t-acc rounded-full animate-spin-slow" />
    </div>
  );

  const d = data!;

  return (
    <div className="min-h-screen flex flex-col">
      {/* Topbar */}
      <header className="border-b border-white/5 bg-bg/80 backdrop-blur-md sticky top-0 z-20">
        <div className="max-w-5xl mx-auto px-6 h-14 flex items-center gap-4">
          <Link href="/learn" className="text-t2 hover:text-t0 text-sm transition-colors">← Courses</Link>
          <span className="text-xl font-black">S<span className="text-acc">AGE</span></span>
          <span className="text-t3 text-sm">Dashboard</span>
          <div className="ml-auto flex items-center gap-3">
            <span className={`text-[10px] font-bold px-2.5 py-1 rounded-full border ${
              d.user.subscription_tier === 'pro' ? 'text-yel border-yel/30 bg-yel/10' :
              d.user.subscription_tier === 'expert' ? 'text-pur border-pur/30 bg-pur/10' :
              'text-t2 border-white/10 bg-bg2'
            }`}>
              {d.user.subscription_tier.toUpperCase()}
            </span>
            <button onClick={() => { clearAuth(); router.push('/'); }} className="text-t2 text-sm hover:text-t0">Sign out</button>
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-5xl mx-auto px-6 py-10 w-full space-y-8">
        {/* Welcome */}
        <div>
          <h1 className="text-2xl font-bold">Hey, {d.user.display_name} 👋</h1>
          <p className="text-t2 text-sm mt-1">Here's your learning progress across all SAGE courses.</p>
        </div>

        {/* Stat cards */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          {[
            { label: 'Sessions (30d)', value: d.stats.sessions_30d, color: 'text-acc', suffix: '' },
            { label: 'Day Streak', value: d.stats.streak_days, color: 'text-yel', suffix: '🔥' },
            { label: 'Time Spent', value: d.stats.time_spent_minutes, color: 'text-grn', suffix: 'm' },
            { label: 'Mastered', value: d.stats.concepts_mastered, color: 'text-grn', suffix: '' },
            { label: 'In Progress', value: d.stats.concepts_in_progress, color: 'text-acc', suffix: '' },
            { label: 'Verify Rate', value: Math.round((1 - d.stats.verification_fail_rate) * 100), color: 'text-pur', suffix: '%' },
          ].map(s => (
            <div key={s.label} className="bg-bg1 border border-white/5 rounded-2xl p-4 text-center">
              <div className={`text-2xl font-black ${s.color}`}>{s.value}{s.suffix}</div>
              <div className="text-[10px] text-t3 mt-1 font-medium">{s.label}</div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Mastery breakdown */}
          <div className="bg-bg1 border border-white/5 rounded-2xl p-5">
            <div className="text-[10px] font-bold uppercase tracking-widest text-t3 mb-4">Concept Mastery</div>
            {d.mastery.mastered.length > 0 && (
              <div className="mb-3">
                <div className="text-[10px] text-grn font-semibold mb-2">✓ Mastered ({d.mastery.mastered.length})</div>
                <div className="flex flex-wrap gap-1.5">
                  {d.mastery.mastered.map(c => (
                    <span key={c.id} className="text-[10px] text-grn bg-grn/10 border border-grn/20 px-2 py-0.5 rounded-full">{c.label}</span>
                  ))}
                </div>
              </div>
            )}
            {d.mastery.in_progress.length > 0 && (
              <div className="mb-3">
                <div className="text-[10px] text-acc font-semibold mb-2">↗ In Progress ({d.mastery.in_progress.length})</div>
                <div className="space-y-2">
                  {d.mastery.in_progress.map(c => (
                    <div key={c.id}>
                      <div className="flex justify-between text-[10px] mb-1"><span className="text-t1">{c.label}</span><span className="text-t3">{Math.round(c.score * 100)}%</span></div>
                      <div className="h-1 bg-bg3 rounded-full"><div className="h-full rounded-full bg-acc" style={{ width: `${c.score * 100}%` }} /></div>
                    </div>
                  ))}
                </div>
              </div>
            )}
            {d.mastery.weak_areas.length > 0 && (
              <div>
                <div className="text-[10px] text-pnk font-semibold mb-2">⚠ Needs Attention</div>
                {d.mastery.weak_areas.map(c => (
                  <div key={c.id} className="flex items-center gap-2 text-[10px] text-t1 mb-1">
                    <span className="text-pnk">✗</span>
                    <span>{c.label}</span>
                    <span className="ml-auto text-t3">{Math.round(c.score * 100)}% · {c.attempts} tries</span>
                  </div>
                ))}
              </div>
            )}
            {!d.mastery.mastered.length && !d.mastery.in_progress.length && (
              <div className="text-t2 text-xs text-center py-4">Start a lesson to build your mastery map!</div>
            )}
          </div>

          {/* Cognition metrics */}
          <div className="space-y-4">
            <div className="bg-bg1 border border-pur/15 rounded-2xl p-5">
              <div className="text-[10px] font-bold uppercase tracking-widest text-pur mb-3">Cognition Track Metrics</div>
              <div className="space-y-3">
                {[
                  { label: 'Semantic Retrievals', value: d.cognition_metrics.semantic_retrievals, color: '#9d78f5' },
                  { label: 'Verification Checks', value: d.cognition_metrics.verification_checks, color: '#9d78f5' },
                  { label: 'Pass Rate', value: `${Math.round(d.cognition_metrics.verification_pass_rate * 100)}%`, color: d.cognition_metrics.verification_pass_rate > 0.9 ? '#2dd4a4' : '#f5c842' },
                ].map(m => (
                  <div key={m.label} className="flex justify-between items-center">
                    <span className="text-xs text-t1">{m.label}</span>
                    <span className="text-sm font-bold" style={{ color: m.color }}>{m.value}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Active courses */}
            <div className="bg-bg1 border border-white/5 rounded-2xl p-5">
              <div className="text-[10px] font-bold uppercase tracking-widest text-t3 mb-3">Active Courses</div>
              {d.courses_active.length ? (
                d.courses_active.map(c => (
                  <Link key={c.id} href={`/learn`}
                    className="flex items-center gap-2 text-xs text-t1 hover:text-acc transition-colors py-1.5 group">
                    <div className="w-1.5 h-1.5 rounded-full bg-acc/60" />
                    {c.title}
                    <span className="ml-auto text-t3 group-hover:text-acc">→</span>
                  </Link>
                ))
              ) : (
                <div className="text-t2 text-xs">No courses started yet.</div>
              )}
            </div>

            {/* Recent sessions */}
            <div className="bg-bg1 border border-white/5 rounded-2xl p-5">
              <div className="text-[10px] font-bold uppercase tracking-widest text-t3 mb-3">Recent Sessions</div>
              {d.recent_sessions.length ? d.recent_sessions.slice(0, 4).map(s => (
                <div key={s.id} className="flex items-center gap-2 py-1.5 text-xs">
                  <div className="w-1.5 h-1.5 rounded-full bg-t3 flex-shrink-0" />
                  <span className="text-t1">Session #{s.id}</span>
                  <span className="text-[9px] text-t3 bg-bg2 px-2 py-0.5 rounded">{s.teaching_mode}</span>
                  <span className="ml-auto text-[9px] text-t3">{new Date(s.started_at).toLocaleDateString()}</span>
                </div>
              )) : <div className="text-t2 text-xs">No sessions yet.</div>}
            </div>
          </div>
        </div>

        {/* Subscription CTA */}
        {d.user.subscription_tier === 'free' && (
          <div className="bg-gradient-to-r from-pur/10 to-acc/10 border border-pur/20 rounded-2xl p-6 flex items-center justify-between">
            <div>
              <div className="text-sm font-bold text-t0 mb-1">Unlock Expert Peer Matching</div>
              <div className="text-xs text-t2">Pro connects you with verified experts in minutes — like Uber, but for understanding hard concepts.</div>
            </div>
            <button className="ml-6 flex-shrink-0 bg-pur text-white font-bold text-xs px-5 py-2.5 rounded-xl hover:bg-purple-400 transition-all shadow-lg shadow-pur/20">
              Upgrade to Pro →
            </button>
          </div>
        )}
      </main>
    </div>
  );
}
