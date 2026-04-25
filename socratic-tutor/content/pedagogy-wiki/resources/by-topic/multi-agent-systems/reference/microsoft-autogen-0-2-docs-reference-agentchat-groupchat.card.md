# Card: AutoGen GroupChat & GroupChatManager (speaker selection + defaults)
**Source:** https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/groupchat/  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Concrete parameter defaults + semantics for GroupChat/GroupChatManager (admin, rounds, function-call filtering, auto speaker selection, last_speaker)

## Key Content
- **GroupChat dataclass fields (core config):**
  - `agents`: list of participating agents; `messages`: group message list; `max_round`: max conversation rounds.
  - `admin_name` default **"Admin"**; **KeyboardInterrupt** causes admin agent to take over.
  - `func_call_filter` default **True**: if a message is a *function call suggestion*, next speaker must be an agent whose `function_map` contains that function name.
- **Speaker selection configuration (defaults + options):**
  - `speaker_selection_method` default **"auto"**. Allowed: `"auto"`, `"manual"`, `"random"`, `"round_robin"` (case-insensitive), or a **Callable** `(last_speaker, groupchat) -> Agent | str | None`.
    - Callable may return: an `Agent` in the chat; a string selecting a default method; or `None` to terminate gracefully.
  - `max_retries_for_selecting_speaker` default **2** (auto mode requery attempts when LLM returns multiple/no names).
  - `allow_repeat_speaker` default **True**; can be `False` (no repeats) or a **list of Agents** allowed to repeat.
  - `allowed_or_disallowed_speaker_transitions` (dict) + `speaker_transitions_type` (`"allowed"`/`"disallowed"`). Mutually exclusive with `allow_repeat_speaker`.
- **Auto speaker selection workflow (procedure):**
  1. Create nested **two-agent** chat: *speaker selector* + *speaker validator*.
  2. Inject group messages; selector proposes next agent.
  3. If invalid (multiple/none), append follow-up prompt and retry up to `max_retries_for_selecting_speaker`.
  4. If still unresolved, fallback: **next agent in list**.
- **Prompt templates (defaults):**
  - `select_speaker_message_template` default: role-play instruction with `{roles}` and `{agentlist}`; appears **first** in context.
  - `select_speaker_prompt_template` default: “Read the above… select next role from {agentlist}… Only return the role.” Appears **last**; set to `None` to disable.
  - Follow-ups: `select_speaker_auto_multiple_template`, `select_speaker_auto_none_template` (both enforce returning **ONLY** one case-sensitive agent name).
- **GroupChatManager `last_speaker` property (semantics):**
  - Agents receive messages from the manager; `sender.last_speaker` reveals the **real originating agent** of the last group message.

## When to surface
Use when students ask how AutoGen GroupChat chooses the next speaker (auto/manual/random/round-robin/custom), how function-call suggestions constrain speaker choice (`func_call_filter`), or how to interpret `GroupChatManager.last_speaker` and key defaults (e.g., `"Admin"`, retries=2).