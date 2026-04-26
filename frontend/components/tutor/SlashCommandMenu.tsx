"use client";
import { useEffect, useRef } from "react";

export interface SlashCommand {
  name: string;
  description: string;
}

export const SLASH_COMMANDS: SlashCommand[] = [
  { name: "quiz", description: "Generate a knowledge check on the current concept" },
  { name: "hint", description: "Get a small nudge without spoiling the answer" },
  { name: "simpler", description: "Re-explain the previous answer in simpler terms" },
  { name: "deeper", description: "Go deeper on the current topic with rigor" },
  { name: "feedback", description: "Get feedback on your understanding so far" },
];

export function matchSlashCommands(input: string): SlashCommand[] | null {
  if (!input.startsWith("/")) return null;
  const head = input.slice(1).split(/\s/, 1)[0]?.toLowerCase() ?? "";
  // Only show the menu while the user is still typing the command (no space yet).
  if (input.includes(" ")) return null;
  return SLASH_COMMANDS.filter((c) => c.name.startsWith(head));
}

interface SlashCommandMenuProps {
  matches: SlashCommand[];
  activeIndex: number;
  onSelect: (cmd: SlashCommand) => void;
  onHover: (index: number) => void;
}

export function SlashCommandMenu({
  matches,
  activeIndex,
  onSelect,
  onHover,
}: SlashCommandMenuProps) {
  const listRef = useRef<HTMLUListElement>(null);

  useEffect(() => {
    const item = listRef.current?.children[activeIndex] as HTMLElement | undefined;
    item?.scrollIntoView({ block: "nearest" });
  }, [activeIndex]);

  if (matches.length === 0) return null;

  return (
    <div
      role="listbox"
      aria-label="Slash command suggestions"
      className="absolute bottom-full left-0 right-0 mb-2 rounded-xl border border-border bg-popover shadow-lg overflow-hidden z-30"
    >
      <ul ref={listRef} className="max-h-60 overflow-y-auto py-1">
        {matches.map((cmd, i) => (
          <li
            key={cmd.name}
            role="option"
            aria-selected={i === activeIndex}
            onMouseEnter={() => onHover(i)}
            onMouseDown={(e) => {
              // mousedown fires before the textarea blur, so the click registers.
              e.preventDefault();
              onSelect(cmd);
            }}
            className={`flex items-baseline gap-2 px-3 py-2 cursor-pointer text-sm ${
              i === activeIndex
                ? "bg-primary/10 text-foreground"
                : "text-foreground hover:bg-muted/50"
            }`}
          >
            <span className="font-mono font-medium text-primary">/{cmd.name}</span>
            <span className="text-xs text-muted-foreground truncate">
              {cmd.description}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
