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
    <div className="au">
      <aside className="au-hero">
        <Link href="/" className="au-mark">
          SAGE<span className="period">.</span>
        </Link>

        <div className="au-hero-body">
          <div className="au-eyebrow">02 · Authentication</div>
          <h2 className="au-h1">
            Resume the<br />inquiry<span className="period">.</span>
          </h2>
          <p className="au-tag">
            Six agents have been waiting. Pick up the thread you left, or take it somewhere new.
          </p>
        </div>

        <div className="au-hero-foot">Fetch.ai Powered · Multi-Agent Architecture</div>
      </aside>

      <main className="au-panel">
        <div className="au-panel-inner">
          <Link href="/" className="au-mark au-mark-mobile">
            SAGE<span className="period">.</span>
          </Link>

          <div className="au-step">Sign In</div>
          <h1 className="au-title">
            Welcome back<span className="period">.</span>
          </h1>

          <form onSubmit={handleSubmit} noValidate>
            <div className="au-field">
              <label htmlFor="au-email" className="au-label">Email</label>
              <input
                id="au-email"
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                className="au-input"
                placeholder="you@example.com"
                autoComplete="email"
                required
              />
            </div>

            <div className="au-field">
              <label htmlFor="au-password" className="au-label">Password</label>
              <input
                id="au-password"
                type="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                className="au-input"
                placeholder="••••••••"
                autoComplete="current-password"
                required
              />
            </div>

            {error && <p className="au-error" role="alert">{error}</p>}

            <button type="submit" disabled={loading} className="au-submit">
              {loading ? 'Signing in…' : 'Sign In →'}
            </button>
          </form>

          <div className="au-foot">
            <span className="au-foot-line">
              No account?{' '}
              <Link href="/register" className="au-foot-link">Create one</Link>
            </span>
            <span className="au-demo">Demo · demo@sage.ai · demo1234</span>
          </div>
        </div>
      </main>
    </div>
  );
}
