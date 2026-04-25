# Agent Skills Safety

## Video (best)
- **Stanford HAI** — "Agentic AI: A Progression of Language Model Applications"
- youtube_id: kJLiOGle3Lw
- Why: Stanford HAI panel covering agent safety, security, and trust — addresses guardrails and operational safety concerns for agentic systems.
- Level: intermediate

> ⚠️ **Coverage Gap**: No excellent video exists for this specific topic from the preferred educator list. General agentic AI videos (e.g., from LangChain or AutoGPT walkthroughs) touch on safety tangentially but do not address skill composition safety, principle of least privilege in agents, or defense-in-depth architectures for CLI/code agents.

---

## Blog / Written explainer (best)
- **Lilian Weng** — "LLM Powered Autonomous Agents"
- url: https://lilianweng.github.io/posts/2023-06-23-agent/
- Why: Weng's post is the most cited and pedagogically rigorous treatment of agentic architectures available. It covers tool use, skill composition, memory, and planning — providing the conceptual scaffolding needed to understand *why* safety constraints (sandboxing, least privilege, guardrails) are necessary. The section on tool use maps directly to skill registry and skill discovery concepts. It is dense but well-structured, making it ideal for learners in both intro-to-agentic-ai and intro-to-multimodal contexts.
- Level: intermediate

---

## Deep dive
- **OWASP LLM Top 10 — LLM06: Sensitive Information Disclosure / LLM01: Prompt Injection**
- url: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Why: The OWASP LLM Top 10 project is the most operationally grounded reference for agent security risks. It directly addresses prompt injection (critical for CLI agents and Claude Code), privilege escalation, and insecure plugin/skill design — mapping cleanly onto defense-in-depth and principle of least privilege concepts in this topic. It is practitioner-oriented and regularly updated, making it more actionable than academic papers for course designers.
- Level: intermediate/advanced

---

## Original paper
- **Perez & Ribeiro (2022)** — "Ignore Previous Prompt: Attack Techniques For Language Models"
- url: https://arxiv.org/abs/2211.09527
- Why: This is the most readable seminal paper specifically on prompt injection as an attack vector — the foundational safety concern for any agent that composes skills, executes CLI commands, or processes external inputs. It is short, accessible, and directly motivates the guardrails and sandboxing concepts in this topic. More pedagogically appropriate than broader alignment papers for this specific operational safety focus.
- Level: intermediate

---

## Code walkthrough
- **NVIDIA NeMo Guardrails — Official Documentation & Colabs**
- url: https://github.com/NVIDIA/NeMo-Guardrails
- Why: NeMo Guardrails is explicitly listed as a related concept for this topic, and the official repo contains runnable notebooks demonstrating how to implement input/output rails, topical guardrails, and dialog flow constraints on LLM agents. This is the most direct hands-on implementation resource that bridges the conceptual (guardrails, defense in depth) with working code. Learners can see how guardrails compose with agent skill calls in practice.
- Level: intermediate/advanced

---

## Coverage notes
- **Strong**: Prompt injection theory, agentic architecture concepts (Weng), NeMo Guardrails implementation, OWASP operational risk framing
- **Weak**: Skill registry design patterns, skill discovery safety, cost optimization and latency management as safety-adjacent concerns, multi-modal deployment-specific risks
- **Gap**: No high-quality video exists from preferred educators (3Blue1Brown, Karpathy, Kilcher, etc.) that addresses agent skills safety as a unified topic. Claude Code and Cursor-specific safety patterns are not well covered in public educational resources. Defense-in-depth architectures for multi-agent systems lack a canonical explainer.

---

## Cross-validation
This topic appears in 2 courses: **intro-to-agentic-ai**, **intro-to-multimodal**

- The Weng blog post and OWASP deep dive serve both courses well — agentic AI learners need the architectural grounding; multimodal learners need to understand how additional input surfaces (images, audio) expand the attack surface for prompt injection and skill misuse.
- The NeMo Guardrails code walkthrough is most relevant to intro-to-agentic-ai; multimodal courses may need supplementary resources on modality-specific safety (e.g., vision-based prompt injection).

---

## Last Verified
2025-01-01 (resource existence confirmed to knowledge cutoff; URLs marked should be checked before publication)