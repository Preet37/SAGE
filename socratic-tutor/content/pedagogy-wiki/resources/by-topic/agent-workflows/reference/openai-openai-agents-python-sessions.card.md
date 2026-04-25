# Card: OpenAI Agents SDK (Python) — Session backends & persistence semantics
**Source:** https://openai.github.io/openai-agents-python/sessions/  
**Role:** reference_doc | **Need:** COMPARISON_DATA  
**Anchor:** Concrete session backends + what’s stored, how runs resume, and how conversation state is represented.

## Key Content
- **Core session semantics (client-side memory):**
  - **Before each run:** Runner fetches session history via `session.get_items(...)` and **prepends** it to the new turn input.
  - **After each run:** Runner **persists all new items** from the run (user input, assistant outputs, tool calls, etc.) into the session.
  - **Result:** Subsequent `Runner.run(..., session=...)` includes **full stored history** automatically (no manual `.to_input_list()`).
- **Mutual exclusivity (important constraint):** Sessions **cannot** be combined with `conversation_id`, `previous_response_id`, or `auto_previous_response_id` in the same run. Use sessions *or* OpenAI server-managed continuation mechanisms.
- **Resuming interrupted / HITL runs:** If a run pauses for approval, resume by calling `Runner.run(...)` again **with the same session** (or another instance pointing to the same backing store) so history continues consistently.
- **History merge control (procedure):** `RunConfig.session_input_callback(history, new_input) -> final_input`
  - Receives **copies** of `history` and `new_input` (safe to mutate).
  - Returned list controls model input **for that turn**, but SDK persists **only new-turn items** (filtering/reordering old history doesn’t re-save it).
  - Example policy: keep last **10** history items: `history[-10:] + new_input`.
- **Retrieval limiting (default/parameter):** `SessionSettings(limit=None)` retrieves **all** items (default). `limit=N` retrieves **most recent N** items; set per-run via `RunConfig(session_settings=SessionSettings(limit=50))`.
- **Built-in backends (comparison table):**
  - `SQLiteSession` (file-backed or in-memory), `AsyncSQLiteSession` (aiosqlite), `RedisSession`, `SQLAlchemySession`, `DaprSession` (supports TTL + consistency options), `OpenAIConversationsSession` (OpenAI Conversations API), wrappers: `OpenAIResponsesCompactionSession` (Responses API `responses.compact`), `EncryptedSession` (encryption + TTL), `AdvancedSQLiteSession` (branching/analytics).
- **Compaction specifics:** `OpenAIResponsesCompactionSession` can auto-compact after turns; **may block streaming** until compaction completes. Modes: `"previous_response_id"` (best when chaining response IDs), `"input"` (rebuild from session items), default `"auto"`; if `ModelSettings(store=False)`, `"auto"` falls back to input-based compaction. Do **not** wrap `OpenAIConversationsSession` with compaction wrapper.

## When to surface
Use when students ask how OpenAI Agents SDK handles **durable conversation state**, how to **resume** runs, or to compare **memory/persistence backends** (SQLite/Redis/SQLAlchemy/Dapr/OpenAI-hosted) and **compaction/TTL/encryption** options versus other agent frameworks.