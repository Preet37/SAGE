const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };

interface Mode {
  id: string;
  label: string;
  description: string;
}

const MODES: Mode[] = [
  { id: "default",   label: "Default",   description: "Balanced explanation" },
  { id: "eli5",      label: "ELI5",      description: "Simple analogies" },
  { id: "analogy",   label: "Analogy",   description: "Real-world comparisons" },
  { id: "code",      label: "Code",      description: "Code-first examples" },
  { id: "deep_dive", label: "Deep Dive", description: "Mathematical depth" },
];

interface ExplainDifferentlyBarProps {
  activeMode: string;
  onModeChange: (mode: string) => void;
}

export function ExplainDifferentlyBar({ activeMode, onModeChange }: ExplainDifferentlyBarProps) {
  return (
    <div style={{ maxWidth: "48rem", margin: "0 auto", padding: "0.5rem 1rem 0" }}>
      <div style={{ display: "flex", alignItems: "center", gap: "0.35rem" }}>
        <span style={{ ...mono, fontSize: "0.48rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)", marginRight: "0.25rem", flexShrink: 0 }}>
          Mode:
        </span>
        {MODES.map((mode) => {
          const isActive = activeMode === mode.id;
          return (
            <button
              key={mode.id}
              onClick={() => onModeChange(mode.id)}
              title={mode.description}
              style={{
                ...mono,
                fontSize: "0.48rem",
                letterSpacing: "0.08em",
                textTransform: "uppercase",
                padding: "0.25rem 0.6rem",
                flexShrink: 0,
                background: isActive ? "rgba(196,152,90,0.15)" : "transparent",
                color: isActive ? "var(--gold)" : "var(--cream-2)",
                border: isActive ? "1px solid rgba(196,152,90,0.35)" : "1px solid transparent",
                cursor: "pointer",
                transition: "all 0.15s",
              }}
            >
              {mode.label}
            </button>
          );
        })}
      </div>
    </div>
  );
}
