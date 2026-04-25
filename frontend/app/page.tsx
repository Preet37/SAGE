'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store';
import Link from 'next/link';

export default function Home() {
  const { token } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (token) router.push('/learn');
  }, [token, router]);

  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-6 py-16 relative overflow-hidden">
      {/* Background glow */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-acc/5 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-0 w-[400px] h-[400px] bg-pur/4 rounded-full blur-3xl" />
      </div>

      <div className="relative z-10 flex flex-col items-center text-center max-w-2xl">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 text-[10.5px] font-semibold tracking-widest uppercase text-acc bg-acc/10 border border-acc/30 rounded-full px-4 py-1.5 mb-8 animate-fade-up">
          <span className="w-1.5 h-1.5 rounded-full bg-acc animate-pulse" />
          Light the Way · LA Hacks 2026
        </div>

        {/* Wordmark */}
        <h1 className="text-[90px] font-black tracking-tight leading-none mb-4 animate-fade-up" style={{ animationDelay: '0.1s' }}>
          S<span className="text-acc">AGE</span>
        </h1>
        <p className="text-xl text-t1 mb-2 animate-fade-up" style={{ animationDelay: '0.18s' }}>
          Socratic Agent for Guided Education
        </p>
        <p className="text-sm text-t2 mb-12 animate-fade-up" style={{ animationDelay: '0.25s' }}>
          6 AI agents · live concept maps · voice · peer learning · Fetch.ai powered
        </p>

        {/* CTAs */}
        <div className="flex gap-4 mb-16 animate-fade-up" style={{ animationDelay: '0.32s' }}>
          <Link
            href="/register"
            className="bg-acc text-white font-bold px-6 py-3 rounded-xl text-sm tracking-wide hover:bg-blue-400 transition-all shadow-lg shadow-acc/20"
          >
            Start Learning →
          </Link>
          <Link
            href="/login"
            className="border border-white/10 text-t1 font-medium px-6 py-3 rounded-xl text-sm hover:border-white/20 hover:text-t0 transition-all"
          >
            Sign In
          </Link>
        </div>

        {/* Feature grid */}
        <div className="grid grid-cols-3 gap-3 w-full animate-fade-up" style={{ animationDelay: '0.4s' }}>
          {[
            { icon: '⚡', label: 'Fetch.ai Agents', desc: '6 parallel agents fire on every question' },
            { icon: '◎', label: 'Live Concept Map', desc: 'D3 knowledge graph updates as you learn' },
            { icon: '◉', label: 'Voice Agent', desc: 'Speak questions, hear Socratic answers' },
            { icon: '✓', label: 'Verified Outputs', desc: 'Every response checked for hallucinations' },
            { icon: '◈', label: 'Peer Matching', desc: 'Arista-style routing to study partners' },
            { icon: '↩', label: 'Session Replay', desc: 'Every agent decision logged and replayable' },
          ].map((f) => (
            <div key={f.label} className="bg-bg1 border border-white/5 rounded-2xl p-4 text-left hover:border-white/10 transition-colors">
              <div className="text-2xl mb-2">{f.icon}</div>
              <div className="text-xs font-bold text-t0 mb-1">{f.label}</div>
              <div className="text-xs text-t2 leading-relaxed">{f.desc}</div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
