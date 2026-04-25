# Card: Tree of Thoughts (ToT) = deliberate search over “thoughts”
**Source:** https://proceedings.neurips.cc/paper_files/paper/2023/file/271db9922b8d1f4dd7aaef84ed5ac703-Paper-Conference.pdf  
**Role:** paper | **Need:** COMPARISON_DATA  
**Anchor:** Explicit ToT search procedure (generate–evaluate–select/backtrack) + compute-vs-performance vs linear CoT

## Key Content
- **LM sequence model (Sec. 2):** For tokens \(x=(x[1],...,x[n])\), \(p_\theta(x)=\prod_{i=1}^n p_\theta(x[i]\mid x[1..i])\).  
  IO prompting: \(y\sim p^{IO}_\theta(y\mid x)\).  
  CoT: sample thoughts sequentially \(z_i\sim p^{CoT}_\theta(z_{i}\mid x,z_{1..i-1})\), then \(y\sim p^{CoT}_\theta(y\mid x,z_{1..n})\).  
  CoT-SC: sample \(k\) chains, return \(\arg\max_y \#\{i\mid y^{(i)}=y\}\).
- **ToT framing (Sec. 3):** search tree over **states** \(s=[x,z_{1..i}]\) (partial solution). Instantiation choices: (1) thought decomposition granularity; (2) generator \(G(p_\theta,s,k)\); (3) evaluator \(V(p_\theta,S)\); (4) search algorithm.
- **Thought decomposition rationale:** thoughts must be “small enough” for diverse generation but “big enough” for evaluability; examples: word (crosswords), equation line (24), paragraph plan (writing).
- **Generation (Sec. 3.2):** (a) i.i.d. sampling \(z^{(j)}\sim p^{CoT}_\theta(z_{i+1}\mid s)\) for rich spaces; (b) sequential “propose prompt” \([z^{(1)}..z^{(k)}]\sim p^{propose}_\theta(z_{i+1}^{(1..k)}\mid s)\) to reduce duplicates in constrained spaces.
- **Evaluation (Sec. 3.3):** (a) value each state \(V(s)\sim p^{value}_\theta(v\mid s)\) (scalar or classes like sure/maybe/impossible); (b) vote: pick best \(s^*\sim p^{vote}_\theta(s^*\mid S)\).
- **Search algorithms (Sec. 3.4):**
  - **ToT-BFS (Alg. 1):** expand frontier with \(k\) thoughts/state; score via \(V\); keep top breadth \(b\) each step up to depth \(T\).
  - **ToT-DFS (Alg. 2):** explore best-first with pruning if \(V(s)\le v_{th}\); **backtrack** on prune/failure.
- **Empirical results (GPT-4, Game of 24; Table 2):** IO 7.3%, CoT 4.0%, CoT-SC(k=100) 9.0%, ToT(b=1) 45%, **ToT(b=5) 74%**; IO+Refine(k=10) 27%; best-of-100: IO 33%, CoT 49%.
- **Compute/cost (App. B.3, Table 7):** Game of 24 per case: IO(best-of-100) 1.8k completion/1.0k prompt tokens, $0.13, 33%; CoT(best-of-100) 6.7k/2.2k, $0.47, 49%; **ToT 5.5k/1.4k, $0.74, 74%**.
- **Default experimental knobs:** GPT-4 chat completion, temperature 0.7; Game of 24 ToT: BFS, depth \(T=3\), breadth \(b=5\), propose prompt, value prompt (“sure/maybe/impossible”), sample values 3× per thought.

## When to surface
Use when students ask how “agentic” LLM reasoning differs from linear CoT, or how adding search (BFS/DFS), self-evaluation, and backtracking trades extra compute for large performance gains.