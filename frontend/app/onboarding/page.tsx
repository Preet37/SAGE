"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { SageLogo } from "@/components/SageLogo";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";

const TOPICS = [
  { id: "llms",            label: "Large Language Models",   desc: "GPT, Claude, Llama, tokenization, RLHF" },
  { id: "agents",          label: "Agents & Reasoning",      desc: "Tool use, planning, multi-agent systems" },
  { id: "neural-networks", label: "Neural Networks",         desc: "Backprop, CNNs, RNNs, transformers" },
  { id: "multimodal",      label: "Multimodal AI",           desc: "Vision, audio, image generation" },
  { id: "generative",      label: "Generative Models",       desc: "Diffusion, GANs, VAEs, NeRFs" },
  { id: "ml-engineering",  label: "ML Engineering",          desc: "Training, fine-tuning, inference, MLOps" },
  { id: "rag",             label: "RAG & Embeddings",        desc: "Vector DBs, retrieval, semantic search" },
  { id: "reinforcement",   label: "Reinforcement Learning",  desc: "Policy gradients, reward modeling, PPO" },
  { id: "math",            label: "Math for ML",             desc: "Linear algebra, calculus, probability" },
  { id: "safety",          label: "AI Safety & Alignment",   desc: "Alignment, interpretability, red-teaming" },
  { id: "nlp",             label: "NLP Fundamentals",        desc: "Tokenization, embeddings, attention" },
  { id: "physics-ai",      label: "Physics & Scientific AI", desc: "Physics simulations, scientific computing" },
];

const LEVELS = [
  { id: "beginner",     label: "Beginner",     tag: "I",   desc: "New to ML/AI — I want a solid foundation" },
  { id: "intermediate", label: "Intermediate", tag: "II",  desc: "I know the basics, ready to go deeper" },
  { id: "advanced",     label: "Advanced",     tag: "III", desc: "I'm experienced — show me cutting-edge content" },
];

const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };
const serif: React.CSSProperties = { fontFamily: "var(--font-cormorant)" };
const body: React.CSSProperties = { fontFamily: "var(--font-crimson)" };

export default function OnboardingPage() {
  const router = useRouter();
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [step, setStep] = useState<"interests" | "level">("interests");
  const [level, setLevel] = useState<string | null>(null);
  const [creating, setCreating] = useState(false);

  function toggleTopic(id: string) {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  async function handleContinue() {
    if (step === "interests" && selected.size > 0) {
      setStep("level");
    } else if (step === "level" && level) {
      localStorage.setItem("sage_interests", JSON.stringify([...selected]));
      localStorage.setItem("sage_level", level);
      localStorage.setItem("sage_onboarded", "true");

      const token = getToken();
      if (token) {
        const topicLabels = TOPICS
          .filter(t => selected.has(t.id))
          .map(t => t.label);
        const goal = `${topicLabels.join(", ")} — ${level} level`;
        setCreating(true);
        try {
          const draft = await api.courseCreator.createDraft(goal, goal, token);
          router.push(`/create/${draft.id}`);
        } catch {
          router.push("/learn");
        }
      } else {
        router.push("/learn");
      }
    }
  }

  function handleSkip() {
    localStorage.setItem("sage_onboarded", "true");
    router.push("/learn");
  }

  if (creating) {
    return (
      <div
        className="min-h-screen flex flex-col items-center justify-center px-6"
        style={{ background: "var(--ink)", color: "var(--cream-0)" }}
      >
        <SageLogo fontSize="2rem" />
        <p
          style={{
            ...mono,
            fontSize: "0.62rem",
            letterSpacing: "0.18em",
            textTransform: "uppercase",
            color: "var(--gold)",
            marginTop: "2.5rem",
          }}
        >
          Building your course…
        </p>
        <p
          style={{
            ...body,
            fontSize: "0.95rem",
            color: "var(--cream-2)",
            marginTop: "0.6rem",
          }}
        >
          Hang tight while we set up your personalised learning path.
        </p>
      </div>
    );
  }

  return (
    <div
      className="min-h-screen flex flex-col items-center justify-center px-6 py-14"
      style={{ background: "var(--ink)", color: "var(--cream-0)" }}
    >
      <div className="w-full max-w-3xl">
        {/* Logo */}
        <div className="text-center mb-12">
          <SageLogo fontSize="2rem" />
        </div>

        {/* Progress */}
        <div className="flex items-center justify-center gap-2 mb-10">
          <div
            style={{
              height: "2px",
              width: "2.5rem",
              background: "var(--gold)",
              transition: "opacity 0.3s",
            }}
          />
          <div
            style={{
              height: "2px",
              width: "2.5rem",
              background: step === "level" ? "var(--gold)" : "rgba(240,233,214,0.15)",
              transition: "background 0.4s",
            }}
          />
        </div>

        {/* Heading */}
        <div className="text-center mb-10">
          <p
            style={{
              ...mono,
              fontSize: "0.6rem",
              letterSpacing: "0.16em",
              textTransform: "uppercase",
              color: "var(--gold)",
              marginBottom: "0.75rem",
            }}
          >
            {step === "interests" ? "01 · Interests" : "02 · Depth"}
          </p>
          <h1
            style={{
              ...serif,
              fontWeight: 700,
              fontStyle: "italic",
              fontSize: "clamp(2.2rem, 5vw, 3.5rem)",
              lineHeight: 1.1,
              color: "var(--cream-0)",
              marginBottom: "0.6rem",
            }}
          >
            {step === "interests"
              ? <>What calls to you<span style={{ color: "var(--gold)" }}>?</span></>
              : <>How far have you gone<span style={{ color: "var(--gold)" }}>?</span></>}
          </h1>
          <p
            style={{
              ...body,
              fontWeight: 300,
              fontSize: "1rem",
              color: "var(--cream-1)",
              lineHeight: 1.6,
            }}
          >
            {step === "interests"
              ? "Pick the domains that excite you — we'll shape your path around them."
              : "This sets the pace and depth of every lesson."}
          </p>
          {step === "interests" && selected.size === 0 && (
            <p
              style={{
                ...mono,
                fontSize: "0.55rem",
                letterSpacing: "0.12em",
                textTransform: "uppercase",
                color: "var(--cream-2)",
                marginTop: "0.5rem",
              }}
            >
              Select at least one
            </p>
          )}
        </div>

        {/* Topic grid */}
        {step === "interests" && (
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(3, 1fr)",
              gap: "0.75rem",
              marginBottom: "2.5rem",
            }}
          >
            {TOPICS.map((topic) => {
              const on = selected.has(topic.id);
              return (
                <button
                  key={topic.id}
                  onClick={() => toggleTopic(topic.id)}
                  className={`topic-card${on ? " selected" : ""}`}
                  style={{
                    textAlign: "left",
                    padding: "1.1rem 1.2rem",
                    background: on ? "rgba(196,152,90,0.07)" : "var(--ink-1)",
                    border: `1px solid ${on ? "var(--gold)" : "rgba(240,233,214,0.08)"}`,
                    cursor: "pointer",
                    position: "relative",
                  }}
                >
                  {on && (
                    <span
                      style={{
                        position: "absolute",
                        top: "0.6rem",
                        right: "0.75rem",
                        ...mono,
                        fontSize: "0.55rem",
                        letterSpacing: "0.1em",
                        color: "var(--gold)",
                      }}
                    >
                      ✓
                    </span>
                  )}
                  <p
                    style={{
                      ...serif,
                      fontWeight: 600,
                      fontStyle: "italic",
                      fontSize: "1rem",
                      color: on ? "var(--cream-0)" : "var(--cream-1)",
                      lineHeight: 1.3,
                      marginBottom: "0.3rem",
                      transition: "color 0.2s",
                    }}
                  >
                    {topic.label}
                  </p>
                  <p
                    style={{
                      ...mono,
                      fontSize: "0.58rem",
                      letterSpacing: "0.06em",
                      color: "var(--cream-2)",
                      lineHeight: 1.5,
                    }}
                  >
                    {topic.desc}
                  </p>
                </button>
              );
            })}
          </div>
        )}

        {/* Level selection */}
        {step === "level" && (
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "0.75rem",
              maxWidth: "32rem",
              margin: "0 auto 2.5rem",
            }}
          >
            {LEVELS.map((l) => {
              const on = level === l.id;
              return (
                <button
                  key={l.id}
                  onClick={() => setLevel(l.id)}
                  className={`topic-card${on ? " selected" : ""}`}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "1.25rem",
                    textAlign: "left",
                    padding: "1.25rem 1.5rem",
                    background: on ? "rgba(196,152,90,0.07)" : "var(--ink-1)",
                    border: `1px solid ${on ? "var(--gold)" : "rgba(240,233,214,0.08)"}`,
                    cursor: "pointer",
                  }}
                >
                  <span
                    style={{
                      ...mono,
                      fontSize: "0.7rem",
                      letterSpacing: "0.08em",
                      color: on ? "var(--gold)" : "var(--cream-2)",
                      minWidth: "1.5rem",
                      transition: "color 0.2s",
                    }}
                  >
                    {l.tag}
                  </span>
                  <div style={{ flex: 1 }}>
                    <p
                      style={{
                        ...serif,
                        fontWeight: 600,
                        fontStyle: "italic",
                        fontSize: "1.15rem",
                        color: on ? "var(--cream-0)" : "var(--cream-1)",
                        marginBottom: "0.15rem",
                        transition: "color 0.2s",
                      }}
                    >
                      {l.label}
                    </p>
                    <p
                      style={{
                        ...body,
                        fontWeight: 300,
                        fontSize: "0.9rem",
                        color: "var(--cream-2)",
                      }}
                    >
                      {l.desc}
                    </p>
                  </div>
                  {on && (
                    <span style={{ color: "var(--gold)", fontSize: "0.8rem", ...mono }}>→</span>
                  )}
                </button>
              );
            })}
          </div>
        )}

        {/* Continue */}
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "1.25rem" }}>
          <button
            onClick={handleContinue}
            disabled={creating || (step === "interests" ? selected.size === 0 : !level)}
            style={{
              ...mono,
              fontSize: "0.68rem",
              letterSpacing: "0.15em",
              textTransform: "uppercase",
              background: "var(--gold)",
              color: "var(--ink)",
              border: "none",
              padding: "0.9rem 3rem",
              cursor: (creating || (selected.size === 0 && step === "interests")) ? "not-allowed" : "pointer",
              opacity: (creating || (step === "interests" ? selected.size === 0 : !level)) ? 0.45 : 1,
              transition: "opacity 0.2s",
            }}
          >
            {step === "level" ? "Start Learning →" : "Continue →"}
          </button>

          <button
            onClick={handleSkip}
            style={{
              ...mono,
              fontSize: "0.58rem",
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              color: "var(--cream-2)",
              background: "none",
              border: "none",
              cursor: "pointer",
              transition: "color 0.2s",
            }}
            onMouseEnter={(e) => ((e.currentTarget as HTMLButtonElement).style.color = "var(--cream-1)")}
            onMouseLeave={(e) => ((e.currentTarget as HTMLButtonElement).style.color = "var(--cream-2)")}
          >
            Skip for now
          </button>
        </div>
      </div>
    </div>
  );
}
