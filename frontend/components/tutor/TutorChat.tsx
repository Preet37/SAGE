'use client';
import { useRef, useEffect, useState, KeyboardEvent } from 'react';
import { useTutorStore } from '@/lib/store';
import MessageBubble from './MessageBubble';

interface Props {
  onSend: (text: string) => void;
  lesson: { title: string; key_concepts: string[] };
}

const STARTERS = [
  "What's the core idea behind this?",
  "Can you give me an example?",
  "I'm confused about...",
  "How does this relate to...",
];

export default function TutorChat({ onSend, lesson }: Props) {
  const { messages, isStreaming } = useTutorStore();
  const [input, setInput] = useState('');
  const bottomRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  }

  function submit() {
    const text = input.trim();
    if (!text || isStreaming) return;
    setInput('');
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
    onSend(text);
  }

  function autoResize(e: React.ChangeEvent<HTMLTextAreaElement>) {
    setInput(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
  }

  return (
    <div className="flex flex-col h-full">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-5 py-5 space-y-4">
        {messages.map(msg => (
          <MessageBubble key={msg.id} message={msg} />
        ))}

        {/* Typing indicator */}
        {isStreaming && messages[messages.length - 1]?.content === '' && (
          <div className="flex gap-1.5 px-3 py-2 bg-bg2 border border-white/5 rounded-2xl rounded-tl-sm w-fit">
            {[0, 1, 2].map(i => (
              <div
                key={i}
                className="w-1.5 h-1.5 rounded-full bg-t2"
                style={{ animation: `typing 1.2s ease infinite ${i * 0.2}s` }}
              />
            ))}
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Quick starters */}
      {messages.length <= 1 && (
        <div className="px-4 pb-2">
          <div className="flex flex-wrap gap-2">
            {STARTERS.map(s => (
              <button
                key={s}
                onClick={() => onSend(s)}
                className="text-xs text-t2 bg-bg2 border border-white/5 hover:border-acc/25 hover:text-acc rounded-full px-3 py-1.5 transition-all"
              >
                {s}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <div className="flex-shrink-0 px-4 pb-4 pt-2 border-t border-white/5">
        <div className={`flex items-end gap-2 bg-bg2 border rounded-2xl px-4 py-3 transition-all ${isStreaming ? 'border-white/5' : 'border-white/10 focus-within:border-acc/40'}`}>
          <textarea
            ref={textareaRef}
            value={input}
            onChange={autoResize}
            onKeyDown={handleKeyDown}
            placeholder={isStreaming ? 'SAGE is thinking…' : 'Ask anything…'}
            disabled={isStreaming}
            rows={1}
            className="flex-1 bg-transparent outline-none resize-none text-sm text-t0 placeholder-t3 max-h-28 font-sans"
          />
          <button
            onClick={submit}
            disabled={isStreaming || !input.trim()}
            className="w-8 h-8 rounded-full bg-acc text-white flex items-center justify-center flex-shrink-0 hover:bg-blue-400 transition-all disabled:opacity-30 disabled:cursor-not-allowed"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" className="w-3.5 h-3.5">
              <path d="M22 2L11 13M22 2L15 22l-4-9-9-4 20-7z" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
