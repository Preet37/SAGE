"use client";
import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Loader2 } from "lucide-react";

export default function JoinPage() {
  const router = useRouter();
  const params = useParams();
  const token = params.token as string;
  const [error, setError] = useState("");

  useEffect(() => {
    const authToken = getToken();
    if (!authToken) {
      router.push("/login");
      return;
    }
    api.learningPaths.joinViaLink(token, authToken)
      .then((res) => {
        router.push(`/learn/${res.slug}`);
      })
      .catch((e) => {
        setError(e instanceof Error ? e.message : "Invalid or expired share link");
      });
  }, [token, router]);

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-dvh gap-4">
        <p className="text-red-500">{error}</p>
        <a href="/learn" className="text-primary hover:underline text-sm">Go to Learn</a>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center h-dvh">
      <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
    </div>
  );
}
