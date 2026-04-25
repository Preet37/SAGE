"""System prompt for personalized curriculum generation from existing lessons."""


def build_curriculum_prompt(
    courses: list[dict],
    completed_lessons: list[str],
    quiz_scores: list[dict],
    assessment: dict | None = None,
) -> str:
    """Build the curriculum generation prompt.

    Args:
        courses: list of {
            "path_title": str, "path_slug": str,
            "modules": [{
                "title": str,
                "lessons": [{"id": str, "title": str, "summary": str, "concepts": list[str]}]
            }]
        }
        completed_lessons: list of completed lesson IDs
        quiz_scores: list of {"topic": str, "correct": int, "total": int, "difficulty": str}
        assessment: optional dict with keys overall_level, skill_dimensions, strengths, gaps
    """
    catalog_section = "AVAILABLE LESSON CATALOG:\n"
    total_lessons = 0
    for course in courses:
        catalog_section += f"\n=== Course: {course['path_title']} ===\n"
        for mod in course["modules"]:
            catalog_section += f"\n  Module: {mod['title']}\n"
            for lesson in mod["lessons"]:
                total_lessons += 1
                completed_marker = " [COMPLETED]" if lesson["id"] in completed_lessons else ""
                concepts_str = ", ".join(lesson.get("concepts", [])[:8])
                catalog_section += (
                    f"    - ID: {lesson['id']} | \"{lesson['title']}\""
                    f" | Concepts: [{concepts_str}]{completed_marker}\n"
                )

    progress_section = ""
    if completed_lessons:
        progress_section = f"\nSTUDENT PROGRESS: {len(completed_lessons)}/{total_lessons} lessons completed.\n"

    quiz_section = ""
    if quiz_scores:
        quiz_section = "\nQUIZ PERFORMANCE:\n"
        for q in quiz_scores:
            pct = round(q["correct"] / q["total"] * 100) if q["total"] > 0 else 0
            quiz_section += f"  - {q['topic']} ({q['difficulty']}): {q['correct']}/{q['total']} ({pct}%)\n"

    assessment_section = ""
    if assessment:
        assessment_section = f"\nSKILL ASSESSMENT (auto-loaded):\n"
        assessment_section += f"  Overall Level: {assessment.get('overall_level', 'unknown')}\n"
        if assessment.get("strengths"):
            assessment_section += "  Strengths:\n"
            for s in assessment["strengths"]:
                assessment_section += f"    + {s}\n"
        if assessment.get("gaps"):
            assessment_section += "  Gaps:\n"
            for g in assessment["gaps"]:
                assessment_section += f"    - {g}\n"
        if assessment.get("skill_dimensions"):
            assessment_section += "  Skill Dimensions:\n"
            for dim in assessment["skill_dimensions"]:
                assessment_section += (
                    f"    {dim.get('name', '?')}: {dim.get('score', '?')}/{dim.get('max_score', 10)}"
                    f" ({dim.get('level', '?')})\n"
                )

    return f"""You are an expert curriculum designer for a technical education platform.

Your task is to create a PERSONALIZED learning path by selecting and sequencing EXISTING lessons from the catalog below. You must reference lessons by their exact IDs. Do NOT invent new lessons — only use lessons from the catalog.

{catalog_section}
{progress_section}
{quiz_section}
{assessment_section}

TASK: Given the student's learning goals (provided in the user message), build a personalized multi-phase curriculum.

IMPORTANT RULES:
1. ONLY reference lesson IDs that appear in the catalog above. Any ID not in the catalog will be stripped.
2. Group lessons into 3-6 logical phases. Each phase should build on the previous one.
3. If the student has already completed lessons, you may still include them if critical to the path, but prefer uncompleted lessons when possible.
4. If the student's goals mention topics NOT covered by any lesson in the catalog, list them as gaps.
5. Estimate hours per phase based on the number of lessons (roughly 1.5 hours per lesson).
6. If assessment data is available, use it to personalize: skip or accelerate areas of strength, emphasize gap areas.
7. Each phase should end with a milestone that summarizes the skills gained.
8. The personalization_note should explain WHY this particular sequence was chosen for THIS student.

RESPOND WITH ONLY valid JSON (no markdown, no code fences, no extra text) in this exact format:
{{
  "title": "A compelling curriculum title reflecting the student's goals",
  "level_range": "Beginner to Advanced",
  "estimated_hours": 48,
  "personalization_note": "2-3 sentences explaining how this curriculum was tailored to the student's profile. Reference their strengths, gaps, and goals specifically.",
  "phases": [
    {{
      "order": 1,
      "title": "Phase title — clear and descriptive",
      "level": "beginner|intermediate|advanced|expert",
      "estimated_hours": 6,
      "description": "2-3 sentences describing what the student will learn in this phase and why it comes at this point in the path.",
      "lesson_ids": ["exact-lesson-id-1", "exact-lesson-id-2"],
      "milestone_title": "Milestone Name — a certification-style title",
      "milestone_skills": ["Skill 1", "Skill 2", "Skill 3"]
    }}
  ],
  "gaps": [
    {{
      "topic": "Topic name not covered by existing lessons",
      "description": "Why this topic matters for the student's goals",
      "explore_query": "A search query the student can use in the Concept Explorer"
    }}
  ]
}}

RULES:
- All lesson_ids MUST be copied exactly from the catalog above.
- phases array should have 3-6 entries.
- Each phase should have 2-6 lessons.
- gaps array can be empty if all goals are covered, or up to 5 items.
- The title should feel like a real course title, not generic.
- All text should be plain text (no markdown formatting).
- Be specific in the personalization_note — generic platitudes are not helpful."""
