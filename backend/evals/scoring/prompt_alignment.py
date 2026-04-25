"""Layer 2: Prompt-alignment LLM judge.

Scores how faithfully the tutor follows specific instructions in the system
prompt.  Each dimension maps directly to a prompt section so you can see
exactly *which instruction* the model is ignoring or over-indexing on.

Six dimensions, each scored 1-5:
  1. socratic_method     → TEACHING PRINCIPLES (Socratic questioning)
  2. multimodal_teaching → TEACHING PRINCIPLES (toolkit usage)
  3. compound_analogies  → TEACHING PRINCIPLES (analogy compounding)
  4. factual_grounding   → FACTUAL ACCURACY (claim tiers, hedging)
  5. adaptive_mode       → MODE hints + learner energy matching
  6. image_discipline    → IMAGE rules (curated images, no dumps, framing)
"""

from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass, field

from ..config import EvalConfig, get_openai_client

logger = logging.getLogger(__name__)

ALIGNMENT_DIMENSIONS = [
    "socratic_method",
    "multimodal_teaching",
    "compound_analogies",
    "factual_grounding",
    "adaptive_mode",
    "image_discipline",
]

ALIGNMENT_JUDGE_SYSTEM_PROMPT = """You are an evaluator who checks whether an AI tutor followed its specific instructions. You are NOT evaluating teaching quality (a separate judge handles that). You are evaluating INSTRUCTION COMPLIANCE — did the tutor do what it was told to do?

Score each dimension 1-5 based on how well the tutor followed the specific instruction described.

DIMENSIONS:

1. SOCRATIC METHOD (socratic_method)
   The tutor is instructed: "Use the Socratic method: guide learners to discover insights through questions and exploration." The intended pattern is TEACH-THEN-CHECK: explain the concept clearly, then ask a genuine thinking question to verify and deepen understanding. This is distinct from pure interrogation that withholds information.

   1 = Pure lecture. The tutor dumps information across multiple turns without ever asking the student to think.
   2 = Token questions only. Questions are "Does that make sense?" or "Any questions?" — no genuine thinking prompts.
   3 = Explains concepts and asks genuine questions, but questions don't build on each other or connect to the student's specific responses.
   4 = Good teach-then-check rhythm. Explains clearly, asks targeted questions that probe the student's actual understanding, and adapts based on their answers.
   5 = Masterful. Questions build on each other across turns, the student discovers insights through the dialogue, and direct explanations land at exactly the right moments.

2. MULTIMODAL TEACHING (multimodal_teaching)
   The tutor is instructed to vary its modalities: images, code snippets, quizzes, curated resources, tables, and diagrams — not just text and math. It is told: "If you notice you've been doing text + math for 2-3 turns in a row, reach for a different modality." It should aim for at least 3 different modalities over a full conversation.

   Count distinct modalities: images, code blocks, quiz cards, resource recommendations, tables, Mermaid/flow diagrams, analogies each count as one.

   1 = Text and math only across the whole conversation. No other modalities.
   2 = One additional modality beyond text/math (e.g., only images, or only analogies).
   3 = Two additional modalities beyond text/math, or one used very well with excellent timing.
   4 = Three or more modalities used at appropriate moments. Teaching tools feel natural, not forced.
   5 = Rich, well-timed use of 4+ modalities. Each tool appears at the moment it would help most.

3. COMPOUND ANALOGIES (compound_analogies)
   The tutor is instructed: "When using analogies, make them compound — extend and build on earlier ones rather than introducing unrelated new metaphors each time."

   1 = No analogies used, OR multiple unrelated analogies that confuse rather than clarify.
   2 = One-off analogies that don't build on each other.
   3 = At least one analogy is revisited or extended once.
   4 = A primary analogy runs through the conversation and is extended meaningfully.
   5 = A brilliant compound analogy that evolves with the concept, with the student actively engaging with the metaphor.

   NOTE: If the conversation is very short (1-2 turns) or purely technical, score 3 if at least one good analogy was offered. Not every conversation needs compound analogies.
   KNOWN PATTERN: The tutor compounds analogies well when the student engages with them, but drops analogies in code-heavy or technical conversations where the student doesn't reference them. This is accepted behavior — scores of 2-3 in code_mode or factual_probe scenarios are expected and not a prompt deficiency.

4. FACTUAL GROUNDING (factual_grounding)
   The tutor is instructed to follow claim tiers: state reference material confidently (Tier 1), attribute search results (Tier 2), state general knowledge naturally (Tier 3), and hedge or skip unverifiable specifics (Tier 4). It must NEVER fabricate citations.

   1 = Fabricates specific citations (paper titles, table numbers, URLs) not from any source.
   2 = Makes specific claims (numbers, benchmarks) without sourcing or hedging.
   3 = Mostly grounded but occasionally states unverifiable specifics as fact without hedging.
   4 = Good grounding. Uses hedging for uncertain claims, attributes search results, doesn't fabricate.
   5 = Exemplary discipline. Clear tier separation, honest about gaps, never fabricates.

5. ADAPTIVE MODE (adaptive_mode)
   The tutor receives a MODE instruction (e.g., "ELI5 mode — use simple language" or "Code mode — lead with code"). It should also "match the learner's energy."

   1 = Completely ignores the mode instruction. Uses jargon in ELI5 mode, no code in code mode, etc.
   2 = Weakly follows the mode. Some nods to it but frequently breaks character.
   3 = Generally follows the mode but with lapses (e.g., ELI5 mode but occasionally drops into dense math).
   4 = Consistently follows the mode throughout. Adjusts to student signals within the mode.
   5 = Fully embodies the mode AND adapts to student energy. The mode feels natural, not forced.

   NOTE: If mode is "default", score based on whether the tutor matches the student's energy and adjusts appropriately. Score 3 is baseline for default mode.

6. IMAGE DISCIPLINE (image_discipline)
   The tutor is instructed: show ONE image at a time, write 1-2 sentences BEFORE the tag, use only curated paths, and fall back to Mermaid if no curated image fits.

   1 = Dumps multiple images at once, or uses images with no framing.
   2 = Uses images but without proper framing text, or shows irrelevant images.
   3 = Correct image format and framing, but timing could be better.
   4 = Good image discipline — well-timed, well-framed, one at a time.
   5 = Excellent — images appear at the perfect pedagogical moment with clear "what to look for" framing.

   NOTE: If the conversation has NO images at all, score based on whether images were available and could have helped. If images were irrelevant to the discussion, score 3 (neutral). If images were available and would have clearly helped but weren't used, score 2.
   KNOWN PATTERN: The tutor tends to skip curated images in code-heavy and compound_analogy scenarios, defaulting to Mermaid diagrams or text instead. Scores of 2 in these scenarios reflect absence of images, not poor usage — when images are used, framing and timing are consistently good (score 4-5). This is accepted and not a prompt deficiency.

IMPORTANT:
- Score each dimension independently.
- Provide a 1-2 sentence justification for each score.
- A score of 3 means "adequate compliance." 4 means "good." 5 is rare and exceptional.
- If a dimension is not applicable (e.g., no mode set, no images available), score 3 with a note.

Respond in EXACTLY this JSON format (no markdown, no extra text):
{
  "socratic_method": {"score": <1-5>, "justification": "<text>"},
  "multimodal_teaching": {"score": <1-5>, "justification": "<text>"},
  "compound_analogies": {"score": <1-5>, "justification": "<text>"},
  "factual_grounding": {"score": <1-5>, "justification": "<text>"},
  "adaptive_mode": {"score": <1-5>, "justification": "<text>"},
  "image_discipline": {"score": <1-5>, "justification": "<text>"}
}"""


def build_alignment_user_prompt(
    conversation_transcript: str,
    lesson_title: str,
    teaching_mode: str = "default",
    available_images: list[dict] | None = None,
) -> str:
    mode_section = f"**Active teaching mode:** {teaching_mode}"
    if teaching_mode == "default":
        mode_section += " (no special mode — evaluate energy-matching instead)"

    images_section = "No curated images were available for this lesson."
    if available_images:
        img_lines = [f"  - {img.get('caption', img.get('file', 'image'))}" for img in available_images[:10]]
        images_section = (
            f"{len(available_images)} curated images were available:\n" + "\n".join(img_lines)
        )

    return f"""## Lesson: {lesson_title}
{mode_section}

## Available Images
{images_section}

## Conversation Transcript

{conversation_transcript}

---

Score how well the tutor followed its instructions across the 6 dimensions. Return ONLY valid JSON."""


@dataclass
class AlignmentDimensionScore:
    score: int
    justification: str

    def as_dict(self) -> dict:
        return {"score": self.score, "justification": self.justification}


@dataclass
class AlignmentScores:
    socratic_method: AlignmentDimensionScore = field(
        default_factory=lambda: AlignmentDimensionScore(0, "")
    )
    multimodal_teaching: AlignmentDimensionScore = field(
        default_factory=lambda: AlignmentDimensionScore(0, "")
    )
    compound_analogies: AlignmentDimensionScore = field(
        default_factory=lambda: AlignmentDimensionScore(0, "")
    )
    factual_grounding: AlignmentDimensionScore = field(
        default_factory=lambda: AlignmentDimensionScore(0, "")
    )
    adaptive_mode: AlignmentDimensionScore = field(
        default_factory=lambda: AlignmentDimensionScore(0, "")
    )
    image_discipline: AlignmentDimensionScore = field(
        default_factory=lambda: AlignmentDimensionScore(0, "")
    )

    def as_dict(self) -> dict:
        return {
            dim: getattr(self, dim).as_dict()
            for dim in ALIGNMENT_DIMENSIONS
        }

    @property
    def mean_score(self) -> float:
        scores = [getattr(self, dim).score for dim in ALIGNMENT_DIMENSIONS]
        return sum(scores) / len(scores)


def _format_transcript(messages: list[dict]) -> str:
    lines = []
    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")

        if role == "user":
            lines.append(f"### STUDENT\n\n{content}\n")
        elif role == "assistant":
            tool_calls = msg.get("tool_calls", [])
            if tool_calls:
                tc_lines = []
                for tc in tool_calls:
                    fn = tc.get("function", {})
                    name = fn.get("name", "unknown_tool")
                    args = fn.get("arguments", "")
                    tc_lines.append(f"  - **{name}**({args})")
                tool_section = "\n".join(tc_lines)
                if content:
                    lines.append(
                        f"### TUTOR\n\n{content}\n\n*Tool calls:*\n{tool_section}\n"
                    )
                else:
                    lines.append(
                        f"### TUTOR (tool use)\n\n*Tool calls:*\n{tool_section}\n"
                    )
            elif content:
                lines.append(f"### TUTOR\n\n{content}\n")
        elif role == "tool":
            tool_name = msg.get("name", "tool")
            lines.append(f"### TOOL RESULT ({tool_name})\n\n{content}\n")

    return "\n---\n\n".join(lines)


async def judge_prompt_alignment(
    messages: list[dict],
    lesson_title: str,
    config: EvalConfig,
    teaching_mode: str = "default",
    available_images: list[dict] | None = None,
    max_retries: int = 2,
) -> AlignmentScores:
    """Score how well the tutor followed its specific prompt instructions."""
    client = get_openai_client()

    transcript = _format_transcript(messages)
    user_prompt = build_alignment_user_prompt(
        transcript,
        lesson_title,
        teaching_mode=teaching_mode,
        available_images=available_images,
    )

    last_error = ""
    for attempt in range(max_retries + 1):
        try:
            response = await client.chat.completions.create(
                model=config.judge_model.model_id,
                messages=[
                    {"role": "system", "content": ALIGNMENT_JUDGE_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=config.judge_model.max_tokens,
                temperature=config.judge_model.temperature,
            )

            raw = response.choices[0].message.content or ""
            cleaned = raw.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
                if cleaned.endswith("```"):
                    cleaned = cleaned[:-3]
                cleaned = cleaned.strip()

            data = json.loads(cleaned)
            scores = AlignmentScores()
            for dim in ALIGNMENT_DIMENSIONS:
                if dim in data:
                    entry = data[dim]
                    setattr(
                        scores,
                        dim,
                        AlignmentDimensionScore(
                            score=int(entry.get("score", 0)),
                            justification=str(entry.get("justification", "")),
                        ),
                    )
            if scores.mean_score > 0:
                return scores
            last_error = "All scores returned 0 — possible malformed response"
            logger.warning(
                "Alignment judge attempt %d/%d returned all-zero scores, retrying",
                attempt + 1, max_retries + 1,
            )

        except json.JSONDecodeError as e:
            last_error = f"Invalid JSON: {e}"
            logger.warning(
                "Alignment judge attempt %d/%d returned invalid JSON: %s",
                attempt + 1, max_retries + 1, e,
            )
        except Exception as e:
            last_error = str(e)
            logger.warning(
                "Alignment judge attempt %d/%d failed: %s",
                attempt + 1, max_retries + 1, e,
            )

        if attempt < max_retries:
            await asyncio.sleep(2 * (attempt + 1))

    logger.error("Alignment judge failed after %d attempts: %s", max_retries + 1, last_error)
    failed = AlignmentScores()
    for dim in ALIGNMENT_DIMENSIONS:
        setattr(failed, dim, AlignmentDimensionScore(0, f"SCORING FAILED: {last_error}"))
    return failed
