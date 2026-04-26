interface ExploreSuggestedPromptsProps {
  onSelect: (prompt: string) => void;
}

const PROMPTS = [
  "I'm building a transformer from scratch and my attention scores are all going to zero after softmax — I think my scaling is wrong but I'm not sure why we divide by sqrt(d_k)",
  "I'm trying to fine-tune Llama on my own dataset but my GPU keeps running out of memory — I heard LoRA can help but I don't understand what it actually changes vs full fine-tuning",
  "How does CLIP connect vision and language? I get that it learns embeddings but I don't understand how you train on image-text pairs without any labeled categories",
  "I want to build an AI agent that can browse the web and fill out forms — how do ReAct-style agents decide when to think vs when to act, and what stops them from looping forever?",
  "What's the difference between sim-to-real transfer and domain randomization in robotics? I keep seeing both terms but they seem like the same idea",
  "I read that QLoRA uses 4-bit quantization with LoRA but I'm confused about how you can train in 4-bit without destroying the gradients — doesn't quantization kill backprop?",
];

export function ExploreSuggestedPrompts({ onSelect }: ExploreSuggestedPromptsProps) {
  return (
    <div className="w-full max-w-2xl grid grid-cols-1 sm:grid-cols-2 gap-2">
      {PROMPTS.slice(0, 4).map((p, i) => (
        <button
          key={i}
          onClick={() => onSelect(p)}
          className="text-left text-sm rounded-xl px-4 py-3 transition-colors"
          style={{
            border: "1px solid rgba(240,233,214,0.1)",
            background: "var(--ink-1)",
            color: "var(--cream-1)",
          }}
          onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(196,152,90,0.4)"; (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-0)"; }}
          onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(240,233,214,0.1)"; (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-1)"; }}
        >
          {p}
        </button>
      ))}
    </div>
  );
}
