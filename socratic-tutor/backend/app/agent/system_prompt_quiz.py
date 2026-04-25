"""System prompt for quiz question generation.

Generates structured JSON quiz questions grounded in lesson content.
"""
import random

DIFFICULTY_PROFILES = {
    "beginner": {
        "label": "Beginner",
        "mix": "Generate 80% easy and 20% intermediate questions.",
        "description": (
            "Focus on recall and recognition: definitions, identifying correct terms, "
            "matching concepts to descriptions. Questions should be approachable for "
            "someone who just read the material for the first time."
        ),
    },
    "intermediate": {
        "label": "Intermediate",
        "mix": "Generate 20% easy, 60% intermediate, and 20% advanced questions.",
        "description": (
            "Focus on understanding and application: 'Why does X work this way?', "
            "comparing approaches, predicting outcomes of simple scenarios, "
            "applying concepts to straightforward problems."
        ),
    },
    "advanced": {
        "label": "Advanced",
        "mix": "Generate 20% intermediate, 60% advanced, and 20% expert questions.",
        "description": (
            "Focus on analysis and evaluation: multi-step reasoning, trade-off analysis, "
            "debugging scenarios, 'What would happen if you changed X?', identifying "
            "flaws in reasoning, comparing multiple approaches."
        ),
    },
    "expert": {
        "label": "Expert",
        "mix": "Generate 20% advanced and 80% expert questions.",
        "description": (
            "Focus on synthesis and creation: design decisions, novel problem solving, "
            "edge cases, cross-concept integration, 'Design a system that...', "
            "optimizing under constraints, evaluating research trade-offs."
        ),
    },
}


def build_quiz_prompt(
    lesson_title: str,
    lesson_summary: str,
    lesson_content: str,
    concepts: list[str],
    reference_kb: str,
    difficulty: str,
    num_questions: int,
) -> str:
    profile = DIFFICULTY_PROFILES.get(difficulty, DIFFICULTY_PROFILES["intermediate"])
    concepts_str = ", ".join(concepts) if concepts else "General concepts from the lesson"

    example_correct = random.choice(["a", "b", "c", "d"])

    reference_section = ""
    if reference_kb:
        reference_section = f"""
DETAILED REFERENCE KNOWLEDGE (use this for factual grounding):
{reference_kb}
"""

    return f"""You are a quiz question generator for a technical education platform.

TASK: Generate exactly {num_questions} multiple-choice questions about the following lesson.

LESSON: {lesson_title}
SUMMARY: {lesson_summary}
KEY CONCEPTS: {concepts_str}

LESSON CONTENT:
{lesson_content}
{reference_section}
DIFFICULTY LEVEL: {profile["label"]}
{profile["description"]}

QUESTION MIX: {profile["mix"]}

RULES:
- Every question MUST be grounded in the lesson content or reference material provided above. Do NOT invent facts, numbers, or claims not present in the source material.
- Each question must have exactly 4 options (ids: "a", "b", "c", "d").
- Exactly one option must be correct.
- CRITICAL: Distribute the correct answer evenly across positions a, b, c, and d. Do NOT always put the correct answer in the same position.
- Wrong options (distractors) should be plausible but clearly wrong to someone who understands the material.
- The hint should nudge toward the answer without giving it away.
- The explanation should teach — explain WHY the correct answer is right and why key distractors are wrong.
- Vary question types: definitions, comparisons, scenarios, "what happens if", fill-in-the-blank reasoning, true/false framed as MCQ.
- Tag each question with its individual difficulty: "easy", "medium", "hard", or "expert".
- Do NOT repeat questions or test the same concept twice in the same way.

RESPOND WITH ONLY valid JSON in this exact format (no markdown, no code fences, no extra text):
{{
  "questions": [
    {{
      "question_text": "The question",
      "difficulty": "easy",
      "options": [
        {{"id": "a", "text": "Option A"}},
        {{"id": "b", "text": "Option B"}},
        {{"id": "c", "text": "Option C"}},
        {{"id": "d", "text": "Option D"}}
      ],
      "correct_option_id": "{example_correct}",
      "hint": "Think about...",
      "explanation": "The correct answer is {example_correct.upper()} because..."
    }}
  ]
}}"""
