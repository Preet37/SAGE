"use client";

import { useRouter } from "next/navigation";
import { useEffect, type ReactNode } from "react";

import { useAuth } from "@/lib/auth";

export default function ProtectedRoute({ children }: { children: ReactNode }) {
  const { token, ready } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (ready && !token) router.replace("/login");
  }, [ready, token, router]);

  if (!ready) {
    return (
      <main className="grid h-screen place-items-center">
        <div className="card px-6 py-4 text-sm opacity-70">Loading…</div>
      </main>
    );
  }
  if (!token) return null;
  return <>{children}</>;
}
