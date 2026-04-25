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
    <div className="h-screen w-screen overflow-hidden bg-background">
      {children}
    </div>
  );
}
