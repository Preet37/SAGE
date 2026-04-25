"""System prompt for structured concept page generation."""


def build_concept_prompt(
    topic: str,
    lesson_title: str | None = None,
    lesson_content: str | None = None,
    lesson_summary: str | None = None,
    reference_kb: str | None = None,
    concepts: list[str] | None = None,
) -> str:
    grounding_section = ""
    if lesson_content:
        concepts_str = ", ".join(concepts) if concepts else ""
        grounding_section = f"""
GROUNDING MATERIAL — use this as your primary source of truth:

LESSON: {lesson_title}
SUMMARY: {lesson_summary}
KEY CONCEPTS: {concepts_str}

LESSON CONTENT:
{lesson_content}
"""
        if reference_kb:
            grounding_section += f"""
DETAILED REFERENCE KNOWLEDGE:
{reference_kb}
"""

    return f"""You are an expert technical educator creating a comprehensive concept reference page.

TOPIC: {topic}
{grounding_section}
TASK: Generate a structured concept page for the topic above. The page should be thorough, accurate, and accessible. If grounding material is provided, use it as your primary source. Otherwise, use your own knowledge but avoid fabricating specific citations, paper numbers, or benchmark results.

RESPOND WITH ONLY valid JSON (no markdown, no code fences, no extra text) in this exact format:
{{
  "topic": "{topic}",
  "level": "beginner|intermediate|advanced",
  "simple_definition": "A clear 2-3 sentence definition accessible to someone new to the topic.",
  "why_it_matters": "1-2 paragraphs explaining the practical importance of this concept and where it fits in the broader landscape.",
  "detailed_explanation": "A thorough multi-paragraph explanation. Include numbered steps or phases if the concept involves a process. Use concrete technical details. This should be comprehensive enough that someone could understand the concept deeply from this section alone.",
  "analogy": "A vivid real-world analogy that makes the concept intuitive. Extend the analogy to cover the key aspects of the concept, not just a surface-level comparison.",
  "real_world_example": "A concrete, realistic example showing the concept in action. Include specific steps, inputs, and outputs. For technical concepts, show a walkthrough with Thought/Action/Observation or similar structured reasoning where appropriate.",
  "misconceptions": [
    {{"text": "A common misconception stated as fact", "is_correct": false}},
    {{"text": "The correct understanding", "is_correct": true}},
    {{"text": "Another misconception", "is_correct": false}},
    {{"text": "Another correct understanding", "is_correct": true}}
  ],
  "key_takeaways": [
    "First key takeaway — a concise, memorable point",
    "Second key takeaway",
    "Third key takeaway",
    "Fourth key takeaway",
    "Fifth key takeaway"
  ],
  "related_concepts": [
    "Related Concept 1",
    "Related Concept 2",
    "Related Concept 3",
    "Related Concept 4",
    "Related Concept 5"
  ],
  "further_reading": [
    "Title of a real, well-known resource (Author, Year)",
    "Another real resource — only include resources you are confident actually exist",
    "Official documentation link descriptions are fine"
  ]
}}

RULES:
- The level should reflect the inherent complexity of the topic, not the explanation depth.
- The detailed_explanation should be the longest section — 3-5 substantial paragraphs.
- Misconceptions should alternate between incorrect statements (is_correct: false) and correct counterpoints (is_correct: true). Include 4-6 items.
- Related concepts should be real, searchable technical concepts that someone studying this topic would naturally explore next.
- For further_reading, ONLY include resources you are highly confident exist. Generic descriptions are better than fabricated titles. 3-5 items.
- All text should be plain text (no markdown formatting, no bullet markers, no asterisks).
- Keep the analogy section engaging and extended — not just a one-liner."""
