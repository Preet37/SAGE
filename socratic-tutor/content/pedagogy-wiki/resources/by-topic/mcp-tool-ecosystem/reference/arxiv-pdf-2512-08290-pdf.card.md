# Card: MCP Security & Safety Threat Taxonomy + Defenses
**Source:** https://arxiv.org/pdf/2512.08290.pdf  
**Role:** paper | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Threat taxonomy + security/trust model for MCP ecosystems (prompt/tool/context attacks, governance layers, mitigations)

## Key Content
- **MCP architecture/security boundary (Sec. II):** Host mediates all LLM interactions; **LLM never connects directly** to data sources/tools. Protocol uses **JSON-RPC 2.0** over **Stdio** (local isolation) or **SSE** (remote). Starts with **capability negotiation handshake** (declare supported features like resources/prompts/logging).
- **Core primitives (Sec. II-C):**
  - **Resources:** read-only context streams identified by URIs (e.g., `file:///logs/error.txt`), can support subscriptions.
  - **Prompts:** server-defined templates bundling resources + instructions (“best practice workflows”).
  - **Tools:** executable actions exposed by servers; host is policy enforcement point.
- **Security vs Safety convergence (Sec. I-B, III-B):** security breaches (e.g., indirect prompt injection) can trigger safety failures (model “honestly” believes it’s authorized), and safety failures (hallucinated parameters) can cause security breaches (exfiltration).
- **Security vulnerability taxonomy (Table III, Sec. IV-A):**  
  Context Poisoning; Prompt Injection; Unauthorized Context Injection; Data Leakage & Privacy; Cross-Session Contamination; Supply-Chain & Model-Switch; Protocol Abuse & Name Collisions; DoS & Resource Exhaustion. Includes **phases** (Install/Update/Exec) and **impacts** (e.g., unauthorized command execution, integrity breach, cost escalation).
- **Concrete empirical result (Sec. VII-A):** **43% of MCP server implementations tested** (Equixly) **executed unsafe shell calls**, enabling RCE risk.
- **Mitigation stack (Sec. VI):**
  - **ETDI**: **cryptographically signed tool manifests**, **immutable version identifiers**, registry-based approval; **verify signatures at load + invocation**; re-authorization on functional change (anti “rug-pull”).
  - **Capability-bound execution**: OAuth-enhanced tool definitions, least privilege, short-lived creds, **mTLS**, continuous verification (Zero Trust).
  - **Context validation/sanitization**: strict delimiters separating system/user/tool content; deterministic filtering of tool outputs; provenance tracking (e.g., DDG/MindGuard).
  - **Isolation + integrity**: sandboxing (e.g., gVisor syscall interception); schema validation + signatures + nonces/timestamps to prevent replay.

## When to surface
Use when students ask about **MCP-specific attack vectors** (prompt injection via tool outputs, tool poisoning, server spoofing) or **how to design MCP hosts/registries** with provenance, permissions, isolation, and auditability.