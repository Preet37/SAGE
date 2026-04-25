"use client";
import { useState, useRef } from "react";
import { getToken } from "@/lib/auth";
import {
  api,
  QuizSessionResponse,
  QuizQuestionResponse,
  QuizAnswerResponse,
} from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
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

const DIFFICULTIES = [
  { id: "beginner", label: "Beginner", color: "bg-green-500/20 text-green-400 border-green-500/30" },
  { id: "intermediate", label: "Intermediate", color: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30" },
  { id: "advanced", label: "Advanced", color: "bg-orange-500/20 text-orange-400 border-orange-500/30" },
  { id: "expert", label: "Expert", color: "bg-red-500/20 text-red-400 border-red-500/30" },
] as const;

const QUESTION_COUNTS = [5, 10, 15] as const;
const OPTION_LETTERS = ["A", "B", "C", "D"];

function DifficultyBadge({ difficulty }: { difficulty: string }) {
  const d = DIFFICULTIES.find((x) => x.id === difficulty) ?? DIFFICULTIES[1];
  return (
    <span className={cn("text-xs px-2.5 py-0.5 rounded-full font-medium border", d.color)}>
      {d.label}
    </span>
  );
}

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
        token
      );
      setAnswerResult(result);
      setSession((prev) =>
        prev ? { ...prev, correct_count: result.correct_count, completed: result.completed } : prev
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
    if (nextIdx >= session.total_questions) {
      setView("results");
      return;
    }
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
    return (
      <div className="flex flex-col items-center justify-center h-full px-6">
        <div className="w-full max-w-md space-y-6">
          <div className="text-center">
            <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-3">
              <Trophy className="h-6 w-6 text-primary" />
            </div>
            <h2 className="text-lg font-bold mb-1">Quiz Yourself</h2>
            <p className="text-sm text-muted-foreground">{lessonTitle}</p>
          </div>

          <div className="space-y-4 p-5 rounded-xl border border-border bg-card/50">
            <div>
              <p className="text-xs text-muted-foreground font-medium mb-2">Difficulty</p>
              <div className="flex flex-wrap gap-1.5">
                {DIFFICULTIES.map((d) => (
                  <button
                    key={d.id}
                    onClick={() => setDifficulty(d.id)}
                    className={cn(
                      "text-xs px-3 py-1.5 rounded-full font-medium border transition-all",
                      difficulty === d.id
                        ? d.color + " ring-1 ring-current ring-offset-1 ring-offset-background"
                        : "border-border text-muted-foreground hover:text-foreground"
                    )}
                  >
                    {d.label}
                  </button>
                ))}
              </div>
            </div>
            <div>
              <p className="text-xs text-muted-foreground font-medium mb-2">Questions</p>
              <div className="flex gap-1.5">
                {QUESTION_COUNTS.map((n) => (
                  <button
                    key={n}
                    onClick={() => setNumQuestions(n)}
                    className={cn(
                      "text-xs px-3 py-1.5 rounded-full font-medium border transition-all",
                      numQuestions === n
                        ? "bg-primary/20 text-primary border-primary/30"
                        : "border-border text-muted-foreground hover:text-foreground"
                    )}
                  >
                    {n}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <Button onClick={handleGenerate} disabled={generating} className="w-full rounded-xl h-11 gap-2">
            {generating ? (
              <><Loader2 className="h-4 w-4 animate-spin" /> Generating...</>
            ) : (
              <><Sparkles className="h-4 w-4" /> Start Quiz</>
            )}
          </Button>
        </div>
      </div>
    );
  }

  if (view === "results" && session) {
    const pct = session.total_questions > 0
      ? Math.round((session.correct_count / session.total_questions) * 100)
      : 0;
    const grade =
      pct >= 90 ? { label: "Excellent", color: "text-green-400" }
      : pct >= 70 ? { label: "Good", color: "text-yellow-400" }
      : pct >= 50 ? { label: "Fair", color: "text-orange-400" }
      : { label: "Needs Practice", color: "text-red-400" };

    return (
      <div className="flex flex-col items-center justify-center h-full px-6">
        <div className="w-full max-w-sm text-center space-y-6">
          <div className="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto">
            <Trophy className="h-7 w-7 text-primary" />
          </div>
          <div>
            <h2 className="text-xl font-bold mb-1">Quiz Complete</h2>
            <p className="text-sm text-muted-foreground">{lessonTitle}</p>
          </div>
          <div className="rounded-xl border border-border bg-card p-6">
            <div className="text-5xl font-bold mb-1">
              <span className={grade.color}>{pct}%</span>
            </div>
            <div className={cn("font-medium mb-1", grade.color)}>{grade.label}</div>
            <p className="text-sm text-muted-foreground">
              {session.correct_count} / {session.total_questions} correct
            </p>
            <div className="mt-4 h-2.5 bg-muted rounded-full overflow-hidden flex">
              <div className="h-full bg-green-500" style={{ width: `${pct}%` }} />
              <div className="h-full bg-red-500/60" style={{ width: `${100 - pct}%` }} />
            </div>
          </div>
          <Button variant="outline" onClick={handleRetake} className="rounded-xl gap-2">
            <RotateCcw className="h-4 w-4" /> Try Again
          </Button>
        </div>
      </div>
    );
  }

  const question = session?.questions[currentIndex];
  if (!session || !question) return null;

  const progress = ((currentIndex + (answerResult ? 1 : 0)) / session.total_questions) * 100;
  const isLastQuestion = currentIndex + 1 >= session.total_questions;

  return (
    <div className="flex flex-col h-full overflow-y-auto">
      <div className="max-w-2xl mx-auto w-full px-4 py-5 space-y-4">
        {/* Progress header */}
        <div className="p-3 rounded-xl border border-border bg-card/50">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <DifficultyBadge difficulty={session.difficulty} />
              <span className="text-xs text-muted-foreground">
                Question {currentIndex + 1} / {session.total_questions}
              </span>
            </div>
            <span className="text-sm font-bold text-primary">
              {session.correct_count}/{session.total_questions}
            </span>
          </div>
          <div className="h-1.5 bg-muted rounded-full overflow-hidden">
            <div className="h-full bg-primary rounded-full transition-all duration-500" style={{ width: `${progress}%` }} />
          </div>
        </div>

        {/* Question */}
        <div className="rounded-xl border border-border bg-card p-5">
          <h3 className="font-medium mb-5 leading-relaxed">{question.question_text}</h3>

          <div className="space-y-2.5">
            {question.options.map((opt, idx) => {
              const letter = OPTION_LETTERS[idx] || String(idx + 1);
              const isSelected = selectedOption === opt.id;
              const isAnswered = answerResult !== null;
              const isCorrect = answerResult?.correct_option_id === opt.id;
              const isWrong = isAnswered && isSelected && !answerResult.is_correct;

              return (
                <button
                  key={opt.id}
                  onClick={() => !isAnswered && setSelectedOption(opt.id)}
                  disabled={isAnswered}
                  className={cn(
                    "w-full flex items-center gap-3 px-4 py-3 rounded-xl border text-left text-sm transition-all",
                    isAnswered && isCorrect && "border-green-500 bg-green-500/10",
                    isAnswered && isWrong && "border-red-500 bg-red-500/10",
                    isAnswered && !isCorrect && !isWrong && "opacity-50",
                    !isAnswered && isSelected && "border-primary bg-primary/5 ring-1 ring-primary/30",
                    !isAnswered && !isSelected && "border-border hover:border-foreground/20",
                  )}
                >
                  <span
                    className={cn(
                      "flex-shrink-0 w-7 h-7 rounded-lg flex items-center justify-center text-xs font-semibold border",
                      isAnswered && isCorrect && "bg-green-500 text-white border-green-500",
                      isAnswered && isWrong && "bg-red-500 text-white border-red-500",
                      !isAnswered && isSelected && "bg-primary text-primary-foreground border-primary",
                      !isAnswered && !isSelected && "bg-muted border-border text-muted-foreground",
                      isAnswered && !isCorrect && !isWrong && "bg-muted border-border text-muted-foreground",
                    )}
                  >
                    {isAnswered && isCorrect ? <CheckCircle2 className="h-3.5 w-3.5" /> :
                     isAnswered && isWrong ? <XCircle className="h-3.5 w-3.5" /> : letter}
                  </span>
                  <span>{opt.text}</span>
                </button>
              );
            })}
          </div>

          {!answerResult && question.hint && (
            <div className="mt-3">
              <button
                onClick={() => setShowHint(!showHint)}
                className="flex items-center gap-1.5 text-xs text-primary hover:text-primary/80 transition-colors"
              >
                <Lightbulb className="h-3.5 w-3.5" />
                {showHint ? "Hide Hint" : "Show Hint"}
              </button>
              {showHint && (
                <div className="mt-2 px-3 py-2 rounded-lg bg-primary/5 border border-primary/20 text-sm text-primary">
                  {question.hint}
                </div>
              )}
            </div>
          )}

          {answerResult && (
            <div className={cn(
              "mt-3 px-3 py-2.5 rounded-lg border text-sm",
              answerResult.is_correct
                ? "bg-green-500/5 border-green-500/20"
                : "bg-red-500/5 border-red-500/20"
            )}>
              <div className="font-medium mb-1 flex items-center gap-1.5">
                {answerResult.is_correct ? (
                  <><CheckCircle2 className="h-4 w-4 text-green-400" /> Correct!</>
                ) : (
                  <><XCircle className="h-4 w-4 text-red-400" /> Incorrect</>
                )}
              </div>
              <p className="text-muted-foreground">{answerResult.explanation}</p>
            </div>
          )}

          <div className="mt-4 flex justify-end">
            {!answerResult ? (
              <Button onClick={handleSubmitAnswer} disabled={!selectedOption || submitting} className="rounded-xl px-5">
                {submitting && <Loader2 className="h-4 w-4 animate-spin mr-2" />}
                Submit
              </Button>
            ) : (
              <Button onClick={handleNext} disabled={loadingNext} className="rounded-xl px-5 gap-1.5">
                {loadingNext ? (
                  <><Loader2 className="h-4 w-4 animate-spin" /> Loading...</>
                ) : isLastQuestion ? (
                  <><Trophy className="h-4 w-4" /> View Results</>
                ) : (
                  <>Next <ArrowRight className="h-4 w-4" /></>
                )}
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
