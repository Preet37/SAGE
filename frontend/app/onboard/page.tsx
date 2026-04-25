'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getDiagnosticQuestions, submitDiagnostic, submitDiagnosticForUser } from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import Link from 'next/link';

interface Question {
  id: string;
  text: string;
  options: string[];
  subject: string;
}

interface DiagnosticResult {
  knowledge_profile: string;
  gaps: string[];
  recommended_start: string;
  grade_estimate: string;
  encouragement: string;
}

type Step = 'intro' | 'quiz' | 'result';

export default function OnboardPage() {
  const router = useRouter();
  const { token } = useAuthStore();
  const [step, setStep] = useState<Step>('intro');
  const [name, setName] = useState('');
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [current, setCurrent] = useState(0);
  const [result, setResult] = useState<DiagnosticResult | null>(null);
  const [loading, setLoading] = useState(false);

  async function loadQuestions() {
    setLoading(true);
    try {
      const qs = await getDiagnosticQuestions();
      setQuestions(qs);
    } finally {
      setLoading(false);
    }
  }

  function selectAnswer(qid: string, option: string) {
    const letter = option.split(')')[0].trim().toLowerCase();
    setAnswers((prev) => ({ ...prev, [qid]: letter }));
  }

  async function finish() {
    setLoading(true);
    try {
      const data = token
        ? await submitDiagnosticForUser(token, answers, name)
        : await submitDiagnostic(answers, name);
      setResult(data);
      setStep('result');
    } finally {
      setLoading(false);
    }
  }

  function next() {
    if (current < questions.length - 1) {
      setCurrent((c) => c + 1);
    } else {
      finish();
    }
  }

  const q = questions[current];
  const answered = q ? !!answers[q.id] : false;
  const totalAnswered = Object.keys(answers).length;

  return (
    <div className="min-h-screen bg-bg flex flex-col items-center justify-center px-4 py-12">
      {/* Header */}
      <div className="w-full max-w-lg mb-8 flex items-center justify-between">
        <Link href="/" className="text-t2 hover:text-t0 text-sm transition-colors">← Back</Link>
        <span className="font-black text-lg">S<span className="text-acc">AGE</span></span>
      </div>

      {step === 'intro' && (
        <div className="w-full max-w-lg space-y-6">
          <div className="text-center space-y-3">
            <div className="text-3xl font-bold text-t0">Welcome to SAGE</div>
            <p className="text-t2 leading-relaxed">
              If you've changed schools, moved to a new place, or missed time in class —
              this quick check-in helps SAGE understand where you are so we can start
              in exactly the right place for <em>you</em>.
            </p>
            <p className="text-t3 text-sm">5 questions · no wrong answers · takes 2 minutes</p>
          </div>

          <div>
            <label className="block text-xs text-t3 font-semibold uppercase tracking-wider mb-1.5">
              Your name (optional)
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="What should SAGE call you?"
              className="w-full bg-bg2 border border-white/10 rounded-xl px-4 py-3 text-t0 text-sm placeholder:text-t3 focus:outline-none focus:border-acc/50 transition-colors"
              onKeyDown={(e) => e.key === 'Enter' && !loading && (loadQuestions(), setStep('quiz'))}
            />
          </div>

          <button
            onClick={() => { loadQuestions(); setStep('quiz'); }}
            disabled={loading}
            className="w-full bg-acc hover:bg-acc/90 text-white font-semibold py-3 rounded-xl transition-all disabled:opacity-50"
          >
            {loading ? 'Loading…' : "Let's begin"}
          </button>

          <p className="text-center text-t3 text-xs">
            Already have an account?{' '}
            <Link href="/login" className="text-acc hover:underline">Sign in</Link>
          </p>
        </div>
      )}

      {step === 'quiz' && q && (
        <div className="w-full max-w-lg space-y-6">
          {/* Progress */}
          <div className="space-y-1.5">
            <div className="flex justify-between text-xs text-t3">
              <span>Question {current + 1} of {questions.length}</span>
              <span className="capitalize text-acc/70">{q.subject}</span>
            </div>
            <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
              <div
                className="h-full bg-acc rounded-full transition-all duration-500"
                style={{ width: `${((current + 1) / questions.length) * 100}%` }}
              />
            </div>
          </div>

          {/* Question */}
          <div className="bg-bg2 border border-white/10 rounded-2xl p-6 space-y-5">
            <p className="text-t0 text-base leading-relaxed font-medium">{q.text}</p>

            <div className="space-y-2.5">
              {q.options.map((opt) => {
                const letter = opt.split(')')[0].trim().toLowerCase();
                const selected = answers[q.id] === letter;
                return (
                  <button
                    key={opt}
                    onClick={() => selectAnswer(q.id, opt)}
                    className={`w-full text-left px-4 py-3 rounded-xl border text-sm transition-all ${
                      selected
                        ? 'border-acc bg-acc/15 text-t0'
                        : 'border-white/10 bg-white/3 text-t1 hover:border-white/20 hover:bg-white/5'
                    }`}
                  >
                    {opt}
                  </button>
                );
              })}
            </div>
          </div>

          <button
            onClick={next}
            disabled={!answered || loading}
            className="w-full bg-acc hover:bg-acc/90 disabled:opacity-40 text-white font-semibold py-3 rounded-xl transition-all"
          >
            {loading
              ? 'Analysing…'
              : current === questions.length - 1
              ? 'See my results'
              : 'Next question →'}
          </button>
        </div>
      )}

      {step === 'result' && result && (
        <div className="w-full max-w-lg space-y-5">
          <div className="text-center space-y-2">
            <div className="text-2xl font-bold text-t0">
              {name ? `Great job, ${name}!` : 'You did it!'}
            </div>
            <p className="text-t2 text-sm">{result.encouragement}</p>
          </div>

          <div className="bg-bg2 border border-white/10 rounded-2xl p-5 space-y-4">
            <div>
              <div className="text-[10px] font-bold uppercase tracking-widest text-t3 mb-1.5">Your knowledge profile</div>
              <p className="text-t1 text-sm leading-relaxed">{result.knowledge_profile}</p>
            </div>

            <div className="flex gap-4">
              <div className="flex-1">
                <div className="text-[10px] font-bold uppercase tracking-widest text-t3 mb-1.5">Estimated level</div>
                <div className="text-acc font-semibold text-sm">{result.grade_estimate}</div>
              </div>
              <div className="flex-1">
                <div className="text-[10px] font-bold uppercase tracking-widest text-t3 mb-1.5">Where to start</div>
                <div className="text-t1 text-sm font-medium">{result.recommended_start}</div>
              </div>
            </div>

            {result.gaps.length > 0 && (
              <div>
                <div className="text-[10px] font-bold uppercase tracking-widest text-t3 mb-1.5">Areas to strengthen</div>
                <div className="flex flex-wrap gap-1.5">
                  {result.gaps.map((gap) => (
                    <span key={gap} className="text-[11px] px-2.5 py-1 bg-ora/10 text-ora rounded-full border border-ora/20">
                      {gap}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="flex gap-3">
            <Link
              href="/register"
              className="flex-1 text-center bg-acc hover:bg-acc/90 text-white font-semibold py-3 rounded-xl transition-all text-sm"
            >
              Create free account
            </Link>
            <Link
              href="/learn"
              className="flex-1 text-center border border-white/10 text-t1 hover:text-t0 hover:border-white/20 font-semibold py-3 rounded-xl transition-all text-sm"
            >
              Start learning →
            </Link>
          </div>

          <p className="text-center text-t3 text-xs">
            Free resources:{' '}
            <a href="https://lite.khanacademy.org" target="_blank" rel="noopener noreferrer" className="text-acc hover:underline">Khan Academy Lite</a>
            {' · '}
            <a href="https://www.unhcr.org/what-we-do/build-better-futures/education" target="_blank" rel="noopener noreferrer" className="text-acc hover:underline">UNHCR Education</a>
          </p>
        </div>
      )}
    </div>
  );
}
