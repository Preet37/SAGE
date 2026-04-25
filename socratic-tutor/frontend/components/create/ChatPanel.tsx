"use client";
import { useState, useRef, useEffect } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { Send, Loader2, Sparkles, RefreshCw, Check, X } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { useCreatorState, PendingAction } from "@/lib/useCreatorState";

function stripActionBlocks(text: string): string {
  return text
    .replace(/```json\s*\n[\s\S]*?"draft_actions"[\s\S]*?\n```/g, "")
    .replace(/```json\s*\n[\s\S]*?"outline_actions"[\s\S]*?\n```/g, "")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

interface ChatPanelProps {
  state: ReturnType<typeof useCreatorState>;
}

export function ChatPanel({ state }: ChatPanelProps) {
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [state.chatMessages]);

  function handleSend() {
    const trimmed = input.trim();
    if (!trimmed || state.chatStreaming) return;
    setInput("");
    state.sendChat(trimmed);
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  const hasMessages = state.chatMessages.length > 0;

  return (
    <div className="flex flex-col h-full min-h-0 bg-card/30">
      {/* Chat header */}
      <div className="flex items-center gap-2 px-4 py-3 border-b border-border shrink-0">
        <Sparkles className="h-4 w-4 text-primary" />
        <span className="text-sm font-medium">Course Assistant</span>
      </div>

      {/* Messages */}
      <ScrollArea className="flex-1 min-h-0 px-4">
        <div className="py-4 space-y-4">
          {!hasMessages && (
            <WelcomeMessage phase={state.phase} generating={state.generating} />
          )}
          {state.chatMessages.map((msg) => (
            <div key={msg.id} className={`flex flex-col ${msg.role === "user" ? "items-end" : "items-start"}`}>
              <div
                className={`max-w-[85%] rounded-xl px-3.5 py-2.5 text-sm leading-relaxed ${
                  msg.role === "user"
                    ? "bg-primary text-primary-foreground"
                    : "bg-muted/50"
                }`}
              >
                {msg.role === "assistant" ? (
                  <div className="prose prose-sm dark:prose-invert max-w-none prose-p:my-1 prose-headings:my-2 prose-ul:my-1 prose-li:my-0">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {stripActionBlocks(msg.content || "...")}
                    </ReactMarkdown>
                  </div>
                ) : (
                  msg.content
                )}
              </div>
              {/* Inline pending action cards */}
              {msg.pendingActions && msg.pendingActions.length > 0 && (
                <div className="mt-2 max-w-[85%] space-y-2">
                  {msg.pendingActions.map((action) => (
                    <PendingActionCard
                      key={action.id}
                      action={action}
                      onApprove={() => state.approvePendingAction(msg.id, action.id)}
                      onDismiss={() => state.dismissPendingAction(msg.id, action.id)}
                    />
                  ))}
                </div>
              )}
            </div>
          ))}
          {state.chatStreaming && (
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <Loader2 className="h-3 w-3 animate-spin" />
              Thinking...
            </div>
          )}
          <div ref={bottomRef} />
        </div>
      </ScrollArea>

      {/* Input */}
      <div className="p-3 border-t border-border shrink-0">
        <div className="flex items-end gap-2">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Refine your course..."
            rows={1}
            className="flex-1 resize-none rounded-lg border border-border bg-background px-3 py-2 text-sm placeholder:text-muted-foreground/60 focus:outline-none focus:border-primary/40 min-h-[36px] max-h-[120px]"
            disabled={state.chatStreaming}
          />
          <Button
            size="sm"
            className="h-9 w-9 p-0 shrink-0"
            onClick={handleSend}
            disabled={!input.trim() || state.chatStreaming}
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}

function PendingActionCard({
  action,
  onApprove,
  onDismiss,
}: {
  action: PendingAction;
  onApprove: () => void;
  onDismiss: () => void;
}) {
  const isDone = action.status === "approved" || action.status === "skipped";

  return (
    <div className={`rounded-lg border border-border bg-background px-3 py-2.5 text-sm transition-opacity ${isDone ? "opacity-50" : ""}`}>
      <div className="flex items-start gap-2">
        <RefreshCw className={`h-3.5 w-3.5 mt-0.5 shrink-0 text-muted-foreground ${action.status === "loading" ? "animate-spin" : ""}`} />
        <div className="flex-1 min-w-0">
          <p className="font-medium text-xs text-foreground leading-snug">{action.label}</p>
          <p className="text-xs text-muted-foreground mt-0.5">Full lesson regeneration from wiki</p>
        </div>
      </div>
      {!isDone && action.status !== "loading" && (
        <div className="flex gap-1.5 mt-2 justify-end">
          <Button
            variant="ghost"
            size="sm"
            className="h-6 px-2 text-xs gap-1 text-muted-foreground"
            onClick={onDismiss}
          >
            <X className="h-3 w-3" />
            Skip
          </Button>
          <Button
            variant="secondary"
            size="sm"
            className="h-6 px-2 text-xs gap-1"
            onClick={onApprove}
          >
            <Check className="h-3 w-3" />
            Approve
          </Button>
        </div>
      )}
      {action.status === "approved" && (
        <p className="text-xs text-green-600 mt-1.5 flex items-center gap-1">
          <Check className="h-3 w-3" /> Regeneration started
        </p>
      )}
      {action.status === "skipped" && (
        <p className="text-xs text-muted-foreground mt-1.5">Skipped</p>
      )}
    </div>
  );
}

function WelcomeMessage({ phase, generating }: { phase: string; generating: boolean }) {
  if (generating) {
    return (
      <div className="flex items-center gap-3 text-sm text-muted-foreground py-8 justify-center">
        <Loader2 className="h-4 w-4 animate-spin" />
        <span>Generating your course outline...</span>
      </div>
    );
  }

  const tips: Record<string, string[]> = {
    shaping: [
      "\"Add a hands-on section on fine-tuning\"",
      "\"Make this more beginner-friendly\"",
      "\"Remove the math-heavy parts\"",
      "\"Split the attention lesson into two\"",
    ],
    building: [
      "Content is being generated — feel free to ask questions about the course!",
    ],
    reviewing: [
      "\"Remove the duplicate links in the intro lesson\"",
      "\"Add an example of backprop to lesson 3\"",
      "\"Simplify the math section of the transformer lesson\"",
      "\"Regenerate lesson 2 with more depth on gradients\"",
    ],
    published: [
      "Your course is published! Head to the Learn section to start studying.",
    ],
  };

  const suggestions = tips[phase] || tips.shaping;

  return (
    <div className="py-8 space-y-4 text-center">
      <p className="text-sm text-muted-foreground">
        {phase === "shaping"
          ? "Your outline is ready. Tell me how to refine it, or explore the tabs on the right."
          : phase === "reviewing"
            ? "Review your lessons. Tell me if anything needs changes."
            : ""}
      </p>
      <div className="space-y-1.5">
        {suggestions.map((tip, i) => (
          <p key={i} className="text-xs text-muted-foreground/70 italic">
            {tip}
          </p>
        ))}
      </div>
    </div>
  );
}
