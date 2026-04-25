# Card: Amazon States Language (ASL) — State machine definition skeleton + example
**Source:** https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Authoritative ASL workflow definition structure; example showing `Task`, `Choice`, `Fail` and transitions

## Key Content
- **ASL definition (what it is):** A **JSON-based structured language** to define a Step Functions **state machine** (a collection of states) that can:
  - do work with **`Task`** states,
  - branch with **`Choice`** states,
  - stop with error using **`Fail`** states, etc.
- **File naming requirement (outside console):** Save definitions with extension **`.asl.json`**.
- **Top-level required structure (example):**
  - `Comment`: free-text description.
  - `QueryLanguage`: example sets **`"JSONata"`**.
  - `StartAt`: name of first state (example: **`"FirstState"`**).
  - `States`: object mapping state names → state definitions.
- **State transition fields (example):**
  - `Next`: name of next state (used by `Task`, `Choice` branches).
  - `End: true`: marks terminal state (example: `NextState`).
  - `Default`: fallback transition for `Choice` (example: **`"DefaultState"`**).
- **`Task` state fields (example):**
  - `Type: "Task"`
  - `Resource`: ARN (example Lambda ARN format: `arn:aws:lambda:region:123456789012:function:FUNCTION_NAME`)
  - Optional `Assign` (JSONata) to set variables (example assigns `foo` from `$states.input.foo_input`).
- **`Choice` state fields (example):**
  - `Type: "Choice"`
  - `Choices`: array of rules, each with `Condition` (JSONata) and `Next`.
- **`Fail` state fields (example):**
  - `Type: "Fail"`, plus `Error` and `Cause` strings.

## When to surface
Use when a student asks how to **structure an ASL JSON**, how **state transitions** (`StartAt`, `Next`, `End`, `Default`) work, or wants a concrete **Task/Choice/Fail** example (including JSONata `QueryLanguage` / `Condition` / `Assign`).