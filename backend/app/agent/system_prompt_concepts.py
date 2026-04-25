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

    return f"""You are an expert technical educator creating a rich, research-grade concept reference page.

TOPIC: {topic}
{grounding_section}
TASK: Generate a comprehensive, deeply detailed concept page. This should feel like the best Wikipedia article merged with a graduate textbook chapter — covering theory, equations, real research, and curated learning resources.

OUTPUT FORMAT: Respond with ONLY valid JSON. No markdown fences, no commentary, no trailing text. Start your response with {{ and end with }}.

Required JSON structure:
{{
  "topic": "{topic}",
  "level": "beginner|intermediate|advanced",
  "simple_definition": "A crisp 2-3 sentence definition accessible to a curious newcomer.",
  "why_it_matters": "2-3 paragraphs on practical significance, industry impact, and where this fits in the broader landscape. Be specific about real applications.",
  "detailed_explanation": "The core of the page — 4-6 substantial paragraphs. Cover the mechanism, theory, variants/extensions, trade-offs, and historical context. For mathematical topics, describe the key ideas that would be expressed as equations. Be thorough enough that someone could implement or use this concept after reading.",
  "analogy": "A vivid, extended real-world analogy. Go beyond a surface comparison — trace the analogy through at least 3 aspects of the concept to make it deeply intuitive.",
  "real_world_example": "A concrete worked example: show a specific scenario with inputs, the process step by step, and the output/result. For ML/CS topics show realistic pseudocode or a worked numeric example.",
  "misconceptions": [
    {{"text": "A common misconception stated as if true", "is_correct": false}},
    {{"text": "The correct understanding that corrects the above", "is_correct": true}},
    {{"text": "Another frequent misconception", "is_correct": false}},
    {{"text": "The correct counterpoint", "is_correct": true}},
    {{"text": "A subtler but important misconception", "is_correct": false}},
    {{"text": "The nuanced truth", "is_correct": true}}
  ],
  "key_takeaways": [
    "The single most important insight about this concept",
    "A key practical implication",
    "A common pitfall to avoid",
    "How this connects to adjacent concepts",
    "The key condition under which this concept works / breaks"
  ],
  "prerequisites": [
    "Prerequisite Concept 1",
    "Prerequisite Concept 2",
    "Prerequisite Concept 3"
  ],
  "key_equations": [
    {{
      "label": "Short name for the equation",
      "latex": "LaTeX string, e.g. E = mc^2 (without $ delimiters)",
      "description": "What this equation represents and when to use it"
    }},
    {{
      "label": "Second equation name",
      "latex": "Another LaTeX expression",
      "description": "Description of second equation"
    }},
    {{
      "label": "Third equation name",
      "latex": "Third LaTeX expression",
      "description": "Description of third equation"
    }}
  ],
  "related_concepts": [
    "Directly Related Concept 1",
    "Directly Related Concept 2",
    "Directly Related Concept 3",
    "Broader Context Concept",
    "Downstream Application Concept"
  ],
  "papers": [
    {{
      "title": "Title of a seminal or highly cited real paper on this topic",
      "authors": "Last, F. and Last, F.",
      "year": "YYYY",
      "description": "One sentence on what this paper contributed and why it matters"
    }},
    {{
      "title": "Title of a second key paper",
      "authors": "Last, F. et al.",
      "year": "YYYY",
      "description": "One sentence on its contribution"
    }},
    {{
      "title": "Title of a more recent influential paper",
      "authors": "Last, F. et al.",
      "year": "YYYY",
      "description": "One sentence on its contribution"
    }}
  ],
  "videos": [
    {{
      "title": "Descriptive title for a video that would explain this well",
      "channel": "Name of a real YouTube channel known for this topic (3Blue1Brown, Andrej Karpathy, MIT OpenCourseWare, StatQuest, Yannic Kilcher, etc.)",
      "search_query": "Exact YouTube search query that would find a relevant video on this topic"
    }},
    {{
      "title": "Title of a second useful video",
      "channel": "Channel name",
      "search_query": "YouTube search query for this video"
    }},
    {{
      "title": "A hands-on tutorial video title",
      "channel": "Channel name",
      "search_query": "YouTube search query"
    }}
  ],
  "further_reading": [
    "A real textbook or online course that covers this thoroughly (Author, Year or URL description)",
    "Official documentation or a highly reputable reference",
    "A blog post or tutorial from a respected practitioner"
  ]
}}

STRICT RULES:
- Output ONLY the JSON object. The very first character must be {{ and the last must be }}.
- All field values must be plain text — no markdown, no asterisks, no bullet markers inside strings.
- key_equations: include 2-5 equations relevant to the topic. For non-mathematical topics, include the closest quantitative relations (e.g. cost functions, ratios). If truly no equations apply, return an empty array [].
- papers: only include real, well-known papers you are confident actually exist with correct titles, authors, and years. 2-4 papers.
- videos: always include 2-3 video entries with realistic search queries. Use real channel names.
- prerequisites: list 2-4 concepts someone should understand first.
- detailed_explanation: this must be the longest section — minimum 4 paragraphs."""
