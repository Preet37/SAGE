const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };
const body: React.CSSProperties = { fontFamily: "var(--font-crimson)" };

interface SuggestedPromptsProps {
  lessonTitle: string;
  concepts: string[];
  onSelect: (prompt: string) => void;
}

const BASE_PROMPTS = [
  "Can you give me an overview of this lesson?",
  "What should I focus on to understand this topic?",
  "How does this connect to what I've learned before?",
];

function conceptPrompts(concepts: string[]): string[] {
  if (concepts.length === 0) return [];
  return [
    `Explain ${concepts[0]} in simple terms`,
    concepts.length > 1
      ? `How does ${concepts[0]} relate to ${concepts[1]}?`
      : `What's a real-world example of ${concepts[0]}?`,
  ];
}

export function SuggestedPrompts({ lessonTitle, concepts, onSelect }: SuggestedPromptsProps) {
  const prompts = [
    `What's the key intuition behind "${lessonTitle}"?`,
    ...conceptPrompts(concepts),
    ...BASE_PROMPTS,
  ].slice(0, 4);

  return (
    <div style={{ width: "100%", maxWidth: "42rem", display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: "0.5rem" }}>
      {prompts.map((p, i) => (
        <button
          key={i}
          onClick={() => onSelect(p)}
          style={{
            ...body,
            textAlign: "left",
            fontSize: "0.9rem",
            color: "var(--cream-1)",
            background: "var(--ink-1)",
            border: "1px solid rgba(240,233,214,0.08)",
            padding: "0.75rem 1rem",
            cursor: "pointer",
            lineHeight: 1.4,
            transition: "border-color 0.15s, color 0.15s",
          }}
          onMouseEnter={e => {
            (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(196,152,90,0.35)";
            (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-0)";
          }}
          onMouseLeave={e => {
            (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(240,233,214,0.08)";
            (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-1)";
          }}
        >
          {p}
        </button>
      ))}
    </div>
  );
}
