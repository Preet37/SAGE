'use client';
import { useRef, useEffect, useState, KeyboardEvent } from 'react';
import { useTutorStore } from '@/lib/store';
import MessageBubble from './MessageBubble';
import VisualUpload from '@/components/cloudinary/VisualUpload';

interface Props {
  onSend: (text: string, imageUrl?: string, extractedText?: string) => void;
  lesson: { id: number; title: string; key_concepts: string[] };
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
  const [pendingImage, setPendingImage] = useState<{ url: string; text: string } | null>(null);
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
    if ((!text && !pendingImage) || isStreaming) return;
    setInput('');
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
    onSend(
      text || (pendingImage ? 'What does this show?' : ''),
      pendingImage?.url,
      pendingImage?.text,
    );
    setPendingImage(null);
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

      {/* Pending image preview */}
      {pendingImage && (
        <div className="mx-4 mb-2 flex items-center gap-2 p-2 rounded-xl bg-ora/5 border border-ora/20">
          <img
            src={pendingImage.url}
            alt="pending"
            className="w-12 h-12 object-cover rounded-lg flex-shrink-0"
          />
          <div className="flex-1 min-w-0">
            <div className="text-[10px] font-bold text-ora uppercase tracking-widest">Image attached</div>
            <div className="text-[10px] text-t2 truncate">
              {pendingImage.text ? `OCR: ${pendingImage.text.slice(0, 80)}…` : 'no text detected'}
            </div>
          </div>
          <button
            onClick={() => setPendingImage(null)}
            className="text-t3 hover:text-t0 text-xs px-2"
            aria-label="Remove image"
          >
            ×
          </button>
        </div>
      )}

      {/* Input */}
      <div className="flex-shrink-0 px-4 pb-4 pt-2 border-t border-white/5">
        <div className={`flex items-end gap-2 bg-bg2 border rounded-2xl px-4 py-3 transition-all ${isStreaming ? 'border-white/5' : 'border-white/10 focus-within:border-acc/40'}`}>
          <VisualUpload
            lessonId={lesson.id}
            disabled={isStreaming}
            onUpload={(url, text) => setPendingImage({ url, text })}
          />
          <textarea
            ref={textareaRef}
            value={input}
            onChange={autoResize}
            onKeyDown={handleKeyDown}
            placeholder={isStreaming ? 'SAGE is thinking…' : pendingImage ? 'Ask about the image…' : 'Ask anything…'}
            disabled={isStreaming}
            rows={1}
            className="flex-1 bg-transparent outline-none resize-none text-sm text-t0 placeholder-t3 max-h-28 font-sans"
          />
          <button
            onClick={submit}
            disabled={isStreaming || (!input.trim() && !pendingImage)}
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
