# Card: LinkedIn Talent Search/RecSys Production Architecture (SIGIR’18)
**Source:** https://engineering.linkedin.com/content/dam/me/engineering/li-en/research/SIGIR-2018.pdf  
**Role:** paper | **Need:** DEPLOYMENT_CASE  
**Anchor:** End-to-end production retrieval/ranking architecture + operational constraints/trade-offs (multi-pass ranking, logging, offline training, near-real-time index updates)

## Key Content
- **Problem setting (scale + query complexity):** Rank “most relevant candidates in real-time among **hundreds of millions** of structured member profiles.” Queries can combine **structured facets** (canonical title(s), canonical skill(s), company name, region) + **unstructured free-text keywords**.
- **Two-sided objective / metrics rationale:** Talent search requires **mutual interest**: not only candidate relevance to recruiter query, but also candidate interest in the opportunity. Example optimization/AB metrics mentioned: likelihood of **receiving an InMail** and **responding positively**; “ideal” metrics like job offer/accept may be **unavailable or delayed**.
- **Online serving architecture (Figure 1):**
  - Input: recruiter request (explicit query or implicit via **job opening / ideal candidate(s)**) + recruiter/session context.
  - Transform into complex query; issue to LinkedIn **Galene** search engine.
  - **Retrieve candidate set** from search index.
  - **Multi-pass ranking** with ML scoring models “of varying complexity.”
  - Return top-ranked candidates to frontend; **log recruiter interactions**.
  - Search index updated in **near real-time** as member data changes.
- **Offline modeling pipeline (Figure 2):**
  - Periodically train ranking models using **recruiter usage logs**.
  - Training labels from recruiter interactions + candidate responses to messages.
  - **Log computed features at serving time** along with shown results (instead of recomputing later) because member data changes over time.
  - Pipeline designed for **feature engineering ease**, supporting different model types, and **experimentation agility**.
- **No equations/hyperparameters/numeric benchmarks** provided in this 2-page paper.

## When to surface
Use when students ask how large-scale search/recommendation systems are deployed end-to-end (retrieval → multi-pass ranking → logging → offline training), or why production systems log features and use proxy metrics under latency/data-delay constraints.