# Card: LangGraph `add_messages` reducer (exact merge + deletion semantics)
**Source:** https://github.com/langchain-ai/langgraph/blob/main/libs/langgraph/langgraph/graph/message.py  
**Role:** code | **Need:** WORKING_EXAMPLE  
**Anchor:** Reference implementation of message-state reducer utilities (`add_messages`), including ID-based merging, conversion helpers, and `RemoveMessage` behavior.

## Key Content
- **Reducer signature (Eq. 1):**  
  `add_messages(left, right, *, format: Literal["langchain-openai"]|None=None) -> Messages`  
  - `Messages = list[MessageLikeRepresentation] | MessageLikeRepresentation`
- **Wrapper behavior:** must pass **both** `left` and `right` (non-null) or neither (returns `partial`); else raises `ValueError("Must specify non-null arguments for both 'left' and 'right'...")`.
- **Coercion pipeline (Procedure A):**
  1. If `left`/`right` not a list → wrap into list.
  2. Convert to `BaseMessage` via `convert_to_messages(...)`.
  3. Convert chunks to full messages via `message_chunk_to_message(...)`.
  4. **Assign missing IDs:** if `m.id is None` → `m.id = str(uuid.uuid4())` (done for all in `left` and `right`).
- **Remove-all sentinel (Procedure B):**
  - Constant: `REMOVE_ALL_MESSAGES = "__remove_all__"`.
  - If any `RemoveMessage` in `right` has `m.id == REMOVE_ALL_MESSAGES`, return **only** messages **after** that index: `right[remove_all_idx+1:]` (drops all prior state).
- **ID-based merge rule (Eq. 2):**
  - Build `merged = left.copy()` and `merged_by_id = {m.id: index}`.
  - For each `m` in `right`:
    - If `m.id` exists: replace `merged[existing_idx] = m`. If `m` is `RemoveMessage`, mark ID for deletion.
    - If `m.id` missing in `left`:
      - If `m` is `RemoveMessage` → **error**: deleting non-existent ID.
      - Else append and record index.
  - After loop: filter out IDs marked for deletion.
- **Formatting parameter:**
  - `format=="langchain-openai"` → `_format_messages` uses `convert_to_openai_messages` then `convert_to_messages`.
  - Any other truthy `format` → `ValueError("Unrecognized format=...")`.
- **State schema helper:**  
  `MessagesState(TypedDict): messages: Annotated[list[AnyMessage], add_messages]`
- **Deprecation:** `MessageGraph(StateGraph)` is deprecated (since v1.0.0; removed v2.0.0); it uses `Annotated[list[AnyMessage], add_messages]` as the whole state.

## When to surface
Use when students ask how LangGraph merges message lists in state (append-only vs overwrite), how message IDs affect updates, or how to delete/clear messages using `RemoveMessage` / `__remove_all__`.