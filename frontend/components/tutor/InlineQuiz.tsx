"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { CheckCircle2, XCircle, ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils";

interface QuizOption {
  id: string;
  text: string;
}

interface QuizData {
  question: string;
  options: QuizOption[];
  correct: string;
  explanation: string;
}

interface InlineQuizProps {
  data: QuizData;
  onSendMessage?: (msg: string) => void;
}

export function InlineQuiz({ data, onSendMessage }: InlineQuizProps) {
  const [selected, setSelected] = useState<string | null>(null);
  const [submitted, setSubmitted] = useState(false);
  const [continued, setContinued] = useState(false);

  const isCorrect = selected === data.correct;
  const selectedOption = data.options.find((o) => o.id === selected);

  function handleContinue() {
    if (!selectedOption || !onSendMessage) return;
    setContinued(true);
    onSendMessage(selectedOption.text);
  }

  return (
    <div className="my-3 rounded-lg border border-border bg-muted/30 p-4 space-y-3">
      <div className="flex items-center gap-2">
        <span className="text-xs font-semibold text-primary uppercase tracking-wider">Quick Check</span>
      </div>
      <p className="text-sm font-medium">{data.question}</p>
      <div className="space-y-2">
        {data.options.map((opt) => {
          const isSelected = selected === opt.id;
          const isRight = opt.id === data.correct;
          return (
            <button
              key={opt.id}
              onClick={() => !submitted && setSelected(opt.id)}
              disabled={submitted}
              className={cn(
                "w-full text-left text-sm rounded-md border px-3 py-2 transition-colors",
                !submitted && "hover:border-primary/50 hover:bg-accent",
                isSelected && !submitted && "border-primary bg-primary/10",
                submitted && isRight && "border-green-500 bg-green-500/10 text-green-700 dark:text-green-400",
                submitted && isSelected && !isRight && "border-red-500 bg-red-500/10 text-red-700 dark:text-red-400",
                submitted && !isSelected && !isRight && "opacity-50"
              )}
            >
              <span className="font-medium mr-2">{opt.id.toUpperCase()}.</span>
              {opt.text}
            </button>
          );
        })}
      </div>
      {!submitted && selected && (
        <Button size="sm" onClick={() => setSubmitted(true)}>
          Submit Answer
        </Button>
      )}
      {submitted && (
        <div className={cn(
          "flex items-start gap-2 text-sm rounded-md p-3",
          isCorrect ? "bg-green-500/10 text-green-700 dark:text-green-400" : "bg-red-500/10 text-red-700 dark:text-red-400"
        )}>
          {isCorrect ? (
            <CheckCircle2 className="h-4 w-4 mt-0.5 flex-shrink-0" />
          ) : (
            <XCircle className="h-4 w-4 mt-0.5 flex-shrink-0" />
          )}
          <div>
            <p className="font-medium">{isCorrect ? "Correct!" : "Not quite."}</p>
            <p className="text-xs mt-1 opacity-90">{data.explanation}</p>
          </div>
        </div>
      )}
      {submitted && onSendMessage && !continued && (
        <Button size="sm" variant="outline" className="gap-1.5" onClick={handleContinue}>
          Continue
          <ArrowRight className="h-3.5 w-3.5" />
        </Button>
      )}
    </div>
  );
}
