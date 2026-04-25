---
title: "Knowledge Graphs & Structured Knowledge"
subject: "Agents & Reasoning"
date: 2026-04-09
tags:
  - "subject/agents-and-reasoning"
  - "level/beginner"
  - "level/intermediate"
  - "level/advanced"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  []
levels:
  - "beginner"
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# Knowledge Graphs

## Video (best)
- **Stanford Online (Dan Jurafsky & Chris Manning)** — "Introduction to Information Extraction (Relation Extraction)" (CS224U lecture)
- youtube_id: "None identified"  
- Why: Clear, foundational treatment of extracting entities/relations that directly supports knowledge graph construction.
- Level: Intermediate

## Blog / Written explainer (best)
- **Neo4j** — "What is a Knowledge Graph?"
- url: https://neo4j.com/blog/knowledge-graph/what-is-knowledge-graph [VERIFY]
- Why: Practical, accessible definition of knowledge graphs with emphasis on entities/relations and graph modeling.
- Level: Beginner

## Deep dive
- **W3C** — "RDF 1.1 Concepts and Abstract Syntax"
- **Link:** [https://www.w3.org/TR/rdf11-concepts/](https://www.w3.org/TR/rdf11-concepts/)
- Why: Authoritative deep dive into triples, IRIs, graphs, and the formal model underlying many knowledge graphs.
- Level: Intermediate–Advanced

## Original paper
- **Tim Berners-Lee, James Hendler, Ora Lassila (2001)** — "The Semantic Web"
- url: https://www.scientificamerican.com/article/the-semantic-web/ [VERIFY]
- Why: Seminal vision paper that motivated RDF/ontologies and the modern “linked data” view of knowledge graphs.
- Level: Intermediate

## Code walkthrough
- **Neo4j Developer Guides** — "RDF & Semantic Web" (importing/working with RDF in Neo4j)
- url: https://neo4j.com/use-cases/knowledge-graph [VERIFY]
- Why: Hands-on walkthroughs for representing triples and integrating RDF-style data with a property graph workflow.
- Level: Intermediate

## Coverage notes
- Strong: RDF/triples foundations; practical “what is a KG” framing; IE background for entity/relation extraction.
- Weak: Ontology engineering workflows (e.g., OWL modeling patterns) are not covered in a single best-in-class resource above.
- Gap: GraphRAG / graph retrieval / structured grounding: no single, widely-cited canonical tutorial/video identified here; consider adding a dedicated GraphRAG explainer + reference implementation once a stable, well-known source is selected.

---

## Additional Resources for Tutor Depth

> **9 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 ComplEx scoring + logistic NLL objective
**Paper** · [source](https://arxiv.org/pdf/1606.06357.pdf)

*ComplEx scoring function (complex tri-linear product with conjugation) + training objective for link prediction*

<details>
<summary>Key content</summary>

- **Link prediction probability (single relation):**  
  \(P(Y_{so}=1)=\sigma(X_{so})\) (Eq. 1), where \(Y_{so}\in\{-1,1\}\), \(\sigma(x)=\frac{1}{1+e^{-x}}\), and \(X_{so}\) is a real-valued score.
- **Hermitian dot product (complex vectors):**  
  \(\langle u,v\rangle := \overline{u}^{\top}v\) (Eq. 3), with \(u=\Re(u)+i\Im(u)\), \(\overline{u}=\Re(u)-i\Im(u)\). Conjugation breaks symmetry → can model antisymmetry.
- **ComplEx multi-relational scoring:**  
  \(P(Y_{rso}=1)=\sigma(\phi(r,s,o;\Theta))\) (Eq. 8) with  
  \(\phi(r,s,o;\Theta)=\Re(\langle w_r, e_s, \overline{e_o}\rangle)\) (Eq. 9)  
  \(=\Re\left(\sum_{k=1}^{K} w_{rk} e_{sk}\overline{e_{ok}}\right)\) (Eq. 10), where \(e_s,e_o,w_r\in\mathbb{C}^K\).  
  Real-only expansion (Eq. 11):  
  \(\langle \Re(w_r),\Re(e_s),\Re(e_o)\rangle+\langle \Re(w_r),\Im(e_s),\Im(e_o)\rangle+\langle \Im(w_r),\Re(e_s),\Im(e_o)\rangle-\langle \Im(w_r),\Im(e_s),\Re(e_o)\rangle\).  
  Symmetric if \(w_r\) real; antisymmetric if \(w_r\) purely imaginary.
- **Training objective (logistic negative log-likelihood):**  
  \(\min_{\Theta}\sum_{r(s,o)\in\Omega}\log(1+\exp(-Y_{rso}\phi(r,s,o;\Theta)))+\lambda\|\Theta\|_2^2\) (Eq. 12).  
  Negatives via **local closed world**: corrupt subject or object; generate \(\eta\) negatives per positive (runtime).
- **Optimization defaults:** mini-batch SGD + AdaGrad; early stopping on validation filtered MRR (checked every 50 epochs; max 1000). Grid: \(K\in\{10,20,50,100,150,200\}\), \(\lambda\in\{0.1,0.03,0.01,0.003,0.001,0.0003,0\}\), \(\alpha_0\in\{1.0,0.5,0.2,0.1,0.05,0.02,0.01\}\), \(\eta\in\{1,2,5,10\}\); batch size 100.
- **Key empirical results (Table 2):**  
  WN18 filtered MRR: ComplEx **0.941** (DistMult 0.822; TransE 0.454; HolE 0.938).  
  FB15K filtered MRR: ComplEx **0.692** (DistMult 0.654; HolE 0.524; TransE 0.380). Hits@1 FB15K: ComplEx **0.599**.
- **Negatives effect (FB15K):** with \(K=200,\lambda=0.01,\alpha_0=0.5\), \(\eta=100\) gives filtered MRR **0.737** and Hits@1 **64.8%**; performance drops at \(\eta=200\).

</details>

### 📄 DistMult (Bilinear-diag) scoring + margin ranking training
**Paper** · [source](https://arxiv.org/abs/1412.6575)

*DistMult bilinear scoring function and margin-based ranking / negative sampling training*

<details>
<summary>Key content</summary>

- **KB triples:** \((e_1, r, e_2)\) with subject \(e_1\), relation \(r\), object \(e_2\). Goal: learn embeddings so valid triples score higher (Section 3).
- **Entity embeddings (1st layer):** input vectors \(x_{e_1}, x_{e_2}\) (one-hot or n-hot). Projection matrix \(W\). Learned entity vectors \(y_{e_1}, y_{e_2}\) computed via a (linear or non-linear) projection \(y_e = f(W x_e)\) (Section 3.1).
- **DistMult scoring (Bilinear-diag):** bilinear model with relation matrix restricted to diagonal.  
  \[
  f(h,r,t)= h^\top \operatorname{diag}(r)\, t
  \]
  where \(h,t\in\mathbb{R}^d\) are entity embeddings and \(r\in\mathbb{R}^d\) parameterizes the diagonal relation matrix (Section 4; “Bilinear-diag (DistMult)”).
- **Training objective (margin ranking loss):** construct negatives by corrupting subject or object: \((e_1', r, e_2)\) or \((e_1, r, e_2')\), excluding observed positives. Minimize
  \[
  \sum_{(e_1,r,e_2)\in T}\sum_{(e_1',r,e_2')\in T'} \max\big(0,\; 1 - f(e_1,r,e_2) + f(e_1',r,e_2')\big)
  \]
  (Section 3.3).
- **Implementation defaults:** mini-batch SGD with **AdaGrad**; per positive triple sample **2 negatives** (one corrupted head, one corrupted tail); **renormalize entity vectors to unit length after each gradient step**; **L2 regularization** on relation parameters (Implementation details).
- **Key empirical results (HITS@10):** DistMult outperforms TransE (“DistAdd”) on FB15k-401 relation categories (Table 3), e.g. predicting subject for **n-to-1:** DistAdd **21.1** vs DistMult **42.9**; predicting object for **1-to-n:** DistAdd **17.4** vs DistMult **46.7**. Overall HITS@10 (Table 2): FB15k DistMult **57.7** vs Bilinear **51.9**; WN DistMult **94.2** vs Bilinear **92.8**.
- **Design rationale:** diagonal relation matrices reduce parameters (same count as TransE) yet perform strongly; limitation noted: difficulty encoding relation vs inverse (Section 4 discussion).

</details>

### 📄 SACN (WGCN + Conv-TransE) for Knowledge Base Completion
**Paper** · [source](http://arxiv.org/pdf/1811.04441v2.pdf)

*SACN/Conv-TransE definitions + link-prediction results (MRR/Hits@K) on FB15k-237, WN18RR (+ Attr variant)*

<details>
<summary>Key content</summary>

- **KG setting:** triples \((s,r,o)\); link prediction evaluated with **filtered** ranking (filter valid triples before ranking). Metrics: **Hits@1/3/10** and **MRR** (Experiments).
- **WGCN encoder (Eq. 1–5):** multi-relational GCN with learnable relation-type weights \(\alpha_t\).
  - Node update (with self-loop) (Eq. 3):  
    \[
    h^{l+1}_i=\sigma\Big(\sum_{j\in N_i}\alpha^l_t\, h^l_j W^l + h^l_i W^l\Big)
    \]
    where \(h^l_i\in\mathbb{R}^{F_l}\), \(W^l\in\mathbb{R}^{F_l\times F_{l+1}}\), \(\sigma\)=activation.
  - Weighted adjacency (Eq. 4): \(A^l=\sum_{t=1}^T \alpha^l_t A_t + I\). Layer form (Eq. 5): \(H^{l+1}=\sigma(A^l H^l W^l)\).
- **Attributes as nodes:** represent each attribute type as an **attribute node** (not sparse vectors); connect via \((entity, relation, attribute)\) triples to “bridge” entities.
- **Conv-TransE decoder (Eq. 6–8):** no reshaping; uses \(2\times k\) kernels over stacked \((e_s,e_r)\) to preserve translational behavior.
  - Convolution (Eq. 6):  
    \(m_c(e_s,e_r,n)=\sum_{\tau=0}^{K-1}\omega_c(\tau,0)\hat e_s(n+\tau)+\omega_c(\tau,1)\hat e_r(n+\tau)\).
  - Score (Eq. 7): \(\psi(e_s,e_o)= f(\mathrm{vec}(M(e_s,e_r))W)\, e_o\); probability (Eq. 8): \(p=\sigma(\psi)\).
- **Empirical results (Table 3):**
  - **FB15k-237:** ConvE Hits@10/3/1/MRR = **0.49/0.35/0.24/0.32**; Conv-TransE **0.51/0.37/0.24/0.33**; **SACN 0.54/0.39/0.26/0.35**; **SACN+Attr 0.55/0.40/0.27/0.36**.
  - **WN18RR:** ConvE **0.48/0.43/0.39/0.46**; Conv-TransE **0.52/0.47/0.43/0.46**; **SACN 0.54/0.48/0.43/0.47**.
- **Hyperparameter defaults (Experimental Setup):** grid ranges—LR {0.01, 0.005, 0.003, 0.001}, dropout {0.0–0.5}, embedding {100,200,300}, kernels {50,100,200,300}, kernel size {2×1,2×3,2×5}; **WGCN uses 2 layers**. Good settings: dropout **0.2**, LR **0.003**, emb **200**; kernels **100** (FB15k-237) / **300** (WN18RR).
- **Kernel size effect (Table 4, FB15k-237):** SACN MRR improves **0.345 (2×1)** → **0.351 (2×3)** → **0.352 (2×5)**; SACN+Attr MRR **0.351** → **0.360** (2×3/2×5).

</details>

### 📄 TransE scoring + margin ranking loss
**Paper** · [source](https://papers.nips.cc/paper_files/paper/2013/hash/1cecc7a77928ca8133fa24680a88d2f9-Abstract.html)

*Primary TransE scoring function \(f_r(h,t)=\lVert h+r-t\rVert\) (L1/L2), margin-based ranking loss with negative sampling (“corruption”), and core training setup.*

<details>
<summary>Key content</summary>

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

</details>

### 📊 DAEA—Domain Adaptation for Real-World Entity Alignment
**Benchmark** · [source](https://aclanthology.org/2025.coling-main.393v1.pdf)

*Entity-alignment evaluation tables (Hits@1/10, MRR) on real-world KGs + source-KG selection distances + ablations*

<details>
<summary>Key content</summary>

- **Task defs (Section 3):** KG \(G=(E,R,A,V,T_r,T_a)\) with relation triples \(T_r\subseteq E\times R\times E\) and attribute triples \(T_a\subseteq E\times A\times V\). EA: given aligned seed pairs \(S=\{(e_i^1,e_j^2)\mid e_i^1\equiv e_j^2\}\), predict remaining equivalents.
- **Pipeline (Section 4):** (1) **Multi-source KG selection** (Fig.2): choose source DBP15K sub-dataset closest to target via **semantic + structural distance**. (2) **Domain adaptation training** (Fig.3): BERT-INT-style fine-tuning with total loss \(Loss=L_s+L_t+L_{DA}\) (Eq.11).
- **Source selection distance:** \(D_{G_sG_t}=\{D_{G_{s1}G_t},...,D_{G_{su}G_t}\}\) (Eq.1), with \(D_{G_{si}G_t}=d^{SE}_{G_{si}G_t}+d^{ST}_{G_{si}G_t}\) (Eq.2). Semantic distance uses **GloVe** entity-name embeddings + **JS distance** (Eq.5–7). Structural distance uses **2-layer GAT** (Eq.8–9) trained with contrastive loss \(L_c=\frac{1}{|N_i|}\sum_{e_j\in N_i}\max(0,M-\text{Eu}(e_i,e_j))\) (Eq.10).
- **Pairwise margin loss (Eq.12):** for \((e_i^1,e_j^2)\in S\), negative \(e_{j^-}^2\sim E_2\): \(\max\{0,\|e_i^1-e_j^2\|_1-\|e_i^1-e_{j^-}^2\|_1+M\}\).
- **Domain adaptive loss (Eq.13–16):** align source/target **positive** and **negative** distributions using **MMD** with Gaussian kernel (Eq.15); \(L_{DA}=DA_P+DA_N\).
- **Key empirical results (Table 2, real-world):**
  - **DOREMUS:** DAEA **H@1 77.84**, H@10 88.62, MRR 0.815 vs BERT-INT H@1 47.9 (MRR 0.515) and Attr-Int H@1 48.74 (MRR 0.587). Reported improvement: **+29.94 H@1** over prior best.
  - **AGROLD:** DAEA **H@1 27.14**, H@10 34.85, MRR 0.300 vs BERT-INT H@1 21.50 (MRR 0.229). Reported improvement: **+5.64 H@1**.
- **Source-KG choice matters (Table 3):** FR-EN has smallest distance and best results. Example: DOREMUS \(D=67.51\Rightarrow\) H@1 77.84; ZH-EN \(D=90.72\Rightarrow\) H@1 71.25; JA-EN \(D=105.71\Rightarrow\) H@1 70.65.
- **Ablation (Table 4):** removing DA drops DOREMUS H@1 **77.84→71.86**; AGROLD **27.14→26.24**. Using only positives: DOREMUS H@1 76.05; only negatives: AGROLD H@1 27.97 (best for AGROLD).
- **Defaults (Section 5.1.3):** train/test split **3:7**. Batch size: source **24**, AGROLD **19**. DOREMUS training set repeated **6×**, batch size **1**.

</details>

### 📖 Creating Single-Property RANGE Indexes (Neo4j Cypher DDL)
**Reference Doc** · [source](https://www.graphacademy.neo4j.com/courses/cypher-indexes-constraints/3-indexes/02-create-index/)

*Cypher DDL patterns for indexes and how Neo4j uses them in query planning (PROFILE/db hits)*

<details>
<summary>Key content</summary>

- **List metadata**
  - `SHOW CONSTRAINTS` lists constraints.
  - `SHOW INDEXES` lists indexes and their implementation details.
  - **Uniqueness constraints are implemented as RANGE indexes** (with uniqueness lookup characteristics).
  - A graph always contains a **LOOKUP index**; **do not drop it** (used to quickly find nodes by labels and relationships by types).

- **Create RANGE index (node single property) — Eq. 1**
  - **Syntax:**  
    `CREATE INDEX <index_name> IF NOT EXISTS FOR (x:<node_label>) ON (x.<property_key>)`  
    Variables: `<index_name>` name; `x` variable; `<node_label>` label; `<property_key>` property.
  - **IF NOT EXISTS behavior:**  
    - If same **index name** exists → no index created.  
    - Else if an index already exists for the same **label + property** → no index created.  
    - Otherwise → index is created.

- **Create RANGE index (relationship single property) — Eq. 2**
  - **Syntax:**  
    `CREATE INDEX <index_name> IF NOT EXISTS FOR ()-[x:<RELATIONSHIP_TYPE>]-() ON (x.<property_key>)`  
    Variables: `<RELATIONSHIP_TYPE>` relationship type; others as above.
  - Same `IF NOT EXISTS` rules as nodes (name check, then type+property check).

- **Empirical performance example (PROFILE)**
  - Query: `PROFILE MATCH (m:Movie) WHERE m.title STARTS WITH "Toy" RETURN m.title`
    - Before index: **27,376 total db hits**; plan starts with **node by label scan**.
    - After `CREATE INDEX Movie_title IF NOT EXISTS FOR (x:Movie) ON (x.title)`: **8 total db hits**; plan starts with **NodeIndexSeekByRange()**.
  - Case-insensitive variant uses index but increases db hits due to `toLower(m.title)` transformation.

- **Drop index**
  - `DROP INDEX <index_name>`

- **Testing index usage**
  - Use **`PROFILE`** to confirm index usage and view db hits/elapsed time.

</details>

### 📖 Neo4j Cypher Constraints (data integrity for KG canonicalization)
**Reference Doc** · [source](https://neo4j.com/docs/cypher-manual/current/constraints/)

*Constraint semantics (uniqueness, existence, type, key), where to create/list/drop, and schema/operational implications*

<details>
<summary>Key content</summary>

- **Purpose (schema/data quality):** Neo4j constraints “ensure the quality and integrity of data in a graph.”
- **Constraint types available (semantics):**
  - **Property uniqueness constraints:** ensure that **combined property values are unique** for:
    - all **nodes with a specific label**, or
    - all **relationships with a specific type**.
  - **Property existence constraints (Enterprise Edition):** ensure that a property **exists** for:
    - all nodes with a specific label, or
    - all relationships with a specific type.
  - **Property type constraints (Enterprise Edition):** ensure that a property has the **required property type** for:
    - all nodes with a specific label, or
    - all relationships with a specific type.
  - **Key constraints (Enterprise Edition):** ensure **both**:
    - all specified properties **exist**, and
    - the **combined property values are unique**
    for nodes with a specific label or relationships with a specific type.
- **Operational workflow pointers (where to look next in the manual):**
  - “Create constraints”, “Show constraints”, “Drop constraints” pages contain details on **index-backed constraints**, **creation failures**, and **data violation scenarios**.
  - Cypher command reference: **Syntax → Constraints**.
- **Design rationale / schema management guidance:**
  - Constraints created with the older `CREATE CONSTRAINT` syntax are **automatically added to the graph type** of a database.
  - Neo4j **recommends defining a schema using a graph type** because it provides **more sophisticated constraint types** and a **more holistic/simplified** way to constrain and maintain data shape as constraints grow.

</details>

### 📖 Neo4j search-performance index types (overview)
**Reference Doc** · [source](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/)

*Official Cypher Manual overview of search-performance index types + what predicates they solve + planner behavior and hints*

<details>
<summary>Key content</summary>

- **Definition (Search-performance indexes):** Enable quicker retrieval of **exact matches** between an index and the **primary data storage**.
- **There are 4 search-performance index types in Neo4j (Section “Search-performance indexes”):**
  1. **Range indexes** (default index): *Supports most types of predicates.*
  2. **Text indexes:** Solve predicates operating on `STRING` values; **optimized** for filtering with string operators **`CONTAINS`** and **`ENDS WITH`**.
  3. **Point indexes:** Solve predicates on spatial `POINT` values; **optimized** for filtering on **distance** or **within bounding boxes**.
  4. **Token lookup indexes:** Solve **only** node label and relationship type predicates; **cannot** solve predicates filtering on properties.
- **Defaults / built-ins:**
  - **Range index is Neo4j’s default index.**
  - **Two token lookup indexes** are present when a database is created: **one for node labels** and **one for relationship types**.
- **Planner behavior / rationale:**
  - Indexes are **used automatically**.
  - If multiple indexes are available, the **Cypher planner** attempts to use the index (or indexes) that can **most efficiently solve** a predicate.
  - You can **force** use of a particular index with the **`USING`** keyword (index hints).

</details>

### 🔍 End-to-end KG Construction Pipeline & Requirements
**Explainer** · [source](https://arxiv.org/html/2302.11509)

*Taxonomy/pipeline for (incremental) KG construction: extraction → integration/alignment → QA/refinement → maintenance, with RDF vs Property Graph tradeoffs.*

<details>
<summary>Key content</summary>

- **KG definition (Section 2.1):** A KG is “a graph of data consisting of semantically described entities and relations of different types that are **integrated from different sources**.” Entities have **unique identifiers**; semantics can be described by an **ontology** (concepts, relationships, rules; supports inference).
- **RDF model (Section 2.2):** KG as **triples** ⟨subject, predicate, object⟩; optional **named graphs** extend to **quads** ⟨s,p,o,g⟩. Types via ⟨s, `rdf:type`, o⟩. Integrity constraints not native; use **SHACL** / **ShEx**. Query: **SPARQL** (and SPARQL-Star for RDF-Star).
- **Property Graph model (Section 2.2):** Nodes/edges with **labels**; both nodes and edges can have **key–value properties**; easier embedded metadata (provenance/time) but **no built-in ontology** support; capabilities depend on implementation. Query languages include **Cypher/Gremlin/PGQL**; emerging standard **GQL**.
- **Quality dimensions (Section 2.3):** correctness (accuracy + canonicalization/consistency), freshness (timeliness), comprehensiveness (coverage/completeness), succinctness (focus; excludes unnecessary info → scalability/availability), trustworthiness.
- **Incremental update rationale (Section 2.3):** Full recomputation for updates causes **redundant extraction/integration/QA** and repeated manual work; pipelines should support **batch + streaming** incremental ingestion for freshness and scalability.
- **Core pipeline tasks (Section 3):**
  1) Data acquisition & preprocessing (source selection/filtering; adapters; change detection via snapshots/diffs/pub-sub)  
  2) Metadata management (incl. **statement-level provenance**: creation date, confidence, source text span)  
  3) Ontology management (creation + evolution; schema/ontology matching)  
  4) Knowledge extraction: **NER + entity linking + relation extraction** (+ canonical IDs)  
  5) Entity resolution & fusion  
  6) Quality assurance (validate/repair; integrity vs ontology)  
  7) Knowledge completion (predict missing types/relations)

</details>

---

## Related Topics

- [[topics/rag-retrieval|RAG & Retrieval]]
- [[topics/agent-memory|Agent Memory]]
- [[topics/document-understanding|Document Understanding]]
- [[topics/graph-attention-networks-and-structured-data|Graph Attention Networks & Structured Data]]
