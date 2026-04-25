"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";

import { getMe, login, register } from "@/lib/api";
import { setAuth } from "@/lib/auth";

interface AuthFormProps {
  mode: "login" | "register";
}

export default function AuthForm({ mode }: AuthFormProps) {
  const router = useRouter();
  const isLogin = mode === "login";
  const [email, setEmail] = useState(isLogin ? "demo@sage.ai" : "");
  const [password, setPassword] = useState(isLogin ? "demo1234" : "");
  const [name, setName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(e: FormEvent): Promise<void> {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      if (!isLogin) {
        await register(email.trim(), password, name.trim());
      }
      const auth = await login(email.trim(), password);
      const me = await getMe(auth.access_token);
      setAuth(auth.access_token, me);
      router.replace("/learn");
    } catch (err) {
      setError(toMessage(err, isLogin));
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="bg-blobs grid min-h-screen place-items-center p-6">
      <form
        onSubmit={onSubmit}
        className="card w-full max-w-sm space-y-4 p-7"
        aria-label={isLogin ? "Sign in" : "Create account"}
      >
        <header>
          <h1
            className="text-2xl"
            style={{ fontFamily: "var(--font-heading)", fontWeight: 700 }}
          >
            {isLogin ? "Welcome back" : "Join SAGE"}
          </h1>
          <p className="mt-1 text-sm opacity-70">
            {isLogin
              ? "Sign in to continue learning."
              : "Create your account to start learning Socratically."}
          </p>
        </header>

        {!isLogin && (
          <Field
            label="Display name"
            value={name}
            onChange={setName}
            placeholder="Your name"
          />
        )}
        <Field
          label="Email"
          type="email"
          value={email}
          onChange={setEmail}
          autoComplete="email"
          required
        />
        <Field
          label="Password"
          type="password"
          value={password}
          onChange={setPassword}
          autoComplete={isLogin ? "current-password" : "new-password"}
          required
          minLength={8}
        />

        {error && (
          <p
            role="alert"
            className="rounded-xl px-3 py-2 text-sm"
            style={{
              background: "color-mix(in srgb, var(--color-destructive) 12%, white)",
              color: "var(--color-destructive)",
              border: "1px solid var(--color-destructive)",
            }}
          >
            {error}
          </p>
        )}

        <button type="submit" disabled={busy} className="btn-primary w-full disabled:opacity-60">
          {busy ? "Working…" : isLogin ? "Sign in" : "Create account"}
        </button>

        <p className="text-center text-sm opacity-70">
          {isLogin ? (
            <>
              No account?{" "}
              <Link href="/register" className="font-semibold" style={{ color: "var(--color-primary)" }}>
                Register
              </Link>
            </>
          ) : (
            <>
              Already have an account?{" "}
              <Link href="/login" className="font-semibold" style={{ color: "var(--color-primary)" }}>
                Sign in
              </Link>
            </>
          )}
        </p>
      </form>
    </main>
  );
}

interface FieldProps {
  label: string;
  value: string;
  onChange: (v: string) => void;
  type?: string;
  placeholder?: string;
  autoComplete?: string;
  required?: boolean;
  minLength?: number;
}

function Field({
  label,
  value,
  onChange,
  type = "text",
  placeholder,
  autoComplete,
  required,
  minLength,
}: FieldProps) {
  return (
    <label className="block">
      <span className="mb-1 block text-xs font-semibold opacity-80">{label}</span>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        autoComplete={autoComplete}
        required={required}
        minLength={minLength}
        className="w-full rounded-2xl border px-3 py-2 text-sm outline-none focus:ring-2"
        style={{
          background: "var(--color-muted)",
          borderColor: "var(--color-border)",
        }}
      />
    </label>
  );
}

function toMessage(err: unknown, isLogin: boolean): string {
  if (err instanceof Error && err.message) {
    if (err.message.includes("Email already")) return "That email is already registered.";
    if (err.message.toLowerCase().includes("invalid credentials")) {
      return "Invalid email or password.";
    }
    return err.message;
  }
  return isLogin ? "Sign-in failed." : "Registration failed.";
}
