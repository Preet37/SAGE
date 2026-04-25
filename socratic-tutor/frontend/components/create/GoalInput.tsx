"use client";
import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { ArrowRight, Loader2 } from "lucide-react";

interface GoalInputProps {
  onSubmit: (goal: string) => void;
  loading?: boolean;
}

export function GoalInput({ onSubmit, loading }: GoalInputProps) {
  const [value, setValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    textareaRef.current?.focus();
  }, []);

  function handleSubmit() {
    const trimmed = value.trim();
    if (!trimmed || loading) return;
    onSubmit(trimmed);
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }

  return (
    <div className="relative">
      <div className="rounded-xl border border-border bg-card shadow-lg overflow-hidden transition-shadow focus-within:shadow-xl focus-within:border-primary/30">
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="e.g. How LLMs work, from tokenization to RLHF..."
          rows={3}
          className="w-full resize-none bg-transparent px-5 pt-5 pb-14 text-base placeholder:text-muted-foreground/60 focus:outline-none"
          disabled={loading}
        />
        <div className="absolute bottom-3 right-3">
          <Button
            onClick={handleSubmit}
            disabled={!value.trim() || loading}
            size="sm"
            className="rounded-lg px-4 gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Creating...
              </>
            ) : (
              <>
                Build Course
                <ArrowRight className="h-4 w-4" />
              </>
            )}
          </Button>
        </div>
      </div>
      <p className="text-xs text-muted-foreground mt-2 text-center">
        Press Enter to submit, Shift+Enter for new line
      </p>
    </div>
  );
}
