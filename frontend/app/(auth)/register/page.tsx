'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { register } from '@/lib/api';
import { useAuthStore } from '@/lib/store';

export default function RegisterPage() {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { setAuth } = useAuthStore();
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const data = await register(email, username, password, displayName);
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
        <p className="text-t2 text-sm mb-8">Create your account</p>

        <form onSubmit={handleSubmit} className="space-y-4">
          {[
            { label: 'Display Name', value: displayName, set: setDisplayName, type: 'text', placeholder: 'Your name' },
            { label: 'Username', value: username, set: setUsername, type: 'text', placeholder: 'johndoe' },
            { label: 'Email', value: email, set: setEmail, type: 'email', placeholder: 'you@example.com' },
            { label: 'Password', value: password, set: setPassword, type: 'password', placeholder: '••••••••' },
          ].map(f => (
            <div key={f.label}>
              <label className="text-xs font-semibold text-t2 uppercase tracking-widest block mb-1.5">{f.label}</label>
              <input
                type={f.type}
                value={f.value}
                onChange={e => f.set(e.target.value)}
                placeholder={f.placeholder}
                className="w-full bg-bg2 border border-white/10 rounded-xl px-4 py-3 text-sm text-t0 outline-none focus:border-acc/50 transition-colors"
                required
              />
            </div>
          ))}

          {error && <p className="text-pnk text-xs">{error}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-acc text-white font-bold py-3 rounded-xl text-sm hover:bg-blue-400 transition-all disabled:opacity-50"
          >
            {loading ? 'Creating account…' : 'Start Learning →'}
          </button>
        </form>

        <p className="text-t2 text-xs text-center mt-6">
          Already have an account?{' '}
          <Link href="/login" className="text-acc hover:underline">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
