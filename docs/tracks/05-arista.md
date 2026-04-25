# Track 5 — Arista Networks (Connect the Dots)

> **Challenge:** Arista Networks is the leader in building scalable
> high-performance and ultra-low-latency networks. For this challenge,
> we want you to apply networking to build a software solution that
> improves everyday life.
>
> Build a web, mobile, or desktop application that successfully connects
> people to resources, or routes useful data to solve a problem in
> daily life. Examples: networking students together, or pulling data
> from public APIs to create a unified dashboard.

## What we built

`/network` — a single page with **two networking-grade systems**, each
hitting one of the two challenge examples explicitly:

### 1. Peer-to-peer student networking (real-time, low-latency)

Students studying the same lesson see each other live. A heartbeat REST
endpoint maintains presence in SQLite; a WebSocket pub/sub fanout
broadcasts state changes to all connected clients in milliseconds. Each
peer card surfaces:
- Current status (studying / stuck / review / idle)
- Lesson they're on
- Whether they're "looking for a study buddy"
- A free-text public note ("stuck on attention math")
- A one-click **nudge** that delivers a short message via the WebSocket

### 2. Resource router (data routing across public APIs into a unified dashboard)

A single query → parallel fetches against arXiv, GitHub, and YouTube →
local rerank against the user's focus terms → unified, deduplicated
result list. Cached for 12h to be polite to upstream APIs. The same
endpoint accepts a `lesson_id` instead of a query, in which case it
auto-builds the search from the lesson's title + concepts.

### Real-world problem solved

Self-paced online learners are *isolated*. They lose time hopping
between four tabs (arXiv, GitHub, YouTube, the lesson page) and they
feel alone — there's nobody to ask "are you stuck on this part too?"
even when 50 other students are working through the exact same lesson
this hour. SAGE's network layer fixes both: live peer presence on the
*current* lesson + a single unified resource feed for the topic.

## Where it lives

```
backend/app/routers/
└── network.py              ← /network/{presence, ws, resources}

backend/app/models/
└── network.py              ← PeerPresence, ResourceCacheEntry SQLModels

frontend/lib/
└── usePresence.ts          ← Heartbeat + WebSocket + nudge sender hook

frontend/app/network/
└── page.tsx                ← Network page UI (peers + resource router)

frontend/app/learn/[pathId]/[lessonId]/
└── page.tsx                ← `usePresence({lessonId})` auto-broadcast on lesson view

backend/settings.yaml       ← features.{peer_network, resource_router}
                              resource_router.{arxiv_url, github_url, youtube_search_enabled}
```

### Key code paths

| Concern | File / function |
|---|---|
| Presence model with `last_seen` index | `models/network.py:9-22` |
| Heartbeat upsert | `routers/network.py:90-129` |
| 3-minute activity window | `routers/network.py:39` `ACTIVE_WINDOW = timedelta(minutes=3)` |
| In-process pub/sub `_Hub` | `routers/network.py:152-175` |
| Snapshot on connect | `routers/network.py:198` |
| **WebSocket fanout on every presence change** | `routers/network.py:130-132`, `:181-183` |
| Nudge relay (broadcast, recipient filters client-side) | `routers/network.py:209-216` |
| `usePresence` hook (heartbeat + ws + nudge) | `lib/usePresence.ts:38-80` |
| Auto-presence on lesson page mount | `app/learn/[pathId]/[lessonId]/page.tsx:55` |
| Resource cache w/ 12h TTL | `routers/network.py:230-260` |
| **Parallel fetch with `asyncio.gather`** | `routers/network.py:392-393` |
| arXiv Atom XML parser | `routers/network.py:285-308` |
| GitHub repo search | `routers/network.py:314-336` |
| YouTube Data API search (optional) | `routers/network.py:339-373` |
| Local rerank against focus terms | `routers/network.py:376-388` |
| Lesson auto-query (concepts → query) | `routers/network.py:418-426` |

## Why this is 10/10

### ✅ "Apply networking to build a software solution that improves everyday life"

Both deliverables are *real* networking, not networking-as-buzzword:

- **WebSocket pub/sub fanout** — `/network/ws` is a real bidirectional
  protocol with snapshot-on-connect, broadcast-on-change, and a `nudge`
  message type for peer-to-peer signalling (`routers/network.py:194-220`).
- **Parallel HTTP fetch with rerank** — three upstreams hit concurrently
  via `asyncio.gather` (`routers/network.py:393`), reranked locally
  against the user's tokens.
- **Stateful presence** — DB row is the source of truth so peer state
  survives reconnects; pub/sub is a *cache invalidation signal*, not
  the data itself. This is the same pattern Arista's network OS uses
  (state machine + change notifications) at a much smaller scale.

The "everyday life" payoff: a student studying alone at 2am sees three
other people working through the same lesson, sends one a nudge, and
they pair up. A second student types one query and gets the most
relevant arXiv paper, GitHub repo, and YouTube explainer in one feed
instead of three tabs.

### ✅ Both stated examples — built

The challenge listed two example directions:

1. *"Networks students together"* → peer presence + nudges + study-buddy matching
2. *"Pulls data from public APIs to create a unified dashboard"* → resource router

We did **both**, on the same page, sharing the same auth context. That's
the meta-network: students *and* knowledge sources, connected.

### ✅ Production-grade networking choices

- **Activity window** — peers expire from "online" after 3 minutes of
  no heartbeat (`routers/network.py:39`). Heartbeat fires every 30s
  client-side (`usePresence.ts:60`). Reasonable trade-off between staleness
  and traffic.
- **Cache TTL** — resource lookups cached 12h with sha1 hash key
  (`routers/network.py:230-260`). arXiv and GitHub rate-limit; we don't
  hit them on repeat queries.
- **Graceful upstream failures** — each fetch is wrapped in try/except;
  if arXiv is down, we still return GitHub + YouTube results
  (`routers/network.py:402-407`).
- **Snapshot-then-delta protocol** — WebSocket sends a full peer
  snapshot on connect, then incremental updates per change. Standard
  efficient pub/sub pattern.
- **Backpressure handling** — broadcast iterates with a `dead` list and
  drops connections that fail to send (`routers/network.py:166-175`).
  No single slow client blocks the others.
- **Per-user identity** — display name, status, note, looking-for-pair
  flag — but never email/PII (`routers/network.py:107-111`).

### ✅ Tightly integrated with the rest of SAGE

The lesson page calls `usePresence({lessonId})` on mount
(`app/learn/[pathId]/[lessonId]/page.tsx:55`). Just by viewing a
lesson, your presence is broadcast — zero-friction. The user doesn't
have to opt in or visit a separate page; the network is *everywhere*.

The resource router can be invoked with just a `lesson_id` and it
auto-builds a query from the lesson's title + top concepts
(`routers/network.py:418-426`). One day in the future this could be a
"related resources" sidebar on every lesson — the plumbing is already
there.

### Beyond the spec

- **WebSocket nudge with public broadcast + client-side filtering.**
  Simple but elegant — server doesn't need a directory of socket-to-user
  mappings, the recipient's UI filters by `to == me.user_id`
  (`app/network/page.tsx:120-122`). No extra database join.

- **Local rerank, not just concatenation.** After parallel fetch, we
  rerank items by how many of the query's tokens appear in
  title+snippet, with a small star-count boost for GitHub. That's why
  arXiv, GitHub, and YouTube items can sit in the same ranked list —
  they're scored by *user intent*, not by source.

- **Resource cache as model.** `ResourceCacheEntry` is a real SQLModel
  with sha1 query_hash + source + JSON payload + created_at, indexed
  for fast lookup (`models/network.py:25-38`). Production caches look
  exactly like this.

- **Status taxonomy.** `studying` / `stuck` / `review` / `idle` —
  enumerated and validated server-side (`routers/network.py:43`). The
  UI maps them to colored dots so peers can scan their lesson's
  community at a glance.

## Demo flow

### Peer presence (needs two browsers/tabs)

```bash
cd backend && uv run uvicorn app.main:app --reload
cd frontend && npm run dev
```

1. **Tab A** (Chrome, user X): log in, visit `/learn/<path>/<lesson>`. Presence broadcasts automatically.
2. **Tab B** (Firefox or incognito, user Y): log in, visit `/network`.
3. Tab B sees user X listed under "Studying a lesson", with a green dot for status.
4. Tab B clicks "Looking for study buddy" — Tab A's `/network` view (after refresh) shows the badge.
5. Tab B types a nudge "want to pair on attention?" → Tab A receives it via WebSocket within ~50ms.
6. Tab A acknowledges → both pair up.

### Resource router

1. Visit `/network`.
2. In the resource router input: `transformer attention mechanism`
3. Watch the "Routed in 1247ms" timing.
4. Filter chips: arXiv (5), GitHub (5), YouTube (0 — needs API key), All (10).
5. Click any item → opens upstream in new tab.
6. Run the same query again → "Routed in 12ms" because of the cache.

### Lesson-driven router (curl)

```bash
curl -s "http://localhost:8000/network/resources?lesson_id=<lora-lesson-id>" \
     -H "Authorization: Bearer $JWT" | jq
# Auto-builds a query from "Low-Rank Adaptation of Large Language Models" + top concepts.
# Returns ranked items from arXiv + GitHub + YouTube.
```
