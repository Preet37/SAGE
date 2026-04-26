"use client";
import { useState } from "react";
import { CheckCircle2, XCircle, ArrowRight } from "lucide-react";

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

const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };
const body: React.CSSProperties = { fontFamily: "var(--font-crimson)" };

export function InlineQuiz({ data, onSendMessage }: InlineQuizProps) {
  const [selected, setSelected] = useState<string | null>(null);
  const [submitted, setSubmitted] = useState(false);
  const [continued, setContinued] = useState(false);
  const [hovered, setHovered] = useState<string | null>(null);

  const isCorrect = selected === data.correct;
  const selectedOption = data.options.find((o) => o.id === selected);

  function handleContinue() {
    if (!selectedOption || !onSendMessage) return;
    setContinued(true);
    onSendMessage(selectedOption.text);
  }

  return (
    <div style={{
      margin: "0.75rem 0",
      borderRadius: "6px",
      border: "1px solid rgba(240,233,214,0.12)",
      background: "rgba(30,26,20,0.6)",
      padding: "1rem",
    }}>
      {/* Header */}
      <div style={{ marginBottom: "0.6rem" }}>
        <span style={{ ...mono, fontSize: "0.52rem", letterSpacing: "0.14em", textTransform: "uppercase", color: "var(--gold)" }}>
          Quick Check
        </span>
      </div>

      {/* Question */}
      <p style={{ ...body, fontSize: "0.95rem", color: "var(--cream-0)", marginBottom: "0.75rem", lineHeight: 1.5 }}>
        {data.question}
      </p>

      {/* Options */}
      <div style={{ display: "flex", flexDirection: "column", gap: "0.4rem", marginBottom: "0.75rem" }}>
        {data.options.map((opt) => {
          const isSelected = selected === opt.id;
          const isRight = opt.id === data.correct;
          const isHovered = hovered === opt.id && !submitted;

          let borderColor = "rgba(240,233,214,0.15)";
          let bg = "transparent";
          let textColor = "var(--cream-1)";

          if (!submitted) {
            if (isSelected) { borderColor = "var(--gold)"; bg = "rgba(196,152,90,0.1)"; textColor = "var(--cream-0)"; }
            else if (isHovered) { borderColor = "rgba(240,233,214,0.3)"; bg = "rgba(240,233,214,0.04)"; textColor = "var(--cream-0)"; }
          } else {
            if (isRight) { borderColor = "rgba(134,197,152,0.7)"; bg = "rgba(134,197,152,0.1)"; textColor = "var(--cream-0)"; }
            else if (isSelected) { borderColor = "rgba(220,100,100,0.7)"; bg = "rgba(220,100,100,0.1)"; textColor = "var(--cream-1)"; }
            else { textColor = "rgba(240,233,214,0.35)"; }
          }

          return (
            <button
              key={opt.id}
              onClick={() => !submitted && setSelected(opt.id)}
              disabled={submitted}
              onMouseEnter={() => setHovered(opt.id)}
              onMouseLeave={() => setHovered(null)}
              style={{
                width: "100%",
                textAlign: "left",
                ...body,
                fontSize: "0.9rem",
                borderRadius: "4px",
                border: `1px solid ${borderColor}`,
                background: bg,
                color: textColor,
                padding: "0.55rem 0.75rem",
                cursor: submitted ? "default" : "pointer",
                transition: "border-color 0.15s, background 0.15s, color 0.15s",
                display: "flex",
                alignItems: "flex-start",
                gap: "0.5rem",
              }}
            >
              <span style={{ ...mono, fontSize: "0.7rem", opacity: submitted && !isRight && !isSelected ? 0.35 : 0.7, flexShrink: 0, paddingTop: "0.1rem" }}>
                {opt.id.toUpperCase()}.
              </span>
              <span>{opt.text}</span>
            </button>
          );
        })}
      </div>

      {/* Submit button */}
      {!submitted && selected && (
        <button
          onClick={() => setSubmitted(true)}
          style={{
            ...mono, fontSize: "0.55rem", letterSpacing: "0.1em", textTransform: "uppercase",
            padding: "0.45rem 1rem",
            background: "var(--gold)", color: "var(--ink)",
            border: "none", borderRadius: "3px", cursor: "pointer",
            marginBottom: "0.5rem",
          }}
        >
          Submit
        </button>
      )}

      {/* Feedback */}
      {submitted && (
        <div style={{
          display: "flex",
          alignItems: "flex-start",
          gap: "0.5rem",
          padding: "0.65rem 0.75rem",
          borderRadius: "4px",
          border: isCorrect ? "1px solid rgba(134,197,152,0.35)" : "1px solid rgba(220,100,100,0.35)",
          background: isCorrect ? "rgba(134,197,152,0.08)" : "rgba(220,100,100,0.08)",
          marginBottom: onSendMessage && !continued ? "0.75rem" : "0",
        }}>
          {isCorrect
            ? <CheckCircle2 style={{ width: "0.9rem", height: "0.9rem", color: "rgba(134,197,152,0.9)", flexShrink: 0, marginTop: "0.15rem" }} />
            : <XCircle    style={{ width: "0.9rem", height: "0.9rem", color: "rgba(220,100,100,0.9)", flexShrink: 0, marginTop: "0.15rem" }} />
          }
          <div>
            <p style={{ ...mono, fontSize: "0.55rem", letterSpacing: "0.08em", textTransform: "uppercase", color: isCorrect ? "rgba(134,197,152,0.9)" : "rgba(220,100,100,0.9)", marginBottom: "0.25rem" }}>
              {isCorrect ? "Correct!" : "Not quite."}
            </p>
            <p style={{ ...body, fontSize: "0.85rem", color: "var(--cream-1)", lineHeight: 1.55 }}>
              {data.explanation}
            </p>
          </div>
        </div>
      )}

      {/* Continue button */}
      {submitted && onSendMessage && !continued && (
        <button
          onClick={handleContinue}
          style={{
            display: "flex", alignItems: "center", gap: "0.35rem",
            ...mono, fontSize: "0.55rem", letterSpacing: "0.1em", textTransform: "uppercase",
            padding: "0.45rem 0.9rem",
            background: "transparent",
            color: "var(--cream-1)",
            border: "1px solid rgba(240,233,214,0.2)",
            borderRadius: "3px", cursor: "pointer",
            marginTop: "0.75rem",
            transition: "border-color 0.15s, color 0.15s",
          }}
          onMouseEnter={e => { e.currentTarget.style.borderColor = "rgba(240,233,214,0.5)"; e.currentTarget.style.color = "var(--cream-0)"; }}
          onMouseLeave={e => { e.currentTarget.style.borderColor = "rgba(240,233,214,0.2)"; e.currentTarget.style.color = "var(--cream-1)"; }}
        >
          Continue
          <ArrowRight style={{ width: "0.7rem", height: "0.7rem" }} />
        </button>
      )}
    </div>
  );
}
