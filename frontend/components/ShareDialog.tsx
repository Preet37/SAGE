"use client";
import { useEffect, useState } from "react";
import { api, ShareEntry } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Check, Copy, Link2, Loader2, Trash2, X } from "lucide-react";

interface ShareDialogProps {
  slug: string;
  onClose: () => void;
}

export function ShareDialog({ slug, onClose }: ShareDialogProps) {
  const [email, setEmail] = useState("");
  const [shares, setShares] = useState<ShareEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [sharing, setSharing] = useState(false);
  const [error, setError] = useState("");
  const [shareLink, setShareLink] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const token = getToken();
    if (!token) return;
    api.learningPaths.getShares(slug, token)
      .then(setShares)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [slug]);

  async function handleShare() {
    const token = getToken();
    if (!token || !email.trim()) return;
    setSharing(true);
    setError("");
    try {
      const res = await api.learningPaths.share(slug, email.trim(), token);
      if (res.status === "already_shared") {
        setError("Already shared with this user");
      } else {
        setEmail("");
        const updated = await api.learningPaths.getShares(slug, token);
        setShares(updated);
      }
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to share");
    } finally {
      setSharing(false);
    }
  }

  async function handleUnshare(userId: string) {
    const token = getToken();
    if (!token) return;
    try {
      await api.learningPaths.unshare(slug, userId, token);
      setShares(shares.filter(s => s.user_id !== userId));
    } catch {
      // ignore
    }
  }

  async function handleCopyLink() {
    const token = getToken();
    if (!token) return;
    try {
      if (!shareLink) {
        const res = await api.learningPaths.getShareLink(slug, token);
        const link = `${window.location.origin}/join/${res.share_token}`;
        setShareLink(link);
        await navigator.clipboard.writeText(link);
      } else {
        await navigator.clipboard.writeText(shareLink);
      }
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // ignore
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={onClose}>
      <Card className="w-full max-w-md mx-4 shadow-xl" onClick={(e) => e.stopPropagation()}>
        <CardHeader className="flex flex-row items-center justify-between pb-3">
          <CardTitle className="text-lg">Share Course</CardTitle>
          <Button variant="ghost" size="icon" onClick={onClose} className="h-8 w-8">
            <X className="h-4 w-4" />
          </Button>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Share by email */}
          <div className="flex gap-2">
            <Input
              placeholder="Email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleShare()}
              className="flex-1"
            />
            <Button onClick={handleShare} disabled={sharing || !email.trim()} size="sm">
              {sharing ? <Loader2 className="h-4 w-4 animate-spin" /> : "Share"}
            </Button>
          </div>
          {error && <p className="text-sm text-red-500">{error}</p>}

          {/* Copy share link */}
          <Button
            variant="outline"
            size="sm"
            className="w-full gap-2"
            onClick={handleCopyLink}
          >
            {copied ? (
              <>
                <Check className="h-3.5 w-3.5 text-green-500" />
                Copied!
              </>
            ) : (
              <>
                <Link2 className="h-3.5 w-3.5" />
                Copy Share Link
              </>
            )}
          </Button>

          {/* Current shares */}
          {loading ? (
            <p className="text-sm text-muted-foreground">Loading...</p>
          ) : shares.length > 0 ? (
            <div className="space-y-2">
              <p className="text-xs text-muted-foreground font-medium uppercase tracking-wider">
                Shared with
              </p>
              {shares.map((s) => (
                <div key={s.user_id} className="flex items-center justify-between py-1.5">
                  <div>
                    <p className="text-sm font-medium">{s.username}</p>
                    <p className="text-xs text-muted-foreground">{s.email}</p>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-7 w-7 text-muted-foreground hover:text-red-500"
                    onClick={() => handleUnshare(s.user_id)}
                  >
                    <Trash2 className="h-3.5 w-3.5" />
                  </Button>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-xs text-muted-foreground text-center py-2">
              Not shared with anyone yet
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
