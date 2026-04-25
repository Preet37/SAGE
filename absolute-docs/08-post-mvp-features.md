# 08 - Post-MVP Feature Requirements

This file defines the features that should be implemented after MVP release.
These are still required for product maturity, but they are not MVP launch blockers.

## 1. Post-MVP Goals

Post-MVP focuses on:

- Deeper personalization and measurable learning outcomes
- Better collaboration and network effects
- Scalable architecture and enterprise readiness
- Content operations and ecosystem growth

## 2. Priority Roadmap

## 2.1 Phase P1 - Growth and Learning Quality

| ID | Feature | Why It Matters | Definition of Done |
|---|---|---|---|
| POST-101 | Adaptive learning path engine | Moves from static progression to personalized sequences | Learner-specific next lessons are generated from mastery and performance history. |
| POST-102 | Spaced repetition scheduler | Improves retention over time | Concepts are re-surfaced automatically based on forgetting curves and prior attempts. |
| POST-103 | Placement and diagnostic assessment | Faster onboarding and better level fit | New users receive starting level and lesson recommendations in first session. |
| POST-104 | Rich replay timeline UI | Improves trust and debugging | Replay shows turn timeline, agent decisions, and verification outcomes visually. |
| POST-105 | Advanced peer recommendation ranking | Better match quality and completion | Ranking uses mastery, recency, and response quality signals. |
| POST-106 | Async study groups | Expands collaboration beyond live matching | Users can join topic rooms and continue discussions asynchronously. |
| POST-107 | Cross-lesson search | Improves content discoverability | Users can search all lessons and jump directly to relevant sections. |
| POST-108 | Achievement and milestone system | Increases engagement and consistency | Streaks, milestones, and concept badges are awarded from real progress data. |

## 2.2 Phase P2 - Scale and Operations

| ID | Feature | Why It Matters | Definition of Done |
|---|---|---|---|
| POST-201 | Full Fetch.ai Agentverse runtime integration | Delivers intended multi-agent architecture | Production tutor turns can run through deployed agents with health checks. |
| POST-202 | Multi-provider model routing strategy | Reduces cost and improves resilience | Routing policy selects model by latency, cost, and task type. |
| POST-203 | Vector database retrieval layer | Improves retrieval quality and scale | Embeddings and semantic search move to managed vector index. |
| POST-204 | Background job system for heavy tasks | Protects API latency | Plan generation, embedding jobs, and analytics run in queued workers. |
| POST-205 | Multi-tenant org and classroom support | Needed for institutional adoption | Org boundaries, data scopes, and admin policies are enforced. |
| POST-206 | Role-based access control | Enables secure admin workflows | Student, instructor, and admin roles control capabilities per route. |
| POST-207 | Course authoring admin console | Unlocks content velocity | Internal users can create, edit, and publish courses without code edits. |
| POST-208 | Course versioning and rollback | Prevents content regression | Course releases are versioned and can be rolled back safely. |

## 2.3 Phase P3 - Enterprise and Ecosystem

| ID | Feature | Why It Matters | Definition of Done |
|---|---|---|---|
| POST-301 | Billing and subscription lifecycle | Required for monetization | Plans, upgrades, downgrades, invoices, and access controls are operational. |
| POST-302 | Organization analytics dashboard | Required for B2B reporting | Cohort, engagement, and mastery analytics available for org admins. |
| POST-303 | LMS integration interfaces | Enables institutional workflows | Support LTI or equivalent integration with major LMS platforms. |
| POST-304 | SSO with OIDC and SAML | Enterprise security requirement | Enterprise domains can authenticate via managed identity providers. |
| POST-305 | Compliance controls and audit package | Required for regulated customers | Access logs, retention controls, and policy evidence are available. |
| POST-306 | Full localization and multilingual tutoring | Expands global reach | UI and tutoring support multiple languages with quality validation. |
| POST-307 | Mobile apps | Improves retention and access | iOS and Android clients support core learning flows. |
| POST-308 | Offline-first PWA mode | Improves reliability in low-connectivity contexts | Key lesson and notes flows work offline and sync when back online. |
| POST-309 | Plugin and tool integration framework | Extends platform capabilities | External tools can be safely added via stable plugin interfaces. |
| POST-310 | Fully offline on-device AI inference | Serves learners in low-connectivity and no-connectivity regions — particularly in developing countries where internet access is unreliable or unavailable | A small quantized model (e.g., Phi-3.5-mini) runs entirely in-browser via WebLLM; core tutor chat works with zero network requests after one-time model download; download progress is visible and resumable; hybrid mode automatically routes to cloud provider when connectivity is detected and falls back to on-device when offline. |

## 2.4 Ongoing Quality and Intelligence Enhancements

| ID | Feature | Why It Matters | Definition of Done |
|---|---|---|---|
| POST-401 | Automated tutor quality evaluation harness | Prevents silent quality drift | Regression prompts score answer quality, pedagogy, and grounding each release. |
| POST-402 | Hallucination red-team suite | Improves safety assurance | High-risk prompts are tested and flagged in CI and pre-release checks. |
| POST-403 | Experimentation framework for prompts and UI | Supports data-driven improvements | Feature flags and A/B experiments can be launched and measured safely. |
| POST-404 | Learning outcome attribution model | Proves educational impact | System can tie feature usage to measurable mastery improvements. |

## 3. Sequencing Rules

1. Complete all MVP blockers before starting P2 and P3 workstreams.
2. Do not scale agent or retrieval architecture before observability and migration baselines are stable.
3. Ship personalization and collaboration improvements only after replay and verification quality are trusted.
4. Gate enterprise features behind role and tenant security controls.

## 4. Suggested Ownership by Phase

- P1: Product and frontend-heavy with backend support.
- P2: Backend, platform, and data infrastructure-heavy.
- P3: Platform, enterprise, and cross-functional go-to-market heavy.

## 5. Tracking Convention

Use these IDs in roadmap and issue tracking directly, for example POST-202.
