export function splitIntoChunks(text: string): string[] {
  return text
    .split(/\n\n+/)
    .map((c) => c.trim())
    .filter(Boolean);
}

function tokenize(text: string): string[] {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .split(/\s+/)
    .filter(Boolean);
}

function termFreq(tokens: string[]): Map<string, number> {
  const freq = new Map<string, number>();
  for (const t of tokens) freq.set(t, (freq.get(t) ?? 0) + 1);
  return freq;
}

export function retrieveTopK(query: string, chunks: string[], k = 3): string[] {
  if (chunks.length === 0) return [];
  const queryTokens = new Set(tokenize(query));
  const idfBase = Math.log(chunks.length + 1);

  return chunks
    .map((chunk) => {
      const tokens = tokenize(chunk);
      const freq = termFreq(tokens);
      let score = 0;
      for (const qt of queryTokens) {
        const tf = freq.get(qt) ?? 0;
        if (tf > 0) score += (tf / tokens.length) * idfBase;
      }
      return { chunk, score };
    })
    .sort((a, b) => b.score - a.score)
    .slice(0, k)
    .map(({ chunk }) => chunk);
}
