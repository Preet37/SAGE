'use client';
import { useState, useRef, useCallback } from 'react';

interface Props { onTranscript: (text: string) => void }

type VoiceState = 'idle' | 'listening' | 'processing';

export default function VoiceAgent({ onTranscript }: Props) {
  const [state, setState] = useState<VoiceState>('idle');
  const [transcript, setTranscript] = useState('');
  const [supported] = useState(() => typeof window !== 'undefined' && 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window);
  const recogRef = useRef<SpeechRecognition | null>(null);

  const startListening = useCallback(() => {
    if (!supported) return;
    const SpeechRec = (window as unknown as { SpeechRecognition?: typeof SpeechRecognition; webkitSpeechRecognition?: typeof SpeechRecognition }).SpeechRecognition || (window as unknown as { webkitSpeechRecognition?: typeof SpeechRecognition }).webkitSpeechRecognition;
    if (!SpeechRec) return;

    const rec = new SpeechRec();
    rec.continuous = false;
    rec.interimResults = true;
    rec.lang = 'en-US';
    recogRef.current = rec;

    rec.onstart = () => setState('listening');
    rec.onresult = (e: SpeechRecognitionEvent) => {
      let interim = '';
      let final = '';
      for (let i = e.resultIndex; i < e.results.length; i++) {
        if (e.results[i].isFinal) final += e.results[i][0].transcript;
        else interim += e.results[i][0].transcript;
      }
      setTranscript(final || interim);
    };
    rec.onend = () => {
      setState('processing');
      setTimeout(() => {
        if (transcript.trim()) onTranscript(transcript.trim());
        setTranscript('');
        setState('idle');
      }, 600);
    };
    rec.onerror = () => setState('idle');
    rec.start();
  }, [supported, transcript, onTranscript]);

  function stopListening() {
    recogRef.current?.stop();
  }

  return (
    <div className="p-4 border-b border-white/5">
      <div className="text-[9.5px] font-bold uppercase tracking-widest text-t3 mb-3">Voice Agent</div>

      {!supported ? (
        <div className="text-[10px] text-t3 bg-bg2 rounded-xl p-3">
          Voice not supported in this browser. Use Chrome for voice input.
        </div>
      ) : (
        <div className="flex flex-col items-center gap-3">
          {/* Mic button */}
          <button
            onClick={state === 'idle' ? startListening : stopListening}
            className={`relative w-14 h-14 rounded-full flex items-center justify-center transition-all ${
              state === 'listening'
                ? 'bg-pnk/20 border-2 border-pnk shadow-lg shadow-pnk/20'
                : state === 'processing'
                ? 'bg-acc/20 border-2 border-acc'
                : 'bg-bg2 border border-white/10 hover:border-white/20'
            }`}
          >
            {state === 'listening' && (
              <div className="absolute inset-0 rounded-full border-2 border-pnk animate-ping opacity-30" />
            )}
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"
              className={`w-6 h-6 ${state === 'listening' ? 'text-pnk' : state === 'processing' ? 'text-acc' : 'text-t1'}`}>
              <rect x="9" y="3" width="6" height="11" rx="3" />
              <path d="M5 10a7 7 0 0014 0M12 19v3M8 22h8" strokeLinecap="round" />
            </svg>
          </button>

          <div className="text-[10px] text-t2 text-center">
            {state === 'idle' && (supported ? 'Tap to speak' : '')}
            {state === 'listening' && <span className="text-pnk font-semibold">Listening…</span>}
            {state === 'processing' && <span className="text-acc font-semibold">Processing…</span>}
          </div>

          {transcript && (
            <div className="w-full bg-bg2 border border-white/5 rounded-xl p-2 text-[10px] text-t1 italic">
              "{transcript}"
            </div>
          )}

          {/* Soundwave bars */}
          {state === 'listening' && (
            <div className="flex items-end gap-0.5 h-6">
              {[3, 5, 4, 7, 5, 3, 6, 4, 5, 3].map((h, i) => (
                <div
                  key={i}
                  className="w-1 bg-pnk rounded-full"
                  style={{
                    height: `${h * 2}px`,
                    animation: `typing 0.8s ease infinite ${i * 0.08}s`,
                    opacity: 0.7,
                  }}
                />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
