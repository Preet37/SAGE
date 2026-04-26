import json
import logging
from typing import AsyncGenerator
from openai import AsyncOpenAI
from .context import TutorContext
from .tool_handlers import execute_tool
from .system_prompt_v2 import build_system_prompt_v2 as build_system_prompt
from .system_prompt_explore import build_exploration_prompt
from .verifier import verify_response
from ..config import get_settings

logger = logging.getLogger(__name__)

MAX_STEPS = 5
_async_client: AsyncOpenAI | None = None


def get_async_client() -> AsyncOpenAI:
    global _async_client
    if _async_client is None:
        settings = get_settings()
        _async_client = AsyncOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
        )
    return _async_client


async def run_tutor_agent_loop(
    messages: list,
    context: TutorContext,
) -> AsyncGenerator[str, None]:
    client = get_async_client()
    settings = get_settings()
    steps = 0

    # Pick the right prompt builder based on mode
    prompt_builder = build_exploration_prompt if context.exploration_mode else build_system_prompt
    system_text = prompt_builder(context)
    if context.memory_block:
        system_text = f"{system_text}\n\n## Recalled prior context\n{context.memory_block}"
    if context.learner_profile:
        system_text = f"{system_text}\n\n## Learner profile\n{context.learner_profile}"
    if context.slash_instruction:
        system_text = f"{system_text}\n\n## Slash command\n{context.slash_instruction}"
    system_msg = {"role": "system", "content": system_text}
    api_messages = [system_msg] + messages
    full_assistant_text = ""

    while steps < MAX_STEPS:
        steps += 1

        try:
            # Groq's llama models produce malformed tool-call names when given a
            # tools list, causing stream validation errors. Since the lesson content
            # is already injected into the system prompt, the model can answer
            # directly without tool calls.
            stream = await client.chat.completions.create(
                model=settings.llm_model,
                messages=api_messages,
                max_tokens=settings.llm_max_tokens,
                temperature=settings.llm_temperature,
                stream=True,
            )
        except Exception as e:
            logger.error("LLM API call failed: %s", e)
            yield f"data: {json.dumps({'type': 'error', 'message': 'The tutor is temporarily unavailable. Please try again in a moment.'})}\n\n"
            break

        text_content = ""
        collected_tool_calls: list[dict] = []
        finish_reason = None

        try:
            async for chunk in stream:
                choice = chunk.choices[0]
                delta = choice.delta

                if delta.content:
                    text_content += delta.content
                    full_assistant_text += delta.content
                    yield f"data: {json.dumps({'type': 'text', 'delta': delta.content})}\n\n"

                if delta.tool_calls:
                    for tc_chunk in delta.tool_calls:
                        idx = tc_chunk.index
                        while len(collected_tool_calls) <= idx:
                            collected_tool_calls.append({"id": "", "name": "", "arguments": ""})
                        if tc_chunk.id:
                            collected_tool_calls[idx]["id"] = tc_chunk.id
                        if tc_chunk.function and tc_chunk.function.name:
                            collected_tool_calls[idx]["name"] = tc_chunk.function.name
                        if tc_chunk.function and tc_chunk.function.arguments:
                            collected_tool_calls[idx]["arguments"] += tc_chunk.function.arguments

                if choice.finish_reason:
                    finish_reason = choice.finish_reason
        except Exception as e:
            logger.error("LLM stream interrupted: %s", e)
            if not text_content:
                yield f"data: {json.dumps({'type': 'error', 'message': 'The response was interrupted. Please try again.'})}\n\n"
            break

        if finish_reason == "stop" or finish_reason is None:
            break

        if finish_reason == "length":
            truncation_msg = "\n\n[Response was truncated due to length. Please ask a follow-up to continue.]"
            yield f"data: {json.dumps({'type': 'text', 'delta': truncation_msg})}\n\n"
            break

        if finish_reason == "tool_calls":
            # Build the assistant message with tool calls for conversation history
            assistant_msg: dict = {"role": "assistant"}
            if text_content:
                assistant_msg["content"] = text_content
            else:
                assistant_msg["content"] = None
            assistant_msg["tool_calls"] = [
                {
                    "id": tc["id"],
                    "type": "function",
                    "function": {"name": tc["name"], "arguments": tc["arguments"]},
                }
                for tc in collected_tool_calls
            ]
            api_messages.append(assistant_msg)

            # Execute each tool and append results
            for tc in collected_tool_calls:
                yield f"data: {json.dumps({'type': 'tool_call', 'name': tc['name']})}\n\n"

                try:
                    tool_input = json.loads(tc["arguments"])
                except json.JSONDecodeError:
                    tool_input = {}

                result = await execute_tool(tc["name"], tool_input, context)

                api_messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "content": json.dumps(result),
                })
                yield f"data: {json.dumps({'type': 'tool_result', 'name': tc['name'], 'result': result})}\n\n"

    # Cognition track: emit a verification event before 'done' so the
    # frontend can render a confidence chip on the final assistant message.
    if settings.feature_verification and full_assistant_text:
        try:
            result = await verify_response(
                full_assistant_text,
                context.lesson_title,
                context.lesson_content,
                context.reference_kb,
            )
            if result is not None:
                yield f"data: {json.dumps({'type': 'verification', 'result': result.to_dict()})}\n\n"
        except Exception as e:
            logger.warning("Verification failed: %s", e)

    yield f"data: {json.dumps({'type': 'done'})}\n\n"
