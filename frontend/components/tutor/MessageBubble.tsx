'use client';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';
import { useState } from 'react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  verification?: { passed: boolean; flags: string[] };
  quiz?: { question: string; options: string[]; answer: string; explanation: string };
}

interface Props { message: Message }

const QUIZ_REGEX = /<quiz>([\s\S]*?)<\/quiz>/;

export default function MessageBubble({ message }: Props) {
  const [quizAnswer, setQuizAnswer] = useState<string | null>(null);
  const isUser = message.role === 'user';

  const quizMatch = message.content.match(QUIZ_REGEX);
  const cleanContent = message.content.replace(QUIZ_REGEX, '').trim();
  let quiz: { question: string; options: string[]; answer: string; explanation: string } | null = null;
  if (quizMatch) {
    try { quiz = JSON.parse(quizMatch[1]); } catch {}
  }

  if (isUser) {
    return (
      <div className="flex justify-end animate-fade-up">
        <div className="max-w-[78%] bg-acc/15 border border-acc/25 rounded-2xl rounded-tr-sm px-4 py-3">
          <p className="text-sm text-t0 leading-relaxed whitespace-pre-wrap">{message.content}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-2 animate-fade-up">
      <div className="flex items-center gap-2">
        <div className="w-5 h-5 rounded-full bg-acc/20 border border-acc/30 flex items-center justify-center text-[9px] text-acc font-bold">S</div>
        <span className="text-[9.5px] font-bold uppercase tracking-widest text-t3">SAGE</span>
        {message.verification && (
          <span className={`ml-auto text-[9px] font-semibold flex items-center gap-1 px-2 py-0.5 rounded-full ${
            message.verification.passed
              ? 'text-grn bg-grn/10 border border-grn/20'
              : 'text-pnk bg-pnk/10 border border-pnk/20'
          }`}>
            {message.verification.passed ? '✓ Verified' : '⚠ Flagged'}
          </span>
        )}
      </div>

      {cleanContent && (
        <div className="bg-bg2 border border-white/5 rounded-2xl rounded-tl-sm px-4 py-3">
          <div className="prose-sage text-sm">
            <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
              {cleanContent}
            </ReactMarkdown>
          </div>
        </div>
      )}

      {quiz && (
        <div className="bg-bg2 border border-yel/20 rounded-2xl p-4">
          <div className="text-[10px] font-bold uppercase tracking-widest text-yel mb-3">Quiz</div>
          <p className="text-sm text-t0 font-medium mb-3">{quiz.question}</p>
          <div className="space-y-2">
            {quiz.options.map((opt, i) => {
              const letter = String.fromCharCode(65 + i);
              const isSelected = quizAnswer === letter;
              const isCorrect = quizAnswer && letter === quiz!.answer;
              const isWrong = isSelected && letter !== quiz!.answer;
              return (
                <button
                  key={letter}
                  onClick={() => !quizAnswer && setQuizAnswer(letter)}
                  disabled={!!quizAnswer}
                  className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl border text-sm text-left transition-all ${
                    isCorrect ? 'border-grn/50 bg-grn/10 text-grn'
                    : isWrong ? 'border-pnk/50 bg-pnk/10 text-pnk'
                    : isSelected ? 'border-acc/50 bg-acc/10 text-acc'
                    : 'border-white/5 hover:border-white/10 text-t1 hover:text-t0'
                  }`}
                >
                  <span className="w-6 h-6 rounded-lg bg-bg3 flex items-center justify-center text-xs font-bold flex-shrink-0">{letter}</span>
                  {opt}
                </button>
              );
            })}
          </div>
          {quizAnswer && (
            <div className={`mt-3 text-xs p-3 rounded-xl ${quizAnswer === quiz.answer ? 'bg-grn/10 text-grn border border-grn/20' : 'bg-pnk/10 text-pnk border border-pnk/20'}`}>
              {quizAnswer === quiz.answer ? '✓ Correct! ' : `✗ Not quite. The answer is ${quiz.answer}. `}
              {quiz.explanation}
            </div>
          )}
        </div>
      )}

      {message.verification?.flags.length ? (
        <div className="text-[10px] text-pnk/70 px-1">
          {message.verification.flags.map(f => <span key={f} className="block">⚠ {f}</span>)}
        </div>
      ) : null}
    </div>
  );
}
