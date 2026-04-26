"use client";
import { Suspense, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";
import { setToken } from "@/lib/auth";
import { SageLogo } from "@/components/SageLogo";

export default function LoginPage() {
  return (
    <Suspense>
      <LoginForm />
    </Suspense>
  );
}

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const returnTo = searchParams.get("returnTo") || "/learn";
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await api.auth.login(email, password);
      setToken(res.access_token);
      router.push(returnTo);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      className="min-h-screen flex"
      style={{ background: "var(--ink)", color: "var(--cream-0)" }}
    >
      {/* ── Left panel — editorial ───────────────────────── */}
      <div
        className="hidden lg:flex flex-col justify-between w-1/2 px-16 py-14"
        style={{ borderRight: "1px solid rgba(240,233,214,0.07)" }}
      >
        {/* Logo */}
        <div>
          <SageLogo fontSize="1.05rem" />
        </div>

        {/* Editorial centre */}
        <div className="flex flex-col gap-5">
          <span
            style={{
              fontFamily: "var(--font-dm-mono)",
              fontSize: "0.62rem",
              letterSpacing: "0.16em",
              textTransform: "uppercase",
              color: "var(--gold)",
            }}
          >
            02 · Authentication
          </span>
          <h2
            style={{
              fontFamily: "var(--font-cormorant)",
              fontWeight: 700,
              fontStyle: "italic",
              fontSize: "clamp(2.8rem, 5vw, 4.8rem)",
              lineHeight: 1.05,
              color: "var(--cream-0)",
            }}
          >
            Resume the<br />
            inquiry<span style={{ color: "var(--gold)" }}>.</span>
          </h2>
          <p
            style={{
              fontFamily: "var(--font-crimson)",
              fontWeight: 300,
              fontSize: "1.05rem",
              lineHeight: 1.75,
              color: "var(--cream-1)",
              maxWidth: "28rem",
            }}
          >
            Six agents have been waiting. Pick up the thread you left, or take
            it somewhere new.
          </p>
        </div>

        {/* Footer metadata */}
        <p
          style={{
            fontFamily: "var(--font-dm-mono)",
            fontSize: "0.58rem",
            letterSpacing: "0.15em",
            textTransform: "uppercase",
            color: "var(--cream-2)",
          }}
        >
          Fetch.AI Powered · Multi-Agent Architecture
        </p>
      </div>

      {/* ── Right panel — form ───────────────────────────── */}
      <div className="flex flex-col justify-center w-full lg:w-1/2 px-8 lg:px-20">
        <div className="w-full max-w-sm mx-auto">
          {/* Section label */}
          <div className="flex items-center gap-3 mb-9">
            <div
              style={{ width: "1.6rem", height: "1px", background: "var(--gold)" }}
            />
            <span
              style={{
                fontFamily: "var(--font-dm-mono)",
                fontSize: "0.62rem",
                letterSpacing: "0.16em",
                textTransform: "uppercase",
                color: "var(--cream-1)",
              }}
            >
              Sign In
            </span>
          </div>

          <h1
            className="mb-9"
            style={{
              fontFamily: "var(--font-cormorant)",
              fontWeight: 700,
              fontStyle: "italic",
              fontSize: "3rem",
              lineHeight: 1.1,
              color: "var(--cream-0)",
            }}
          >
            Welcome back.
          </h1>

          <form onSubmit={handleSubmit} className="space-y-7">
            {/* Email */}
            <div className="space-y-2">
              <label
                style={{
                  fontFamily: "var(--font-dm-mono)",
                  fontSize: "0.58rem",
                  letterSpacing: "0.15em",
                  textTransform: "uppercase",
                  color: "var(--cream-1)",
                  display: "block",
                }}
              >
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="demo@sage.ai"
                className="w-full bg-transparent outline-none py-2"
                style={{
                  fontFamily: "var(--font-crimson)",
                  fontSize: "1.05rem",
                  color: "var(--cream-0)",
                  borderBottom: "1px solid rgba(240,233,214,0.18)",
                }}
              />
            </div>

            {/* Password */}
            <div className="space-y-2">
              <label
                style={{
                  fontFamily: "var(--font-dm-mono)",
                  fontSize: "0.58rem",
                  letterSpacing: "0.15em",
                  textTransform: "uppercase",
                  color: "var(--cream-1)",
                  display: "block",
                }}
              >
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="••••••••"
                className="w-full bg-transparent outline-none py-2"
                style={{
                  fontFamily: "var(--font-crimson)",
                  fontSize: "1.05rem",
                  color: "var(--cream-0)",
                  borderBottom: "1px solid rgba(240,233,214,0.18)",
                }}
              />
            </div>

            {error && (
              <p
                style={{
                  fontFamily: "var(--font-dm-mono)",
                  fontSize: "0.68rem",
                  color: "var(--rose)",
                }}
              >
                {error}
              </p>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-4 transition-opacity hover:opacity-90 disabled:opacity-50"
              style={{
                background: "var(--gold)",
                fontFamily: "var(--font-dm-mono)",
                fontSize: "0.68rem",
                letterSpacing: "0.15em",
                textTransform: "uppercase",
                color: "var(--ink)",
                cursor: "pointer",
                border: "none",
                marginTop: "0.5rem",
              }}
            >
              {loading ? "Signing in..." : "Sign In →"}
            </button>
          </form>

          {/* Footer links */}
          <div className="mt-7 space-y-3">
            <p
              style={{
                fontFamily: "var(--font-crimson)",
                fontSize: "0.95rem",
                color: "var(--cream-1)",
              }}
            >
              No account?{" "}
              <Link
                href={
                  returnTo !== "/learn"
                    ? `/register?returnTo=${returnTo}`
                    : "/register"
                }
                style={{
                  color: "var(--cream-0)",
                  textDecoration: "underline",
                  textUnderlineOffset: "3px",
                }}
              >
                Create one
              </Link>
            </p>
            <p
              style={{
                fontFamily: "var(--font-dm-mono)",
                fontSize: "0.56rem",
                letterSpacing: "0.13em",
                textTransform: "uppercase",
                color: "var(--cream-2)",
              }}
            >
              Demo · demo@sage.ai · demo1234
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
