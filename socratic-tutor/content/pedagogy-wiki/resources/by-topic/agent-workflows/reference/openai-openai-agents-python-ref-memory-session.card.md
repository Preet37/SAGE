# Source: https://openai.github.io/openai-agents-python/ref/memory/session/
# Author: OpenAI
# Author Slug: openai
# Title: Session - OpenAI Agents SDK (Python) Memory Session Reference
# Fetched via: trafilatura
# Date: 2026-04-10

Session
Session
Bases: Protocol
Protocol for session implementations.
Session stores conversation history for a specific session, allowing agents to maintain context without requiring explicit manual memory management.
Source code in src/agents/memory/session.py
get_items
async
get_items(
limit: int | None = None,
) -> list[[TResponseInputItem](../../items/#agents.items.TResponseInputItem)]
Retrieve the conversation history for this session.
Parameters:
| Name | Type | Description | Default |
|---|---|---|---|
limit
|
int | None
|
Maximum number of items to retrieve. If None, retrieves all items. When specified, returns the latest N items in chronological order. |
None
|
Returns:
| Type | Description |
|---|---|
list[
|
List of input items representing the conversation history |
Source code in src/agents/memory/session.py
add_items
async
add_items(items: list[[TResponseInputItem](../../items/#agents.items.TResponseInputItem)]) -> None
Add new items to the conversation history.
Parameters:
| Name | Type | Description | Default |
|---|---|---|---|
items
|
list[
|
List of input items to add to the history |
required |
pop_item
async
pop_item() -> [TResponseInputItem](../../items/#agents.items.TResponseInputItem) | None
Remove and return the most recent item from the session.
Returns:
| Type | Description |
|---|---|
|
The most recent item if it exists, None if the session is empty |
SessionABC
Bases: ABC
Abstract base class for session implementations.
Session stores conversation history for a specific session, allowing agents to maintain context without requiring explicit manual memory management.
This ABC is intended for internal use and as a base class for concrete implementations. Third-party libraries should implement the Session protocol instead.
Source code in src/agents/memory/session.py
get_items
abstractmethod
async
get_items(
limit: int | None = None,
) -> list[[TResponseInputItem](../../items/#agents.items.TResponseInputItem)]
Retrieve the conversation history for this session.
Parameters:
| Name | Type | Description | Default |
|---|---|---|---|
limit
|
int | None
|
Maximum number of items to retrieve. If None, retrieves all items. When specified, returns the latest N items in chronological order. |
None
|
Returns:
| Type | Description |
|---|---|
list[
|
List of input items representing the conversation history |
Source code in src/agents/memory/session.py
add_items
abstractmethod
async
add_items(items: list[[TResponseInputItem](../../items/#agents.items.TResponseInputItem)]) -> None
Add new items to the conversation history.
Parameters:
| Name | Type | Description | Default |
|---|---|---|---|
items
|
list[
|
List of input items to add to the history |
required |
pop_item
abstractmethod
async
pop_item() -> [TResponseInputItem](../../items/#agents.items.TResponseInputItem) | None
Remove and return the most recent item from the session.
Returns:
| Type | Description |
|---|---|
|
The most recent item if it exists, None if the session is empty |
OpenAIResponsesCompactionArgs
Bases: TypedDict
Arguments for the run_compaction method.
Source code in src/agents/memory/session.py
compaction_mode
instance-attribute
How to provide history for compaction.
- "auto": Use input when the last response was not stored or no response ID is available.
- "previous_response_id": Use server-managed response history.
- "input": Send locally stored session items as input.
store
instance-attribute
Whether the last model response was stored on the server.
When set to False, compaction should avoid "previous_response_id" unless explicitly requested.
OpenAIResponsesCompactionAwareSession
Bases:
, [Session](#agents.memory.session.Session)Protocol
Protocol for session implementations that support responses compaction.
Source code in src/agents/memory/session.py
run_compaction
async
run_compaction(
args: [OpenAIResponsesCompactionArgs](#agents.memory.session.OpenAIResponsesCompactionArgs) | None = None,
) -> None
get_items
async
get_items(
limit: int | None = None,
) -> list[[TResponseInputItem](../../items/#agents.items.TResponseInputItem)]
Retrieve the conversation history for this session.
Parameters:
| Name | Type | Description | Default |
|---|---|---|---|
limit
|
int | None
|
Maximum number of items to retrieve. If None, retrieves all items. When specified, returns the latest N items in chronological order. |
None
|
Returns:
| Type | Description |
|---|---|
list[
|
List of input items representing the conversation history |
Source code in src/agents/memory/session.py
add_items
async
add_items(items: list[[TResponseInputItem](../../items/#agents.items.TResponseInputItem)]) -> None
Add new items to the conversation history.
Parameters:
| Name | Type | Description | Default |
|---|---|---|---|
items
|
list[
|
List of input items to add to the history |
required |
pop_item
async
pop_item() -> [TResponseInputItem](../../items/#agents.items.TResponseInputItem) | None
Remove and return the most recent item from the session.
Returns:
| Type | Description |
|---|---|
|
The most recent item if it exists, None if the session is empty |
is_openai_responses_compaction_aware_session
is_openai_responses_compaction_aware_session(
session: [Session](#agents.memory.session.Session) | None,
) -> TypeGuard[[OpenAIResponsesCompactionAwareSession](#agents.memory.session.OpenAIResponsesCompactionAwareSession)]
Check if a session supports responses compaction.