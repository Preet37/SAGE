"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import type { VerificationEvent } from "@/lib/api";

export type MessageRole = "user" | "sage";

export interface Message {
  role: MessageRole;
  text: string;
  agent?: string;
  verification?: VerificationEvent;
}

export default function MessageBubble({ msg }: { msg: Message }) {
  const isUser = msg.role === "user";
  const ungrounded = msg.verification && !msg.verification.grounded;
  const { prose, quizzes } = isUser ? { prose: msg.text, quizzes: [] } : extractQuizzes(msg.text);

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className="max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed"
        style={{
          background: isUser ? "var(--color-primary)" : "white",
          color: isUser ? "var(--color-on-primary)" : "var(--color-foreground)",
          border: isUser ? "none" : "1px solid var(--color-border)",
          boxShadow: "var(--shadow-sm)",
          fontFamily: "var(--font-body)",
        }}
      >
        {isUser ? <p className="whitespace-pre-wrap">{msg.text}</p> : <Markdown text={prose} />}

        {quizzes.map((q, i) => (
          <Quiz key={i} block={q} />
        ))}

        {msg.verification && (
          <div
            className="mt-2 flex items-center gap-2 text-xs"
            style={{ color: ungrounded ? "var(--color-destructive)" : "var(--color-primary)" }}
          >
            <span>{ungrounded ? "⚠ partially ungrounded" : "✓ grounded"}</span>
            <span style={{ opacity: 0.7 }}>· score {msg.verification.score.toFixed(2)}</span>
            {msg.verification.claims.length > 0 && (
              <span style={{ opacity: 0.7 }}>· {msg.verification.claims.length} claims</span>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

// ---------------- Quiz parsing ----------------

interface QuizBlock {
  question: string;
  choices: string[];
  answer: number;
  explanation?: string;
}

const QUIZ_RE = /<quiz>\s*([\s\S]*?)\s*<\/quiz>/g;

/** Strip <quiz>...</quiz> blocks from prose and return any successfully-parsed blocks. */
function extractQuizzes(text: string): { prose: string; quizzes: QuizBlock[] } {
  const quizzes: QuizBlock[] = [];
  const prose = text.replace(QUIZ_RE, (_full, raw: string) => {
    try {
      const parsed = JSON.parse(raw) as Partial<QuizBlock>;
      if (
        parsed &&
        typeof parsed.question === "string" &&
        Array.isArray(parsed.choices) &&
        typeof parsed.answer === "number" &&
        parsed.choices.every((c) => typeof c === "string")
      ) {
        quizzes.push({
          question: parsed.question,
          choices: parsed.choices as string[],
          answer: parsed.answer,
          explanation:
            typeof parsed.explanation === "string" ? parsed.explanation : undefined,
        });
      }
    } catch {
      /* ignore malformed quiz block */
    }
    return "";
  });
  return { prose: prose.trim(), quizzes };
}

function Quiz({ block }: { block: QuizBlock }) {
  const [picked, setPicked] = useState<number | null>(null);
  const correct = picked !== null && picked === block.answer;

  return (
    <div
      className="mt-3 rounded-2xl p-3"
      style={{
        background: "var(--color-muted)",
        border: "1px solid var(--color-border)",
      }}
    >
      <p className="text-sm font-semibold">{block.question}</p>
      <ul className="mt-2 space-y-1.5">
        {block.choices.map((c, i) => {
          const chosen = picked === i;
          const reveal = picked !== null;
          const isAnswer = i === block.answer;
          const bg = !reveal
            ? "white"
            : isAnswer
              ? "color-mix(in srgb, var(--color-secondary) 35%, white)"
              : chosen
                ? "color-mix(in srgb, var(--color-destructive) 25%, white)"
                : "white";
          return (
            <li key={i}>
              <button
                type="button"
                onClick={() => picked === null && setPicked(i)}
                disabled={picked !== null}
                className="w-full rounded-xl px-3 py-2 text-left text-xs"
                style={{
                  background: bg,
                  border: "1px solid var(--color-border)",
                  cursor: picked === null ? "pointer" : "default",
                }}
              >
                <span style={{ fontWeight: 600 }}>{String.fromCharCode(65 + i)}.</span> {c}
              </button>
            </li>
          );
        })}
      </ul>
      {picked !== null && (
        <p
          className="mt-2 text-xs"
          style={{ color: correct ? "var(--color-primary)" : "var(--color-destructive)" }}
        >
          {correct ? "Correct." : `Not quite — the answer is ${String.fromCharCode(65 + block.answer)}.`}
          {block.explanation && (
            <span style={{ color: "var(--color-foreground)", opacity: 0.8 }}> {block.explanation}</span>
          )}
        </p>
      )}
    </div>
  );
}

function Markdown({ text }: { text: string }) {
  if (!text) return <span style={{ opacity: 0.6 }}>…</span>;
  return (
    <div className="sage-md">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          p: (p) => <p className="my-1" {...p} />,
          ul: (p) => <ul className="my-1 ml-5 list-disc" {...p} />,
          ol: (p) => <ol className="my-1 ml-5 list-decimal" {...p} />,
          li: (p) => <li className="my-0.5" {...p} />,
          h1: (p) => <h3 className="mt-2 text-base font-semibold" {...p} />,
          h2: (p) => <h3 className="mt-2 text-base font-semibold" {...p} />,
          h3: (p) => <h3 className="mt-2 text-sm font-semibold" {...p} />,
          strong: (p) => (
            <strong style={{ color: "var(--color-accent)", fontWeight: 700 }} {...p} />
          ),
          em: (p) => <em style={{ color: "var(--color-primary)" }} {...p} />,
          code: ({ className, children, ...rest }) => {
            const block = /language-/.test(className ?? "");
            return block ? (
              <pre
                className="my-2 overflow-x-auto rounded-xl p-3 text-xs"
                style={{ background: "var(--color-muted)" }}
              >
                <code className={className} {...rest}>
                  {children}
                </code>
              </pre>
            ) : (
              <code
                className="rounded px-1 py-0.5 text-xs"
                style={{ background: "var(--color-muted)", fontFamily: "ui-monospace, monospace" }}
                {...rest}
              >
                {children}
              </code>
            );
          },
          a: (p) => (
            <a
              {...p}
              target="_blank"
              rel="noreferrer"
              style={{ color: "var(--color-primary)", textDecoration: "underline" }}
            />
          ),
          blockquote: (p) => (
            <blockquote
              className="my-2 border-l-4 pl-3 italic"
              style={{ borderColor: "var(--color-secondary)" }}
              {...p}
            />
          ),
          table: (p) => (
            <div className="my-2 overflow-x-auto">
              <table className="w-full text-xs" {...p} />
            </div>
          ),
          th: (p) => (
            <th
              className="px-2 py-1 text-left"
              style={{ borderBottom: "1px solid var(--color-border)" }}
              {...p}
            />
          ),
          td: (p) => (
            <td
              className="px-2 py-1"
              style={{ borderBottom: "1px solid var(--color-border)" }}
              {...p}
            />
          ),
        }}
      >
        {text}
      </ReactMarkdown>
    </div>
  );
}
