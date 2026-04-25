"use client";

import { useEffect, useRef, useState } from "react";

interface VoiceAgentProps {
  onTranscript: (text: string) => void;
}

interface SpeechResultLike {
  isFinal: boolean;
  0: { transcript: string };
}
interface SpeechResultsLike {
  length: number;
  [i: number]: SpeechResultLike;
}
interface SpeechRecognitionEventLike {
  resultIndex: number;
  results: SpeechResultsLike;
}
interface SpeechRecognitionLike {
  lang: string;
  interimResults: boolean;
  continuous: boolean;
  onresult: ((e: SpeechRecognitionEventLike) => void) | null;
  onerror: ((e: unknown) => void) | null;
  onend: (() => void) | null;
  start: () => void;
  stop: () => void;
}

type Ctor = new () => SpeechRecognitionLike;

function getSpeech(): Ctor | null {
  if (typeof window === "undefined") return null;
  const w = window as unknown as {
    SpeechRecognition?: Ctor;
    webkitSpeechRecognition?: Ctor;
  };
  return w.SpeechRecognition ?? w.webkitSpeechRecognition ?? null;
}

export default function VoiceAgent({ onTranscript }: VoiceAgentProps) {
  const recRef = useRef<SpeechRecognitionLike | null>(null);
  const [supported, setSupported] = useState(true);
  const [listening, setListening] = useState(false);

  useEffect(() => {
    setSupported(getSpeech() !== null);
  }, []);

  useEffect(() => {
    return () => recRef.current?.stop();
  }, []);

  const start = () => {
    const Ctor = getSpeech();
    if (!Ctor) return;
    const rec = new Ctor();
    rec.lang = "en-US";
    rec.interimResults = false;
    rec.continuous = false;
    rec.onresult = (e) => {
      let text = "";
      for (let i = e.resultIndex; i < e.results.length; i++) {
        if (e.results[i].isFinal) text += e.results[i][0].transcript;
      }
      if (text) onTranscript(text.trim());
    };
    rec.onerror = () => setListening(false);
    rec.onend = () => setListening(false);
    rec.start();
    recRef.current = rec;
    setListening(true);
  };

  const stop = () => {
    recRef.current?.stop();
    setListening(false);
  };

  return (
    <div
      className="rounded-2xl p-4"
      style={{ background: "var(--color-muted)", border: "1px solid var(--color-border)" }}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-semibold">Voice input</p>
          <p className="text-xs opacity-60">
            {supported ? "Tap to dictate your question." : "Not supported in this browser."}
          </p>
        </div>
        <button
          type="button"
          onClick={listening ? stop : start}
          disabled={!supported}
          className="rounded-full px-3 py-1.5 text-xs font-semibold disabled:opacity-50"
          style={{
            background: listening ? "var(--color-destructive)" : "var(--color-primary)",
            color: "white",
            cursor: "pointer",
          }}
        >
          {listening ? "Stop" : "Speak"}
        </button>
      </div>
    </div>
  );
}
