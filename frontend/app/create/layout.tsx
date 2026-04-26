"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";

export default function CreateLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [authed, setAuthed] = useState(false);

  useEffect(() => {
    if (!getToken()) {
      router.push("/login?returnTo=/create");
    } else {
      setAuthed(true);
    }
  }, [router]);

  if (!authed) {
    return null;
  }

  return (
    <div style={{ height: "100vh", width: "100vw", overflow: "hidden", background: "var(--ink)" }}>
      {children}
    </div>
  );
}
