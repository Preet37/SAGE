"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Loader2, Save, X } from "lucide-react";
import { api, LearnerProfileResponse } from "@/lib/api";
import { getToken } from "@/lib/auth";

const EXPERTISE = ["beginner", "intermediate", "advanced", "unspecified"] as const;
const STYLES = ["default", "eli5", "analogy", "code", "deep_dive"] as const;

const STYLE_LABELS: Record<string, string> = {
  default: "Default",
  eli5: "ELI5 — simple language and analogies",
  analogy: "Analogy-led explanations",
  code: "Code-first examples",
  deep_dive: "Deep dive with rigor",
};

export default function ProfilePage() {
  const router = useRouter();
  const [profile, setProfile] = useState<LearnerProfileResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [savedAt, setSavedAt] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [interestInput, setInterestInput] = useState("");

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }
    api.profile
      .get(token)
      .then(setProfile)
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load"))
      .finally(() => setLoading(false));
  }, [router]);

  async function save(next: Partial<LearnerProfileResponse>) {
    const token = getToken();
    if (!token || !profile) return;
    setSaving(true);
    setError(null);
    try {
      const updated = await api.profile.update(next, token);
      setProfile(updated);
      setSavedAt(Date.now());
    } catch (e) {
      setError(e instanceof Error ? e.message : "Save failed");
    } finally {
      setSaving(false);
    }
  }

  function addInterest() {
    if (!profile) return;
    const tag = interestInput.trim();
    if (!tag) return;
    if (profile.interests.includes(tag)) {
      setInterestInput("");
      return;
    }
    save({ interests: [...profile.interests, tag] });
    setInterestInput("");
  }

  function removeInterest(tag: string) {
    if (!profile) return;
    save({ interests: profile.interests.filter((i) => i !== tag) });
  }

  if (loading || !profile) {
    return (
      <div className="flex items-center justify-center min-h-[40vh] text-muted-foreground gap-2">
        <Loader2 className="h-4 w-4 animate-spin" /> Loading profile...
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold tracking-tight">Your learning profile</h1>
        <p className="text-sm text-muted-foreground mt-1">
          The tutor adapts depth, vocabulary, and analogies to these settings —
          even on the first turn of a new conversation.
        </p>
      </div>

      {error && (
        <div className="mb-4 rounded-lg border border-rose-200 bg-rose-50 dark:border-rose-900 dark:bg-rose-950/40 px-4 py-3 text-sm text-rose-700 dark:text-rose-300">
          {error}
        </div>
      )}

      <div className="space-y-6">
        <section>
          <label className="text-sm font-medium text-foreground" htmlFor="expertise">
            Expertise level
          </label>
          <p className="text-xs text-muted-foreground mb-2">
            Helps the tutor calibrate how much to assume you know.
          </p>
          <select
            id="expertise"
            value={profile.expertise_level}
            onChange={(e) => save({ expertise_level: e.target.value })}
            className="w-full rounded-xl border border-border bg-background px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          >
            {EXPERTISE.map((opt) => (
              <option key={opt} value={opt}>
                {opt.charAt(0).toUpperCase() + opt.slice(1)}
              </option>
            ))}
          </select>
        </section>

        <section>
          <label className="text-sm font-medium text-foreground" htmlFor="style">
            Default explanation style
          </label>
          <p className="text-xs text-muted-foreground mb-2">
            You can still switch styles per-message via the mode bar.
          </p>
          <select
            id="style"
            value={profile.preferred_style}
            onChange={(e) => save({ preferred_style: e.target.value })}
            className="w-full rounded-xl border border-border bg-background px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          >
            {STYLES.map((opt) => (
              <option key={opt} value={opt}>
                {STYLE_LABELS[opt] ?? opt}
              </option>
            ))}
          </select>
        </section>

        <section>
          <span className="text-sm font-medium text-foreground">Interests</span>
          <p className="text-xs text-muted-foreground mb-2">
            Topics the tutor should weave into examples and analogies.
          </p>
          <div className="flex gap-2 flex-wrap mb-2" role="list">
            {profile.interests.map((tag) => (
              <span
                key={tag}
                role="listitem"
                className="inline-flex items-center gap-1 rounded-full bg-primary/10 text-primary px-3 py-1 text-xs"
              >
                {tag}
                <button
                  onClick={() => removeInterest(tag)}
                  aria-label={`Remove ${tag}`}
                  className="hover:text-foreground"
                >
                  <X className="h-3 w-3" />
                </button>
              </span>
            ))}
            {profile.interests.length === 0 && (
              <span className="text-xs text-muted-foreground italic">No interests yet.</span>
            )}
          </div>
          <div className="flex gap-2">
            <input
              type="text"
              value={interestInput}
              onChange={(e) => setInterestInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  addInterest();
                }
              }}
              placeholder="e.g. transformers"
              aria-label="Add an interest"
              className="flex-1 rounded-xl border border-border bg-background px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
            />
            <button
              onClick={addInterest}
              disabled={!interestInput.trim() || saving}
              className="rounded-xl bg-primary text-primary-foreground px-4 py-2 text-sm font-medium hover:bg-primary/90 transition-colors disabled:opacity-50"
            >
              Add
            </button>
          </div>
        </section>

        <section>
          <label className="text-sm font-medium text-foreground" htmlFor="goals">
            Goal
          </label>
          <p className="text-xs text-muted-foreground mb-2">
            One or two sentences on what you're trying to achieve.
          </p>
          <textarea
            id="goals"
            defaultValue={profile.goals}
            onBlur={(e) => {
              if (e.target.value !== profile.goals) save({ goals: e.target.value });
            }}
            placeholder="I'm preparing for a graduate ML class and want intuition more than rigor."
            rows={3}
            className="w-full resize-none rounded-xl border border-border bg-background px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </section>

        <div className="flex items-center gap-2 text-xs text-muted-foreground" aria-live="polite">
          {saving ? (
            <><Loader2 className="h-3 w-3 animate-spin" /> Saving...</>
          ) : savedAt ? (
            <><Save className="h-3 w-3" /> Saved · {new Date(savedAt).toLocaleTimeString()}</>
          ) : (
            <span>Changes save automatically.</span>
          )}
        </div>
      </div>
    </div>
  );
}
