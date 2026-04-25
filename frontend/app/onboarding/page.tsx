"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { ArrowRight, Check } from "lucide-react";

const INTEREST_TOPICS = [
  { id: "llms", label: "Large Language Models", emoji: "🧠", desc: "GPT, Claude, Llama, tokenization, RLHF" },
  { id: "agents", label: "Agents & Reasoning", emoji: "🤖", desc: "Tool use, planning, multi-agent systems" },
  { id: "neural-networks", label: "Neural Networks", emoji: "⚡", desc: "Backprop, CNNs, RNNs, transformers" },
  { id: "multimodal", label: "Multimodal AI", emoji: "👁️", desc: "Vision, audio, image generation" },
  { id: "generative", label: "Generative Models", emoji: "🎨", desc: "Diffusion, GANs, VAEs, NeRFs" },
  { id: "ml-engineering", label: "ML Engineering", emoji: "🔧", desc: "Training, fine-tuning, inference, MLOps" },
  { id: "rag", label: "RAG & Embeddings", emoji: "🔍", desc: "Vector DBs, retrieval, semantic search" },
  { id: "reinforcement", label: "Reinforcement Learning", emoji: "🎮", desc: "Policy gradients, reward modeling, PPO" },
  { id: "math", label: "Math for ML", emoji: "📐", desc: "Linear algebra, calculus, probability" },
  { id: "safety", label: "AI Safety & Alignment", emoji: "🛡️", desc: "Alignment, interpretability, red-teaming" },
  { id: "nlp", label: "NLP Fundamentals", emoji: "💬", desc: "Tokenization, embeddings, attention" },
  { id: "physics-ai", label: "Physics & Scientific AI", emoji: "🔬", desc: "Physics simulations, scientific computing" },
];

export default function OnboardingPage() {
  const router = useRouter();
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [step, setStep] = useState<"interests" | "level">("interests");
  const [level, setLevel] = useState<string | null>(null);

  function toggleTopic(id: string) {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  function handleContinue() {
    if (step === "interests" && selected.size > 0) {
      setStep("level");
    } else if (step === "level" && level) {
      // Save to localStorage
      localStorage.setItem("sage_interests", JSON.stringify([...selected]));
      localStorage.setItem("sage_level", level);
      localStorage.setItem("sage_onboarded", "true");
      router.push("/learn");
    }
  }

  const LEVELS = [
    { id: "beginner", label: "Beginner", desc: "New to ML/AI — I want a solid foundation", emoji: "🌱" },
    { id: "intermediate", label: "Intermediate", desc: "I know the basics, ready to go deeper", emoji: "🚀" },
    { id: "advanced", label: "Advanced", desc: "I'm experienced — show me cutting-edge content", emoji: "⚡" },
  ];

  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center px-4 py-12">
      <div className="w-full max-w-3xl space-y-8">
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center gap-2 mb-4">
            <svg viewBox="0 0 24 24" className="h-8 w-8 text-primary" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/>
              <path d="M8 7h6M8 11h8"/>
            </svg>
            <span className="text-2xl font-bold"><span className="text-primary">S</span>AGE</span>
          </div>
          {step === "interests" ? (
            <>
              <h1 className="text-3xl font-bold">What do you want to learn?</h1>
              <p className="text-muted-foreground">Pick the topics that excite you. We&apos;ll personalize your learning path.</p>
              <p className="text-xs text-muted-foreground/60">Select at least one</p>
            </>
          ) : (
            <>
              <h1 className="text-3xl font-bold">What&apos;s your experience level?</h1>
              <p className="text-muted-foreground">This helps us set the right pace for your courses.</p>
            </>
          )}
        </div>

        {/* Progress dots */}
        <div className="flex items-center justify-center gap-2">
          <div className={`h-2 w-8 rounded-full transition-colors ${step === "interests" ? "bg-primary" : "bg-primary/40"}`} />
          <div className={`h-2 w-8 rounded-full transition-colors ${step === "level" ? "bg-primary" : "bg-muted"}`} />
        </div>

        {step === "interests" ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {INTEREST_TOPICS.map((topic) => {
              const isSelected = selected.has(topic.id);
              return (
                <button
                  key={topic.id}
                  onClick={() => toggleTopic(topic.id)}
                  className={`relative text-left p-4 rounded-xl border-2 transition-all duration-150 hover:scale-[1.02] active:scale-[0.98] ${
                    isSelected
                      ? "border-primary bg-primary/10 shadow-sm shadow-primary/20"
                      : "border-border bg-card hover:border-primary/40"
                  }`}
                >
                  {isSelected && (
                    <div className="absolute top-2 right-2 w-5 h-5 rounded-full bg-primary flex items-center justify-center">
                      <Check className="h-3 w-3 text-primary-foreground" />
                    </div>
                  )}
                  <div className="text-2xl mb-2">{topic.emoji}</div>
                  <p className="font-semibold text-sm text-foreground leading-snug">{topic.label}</p>
                  <p className="text-xs text-muted-foreground mt-1 leading-snug">{topic.desc}</p>
                </button>
              );
            })}
          </div>
        ) : (
          <div className="flex flex-col gap-3 max-w-md mx-auto w-full">
            {LEVELS.map((l) => (
              <button
                key={l.id}
                onClick={() => setLevel(l.id)}
                className={`text-left p-5 rounded-xl border-2 transition-all duration-150 hover:scale-[1.01] ${
                  level === l.id
                    ? "border-primary bg-primary/10 shadow-sm shadow-primary/20"
                    : "border-border bg-card hover:border-primary/40"
                }`}
              >
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{l.emoji}</span>
                  <div>
                    <p className="font-semibold text-foreground">{l.label}</p>
                    <p className="text-sm text-muted-foreground">{l.desc}</p>
                  </div>
                  {level === l.id && (
                    <div className="ml-auto w-5 h-5 rounded-full bg-primary flex items-center justify-center">
                      <Check className="h-3 w-3 text-primary-foreground" />
                    </div>
                  )}
                </div>
              </button>
            ))}
          </div>
        )}

        {/* Continue button */}
        <div className="flex justify-center">
          <Button
            size="lg"
            className="gap-2 px-10"
            onClick={handleContinue}
            disabled={step === "interests" ? selected.size === 0 : !level}
          >
            {step === "level" ? "Start Learning" : "Continue"}
            <ArrowRight className="h-4 w-4" />
          </Button>
        </div>

        {/* Skip */}
        <div className="text-center">
          <button
            onClick={() => {
              localStorage.setItem("sage_onboarded", "true");
              router.push("/learn");
            }}
            className="text-xs text-muted-foreground hover:text-foreground transition-colors"
          >
            Skip for now
          </button>
        </div>
      </div>
    </div>
  );
}
