'use client';
import { useEffect, useRef, useState } from 'react';
import { useTutorStore } from '@/lib/store';
import { t } from '@/lib/i18n';

interface Props {
  onTranscript: (text: string) => void;
  lessonTitle: string;
}

type VoiceState = 'idle' | 'listening' | 'speaking' | 'thinking';

type SpeechResultEvent = {
  results: { length: number; [i: number]: { isFinal: boolean; [i: number]: { transcript: string } } };
};
type SpeechRecognitionLike = {
  lang: string; continuous: boolean; interimResults: boolean;
  onstart: (() => void) | null;
  onresult: ((e: SpeechResultEvent) => void) | null;
  onerror: (() => void) | null;
  onend: (() => void) | null;
  start: () => void; stop: () => void;
};
type SpeechWindow = Window & {
  SpeechRecognition?: new () => SpeechRecognitionLike;
  webkitSpeechRecognition?: new () => SpeechRecognitionLike;
};

export default function VoiceOnlyMode({ onTranscript, lessonTitle }: Props) {
  const { messages, isStreaming, language, setVoiceOnlyMode } = useTutorStore();
  const [voiceState, setVoiceState] = useState<VoiceState>('idle');
  const [transcript, setTranscript] = useState('');
  const recognitionRef = useRef<SpeechRecognitionLike | null>(null);
  const synthRef = useRef<SpeechSynthesisUtterance | null>(null);
  const lastSpokenRef = useRef('');

  // Auto-speak the last assistant message when it arrives
  useEffect(() => {
    const last = messages.at(-1);
    if (!last || last.role !== 'assistant' || !last.content || isStreaming) return;
    if (last.content === lastSpokenRef.current) return;
    lastSpokenRef.current = last.content;

    const text = last.content
      .replace(/[*_`#~]/g, '')
      .replace(/<[^>]+>/g, '')
      .slice(0, 800);

    if (!text.trim()) return;

    window.speechSynthesis?.cancel();
    const utt = new SpeechSynthesisUtterance(text);
    utt.lang = language === 'en' ? 'en-US' : language;
    utt.rate = 0.9;
    utt.pitch = 1.0;
    utt.onstart = () => setVoiceState('speaking');
    utt.onend = () => setVoiceState('idle');
    utt.onerror = () => setVoiceState('idle');
    synthRef.current = utt;
    window.speechSynthesis?.speak(utt);
    setVoiceState('speaking');
  }, [messages, isStreaming, language]);

  useEffect(() => {
    if (isStreaming) setVoiceState('thinking');
  }, [isStreaming]);

  function startListening() {
    window.speechSynthesis?.cancel();
    const sw = window as SpeechWindow;
    const SR = sw.SpeechRecognition ?? sw.webkitSpeechRecognition;
    if (!SR) return;

    const rec = new SR();
    rec.lang = language === 'en' ? 'en-US' : language;
    rec.continuous = false;
    rec.interimResults = true;

    rec.onstart = () => setVoiceState('listening');
    rec.onresult = (e: SpeechResultEvent) => {
      const parts: string[] = [];
      for (let i = 0; i < e.results.length; i++) parts.push(e.results[i][0].transcript);
      const interim = parts.join('');
      setTranscript(interim);
      if (e.results[e.results.length - 1].isFinal) {
        setTranscript('');
        onTranscript(interim);
        setVoiceState('thinking');
      }
    };
    rec.onerror = () => setVoiceState('idle');
    rec.onend = () => { if (voiceState === 'listening') setVoiceState('idle'); };

    recognitionRef.current = rec;
    rec.start();
  }

  function stopListening() {
    recognitionRef.current?.stop();
    setVoiceState('idle');
  }

  useEffect(() => {
    return () => {
      recognitionRef.current?.stop();
      window.speechSynthesis?.cancel();
    };
  }, []);

  const pulse = voiceState === 'listening'
    ? 'animate-pulse bg-red-500/20 border-red-400'
    : voiceState === 'speaking'
    ? 'animate-pulse bg-acc/20 border-acc'
    : voiceState === 'thinking'
    ? 'bg-yel/10 border-yel/50'
    : 'bg-white/5 border-white/10 hover:bg-white/10';

  const label = voiceState === 'listening'
    ? t(language, 'listening')
    : voiceState === 'speaking'
    ? 'SAGE speaking…'
    : voiceState === 'thinking'
    ? 'Thinking…'
    : t(language, 'speak');

  return (
    <div
      className="fixed inset-0 z-50 bg-bg flex flex-col items-center justify-center gap-8"
      aria-live="polite"
      aria-label="Voice-only mode"
    >
      {/* Exit button */}
      <button
        onClick={() => { window.speechSynthesis?.cancel(); setVoiceOnlyMode(false); }}
        className="absolute top-4 right-4 text-t2 hover:text-t0 text-sm px-3 py-1.5 rounded-lg border border-white/10 hover:border-white/20 transition-all"
      >
        {t(language, 'exitVoice')}
      </button>

      {/* SAGE wordmark */}
      <div className="text-center">
        <div className="text-4xl font-black tracking-tight">
          S<span className="text-acc">AGE</span>
        </div>
        <div className="text-t2 text-sm mt-1">{lessonTitle}</div>
      </div>

      {/* Big mic button */}
      <button
        onClick={voiceState === 'listening' ? stopListening : startListening}
        disabled={voiceState === 'thinking' || voiceState === 'speaking'}
        className={`w-32 h-32 rounded-full border-2 transition-all duration-300 flex items-center justify-center ${pulse}`}
        aria-label={label}
      >
        <svg className="w-12 h-12 text-t0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          {voiceState === 'listening' ? (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
              d="M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
          ) : (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
              d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
          )}
        </svg>
      </button>

      {/* Status label */}
      <div className="text-t1 text-sm font-medium h-5">{label}</div>

      {/* Live transcript */}
      {transcript && (
        <div className="max-w-sm text-center text-t2 text-xs italic px-4">{transcript}</div>
      )}

      {/* Last SAGE response */}
      {(() => {
        const last = messages.filter((m) => m.role === 'assistant').at(-1);
        return last?.content ? (
          <div className="max-w-md text-center text-t1 text-sm leading-relaxed px-6 py-4 bg-white/3 rounded-2xl border border-white/5">
            {last.content
              .replace(/[*_`#~]/g, '')
              .replace(/<[^>]+>/g, '')
              .slice(0, 300)}
            {last.content.length > 300 && '…'}
          </div>
        ) : null;
      })()}
    </div>
  );
}
