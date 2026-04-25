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
    concepts.length > 1 ? `How does ${concepts[0]} relate to ${concepts[1]}?` : `What's a real-world example of ${concepts[0]}?`,
  ];
}

export function SuggestedPrompts({ lessonTitle, concepts, onSelect }: SuggestedPromptsProps) {
  const prompts = [
    `What's the key intuition behind "${lessonTitle}"?`,
    ...conceptPrompts(concepts),
    ...BASE_PROMPTS,
  ].slice(0, 4);

  return (
    <div className="w-full max-w-2xl grid grid-cols-1 sm:grid-cols-2 gap-2">
      {prompts.map((p, i) => (
        <button
          key={i}
          onClick={() => onSelect(p)}
          className="text-left text-sm rounded-xl border border-border px-4 py-3
            hover:border-primary/50 hover:bg-accent hover:text-accent-foreground transition-colors"
        >
          {p}
        </button>
      ))}
    </div>
  );
}
