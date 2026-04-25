# Source: https://openai.github.io/openai-agents-python/ref/memory/
# Author: OpenAI
# Author Slug: openai
# Title: Memory - OpenAI Agents SDK (Python) Reference
# Fetched via: trafilatura
# Date: 2026-04-10

Memory
Session
Bases: Protocol
Protocol for session implementations.
Session stores conversation history for a specific session, allowing agents to maintain context without requiring explicit manual memory management.
Source code in src/agents/memory/session.py
get_items
async
get_items(
limit: int | None = None,
) -> list[[TResponseInputItem](../items/#agents.items.TResponseInputItem)]
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
add_items(items: list[[TResponseInputItem](../items/#agents.items.TResponseInputItem)]) -> None
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
pop_item() -> [TResponseInputItem](../items/#agents.items.TResponseInputItem) | None
Remove and return the most recent item from the session.
Returns:
| Type | Description |
|---|---|
|
The most recent item if it exists, None if the session is empty |
SQLiteSession
Bases: [SessionABC](session/#agents.memory.session.SessionABC)
SQLite-based implementation of session storage.
This implementation stores conversation history in a SQLite database. By default, uses an in-memory database that is lost when the process ends. For persistent storage, provide a file path.
Source code in src/agents/memory/sqlite_session.py
|
|
__init__
__init__(
session_id: str,
db_path: str | Path = ":memory:",
sessions_table: str = "agent_sessions",
messages_table: str = "agent_messages",
session_settings: [SessionSettings](session_settings/#agents.memory.session_settings.SessionSettings) | None = None,
)
Initialize the SQLite session.
Parameters:
| Name | Type | Description | Default |
|---|---|---|---|
session_id
|
str
|
Unique identifier for the conversation session |
required |
db_path
|
str | Path
|
Path to the SQLite database file. Defaults to ':memory:' (in-memory database) |
':memory:'
|
sessions_table
|
str
|
Name of the table to store session metadata. Defaults to 'agent_sessions' |
'agent_sessions'
|
messages_table
|
str
|
Name of the table to store message data. Defaults to 'agent_messages' |
'agent_messages'
|
session_settings
|
|
Session configuration settings including default limit for retrieving items. If None, uses default SessionSettings(). |
None
|
Source code in src/agents/memory/sqlite_session.py
get_items
async
get_items(
limit: int | None = None,
) -> list[[TResponseInputItem](../items/#agents.items.TResponseInputItem)]
Retrieve the conversation history for this session.
Parameters:
| Name | Type | Description | Default |
|---|---|---|---|
limit
|
int | None
|
Maximum number of items to retrieve. If None, uses session_settings.limit. When specified, returns the latest N items in chronological order. |
None
|
Returns:
| Type | Description |
|---|---|
list[
|
List of input items representing the conversation history |
Source code in src/agents/memory/sqlite_session.py
add_items
async
add_items(items: list[[TResponseInputItem](../items/#agents.items.TResponseInputItem)]) -> None
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
Source code in src/agents/memory/sqlite_session.py
pop_item
async
pop_item() -> [TResponseInputItem](../items/#agents.items.TResponseInputItem) | None
Remove and return the most recent item from the session.
Returns:
| Type | Description |
|---|---|
|
The most recent item if it exists, None if the session is empty |
Source code in src/agents/memory/sqlite_session.py
clear_session
async
Clear all items for this session.
Source code in src/agents/memory/sqlite_session.py
close
Close the database connection.
Source code in src/agents/memory/sqlite_session.py
OpenAIConversationsSession
Bases: [SessionABC](session/#agents.memory.session.SessionABC)
Source code in src/agents/memory/openai_conversations_session.py
|
|
session_id
property
writable
Get the session ID (conversation ID).
Returns:
| Type | Description |
|---|---|
str
|
The conversation ID for this session. |
Raises:
| Type | Description |
|---|---|
ValueError
|
If the session has not been initialized yet. Call any session method (get_items, add_items, etc.) first to trigger lazy initialization. |