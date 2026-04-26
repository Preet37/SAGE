"use client";
import { useState, useRef } from "react";
import { getToken } from "@/lib/auth";
import {
  api,
  QuizSessionResponse,
  QuizQuestionResponse,
  QuizAnswerResponse,
} from "@/lib/api";
import {
  Loader2,
  Trophy,
  RotateCcw,
  CheckCircle2,
  XCircle,
  ArrowRight,
  Lightbulb,
  Sparkles,
} from "lucide-react";

const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };
const serif: React.CSSProperties = { fontFamily: "var(--font-cormorant)" };
const body: React.CSSProperties = { fontFamily: "var(--font-crimson)" };

const DIFFICULTIES = [
  { id: "beginner",     label: "Beginner",     activeColor: "var(--sage-c)",  activeBg: "rgba(107,153,118,0.15)" },
  { id: "intermediate", label: "Intermediate", activeColor: "var(--gold)",    activeBg: "rgba(196,152,90,0.15)"  },
  { id: "advanced",     label: "Advanced",     activeColor: "#f97316",        activeBg: "rgba(249,115,22,0.12)"  },
  { id: "expert",       label: "Expert",       activeColor: "var(--rose)",    activeBg: "rgba(180,80,80,0.15)"   },
] as const;

const QUESTION_COUNTS = [5, 10, 15] as const;
const OPTION_LETTERS = ["A", "B", "C", "D"];

interface LessonQuizProps {
  lessonId: string;
  lessonTitle: string;
}

export function LessonQuiz({ lessonId, lessonTitle }: LessonQuizProps) {
  const [difficulty, setDifficulty] = useState("intermediate");
  const [numQuestions, setNumQuestions] = useState<number>(5);
  const [generating, setGenerating] = useState(false);
  const [session, setSession] = useState<QuizSessionResponse | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [answerResult, setAnswerResult] = useState<QuizAnswerResponse | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const [loadingNext, setLoadingNext] = useState(false);
  const [view, setView] = useState<"setup" | "quiz" | "results">("setup");
  const submittingRef = useRef(false);

  async function handleGenerate() {
    const token = getToken();
    if (!token) return;
    setGenerating(true);
    try {
      const s = await api.quiz.generate(lessonId, difficulty, numQuestions, token);
      setSession(s);
      setCurrentIndex(0);
      setSelectedOption(null);
      setAnswerResult(null);
      setShowHint(false);
      setView("quiz");
    } catch (err) {
      console.error("Quiz generation failed:", err);
    } finally {
      setGenerating(false);
    }
  }

  async function handleSubmitAnswer() {
    if (!session || !selectedOption || submittingRef.current) return;
    const token = getToken();
    if (!token) return;
    submittingRef.current = true;
    setSubmitting(true);
    try {
      const result = await api.quiz.submitAnswer(
        session.id,
        session.questions[currentIndex].id,
        selectedOption,
        token,
      );
      setAnswerResult(result);
      setSession((prev) =>
        prev ? { ...prev, correct_count: result.correct_count, completed: result.completed } : prev,
      );
    } catch (err) {
      console.error("Answer submission failed:", err);
    } finally {
      setSubmitting(false);
      submittingRef.current = false;
    }
  }

  async function handleNext() {
    if (!session) return;
    const nextIdx = currentIndex + 1;
    if (nextIdx >= session.total_questions) { setView("results"); return; }
    if (nextIdx < session.questions.length) {
      setCurrentIndex(nextIdx);
      setSelectedOption(null);
      setAnswerResult(null);
      setShowHint(false);
      return;
    }
    const token = getToken();
    if (!token) return;
    setLoadingNext(true);
    try {
      let retries = 0;
      while (retries < 30) {
        const updated = await api.quiz.getSession(session.id, token);
        if (updated.questions.length > nextIdx) {
          setSession(updated);
          setCurrentIndex(nextIdx);
          setSelectedOption(null);
          setAnswerResult(null);
          setShowHint(false);
          return;
        }
        retries++;
        await new Promise((r) => setTimeout(r, 1000));
      }
    } catch (err) {
      console.error("Failed to fetch next question:", err);
    } finally {
      setLoadingNext(false);
    }
  }

  function handleRetake() {
    setView("setup");
    setSession(null);
    setCurrentIndex(0);
    setSelectedOption(null);
    setAnswerResult(null);
    setShowHint(false);
  }

  if (view === "setup") {
    const activeDiff = DIFFICULTIES.find((d) => d.id === difficulty) ?? DIFFICULTIES[1];
    return (
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100%", padding: "0 1.5rem" }}>
        <div style={{ width: "100%", maxWidth: "28rem", display: "flex", flexDirection: "column", gap: "1.5rem" }}>
          {/* Header */}
          <div style={{ textAlign: "center" }}>
            <div style={{ width: "3rem", height: "3rem", background: "rgba(196,152,90,0.12)", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 0.75rem" }}>
              <Trophy style={{ width: "1.5rem", height: "1.5rem", color: "var(--gold)" }} />
            </div>
            <h2 style={{ ...serif, fontWeight: 700, fontStyle: "italic", fontSize: "1.5rem", color: "var(--cream-0)", marginBottom: "0.25rem" }}>
              Quiz Yourself
            </h2>
            <p style={{ ...mono, fontSize: "0.55rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)" }}>
              {lessonTitle}
            </p>
          </div>

          {/* Config card */}
          <div style={{ background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.08)", padding: "1.25rem" }}>
            <div style={{ marginBottom: "1rem" }}>
              <p style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)", marginBottom: "0.6rem" }}>
                Difficulty
              </p>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "0.4rem" }}>
                {DIFFICULTIES.map((d) => {
                  const isActive = difficulty === d.id;
                  return (
                    <button
                      key={d.id}
                      onClick={() => setDifficulty(d.id)}
                      style={{
                        ...mono,
                        fontSize: "0.5rem",
                        letterSpacing: "0.08em",
                        textTransform: "uppercase",
                        padding: "0.3rem 0.75rem",
                        background: isActive ? d.activeBg : "transparent",
                        color: isActive ? d.activeColor : "var(--cream-2)",
                        border: isActive ? `1px solid ${d.activeColor}` : "1px solid rgba(240,233,214,0.12)",
                        cursor: "pointer",
                        transition: "all 0.15s",
                      }}
                    >
                      {d.label}
                    </button>
                  );
                })}
              </div>
            </div>

            <div>
              <p style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)", marginBottom: "0.6rem" }}>
                Questions
              </p>
              <div style={{ display: "flex", gap: "0.4rem" }}>
                {QUESTION_COUNTS.map((n) => {
                  const isActive = numQuestions === n;
                  return (
                    <button
                      key={n}
                      onClick={() => setNumQuestions(n)}
                      style={{
                        ...mono,
                        fontSize: "0.5rem",
                        letterSpacing: "0.08em",
                        padding: "0.3rem 0.75rem",
                        background: isActive ? "rgba(196,152,90,0.15)" : "transparent",
                        color: isActive ? "var(--gold)" : "var(--cream-2)",
                        border: isActive ? "1px solid rgba(196,152,90,0.4)" : "1px solid rgba(240,233,214,0.12)",
                        cursor: "pointer",
                        transition: "all 0.15s",
                      }}
                    >
                      {n}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Start button */}
          <button
            onClick={handleGenerate}
            disabled={generating}
            style={{
              display: "flex", alignItems: "center", justifyContent: "center", gap: "0.5rem",
              width: "100%", padding: "0.75rem",
              background: generating ? "var(--ink-3)" : "var(--gold)",
              color: generating ? "var(--cream-2)" : "var(--ink)",
              border: "none", cursor: generating ? "default" : "pointer",
              ...mono, fontSize: "0.55rem", letterSpacing: "0.12em", textTransform: "uppercase",
              transition: "all 0.15s",
            }}
          >
            {generating ? (
              <><Loader2 style={{ width: "0.875rem", height: "0.875rem" }} className="animate-spin" /> Generating…</>
            ) : (
              <><Sparkles style={{ width: "0.875rem", height: "0.875rem" }} /> Start Quiz</>
            )}
          </button>
        </div>
      </div>
    );
  }

  if (view === "results" && session) {
    const pct = session.total_questions > 0
      ? Math.round((session.correct_count / session.total_questions) * 100)
      : 0;
    const grade =
      pct >= 90 ? { label: "Excellent",       color: "var(--sage-c)" }
      : pct >= 70 ? { label: "Good",           color: "var(--gold)"   }
      : pct >= 50 ? { label: "Fair",           color: "#f97316"       }
      : { label: "Needs Practice",             color: "var(--rose)"   };

    return (
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100%", padding: "0 1.5rem" }}>
        <div style={{ width: "100%", maxWidth: "24rem", textAlign: "center", display: "flex", flexDirection: "column", gap: "1.5rem" }}>
          <div style={{ width: "3.5rem", height: "3.5rem", background: "rgba(196,152,90,0.12)", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto" }}>
            <Trophy style={{ width: "1.75rem", height: "1.75rem", color: "var(--gold)" }} />
          </div>
          <div>
            <h2 style={{ ...serif, fontWeight: 700, fontStyle: "italic", fontSize: "1.5rem", color: "var(--cream-0)", marginBottom: "0.25rem" }}>
              Quiz Complete
            </h2>
            <p style={{ ...mono, fontSize: "0.55rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)" }}>
              {lessonTitle}
            </p>
          </div>
          <div style={{ background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.08)", padding: "1.5rem" }}>
            <div style={{ fontSize: "3rem", fontWeight: 700, marginBottom: "0.25rem", color: grade.color, fontFamily: "var(--font-cormorant)" }}>
              {pct}%
            </div>
            <div style={{ ...mono, fontSize: "0.55rem", letterSpacing: "0.1em", textTransform: "uppercase", color: grade.color, marginBottom: "0.5rem" }}>
              {grade.label}
            </div>
            <p style={{ ...mono, fontSize: "0.55rem", color: "var(--cream-2)" }}>
              {session.correct_count} / {session.total_questions} correct
            </p>
            <div style={{ marginTop: "1rem", height: "4px", background: "var(--ink-3)", overflow: "hidden", display: "flex" }}>
              <div style={{ height: "100%", background: "var(--sage-c)", width: `${pct}%` }} />
              <div style={{ height: "100%", background: "rgba(180,80,80,0.5)", width: `${100 - pct}%` }} />
            </div>
          </div>
          <button
            onClick={handleRetake}
            style={{
              display: "flex", alignItems: "center", justifyContent: "center", gap: "0.5rem",
              padding: "0.65rem 1.5rem", margin: "0 auto",
              background: "transparent", color: "var(--cream-1)",
              border: "1px solid rgba(240,233,214,0.15)", cursor: "pointer",
              ...mono, fontSize: "0.52rem", letterSpacing: "0.1em", textTransform: "uppercase",
            }}
          >
            <RotateCcw style={{ width: "0.75rem", height: "0.75rem" }} /> Try Again
          </button>
        </div>
      </div>
    );
  }

  const question = session?.questions[currentIndex];
  if (!session || !question) return null;

  const progress = ((currentIndex + (answerResult ? 1 : 0)) / session.total_questions) * 100;
  const isLastQuestion = currentIndex + 1 >= session.total_questions;
  const activeDiffObj = DIFFICULTIES.find((d) => d.id === session.difficulty) ?? DIFFICULTIES[1];

  return (
    <div style={{ height: "100%", overflowY: "auto" }} className="thin-scrollbar">
      <div style={{ maxWidth: "40rem", margin: "0 auto", padding: "1.25rem 1rem" }}>
        {/* Progress header */}
        <div style={{ background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.08)", padding: "0.75rem 1rem", marginBottom: "1rem" }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "0.5rem" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "0.6rem" }}>
              <span style={{ ...mono, fontSize: "0.48rem", letterSpacing: "0.08em", textTransform: "uppercase", color: activeDiffObj.activeColor, border: `1px solid ${activeDiffObj.activeColor}`, padding: "0.1rem 0.4rem" }}>
                {session.difficulty}
              </span>
              <span style={{ ...mono, fontSize: "0.5rem", color: "var(--cream-2)" }}>
                Question {currentIndex + 1} / {session.total_questions}
              </span>
            </div>
            <span style={{ ...mono, fontSize: "0.58rem", color: "var(--gold)", fontWeight: 600 }}>
              {session.correct_count}/{session.total_questions}
            </span>
          </div>
          <div style={{ height: "3px", background: "var(--ink-3)", overflow: "hidden" }}>
            <div style={{ height: "100%", background: "var(--gold)", width: `${progress}%`, transition: "width 0.5s" }} />
          </div>
        </div>

        {/* Question card */}
        <div style={{ background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.08)", padding: "1.25rem" }}>
          <h3 style={{ ...body, fontSize: "1rem", color: "var(--cream-0)", lineHeight: 1.6, marginBottom: "1.25rem" }}>
            {question.question_text}
          </h3>

          <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
            {question.options.map((opt, idx) => {
              const letter = OPTION_LETTERS[idx] || String(idx + 1);
              const isSelected = selectedOption === opt.id;
              const isAnswered = answerResult !== null;
              const isCorrect = answerResult?.correct_option_id === opt.id;
              const isWrong = isAnswered && isSelected && !answerResult.is_correct;

              let borderColor = "rgba(240,233,214,0.1)";
              let bgColor = "transparent";
              let letterBg = "var(--ink-2)";
              let letterColor = "var(--cream-2)";
              let opacity = 1;

              if (isAnswered && isCorrect) {
                borderColor = "rgba(107,153,118,0.6)";
                bgColor = "rgba(107,153,118,0.08)";
                letterBg = "var(--sage-c)";
                letterColor = "var(--ink)";
              } else if (isAnswered && isWrong) {
                borderColor = "rgba(180,80,80,0.6)";
                bgColor = "rgba(180,80,80,0.08)";
                letterBg = "var(--rose)";
                letterColor = "white";
              } else if (isAnswered) {
                opacity = 0.4;
              } else if (isSelected) {
                borderColor = "rgba(196,152,90,0.5)";
                bgColor = "rgba(196,152,90,0.06)";
                letterBg = "var(--gold)";
                letterColor = "var(--ink)";
              }

              return (
                <button
                  key={opt.id}
                  onClick={() => !isAnswered && setSelectedOption(opt.id)}
                  disabled={isAnswered}
                  style={{
                    display: "flex", alignItems: "center", gap: "0.75rem",
                    padding: "0.75rem 1rem", textAlign: "left",
                    background: bgColor, border: `1px solid ${borderColor}`,
                    cursor: isAnswered ? "default" : "pointer", opacity,
                    transition: "all 0.15s", width: "100%",
                  }}
                >
                  <span style={{
                    flexShrink: 0, width: "1.75rem", height: "1.75rem",
                    display: "flex", alignItems: "center", justifyContent: "center",
                    ...mono, fontSize: "0.55rem", fontWeight: 600,
                    background: letterBg, color: letterColor,
                    border: "none",
                  }}>
                    {isAnswered && isCorrect ? <CheckCircle2 style={{ width: "0.875rem", height: "0.875rem" }} /> :
                     isAnswered && isWrong   ? <XCircle      style={{ width: "0.875rem", height: "0.875rem" }} /> :
                     letter}
                  </span>
                  <span style={{ ...body, fontSize: "0.95rem", color: "var(--cream-1)", lineHeight: 1.4 }}>
                    {opt.text}
                  </span>
                </button>
              );
            })}
          </div>

          {!answerResult && question.hint && (
            <div style={{ marginTop: "0.75rem" }}>
              <button
                onClick={() => setShowHint(!showHint)}
                style={{ display: "flex", alignItems: "center", gap: "0.35rem", background: "none", border: "none", cursor: "pointer", color: "var(--gold)", ...mono, fontSize: "0.5rem", letterSpacing: "0.08em" }}
              >
                <Lightbulb style={{ width: "0.75rem", height: "0.75rem" }} />
                {showHint ? "Hide Hint" : "Show Hint"}
              </button>
              {showHint && (
                <div style={{ marginTop: "0.5rem", padding: "0.6rem 0.75rem", background: "rgba(196,152,90,0.06)", border: "1px solid rgba(196,152,90,0.2)", ...body, fontSize: "0.9rem", color: "var(--gold)", lineHeight: 1.5 }}>
                  {question.hint}
                </div>
              )}
            </div>
          )}

          {answerResult && (
            <div style={{
              marginTop: "0.75rem", padding: "0.75rem 1rem",
              background: answerResult.is_correct ? "rgba(107,153,118,0.06)" : "rgba(180,80,80,0.06)",
              border: answerResult.is_correct ? "1px solid rgba(107,153,118,0.25)" : "1px solid rgba(180,80,80,0.25)",
            }}>
              <div style={{ display: "flex", alignItems: "center", gap: "0.4rem", marginBottom: "0.4rem", ...mono, fontSize: "0.52rem", letterSpacing: "0.08em", textTransform: "uppercase", color: answerResult.is_correct ? "var(--sage-c)" : "var(--rose)", fontWeight: 600 }}>
                {answerResult.is_correct
                  ? <><CheckCircle2 style={{ width: "0.875rem", height: "0.875rem" }} /> Correct!</>
                  : <><XCircle      style={{ width: "0.875rem", height: "0.875rem" }} /> Incorrect</>}
              </div>
              <p style={{ ...body, fontSize: "0.9rem", color: "var(--cream-2)", lineHeight: 1.5 }}>
                {answerResult.explanation}
              </p>
            </div>
          )}

          <div style={{ marginTop: "1rem", display: "flex", justifyContent: "flex-end" }}>
            {!answerResult ? (
              <button
                onClick={handleSubmitAnswer}
                disabled={!selectedOption || submitting}
                style={{
                  display: "flex", alignItems: "center", gap: "0.4rem",
                  padding: "0.55rem 1.25rem",
                  background: (!selectedOption || submitting) ? "var(--ink-3)" : "var(--gold)",
                  color: (!selectedOption || submitting) ? "var(--cream-2)" : "var(--ink)",
                  border: "none", cursor: (!selectedOption || submitting) ? "default" : "pointer",
                  ...mono, fontSize: "0.52rem", letterSpacing: "0.1em", textTransform: "uppercase",
                  transition: "all 0.15s",
                }}
              >
                {submitting && <Loader2 style={{ width: "0.75rem", height: "0.75rem" }} className="animate-spin" />}
                Submit
              </button>
            ) : (
              <button
                onClick={handleNext}
                disabled={loadingNext}
                style={{
                  display: "flex", alignItems: "center", gap: "0.4rem",
                  padding: "0.55rem 1.25rem",
                  background: loadingNext ? "var(--ink-3)" : "var(--gold)",
                  color: loadingNext ? "var(--cream-2)" : "var(--ink)",
                  border: "none", cursor: loadingNext ? "default" : "pointer",
                  ...mono, fontSize: "0.52rem", letterSpacing: "0.1em", textTransform: "uppercase",
                  transition: "all 0.15s",
                }}
              >
                {loadingNext ? (
                  <><Loader2 style={{ width: "0.75rem", height: "0.75rem" }} className="animate-spin" /> Loading…</>
                ) : isLastQuestion ? (
                  <><Trophy style={{ width: "0.75rem", height: "0.75rem" }} /> View Results</>
                ) : (
                  <>Next <ArrowRight style={{ width: "0.75rem", height: "0.75rem" }} /></>
                )}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
