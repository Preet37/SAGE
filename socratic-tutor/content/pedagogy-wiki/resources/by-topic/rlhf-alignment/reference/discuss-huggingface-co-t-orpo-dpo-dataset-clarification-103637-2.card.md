# Card: TRL DPO/ORPO dataset schema (prompt/chosen/rejected)
**Source:** https://discuss.huggingface.co/t/orpo-dpo-dataset-clarification/103637/2  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact dataset schema expectations for DPO/ORPO in TRL; how to derive `(prompt, chosen, rejected)` from chat-style preference data.

## Key Content
- **TRL `DPOTrainer` expected dataset format:** a **triple** of columns/fields  
  **(prompt, chosen, rejected)**  
  - `prompt`: the input context shown to the model  
  - `chosen`: the preferred continuation/response (given the prompt)  
  - `rejected`: the less-preferred continuation/response (given the prompt)
- **Common real-world preference dataset situation:** many datasets provide only **chosen/rejected** as **full chat transcripts** (often including roles like `user`/`assistant`) where the user prompt appears repeated inside both `chosen` and `rejected`.
- **Procedure to convert chat transcripts → TRL triple:**
  1. **Select the first message** in the transcript as the **`prompt`**.
  2. Put the remaining **N−1 messages** (the continuation after the first message) into **`chosen`** and **`rejected`** respectively.  
     - This matches the pattern: prompt = initial user turn; chosen/rejected = rest of conversation/assistant continuation.
  3. Reference implementation is pointed to in the Alignment Handbook code (`alignment-handbook/src/alignment/data.py`, lines ~73–90 in the linked commit).
- **Design rationale / note:** TRL currently requires the explicit triple, but maintainers suggest it could be simplified in the future to accept just chosen/rejected (would require refactoring).

## When to surface
Use when a student asks: “Why do some DPO/ORPO datasets repeat the prompt inside chosen/rejected?” or “How do I format/convert a chat-style preference dataset for TRL’s `DPOTrainer` (and similarly ORPO)?”