'use client';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';
import { useState, useCallback } from 'react';
import { generateVisualPlot } from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import VisualPlotRenderer, { type VisualPlot } from '@/components/visual/VisualPlotRenderer';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  verification?: { passed: boolean; flags: string[] };
  quiz?: { question: string; options: string[]; answer: string; explanation: string };
  lessonId?: number;
}

interface Props { message: Message }

const QUIZ_REGEX = /<quiz>([\s\S]*?)<\/quiz>/;

function isVisualRequest(content: string): boolean {
  const lower = content.toLowerCase();
  return (
    lower.includes('visual') ||
    lower.includes('show me') ||
    lower.includes('diagram') ||
    lower.includes('illustrate') ||
    lower.includes('draw') ||
    lower.includes('picture') ||
    lower.includes('3d') ||
    lower.includes('render') ||
    lower.includes('animate') ||
    lower.includes('graph of') ||
    lower.includes('plot')
  );
}

// Build a rich concept string from the assistant message for the visualizer
function extractConcept(content: string): string {
  // Take first 2 sentences or 200 chars, whichever is shorter
  const sentences = content.replace(/<[^>]+>/g, '').split(/[.!?]/);
  return sentences.slice(0, 3).join('. ').slice(0, 300).trim();
}

export default function MessageBubble({ message }: Props) {
  const [quizAnswer, setQuizAnswer] = useState<string | null>(null);
  const [vizData, setVizData] = useState<VisualPlot | null>(null);
  const [vizLoading, setVizLoading] = useState(false);
  const [vizError, setVizError] = useState<string | null>(null);
  const { token } = useAuthStore();
  const isUser = message.role === 'user';

  const quizMatch = message.content.match(QUIZ_REGEX);
  const cleanContent = message.content.replace(QUIZ_REGEX, '').trim();
  let quiz: { question: string; options: string[]; answer: string; explanation: string } | null = null;
  if (quizMatch) {
    try { quiz = JSON.parse(quizMatch[1]); } catch {}
  }

  const handleVisualize = useCallback(async () => {
    if (!token || vizLoading) return;
    setVizLoading(true);
    setVizError(null);
    try {
      const concept = extractConcept(cleanContent);
      const data = await generateVisualPlot(
        token,
        concept,
        cleanContent.slice(0, 500),
        message.lessonId
      );
      setVizData(data);
    } catch (e) {
      setVizError((e as Error).message || 'Could not generate visualization.');
    } finally {
      setVizLoading(false);
    }
  }, [token, cleanContent, message.lessonId, vizLoading]);

  if (isUser) {
    const wantsVisual = isVisualRequest(message.content);
    return (
      <div className="flex justify-end animate-fade-up">
        <div className="max-w-[78%] flex flex-col gap-1.5 items-end">
          <div className="bg-acc/15 border border-acc/25 rounded-2xl rounded-tr-sm px-4 py-3">
            <p className="text-sm text-t0 leading-relaxed whitespace-pre-wrap">{message.content}</p>
          </div>
          {wantsVisual && (
            <span className="text-[10px] text-indigo-400/70 flex items-center gap-1">
              <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.069A1 1 0 0121 8.867V15.133a1 1 0 01-1.447.902L15 14M3 8a2 2 0 012-2h8a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2V8z" />
              </svg>
              visual request detected
            </span>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-2 animate-fade-up">
      {/* SAGE header */}
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

      {/* Text content */}
      {cleanContent && (
        <div className="bg-bg2 border border-white/5 rounded-2xl rounded-tl-sm px-4 py-3">
          <div className="prose-sage text-sm">
            <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
              {cleanContent}
            </ReactMarkdown>
          </div>

          {/* Visualize button */}
          {!vizData && (
            <div className="mt-3 pt-3 border-t border-white/5 flex items-center gap-3 flex-wrap">
              <button
                onClick={handleVisualize}
                disabled={vizLoading}
                className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/25 text-indigo-300 text-xs font-medium transition-all disabled:opacity-50 disabled:cursor-wait"
              >
                {vizLoading ? (
                  <>
                    <svg className="w-3 h-3 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                    Generating interactive plot…
                  </>
                ) : (
                  <>
                    <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                    Plot Interactive Graph
                  </>
                )}
              </button>
              {!vizLoading && (
                <span className="text-[10px] text-slate-600">sliders · multi-tab plots · real physics</span>
              )}
              {vizLoading && (
                <span className="text-[10px] text-indigo-400/50 italic">
                  Generating interactive plot with parameter sliders…
                </span>
              )}
            </div>
          )}

          {vizError && (
            <div className="mt-2 flex items-start gap-2 p-2.5 rounded-lg bg-red-950/30 border border-red-800/30">
              <svg className="w-3.5 h-3.5 text-red-400 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-xs text-red-400">{vizError}</p>
            </div>
          )}
        </div>
      )}

      {/* Interactive Plotly plot — LLM-generated HTML running in sandboxed iframe */}
      {vizData && (
        <VisualPlotRenderer
          data={vizData}
          onClose={() => setVizData(null)}
        />
      )}

      {/* Quiz */}
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
