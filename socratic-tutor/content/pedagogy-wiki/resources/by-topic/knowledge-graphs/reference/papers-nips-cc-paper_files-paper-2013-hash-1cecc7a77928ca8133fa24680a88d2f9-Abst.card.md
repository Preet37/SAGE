# Card: TransE scoring + margin ranking loss
**Source:** https://papers.nips.cc/paper_files/paper/2013/hash/1cecc7a77928ca8133fa24680a88d2f9-Abstract.html  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Primary TransE scoring function \(f_r(h,t)=\lVert h+r-t\rVert\) (L1/L2), margin-based ranking loss with negative sampling (“corruption”), and core training setup.

## Key Content
- **Embedding model (TransE):** represent each **entity** \(e\) as a vector \( \mathbf{e}\in\mathbb{R}^k\) and each **relation** \(r\) as a vector \( \mathbf{r}\in\mathbb{R}^k\). For a triple \((h,r,t)\), enforce the translation intuition:  
  \[
  \mathbf{h} + \mathbf{r} \approx \mathbf{t}
  \]
- **Scoring function (Eq. 1 / core definition):**  
  \[
  f_r(h,t)=\lVert \mathbf{h}+\mathbf{r}-\mathbf{t}\rVert_{1/2}
  \]
  where \(\lVert\cdot\rVert_{1}\) or \(\lVert\cdot\rVert_{2}\) is used; **lower score = more plausible triple**.
- **Training objective (margin-based ranking loss):** for each positive triple \((h,r,t)\in S\), generate a set of **corrupted negatives** \(S'_{(h,r,t)}\) by replacing **head or tail** (keeping relation fixed), e.g. \((h',r,t)\) or \((h,r,t')\). Minimize:
  \[
  \sum_{(h,r,t)\in S}\ \sum_{(h',r,t')\in S'_{(h,r,t)}} \big[\gamma + f_r(h,t) - f_r(h',t')\big]_+
  \]
  where \([\cdot]_+=\max(0,\cdot)\) and \(\gamma\) is the **margin**.
- **Procedure (workflow):** iterate over training triples → sample corrupted negatives → compute hinge loss → update embeddings via SGD-style optimization; choose L1 vs L2 distance as a design choice.

## When to surface
Use when students ask: “What is TransE’s scoring function?”, “How does TransE generate negatives?”, or “What loss does TransE optimize for knowledge graph triples?”