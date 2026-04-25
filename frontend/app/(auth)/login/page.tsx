'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { login } from '@/lib/api';
import { useAuthStore } from '@/lib/store';

export default function LoginPage() {
  const [email, setEmail] = useState('demo@sage.ai');
  const [password, setPassword] = useState('demo1234');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { setAuth } = useAuthStore();
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const data = await login(email, password);
      setAuth(data.access_token, data.user);
      router.push('/learn');
    } catch (err: unknown) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <h1 className="text-3xl font-black mb-1">S<span className="text-acc">AGE</span></h1>
        <p className="text-t2 text-sm mb-8">Sign in to continue learning</p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-xs font-semibold text-t2 uppercase tracking-widest block mb-1.5">Email</label>
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              className="w-full bg-bg2 border border-white/10 rounded-xl px-4 py-3 text-sm text-t0 outline-none focus:border-acc/50 transition-colors"
              placeholder="you@example.com"
              required
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-t2 uppercase tracking-widest block mb-1.5">Password</label>
            <input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              className="w-full bg-bg2 border border-white/10 rounded-xl px-4 py-3 text-sm text-t0 outline-none focus:border-acc/50 transition-colors"
              placeholder="••••••••"
              required
            />
          </div>

          {error && <p className="text-pnk text-xs">{error}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-acc text-white font-bold py-3 rounded-xl text-sm hover:bg-blue-400 transition-all disabled:opacity-50"
          >
            {loading ? 'Signing in…' : 'Sign In →'}
          </button>
        </form>

        <p className="text-t2 text-xs text-center mt-6">
          No account?{' '}
          <Link href="/register" className="text-acc hover:underline">Create one</Link>
        </p>
        <p className="text-t3 text-xs text-center mt-2">Demo: demo@sage.ai / demo1234</p>
      </div>
    </div>
  );
}
