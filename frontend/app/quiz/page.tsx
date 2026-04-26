"use client";
import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";
import {
  api,
  QuizTopicResponse,
  QuizSessionResponse,
  QuizQuestionResponse,
  QuizSessionSummary,
  QuizAnswerResponse,
} from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import {
  Loader2,
  Trophy,
  RotateCcw,
  History,
  X,
  Trash2,
  CheckCircle2,
  XCircle,
  ArrowRight,
  Lightbulb,
} from "lucide-react";
import { AppHeader } from "@/components/AppHeader";

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

function QuestionDifficultyBadge({ difficulty }: { difficulty: string }) {
  const colorMap: Record<string, string> = {
    easy: "bg-green-500/20 text-green-400",
    medium: "bg-yellow-500/20 text-yellow-400",
    hard: "bg-orange-500/20 text-orange-400",
    expert: "bg-red-500/20 text-red-400",
  };
  return (
    <span className={cn("text-xs px-2 py-0.5 rounded-full font-medium", colorMap[difficulty] || colorMap.medium)}>
      {difficulty.charAt(0).toUpperCase() + difficulty.slice(1)}
    </span>
  );
}

type ViewState = "topics" | "quiz" | "results";

export default function QuizPage() {
  const router = useRouter();

  // Topic selection state
  const [topics, setTopics] = useState<QuizTopicResponse[]>([]);
  const [selectedTopic, setSelectedTopic] = useState<QuizTopicResponse | null>(null);
  const [difficulty, setDifficulty] = useState("intermediate");
  const [numQuestions, setNumQuestions] = useState<number>(5);
  const [topicsLoading, setTopicsLoading] = useState(true);

  // Quiz state
  const [view, setView] = useState<ViewState>("topics");
  const [quizSession, setQuizSession] = useState<QuizSessionResponse | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [generating, setGenerating] = useState(false);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [answerResult, setAnswerResult] = useState<QuizAnswerResponse | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [showHint, setShowHint] = useState(false);

  // Loading next question state
  const [loadingNext, setLoadingNext] = useState(false);

  // History state
  const [showHistory, setShowHistory] = useState(false);
  const [pastSessions, setPastSessions] = useState<QuizSessionSummary[]>([]);
  const [historyLoading, setHistoryLoading] = useState(false);

  useEffect(() => {
    const token = getToken();
    if (!token) { router.push("/login"); return; }

    async function loadTopics() {
      try {
        const t = await api.quiz.getTopics(token!);
        setTopics(t);
      } catch {
        // API unavailable — show empty state
      } finally {
        setTopicsLoading(false);
      }
    }
    loadTopics();
  }, [router]);

  async function handleGenerate() {
    if (!selectedTopic) return;
    const token = getToken();
    if (!token) return;

    setGenerating(true);
    try {
      const session = await api.quiz.generate(
        selectedTopic.lesson_id,
        difficulty,
        numQuestions,
        token
      );
      setQuizSession(session);
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

  const submittingRef = useRef(false);

  async function handleSubmitAnswer() {
    if (!quizSession || !selectedOption || submittingRef.current) return;
    const token = getToken();
    if (!token) return;

    submittingRef.current = true;
    const question = quizSession.questions[currentIndex];
    setSubmitting(true);
    try {
      const result = await api.quiz.submitAnswer(
        quizSession.id,
        question.id,
        selectedOption,
        token
      );
      setAnswerResult(result);
      setQuizSession((prev) =>
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
    if (!quizSession) return;
    const nextIdx = currentIndex + 1;

    if (nextIdx >= quizSession.total_questions) {
      setView("results");
      return;
    }

    if (nextIdx < quizSession.questions.length) {
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
        const updated = await api.quiz.getSession(quizSession.id, token);
        if (updated.questions.length > nextIdx) {
          setQuizSession(updated);
          setCurrentIndex(nextIdx);
          setSelectedOption(null);
          setAnswerResult(null);
          setShowHint(false);
          return;
        }
        retries++;
        await new Promise((r) => setTimeout(r, 1000));
      }
      console.error("Timed out waiting for next question");
    } catch (err) {
      console.error("Failed to fetch next question:", err);
    } finally {
      setLoadingNext(false);
    }
  }

  function handleRetake() {
    setView("topics");
    setQuizSession(null);
    setCurrentIndex(0);
    setSelectedOption(null);
    setAnswerResult(null);
    setShowHint(false);
  }

  async function handleShowHistory() {
    const token = getToken();
    if (!token) return;
    setShowHistory(true);
    setHistoryLoading(true);
    try {
      const s = await api.quiz.getSessions(token);
      setPastSessions(s);
    } catch {
      setPastSessions([]);
    } finally {
      setHistoryLoading(false);
    }
  }

  async function handleDeleteSession(sid: string) {
    const token = getToken();
    if (!token) return;
    try {
      await api.quiz.deleteSession(sid, token);
      setPastSessions((prev) => prev.filter((s) => s.id !== sid));
    } catch (err) {
      console.error("Failed to delete session:", err);
    }
  }

  async function handleLoadSession(sid: string) {
    const token = getToken();
    if (!token) return;
    try {
      const session = await api.quiz.getSession(sid, token);
      setQuizSession(session);
      setCurrentIndex(0);
      setSelectedOption(null);
      setAnswerResult(null);
      setShowHint(false);
      setView(session.completed ? "results" : "quiz");
      setShowHistory(false);
    } catch (err) {
      console.error("Failed to load session:", err);
    }
  }

  // Group topics by learning path
  const topicsByPath = topics.reduce<Record<string, QuizTopicResponse[]>>((acc, t) => {
    if (!acc[t.path_title]) acc[t.path_title] = [];
    acc[t.path_title].push(t);
    return acc;
  }, {});

  const currentQuestion: QuizQuestionResponse | null =
    quizSession?.questions[currentIndex] ?? null;

  return (
    <div className="flex flex-col h-screen bg-background">
      <AppHeader
        leftSlot={
          <>
            <Trophy className="h-5 w-5 text-primary" />
            <span className="font-semibold text-sm">Quiz</span>
            {view === "topics" && (
              <Button variant="ghost" size="sm" onClick={handleShowHistory} className="gap-1.5 text-muted-foreground hover:text-foreground ml-2">
                <History className="h-3.5 w-3.5" />
                <span className="hidden sm:inline">History</span>
              </Button>
            )}
          </>
        }
      />

      {/* History drawer */}
      {showHistory && (
        <div className="border-b border-border bg-card/80 backdrop-blur">
          <div className="max-w-3xl mx-auto px-6 py-4">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-medium">Past Quizzes</h3>
              <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => setShowHistory(false)}>
                <X className="h-3.5 w-3.5" />
              </Button>
            </div>
            {historyLoading ? (
              <div className="text-sm text-muted-foreground py-2">Loading...</div>
            ) : pastSessions.length === 0 ? (
              <div className="text-sm text-muted-foreground py-2">No past quizzes yet.</div>
            ) : (
              <div className="space-y-1 max-h-48 overflow-y-auto">
                {pastSessions.map((s) => (
                  <div key={s.id} className="flex items-center gap-2 group">
                    <button
                      onClick={() => handleLoadSession(s.id)}
                      className="flex-1 text-left text-sm px-3 py-2 rounded-lg hover:bg-accent transition-colors"
                    >
                      <span className="font-medium">{s.topic}</span>
                      <span className="text-muted-foreground ml-2 text-xs">
                        {s.correct_count}/{s.total_questions} correct
                      </span>
                      <DifficultyBadge difficulty={s.difficulty} />
                      <span className="text-muted-foreground ml-2 text-xs">
                        {new Date(s.created_at).toLocaleDateString()}
                      </span>
                    </button>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-7 w-7 opacity-0 group-hover:opacity-100 text-muted-foreground hover:text-destructive"
                      onClick={() => handleDeleteSession(s.id)}
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Main content */}
      <div className="flex-1 overflow-y-auto min-h-0">
        {view === "topics" && (
          <TopicSelection
            topicsByPath={topicsByPath}
            selectedTopic={selectedTopic}
            onSelectTopic={setSelectedTopic}
            difficulty={difficulty}
            onDifficultyChange={setDifficulty}
            numQuestions={numQuestions}
            onNumQuestionsChange={setNumQuestions}
            generating={generating}
            onGenerate={handleGenerate}
            loading={topicsLoading}
          />
        )}

        {view === "quiz" && quizSession && currentQuestion && (
          <QuizView
            session={quizSession}
            question={currentQuestion}
            currentIndex={currentIndex}
            selectedOption={selectedOption}
            onSelectOption={setSelectedOption}
            answerResult={answerResult}
            submitting={submitting}
            showHint={showHint}
            loadingNext={loadingNext}
            onToggleHint={() => setShowHint(!showHint)}
            onSubmit={handleSubmitAnswer}
            onNext={handleNext}
          />
        )}

        {view === "results" && quizSession && (
          <ResultsView session={quizSession} onRetake={handleRetake} />
        )}
      </div>
    </div>
  );
}


/* ── Topic Selection ──────────────────────────────────────────────────────── */

function TopicSelection({
  topicsByPath,
  selectedTopic,
  onSelectTopic,
  difficulty,
  onDifficultyChange,
  numQuestions,
  onNumQuestionsChange,
  generating,
  onGenerate,
  loading,
}: {
  topicsByPath: Record<string, QuizTopicResponse[]>;
  selectedTopic: QuizTopicResponse | null;
  onSelectTopic: (t: QuizTopicResponse) => void;
  difficulty: string;
  onDifficultyChange: (d: string) => void;
  numQuestions: number;
  onNumQuestionsChange: (n: number) => void;
  generating: boolean;
  onGenerate: () => void;
  loading: boolean;
}) {
  return (
    <div className="max-w-3xl mx-auto px-6 py-8">
      <div className="text-center mb-8">
        <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-4">
          <Trophy className="h-6 w-6 text-primary" />
        </div>
        <h1 className="text-2xl font-bold mb-2">Test Your Knowledge</h1>
        <p className="text-muted-foreground text-sm">
          Pick a topic, set the difficulty, and challenge yourself with AI-generated questions.
        </p>
      </div>

      {/* Configuration bar */}
      <div className="flex flex-wrap items-center justify-center gap-4 mb-8 p-4 rounded-xl border border-border bg-card/50">
        <div>
          <div className="text-xs text-muted-foreground mb-1.5 font-medium">Difficulty</div>
          <div className="flex gap-1.5">
            {DIFFICULTIES.map((d) => (
              <button
                key={d.id}
                onClick={() => onDifficultyChange(d.id)}
                className={cn(
                  "text-xs px-3 py-1.5 rounded-full font-medium border transition-all",
                  difficulty === d.id
                    ? d.color + " ring-1 ring-current ring-offset-1 ring-offset-background"
                    : "border-border text-muted-foreground hover:text-foreground hover:border-foreground/30"
                )}
              >
                {d.label}
              </button>
            ))}
          </div>
        </div>
        <div className="h-8 w-px bg-border hidden sm:block" />
        <div>
          <div className="text-xs text-muted-foreground mb-1.5 font-medium">Questions</div>
          <div className="flex gap-1.5">
            {QUESTION_COUNTS.map((n) => (
              <button
                key={n}
                onClick={() => onNumQuestionsChange(n)}
                className={cn(
                  "text-xs px-3 py-1.5 rounded-full font-medium border transition-all",
                  numQuestions === n
                    ? "bg-primary/20 text-primary border-primary/30"
                    : "border-border text-muted-foreground hover:text-foreground hover:border-foreground/30"
                )}
              >
                {n}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Topic list */}
      {loading ? (
        <div className="text-center text-sm text-muted-foreground py-12">
          <Loader2 className="h-5 w-5 animate-spin mx-auto mb-2" />
          Loading topics...
        </div>
      ) : Object.keys(topicsByPath).length === 0 ? (
        <div className="text-center text-sm text-muted-foreground py-12">
          No lessons available yet. Complete some lessons first.
        </div>
      ) : (
        <div className="space-y-6">
          {Object.entries(topicsByPath).map(([pathTitle, pathTopics]) => (
            <div key={pathTitle}>
              <h3 className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-3 px-1">
                {pathTitle}
              </h3>
              <div className="space-y-2">
                {pathTopics.map((topic) => (
                  <button
                    key={topic.lesson_id}
                    onClick={() => onSelectTopic(topic)}
                    className={cn(
                      "w-full text-left px-4 py-3 rounded-xl border transition-all",
                      selectedTopic?.lesson_id === topic.lesson_id
                        ? "border-primary bg-primary/5 ring-1 ring-primary/30"
                        : "border-border bg-card/50 hover:border-foreground/20 hover:bg-card"
                    )}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-medium text-sm">{topic.lesson_title}</span>
                      <DifficultyBadge difficulty={topic.level} />
                    </div>
                    <div className="text-xs text-muted-foreground">{topic.module_title}</div>
                    {topic.concepts.length > 0 && (
                      <div className="flex flex-wrap gap-1.5 mt-2">
                        {topic.concepts.slice(0, 5).map((c) => (
                          <span
                            key={c}
                            className="text-[10px] px-2 py-0.5 rounded-full bg-muted text-muted-foreground"
                          >
                            {c}
                          </span>
                        ))}
                        {topic.concepts.length > 5 && (
                          <span className="text-[10px] text-muted-foreground">
                            +{topic.concepts.length - 5} more
                          </span>
                        )}
                      </div>
                    )}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Start button */}
      {selectedTopic && (
        <div className="sticky bottom-0 py-4 mt-6 bg-gradient-to-t from-background via-background to-transparent">
          <Button
            onClick={onGenerate}
            disabled={generating}
            className="w-full h-12 text-base font-semibold rounded-xl"
          >
            {generating ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
                Generating Quiz...
              </>
            ) : (
              <>
                <Trophy className="h-4 w-4 mr-2" />
                Start Quiz — {selectedTopic.lesson_title}
              </>
            )}
          </Button>
        </div>
      )}
    </div>
  );
}


/* ── Quiz View ────────────────────────────────────────────────────────────── */

function QuizView({
  session,
  question,
  currentIndex,
  selectedOption,
  onSelectOption,
  answerResult,
  submitting,
  showHint,
  loadingNext,
  onToggleHint,
  onSubmit,
  onNext,
}: {
  session: QuizSessionResponse;
  question: QuizQuestionResponse;
  currentIndex: number;
  selectedOption: string | null;
  onSelectOption: (id: string) => void;
  answerResult: QuizAnswerResponse | null;
  submitting: boolean;
  showHint: boolean;
  loadingNext: boolean;
  onToggleHint: () => void;
  onSubmit: () => void;
  onNext: () => void;
}) {
  const progress = ((currentIndex + (answerResult ? 1 : 0)) / session.total_questions) * 100;
  const isLastQuestion = currentIndex + 1 >= session.total_questions;

  return (
    <div className="max-w-3xl mx-auto px-6 py-6">
      {/* Quiz header */}
      <div className="mb-6 p-4 rounded-xl border border-border bg-card/50">
        <div className="flex items-center justify-between mb-3">
          <div>
            <h2 className="font-semibold">{session.topic}</h2>
            <div className="flex items-center gap-2 mt-1">
              <DifficultyBadge difficulty={session.difficulty} />
              <span className="text-xs text-muted-foreground">
                Question {currentIndex + 1} of {session.total_questions}
              </span>
            </div>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-primary">
              {session.correct_count}/{session.total_questions}
            </div>
            <div className="text-xs text-muted-foreground">correct</div>
          </div>
        </div>
        {/* Progress bar */}
        <div className="h-2 bg-muted rounded-full overflow-hidden">
          <div
            className="h-full bg-primary rounded-full transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Question card */}
      <div className="rounded-xl border border-border bg-card p-6">
        <div className="flex items-center gap-2 mb-4">
          <Badge variant="outline" className="text-[11px]">Multiple Choice</Badge>
          <QuestionDifficultyBadge difficulty={question.difficulty} />
        </div>

        <h3 className="text-lg font-medium mb-6 leading-relaxed">{question.question_text}</h3>

        {/* Options */}
        <div className="space-y-3">
          {question.options.map((opt, idx) => {
            const letter = OPTION_LETTERS[idx] || String(idx + 1);
            const isSelected = selectedOption === opt.id;
            const isAnswered = answerResult !== null;
            const isCorrect = answerResult?.correct_option_id === opt.id;
            const isWrong = isAnswered && isSelected && !answerResult.is_correct;

            return (
              <button
                key={opt.id}
                onClick={() => !isAnswered && onSelectOption(opt.id)}
                disabled={isAnswered}
                className={cn(
                  "w-full flex items-center gap-3 px-4 py-3.5 rounded-xl border text-left transition-all",
                  isAnswered && isCorrect && "border-green-500 bg-green-500/10",
                  isAnswered && isWrong && "border-red-500 bg-red-500/10",
                  isAnswered && !isCorrect && !isWrong && "opacity-50",
                  !isAnswered && isSelected && "border-primary bg-primary/5 ring-1 ring-primary/30",
                  !isAnswered && !isSelected && "border-border hover:border-foreground/20 hover:bg-card",
                )}
              >
                <span
                  className={cn(
                    "flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center text-sm font-semibold border",
                    isAnswered && isCorrect && "bg-green-500 text-white border-green-500",
                    isAnswered && isWrong && "bg-red-500 text-white border-red-500",
                    !isAnswered && isSelected && "bg-primary text-primary-foreground border-primary",
                    !isAnswered && !isSelected && "bg-muted border-border text-muted-foreground",
                    isAnswered && !isCorrect && !isWrong && "bg-muted border-border text-muted-foreground",
                  )}
                >
                  {isAnswered && isCorrect ? (
                    <CheckCircle2 className="h-4 w-4" />
                  ) : isAnswered && isWrong ? (
                    <XCircle className="h-4 w-4" />
                  ) : (
                    letter
                  )}
                </span>
                <span className="text-sm">{opt.text}</span>
              </button>
            );
          })}
        </div>

        {/* Hint */}
        {!answerResult && question.hint && (
          <div className="mt-4">
            <button
              onClick={onToggleHint}
              className="flex items-center gap-1.5 text-xs text-primary hover:text-primary/80 transition-colors"
            >
              <Lightbulb className="h-3.5 w-3.5" />
              {showHint ? "Hide Hint" : "Show Hint"}
            </button>
            {showHint && (
              <div className="mt-2 px-4 py-3 rounded-lg bg-primary/5 border border-primary/20 text-sm text-primary">
                {question.hint}
              </div>
            )}
          </div>
        )}

        {/* Explanation (after answering) */}
        {answerResult && (
          <div
            className={cn(
              "mt-4 px-4 py-3 rounded-lg border text-sm",
              answerResult.is_correct
                ? "bg-green-500/5 border-green-500/20 text-green-300"
                : "bg-red-500/5 border-red-500/20 text-red-300"
            )}
          >
            <div className="font-medium mb-1 flex items-center gap-1.5">
              {answerResult.is_correct ? (
                <><CheckCircle2 className="h-4 w-4" /> Correct!</>
              ) : (
                <><XCircle className="h-4 w-4" /> Incorrect</>
              )}
            </div>
            <p className="text-foreground/80">{answerResult.explanation}</p>
          </div>
        )}

        {/* Action buttons */}
        <div className="mt-6 flex justify-end gap-3">
          {!answerResult ? (
            <Button
              onClick={onSubmit}
              disabled={!selectedOption || submitting}
              className="rounded-xl px-6"
            >
              {submitting ? (
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
              ) : null}
              Submit Answer
            </Button>
          ) : (
            <Button onClick={onNext} disabled={loadingNext} className="rounded-xl px-6">
              {loadingNext ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin mr-2" />
                  Preparing next question...
                </>
              ) : isLastQuestion ? (
                <>
                  View Results
                  <Trophy className="h-4 w-4 ml-2" />
                </>
              ) : (
                <>
                  Next Question
                  <ArrowRight className="h-4 w-4 ml-2" />
                </>
              )}
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}


/* ── Results View ─────────────────────────────────────────────────────────── */

function ResultsView({
  session,
  onRetake,
}: {
  session: QuizSessionResponse;
  onRetake: () => void;
}) {
  const pct = session.total_questions > 0
    ? Math.round((session.correct_count / session.total_questions) * 100)
    : 0;

  const grade =
    pct >= 90 ? { label: "Excellent", color: "text-green-400" }
    : pct >= 70 ? { label: "Good", color: "text-yellow-400" }
    : pct >= 50 ? { label: "Fair", color: "text-orange-400" }
    : { label: "Needs Practice", color: "text-red-400" };

  return (
    <div className="max-w-2xl mx-auto px-6 py-12 text-center">
      <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-6">
        <Trophy className="h-8 w-8 text-primary" />
      </div>

      <h2 className="text-2xl font-bold mb-2">Quiz Complete</h2>
      <p className="text-muted-foreground mb-8">{session.topic}</p>

      <div className="rounded-xl border border-border bg-card p-8 mb-8">
        <div className="text-6xl font-bold mb-2">
          <span className={grade.color}>{pct}%</span>
        </div>
        <div className={cn("text-lg font-medium mb-1", grade.color)}>{grade.label}</div>
        <div className="text-muted-foreground text-sm">
          {session.correct_count} out of {session.total_questions} questions correct
        </div>

        <div className="flex items-center justify-center gap-4 mt-6">
          <DifficultyBadge difficulty={session.difficulty} />
          <span className="text-xs text-muted-foreground">
            {new Date(session.created_at).toLocaleDateString()}
          </span>
        </div>

        {/* Score breakdown bar */}
        <div className="mt-6 h-3 bg-muted rounded-full overflow-hidden flex">
          <div
            className="h-full bg-green-500 transition-all"
            style={{ width: `${pct}%` }}
          />
          <div
            className="h-full bg-red-500/60 transition-all"
            style={{ width: `${100 - pct}%` }}
          />
        </div>
        <div className="flex justify-between text-xs text-muted-foreground mt-1">
          <span>{session.correct_count} correct</span>
          <span>{session.total_questions - session.correct_count} incorrect</span>
        </div>
      </div>

      <div className="flex justify-center gap-3">
        <Button variant="outline" onClick={onRetake} className="rounded-xl gap-2">
          <RotateCcw className="h-4 w-4" />
          New Quiz
        </Button>
      </div>
    </div>
  );
}
