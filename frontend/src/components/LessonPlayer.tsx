"use client";

import { useEffect, useMemo, useState } from "react";

import { API_BASE } from "@/lib/api";

export interface LessonStep { title: string; content: string; }
export interface QuizQuestion {
  question: string;
  options: string[];
  correct_index: number;
  explanation: string;
}
export interface Lesson {
  topic: string;
  summary: string;
  steps: LessonStep[];
  quiz: QuizQuestion[];
}

interface LessonPlayerProps {
  topic: string;
  onComplete: (topic: string) => void;
  onClose: () => void;
}

export default function LessonPlayer({ topic, onComplete, onClose }: LessonPlayerProps) {
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [stepIdx, setStepIdx] = useState(0);
  const [phase, setPhase] = useState<"steps" | "quiz" | "review">("steps");
  const [answers, setAnswers] = useState<number[]>([]);

  useEffect(() => {
    let alive = true;
    setLesson(null);
    setError(null);
    setStepIdx(0);
    setPhase("steps");
    setAnswers([]);
    (async () => {
      try {
        const res = await fetch(`${API_BASE}/lesson/generate`, {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ topic }),
        });
        if (!res.ok) throw new Error(`lesson failed (${res.status})`);
        const data = (await res.json()) as Lesson;
        if (!alive) return;
        setLesson(data);
      } catch (e) {
        if (!alive) return;
        setError(e instanceof Error ? e.message : "lesson failed");
      }
    })();
    return () => { alive = false; };
  }, [topic]);

  const score = useMemo(() => {
    if (!lesson || answers.length !== lesson.quiz.length) return 0;
    return lesson.quiz.reduce((s, q, i) => s + (q.correct_index === answers[i] ? 1 : 0), 0);
  }, [lesson, answers]);

  if (error) {
    return (
      <div className="card flex h-full flex-col items-center justify-center gap-3 p-6 text-center">
        <p style={{ color: "var(--color-destructive)" }}>{error}</p>
        <button onClick={onClose} className="btn-ghost">Back to chat</button>
      </div>
    );
  }
  if (!lesson) {
    return (
      <div className="card flex h-full flex-col items-center justify-center gap-3 p-6 text-center">
        <div className="pulse-dot" />
        <p className="text-sm" style={{ opacity: 0.7 }}>
          Designing your lesson on <strong>{topic}</strong>…
        </p>
      </div>
    );
  }

  const totalSteps = lesson.steps.length;
  const progressPct =
    phase === "steps"
      ? (stepIdx / (totalSteps + lesson.quiz.length)) * 100
      : phase === "quiz"
      ? ((totalSteps + answers.length) / (totalSteps + lesson.quiz.length)) * 100
      : 100;

  return (
    <div className="card flex h-full flex-col p-5">
      <header className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="text-xs uppercase tracking-wider" style={{ opacity: 0.55 }}>Lesson</p>
          <h2 className="truncate text-xl" style={{ fontFamily: "var(--font-heading)" }}>
            {lesson.topic}
          </h2>
          <p className="mt-0.5 truncate text-sm" style={{ opacity: 0.7 }}>{lesson.summary}</p>
        </div>
        <button onClick={onClose} aria-label="Close lesson"
          className="rounded-full px-3 py-1 text-xs font-semibold"
          style={{ background: "rgba(0,0,0,0.05)", border: "1px solid var(--glass-border)" }}>
          Close
        </button>
      </header>

      <div className="mt-3 h-1.5 w-full overflow-hidden rounded-full"
        style={{ background: "rgba(108,92,231,0.12)" }}>
        <div className="h-full transition-all"
          style={{ width: `${progressPct}%`, background: "linear-gradient(90deg, var(--color-ring), var(--color-secondary))" }} />
      </div>

      <div className="mt-5 flex-1 overflow-y-auto pr-1">
        {phase === "steps" && (
          <StepView
            step={lesson.steps[stepIdx]}
            index={stepIdx}
            total={totalSteps}
          />
        )}
        {phase === "quiz" && (
          <QuizView
            quiz={lesson.quiz}
            answers={answers}
            setAnswers={setAnswers}
          />
        )}
        {phase === "review" && (
          <ReviewView lesson={lesson} answers={answers} score={score} />
        )}
      </div>

      <footer className="mt-4 flex items-center justify-between gap-3">
        {phase === "steps" && (
          <>
            <button
              onClick={() => setStepIdx((i) => Math.max(0, i - 1))}
              disabled={stepIdx === 0}
              className="btn-ghost disabled:opacity-40"
            >
              Back
            </button>
            <span className="text-xs" style={{ opacity: 0.6 }}>
              Step {stepIdx + 1} of {totalSteps}
            </span>
            {stepIdx < totalSteps - 1 ? (
              <button onClick={() => setStepIdx((i) => i + 1)} className="btn-primary">Next</button>
            ) : (
              <button onClick={() => setPhase("quiz")} className="btn-primary">Start quiz</button>
            )}
          </>
        )}
        {phase === "quiz" && (
          <>
            <span className="text-xs" style={{ opacity: 0.6 }}>
              {answers.length}/{lesson.quiz.length} answered
            </span>
            <button
              onClick={() => setPhase("review")}
              disabled={answers.length !== lesson.quiz.length}
              className="btn-primary disabled:opacity-40"
            >
              Review answers
            </button>
          </>
        )}
        {phase === "review" && (
          <>
            <span className="text-xs" style={{ opacity: 0.6 }}>
              Score {score}/{lesson.quiz.length}
            </span>
            <div className="flex gap-2">
              <button onClick={() => { setAnswers([]); setPhase("quiz"); }} className="btn-ghost">
                Retry quiz
              </button>
              <button
                onClick={() => onComplete(lesson.topic)}
                className="btn-primary"
                style={{
                  background: "linear-gradient(135deg, var(--color-secondary), #F59E0B)",
                  boxShadow: "0 8px 24px rgba(245,158,11,0.4)",
                }}
              >
                ✓ Mark complete
              </button>
            </div>
          </>
        )}
      </footer>
    </div>
  );
}

function StepView({ step, index, total }: { step: LessonStep; index: number; total: number }) {
  return (
    <article className="space-y-3">
      <p className="text-xs font-semibold uppercase tracking-wider"
        style={{ color: "var(--color-ring)" }}>
        Step {index + 1} / {total}
      </p>
      <h3 className="text-2xl" style={{ fontFamily: "var(--font-heading)", fontWeight: 600 }}>
        {step.title}
      </h3>
      <p className="text-base leading-relaxed" style={{ opacity: 0.85 }}>{step.content}</p>
    </article>
  );
}

function QuizView({
  quiz, answers, setAnswers,
}: {
  quiz: QuizQuestion[];
  answers: number[];
  setAnswers: (a: number[]) => void;
}) {
  return (
    <div className="space-y-5">
      {quiz.map((q, qi) => (
        <div key={qi} className="rounded-2xl p-4"
          style={{ background: "rgba(255,255,255,0.55)", border: "1px solid var(--glass-border)" }}>
          <p className="text-sm font-semibold" style={{ opacity: 0.55 }}>Question {qi + 1}</p>
          <p className="mt-1 text-base" style={{ fontWeight: 600 }}>{q.question}</p>
          <ul className="mt-3 space-y-1.5">
            {q.options.map((opt, oi) => {
              const selected = answers[qi] === oi;
              return (
                <li key={oi}>
                  <button
                    onClick={() => {
                      const next = [...answers];
                      next[qi] = oi;
                      setAnswers(next);
                    }}
                    className="w-full rounded-xl px-3 py-2 text-left text-sm transition-colors"
                    style={{
                      background: selected ? "rgba(108,92,231,0.15)" : "rgba(255,255,255,0.6)",
                      border: `1px solid ${selected ? "var(--color-ring)" : "var(--glass-border)"}`,
                      cursor: "pointer",
                    }}
                  >
                    <span className="mr-2 font-semibold" style={{ color: "var(--color-ring)" }}>
                      {String.fromCharCode(65 + oi)}.
                    </span>
                    {opt}
                  </button>
                </li>
              );
            })}
          </ul>
        </div>
      ))}
    </div>
  );
}

function ReviewView({ lesson, answers, score }: { lesson: Lesson; answers: number[]; score: number }) {
  return (
    <div className="space-y-4">
      <div className="rounded-2xl p-4 text-center"
        style={{
          background: score === lesson.quiz.length
            ? "linear-gradient(135deg, rgba(245,158,11,0.18), rgba(108,92,231,0.18))"
            : "rgba(255,255,255,0.55)",
          border: "1px solid var(--glass-border)",
        }}>
        <p className="text-3xl" style={{ fontFamily: "var(--font-heading)", fontWeight: 700 }}>
          {score}/{lesson.quiz.length}
        </p>
        <p className="text-sm" style={{ opacity: 0.7 }}>
          {score === lesson.quiz.length ? "Perfect — ready to add to your knowledge graph." : "Review and try again, or mark complete to add anyway."}
        </p>
      </div>
      {lesson.quiz.map((q, qi) => {
        const correct = q.correct_index === answers[qi];
        return (
          <div key={qi} className="rounded-2xl p-4"
            style={{
              background: correct ? "rgba(16,185,129,0.08)" : "rgba(244,63,94,0.08)",
              border: `1px solid ${correct ? "rgba(16,185,129,0.4)" : "rgba(244,63,94,0.4)"}`,
            }}>
            <p className="text-sm font-semibold">{q.question}</p>
            <p className="mt-1 text-sm" style={{ opacity: 0.8 }}>
              <span style={{ color: correct ? "#059669" : "#E11D48", fontWeight: 600 }}>
                {correct ? "✓ Correct" : "✗ Incorrect"}
              </span>
              {" — "}Answer: <strong>{q.options[q.correct_index]}</strong>
            </p>
            <p className="mt-1 text-xs" style={{ opacity: 0.65 }}>{q.explanation}</p>
          </div>
        );
      })}
    </div>
  );
}
