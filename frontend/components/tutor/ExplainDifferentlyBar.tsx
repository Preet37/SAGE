import { cn } from "@/lib/utils";

interface Mode {
  id: string;
  label: string;
  description: string;
}

const MODES: Mode[] = [
  { id: "default", label: "Default", description: "Balanced explanation" },
  { id: "eli5", label: "ELI5", description: "Simple analogies" },
  { id: "analogy", label: "Analogy", description: "Real-world comparisons" },
  { id: "code", label: "Code", description: "Code-first examples" },
  { id: "deep_dive", label: "Deep Dive", description: "Mathematical depth" },
];

interface ExplainDifferentlyBarProps {
  activeMode: string;
  onModeChange: (mode: string) => void;
}

export function ExplainDifferentlyBar({ activeMode, onModeChange }: ExplainDifferentlyBarProps) {
  return (
    <div className="max-w-3xl mx-auto px-4 pt-2">
      <div className="flex items-center gap-1.5">
        <span className="text-xs text-muted-foreground mr-1 flex-shrink-0">Mode:</span>
        {MODES.map((mode) => (
          <button
            key={mode.id}
            onClick={() => onModeChange(mode.id)}
            title={mode.description}
            className={cn(
              "text-xs px-3 py-1.5 rounded-lg transition-colors flex-shrink-0",
              activeMode === mode.id
                ? "bg-primary text-primary-foreground"
                : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
            )}
          >
            {mode.label}
          </button>
        ))}
      </div>
    </div>
  );
}
