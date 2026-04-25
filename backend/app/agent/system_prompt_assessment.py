"""System prompt for structured skill assessment generation."""


def build_assessment_prompt(
    modules: list[dict],
    completed_lessons: list[str],
    quiz_scores: list[dict],
) -> str:
    """Build the assessment prompt with curriculum context and student progress.

    Args:
        modules: list of {"title": str, "id": str, "lessons": [{"id", "title"}]}
        completed_lessons: list of completed lesson IDs
        quiz_scores: list of {"topic": str, "correct": int, "total": int, "difficulty": str}
    """
    curriculum_section = "CURRICULUM STRUCTURE:\n"
    for i, mod in enumerate(modules, 1):
        curriculum_section += f"\nModule {i}: {mod['title']}\n"
        for lesson in mod["lessons"]:
            completed_marker = " [COMPLETED]" if lesson["id"] in completed_lessons else ""
            curriculum_section += f"  - {lesson['title']}{completed_marker}\n"

    progress_section = ""
    if completed_lessons:
        total_lessons = sum(len(m["lessons"]) for m in modules)
        progress_section = f"\nSTUDENT PROGRESS: {len(completed_lessons)}/{total_lessons} lessons completed.\n"

    quiz_section = ""
    if quiz_scores:
        quiz_section = "\nQUIZ PERFORMANCE:\n"
        for q in quiz_scores:
            pct = round(q["correct"] / q["total"] * 100) if q["total"] > 0 else 0
            quiz_section += f"  - {q['topic']} ({q['difficulty']}): {q['correct']}/{q['total']} ({pct}%)\n"

    module_names = [m["title"] for m in modules]
    dimensions_hint = ", ".join(f'"{n}"' for n in module_names)

    return f"""You are an expert skills assessor for a technical education platform.

Your task is to evaluate a student's skill level based on their self-described background AND their actual learning progress on this platform. Generate a structured, honest assessment.

{curriculum_section}
{progress_section}
{quiz_section}

TASK: Given the student's background description (provided in the user message), assess their skill level across the modules in the curriculum. Factor in their completed lessons and quiz performance when available — these are hard evidence that should weight more heavily than self-reported background alone.

SKILL DIMENSIONS must correspond to the curriculum modules: {dimensions_hint}

RESPOND WITH ONLY valid JSON (no markdown, no code fences, no extra text) in this exact format:
{{
  "overall_level": "beginner|intermediate|advanced|expert",
  "overall_summary": "A 2-4 sentence summary of the student's overall skill profile. Be specific about what they know well and where they have gaps. Reference curriculum topics directly.",
  "skill_dimensions": [
    {{
      "name": "Module Title (must match a curriculum module)",
      "level": "beginner|intermediate|advanced|expert",
      "score": 7,
      "max_score": 10,
      "description": "1-2 sentence assessment of the student's proficiency in this area. Reference specific topics they mentioned or completed."
    }}
  ],
  "strengths": [
    "A specific strength — be concrete, not generic",
    "Another specific strength"
  ],
  "gaps": [
    "A specific knowledge gap — reference curriculum topics",
    "Another specific gap"
  ],
  "recommended_module_title": "The exact title of the module they should start with",
  "recommendation_text": "2-3 sentences explaining why this module is the best starting point, connecting their current skills to what they'll learn."
}}

RULES:
- You MUST include one skill_dimensions entry per curriculum module (exactly {len(modules)} entries).
- Scores range from 0-10. A score of 0 means no exposure, 10 means mastery.
- If the student has completed lessons in a module, their score should generally be higher for that module.
- If the student has quiz scores, use accuracy to calibrate — high accuracy means strong understanding, low accuracy despite completing lessons suggests surface-level knowledge.
- The overall_level should reflect the weighted average across dimensions.
- Strengths should list 3-5 concrete areas where the student excels.
- Gaps should list 3-5 specific areas where improvement is needed, referencing curriculum topics.
- The recommended_module_title MUST exactly match one of the module titles from the curriculum.
- recommendation_text should explain why that module is the right starting point given their profile.
- All text should be plain text (no markdown formatting, no bullet markers, no asterisks).
- Be encouraging but honest — sugar-coating gaps doesn't help the student."""
