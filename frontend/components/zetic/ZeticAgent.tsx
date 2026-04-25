'use client';
/**
 * ZETIC Track — On-Device AI Agent
 *
 * Runs a small LLM (Phi-3 mini via WebLLM) entirely in the browser.
 * No server calls. Full privacy. Works offline.
 *
 * Used for:
 * - Quick concept check questions (instant, private)
 * - Offline tutoring when server is unreachable
 * - Edge inference demo (ZETIC track)
 */
import { useState, useRef, useCallback, useEffect } from 'react';

type ZeticState = 'idle' | 'loading' | 'ready' | 'running' | 'error' | 'unavailable';

interface Props {
  onResponse?: (text: string) => void;
  context?: string;
}

declare global {
  interface Window {
    // WebLLM global when loaded via CDN script tag
    webllm?: {
      CreateMLCEngine: (model: string, opts?: unknown) => Promise<unknown>;
    };
  }
}

const ZETIC_MODEL = 'Phi-3.5-mini-instruct-q4f16_1-MLC';
const ZETIC_SYSTEM = `You are a compact on-device AI assistant for SAGE education platform. 
You run entirely in the student's browser — no server needed. 
Answer questions concisely (50-100 words max). 
You have access to the current lesson context provided.`;

export default function ZeticAgent({ onResponse, context }: Props) {
  const [state, setState] = useState<ZeticState>('idle');
  const [loadProgress, setLoadProgress] = useState(0);
  const [loadText, setLoadText] = useState('');
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [isWebGPU, setIsWebGPU] = useState<boolean | null>(null);
  const engineRef = useRef<unknown>(null);
  const scriptLoadedRef = useRef(false);

  useEffect(() => {
    // Check WebGPU support
    setIsWebGPU('gpu' in navigator);
  }, []);

  async function loadZeticEngine() {
    if (engineRef.current) { setState('ready'); return; }
    if (state === 'loading') return;

    setState('loading');
    setLoadProgress(0);
    setLoadText('Initializing ZETIC on-device engine…');

    try {
      // Dynamically load WebLLM from CDN if not already loaded
      if (!window.webllm && !scriptLoadedRef.current) {
        scriptLoadedRef.current = true;
        await new Promise<void>((resolve, reject) => {
          const script = document.createElement('script');
          script.src = 'https://esm.run/@mlc-ai/web-llm';
          script.type = 'module';
          script.onload = () => resolve();
          script.onerror = () => reject(new Error('WebLLM CDN load failed'));
          document.head.appendChild(script);
        });

        // Wait for webllm to be available
        await new Promise<void>((resolve) => {
          let attempts = 0;
          const check = setInterval(() => {
            if (window.webllm || attempts++ > 50) {
              clearInterval(check);
              resolve();
            }
          }, 200);
        });
      }

      if (!window.webllm) {
        setState('unavailable');
        setLoadText('WebLLM not available in this browser');
        return;
      }

      const engine = await window.webllm.CreateMLCEngine(ZETIC_MODEL, {
        initProgressCallback: (progress: { text: string; progress: number }) => {
          setLoadText(progress.text || 'Loading model…');
          setLoadProgress(Math.round((progress.progress || 0) * 100));
        },
      });

      engineRef.current = engine;
      setState('ready');
      setLoadText('Model ready');
      setLoadProgress(100);
    } catch (err) {
      console.error('ZETIC load error:', err);
      setState('error');
      setLoadText(String(err));
    }
  }

  const runInference = useCallback(async () => {
    if (!query.trim() || !engineRef.current || state !== 'ready') return;
    setState('running');
    setResponse('');

    const messages = [
      { role: 'system', content: ZETIC_SYSTEM + (context ? `\n\nContext: ${context.slice(0, 500)}` : '') },
      { role: 'user', content: query },
    ];

    try {
      const engine = engineRef.current as {
        chat: { completions: { create: (opts: unknown) => Promise<{ choices: { message: { content: string } }[] }> } };
      };

      const result = await engine.chat.completions.create({
        messages,
        max_tokens: 200,
        temperature: 0.7,
      });

      const text = result.choices[0].message.content || '';
      setResponse(text);
      onResponse?.(text);
    } catch (err) {
      setResponse(`Error: ${String(err)}`);
    } finally {
      setState('ready');
    }
  }, [query, state, context, onResponse]);

  return (
    <div className="bg-bg2 border border-pur/20 rounded-2xl p-4">
      {/* Header */}
      <div className="flex items-center gap-2 mb-4">
        <div className="w-6 h-6 rounded-lg bg-pur/20 flex items-center justify-center text-xs text-pur font-bold">Z</div>
        <div className="flex-1">
          <div className="text-xs font-bold text-t0">ZETIC On-Device AI</div>
          <div className="text-[9px] text-t3">Runs in your browser · No server · Full privacy</div>
        </div>
        <div className={`text-[9px] font-bold px-2 py-0.5 rounded-full ${
          state === 'ready' ? 'bg-grn/15 text-grn' :
          state === 'running' ? 'bg-acc/15 text-acc' :
          state === 'loading' ? 'bg-yel/15 text-yel' :
          state === 'error' || state === 'unavailable' ? 'bg-pnk/15 text-pnk' :
          'bg-bg3 text-t3'
        }`}>
          {state === 'idle' ? 'OFF' : state.toUpperCase()}
        </div>
      </div>

      {/* WebGPU warning */}
      {isWebGPU === false && (
        <div className="text-[10px] text-pnk bg-pnk/10 border border-pnk/20 rounded-xl p-3 mb-3">
          ⚠ WebGPU not supported in this browser. On-device AI requires Chrome 113+ on a modern GPU.
        </div>
      )}

      {/* Model info */}
      {state === 'idle' && isWebGPU !== false && (
        <div className="text-[10px] text-t2 mb-3 leading-relaxed">
          Load <span className="text-pur font-mono">Phi-3.5-mini</span> (~2GB) to run AI inference 
          directly on your device. No API key needed. Works offline.
        </div>
      )}

      {/* Load button */}
      {state === 'idle' && (
        <button
          onClick={loadZeticEngine}
          disabled={isWebGPU === false}
          className="w-full py-2 text-xs font-bold bg-pur/15 text-pur border border-pur/25 rounded-xl hover:bg-pur/25 transition-all disabled:opacity-40"
        >
          Load On-Device Model (Phi-3.5 mini)
        </button>
      )}

      {/* Loading progress */}
      {state === 'loading' && (
        <div className="space-y-2">
          <div className="text-[10px] text-t1 truncate">{loadText}</div>
          <div className="h-1.5 bg-bg3 rounded-full overflow-hidden">
            <div
              className="h-full rounded-full bg-pur transition-all duration-500"
              style={{ width: `${loadProgress}%` }}
            />
          </div>
          <div className="text-[9px] text-t3 text-right">{loadProgress}%</div>
        </div>
      )}

      {/* Query interface */}
      {(state === 'ready' || state === 'running') && (
        <div className="space-y-3">
          <div className="flex gap-2">
            <input
              value={query}
              onChange={e => setQuery(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && runInference()}
              placeholder="Ask the on-device model…"
              disabled={state === 'running'}
              className="flex-1 bg-bg3 border border-white/5 rounded-xl px-3 py-2 text-xs text-t0 outline-none focus:border-pur/40 transition-colors placeholder-t3"
            />
            <button
              onClick={runInference}
              disabled={state === 'running' || !query.trim()}
              className="px-3 py-2 bg-pur/20 text-pur rounded-xl text-xs font-bold hover:bg-pur/30 transition-all disabled:opacity-40"
            >
              {state === 'running' ? '…' : '→'}
            </button>
          </div>

          {response && (
            <div className="bg-bg3 border border-pur/15 rounded-xl p-3 text-xs text-t1 leading-relaxed">
              <div className="text-[9px] font-bold uppercase tracking-widest text-pur mb-2">On-Device Response</div>
              {response}
            </div>
          )}
        </div>
      )}

      {/* Error state */}
      {(state === 'error' || state === 'unavailable') && (
        <div className="space-y-2">
          <div className="text-[10px] text-pnk">{loadText}</div>
          <button
            onClick={() => setState('idle')}
            className="text-[10px] text-t2 hover:text-t0 transition-colors"
          >
            ← Reset
          </button>
        </div>
      )}

      {/* ZETIC branding */}
      <div className="mt-3 pt-3 border-t border-white/5 flex items-center gap-2">
        <div className="text-[9px] text-t3">Powered by</div>
        <div className="text-[9px] font-bold text-pur">ZETIC.ai</div>
        <div className="ml-auto text-[9px] text-t3">WebLLM · MLC Engine</div>
      </div>
    </div>
  );
}
