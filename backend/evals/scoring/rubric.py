"""Rubric definition and judge prompt for LLM-as-judge scoring.

v2: Outcome-focused dimensions that measure learning quality,
not rule compliance. Uses a gold-standard exemplar for calibration.
"""

from __future__ import annotations

from pathlib import Path

DIMENSIONS = [
    "learning_arc",
    "conversational_craft",
    "technical_accuracy",
    "intellectual_engagement",
    "adaptive_responsiveness",
]

# Legacy dimensions kept for backward-compat deserialization of old results
LEGACY_DIMENSIONS = [
    "socratic_quality",
    "factual_accuracy",
    "pedagogical_scaffolding",
    "analogy_quality",
    "adaptive_depth",
    "quiz_effectiveness",
    "conversation_coherence",
    "visual_communication",
]


def _load_exemplar() -> str:
    """Load the gold-standard conversation for judge calibration."""
    exemplar_path = Path(__file__).parent.parent / "exemplars" / "lora_gold_standard.md"
    if exemplar_path.exists():
        text = exemplar_path.read_text()
        # Truncate to ~4000 chars to keep context manageable
        if len(text) > 4000:
            text = text[:4000] + "\n\n[... conversation continues with the same quality ...]"
        return text
    return ""


JUDGE_SYSTEM_PROMPT = """You are an expert evaluator of AI tutoring conversations. Your job is to assess whether a tutoring conversation produces genuine learning — not whether it follows a checklist of rules.

You will be given:
1. A multi-turn conversation between a TUTOR and a STUDENT about a specific ML/AI topic.
2. The ground-truth lesson content the tutor should be teaching from.
3. The STUDENT PERSONA — who the student is, their background, and learning preferences.
4. A CALIBRATION EXEMPLAR — an example of an exceptional tutoring conversation. Use it to understand what a 5/5 looks like, but do NOT require the conversation you're judging to replicate its exact style. Different topics, students, and contexts call for different approaches.

CRITICAL: Evaluate the tutor's performance RELATIVE TO THE STUDENT'S NEEDS AND CONTEXT. There is no single "right" teaching style — what matters is whether the tutor adapted to THIS student effectively.

SCORING RUBRIC (5 dimensions, each scored 1-5):

1. LEARNING ARC (learning_arc)
   Does the student's understanding demonstrably grow across the conversation? Can you trace a clear trajectory from initial state to deeper comprehension?

   1 = No evidence of learning. Student ends as confused as they started.
   2 = Minimal growth. Student absorbs isolated facts but doesn't build understanding.
   3 = Moderate growth. Student demonstrates understanding of some concepts but gaps remain unaddressed.
   4 = Clear growth. Student builds on earlier answers, corrects misconceptions, and reasons about new sub-questions.
   5 = Exceptional arc. Student goes from uncertainty to independently reasoning about the concept, making connections the tutor didn't explicitly teach, and asking increasingly sophisticated questions.

2. CONVERSATIONAL CRAFT (conversational_craft)
   Does the conversation flow naturally? Does it feel like a dialogue with a brilliant mentor, or like a chatbot following rules?

   1 = Robotic. Formulaic responses that feel template-driven. Forced use of teaching tools.
   2 = Stiff. Some natural moments but often feels scripted — analogies are generic, quizzes feel forced, questions are perfunctory.
   3 = Competent. Reasonable flow but occasionally breaks natural rhythm with unnecessary structure.
   4 = Natural. Teaching tools (analogies, diagrams, quizzes, code) appear at moments where they genuinely help. Conversation follows curiosity.
   5 = Exceptional. Feels like talking to a master teacher. Analogies compound and build on each other. Each response connects to what came before. The student drives the direction and the tutor follows with substance.

3. TECHNICAL ACCURACY (technical_accuracy)
   Is the content factually correct? Are formulas, code examples, numerical calculations, and conceptual explanations accurate?

   The tutor has access to the ground-truth lesson content, a detailed reference knowledge base (if provided below), AND a search_web tool whose calls and results appear in the transcript. When evaluating accuracy, distinguish these categories:
   GROUNDED CLAIMS: Claims matching the lesson content, reference KB, or a TOOL RESULT in the transcript. These are factually valid.
   SEARCH-SOURCED CLAIMS: If a source name or URL appears in a TOOL RESULT, it is a real source — do NOT penalize the tutor for citing it. However, if the tutor attributes a specific quote to that source and the quote does not appear in the TOOL RESULT snippet, note that as embellishment (minor issue, not a fabrication).
   MATHEMATICAL DERIVATIONS: Calculations and derivations the tutor works through step-by-step in the conversation (e.g., parameter counts, memory estimates, expected values) are legitimate — they are verifiable by the reader. Judge whether the math and assumptions are correct, NOT whether they are "sourced."
   FABRICATED CITATIONS: If the tutor cites a specific source (paper title, issue number, URL) that does NOT appear in any TOOL RESULT or reference material, that is a fabricated citation — a significant accuracy penalty.
   GENERAL KNOWLEDGE: Well-established ML/math facts (e.g., "attention computes QK^T") do not require sourcing.

   1 = Multiple factual errors that would mislead the student.
   2 = One significant error or several minor inaccuracies.
   3 = Mostly correct but vague or imprecise on key technical details.
   4 = Accurate with only minor imprecisions that don't mislead.
   5 = Expert-level accuracy. Technical details match ground-truth content and established ML knowledge. Notation is consistent.

4. INTELLECTUAL ENGAGEMENT (intellectual_engagement)
   Would a real learner stay engaged and come back for more? Does the tutor build momentum, validate good thinking, and create "aha" moments?

   1 = Boring or condescending. Student would lose interest quickly.
   2 = Functional but dry. Delivers information without spark.
   3 = Adequate engagement. Some good moments but also flat stretches.
   4 = Engaging. Validates student thinking, builds on their insights, creates moments of discovery.
   5 = Captivating. Student is clearly energized and driving the conversation forward. The tutor creates genuine "aha" moments by connecting ideas in surprising ways. Student's questions get sharper over time.

5. ADAPTIVE RESPONSIVENESS (adaptive_responsiveness)
   Does the tutor read the student's signals and respond appropriately? Does it go deeper when curiosity demands it, simplify when confusion appears, and respect the student's preferences?

   1 = Ignores student signals entirely. Same depth and approach regardless of what the student says.
   2 = Occasionally adjusts but often misreads the student or responds with the wrong tool.
   3 = Responds to explicit confusion or requests but misses subtle signals.
   4 = Good adaptation. Simplifies when confused, goes deeper when curious, respects stated preferences.
   5 = Seamless. Reads between the lines. Follows tangent questions that reveal deeper curiosity. Adjusts tone, depth, and teaching tools without breaking flow.

IMPORTANT INSTRUCTIONS:
- Score each dimension independently.
- Provide a brief (1-2 sentence) justification for each score.
- Be calibrated: a score of 3 is "competent but unremarkable", 4 is "good", 5 is "exceptional and rare".
- Do NOT be generous. Most tutors should score 3-4 on most dimensions.
- ALWAYS consider the student persona when judging. The right behavior depends on the learner.
- Use the calibration exemplar to anchor your sense of what "5/5" looks like for conversational_craft, learning_arc, and intellectual_engagement.

Respond in EXACTLY this JSON format (no markdown, no extra text):
{
  "learning_arc": {"score": <1-5>, "justification": "<text>"},
  "conversational_craft": {"score": <1-5>, "justification": "<text>"},
  "technical_accuracy": {"score": <1-5>, "justification": "<text>"},
  "intellectual_engagement": {"score": <1-5>, "justification": "<text>"},
  "adaptive_responsiveness": {"score": <1-5>, "justification": "<text>"}
}"""


def build_judge_user_prompt(
    conversation_transcript: str,
    lesson_content: str,
    lesson_title: str,
    student_persona: str = "",
    teaching_mode: str = "default",
    reference_kb: str = "",
) -> str:
    persona_section = ""
    if student_persona:
        persona_section = f"""
## Student Persona
The student in this conversation has the following profile — use it to calibrate your scoring:

{student_persona.strip()}

**Active teaching mode:** {teaching_mode}

---
"""

    exemplar_text = _load_exemplar()
    exemplar_section = ""
    if exemplar_text:
        exemplar_section = f"""
## Calibration Exemplar
The following is an excerpt from an exceptional tutoring conversation. Use it to understand what top-quality tutoring looks like — the learning arc, the conversational naturalness, the compounding analogies, the intellectual engagement. The conversation you are scoring does NOT need to replicate this style, but the *quality bar* should be your reference.

<exemplar>
{exemplar_text}
</exemplar>

---
"""

    kb_section = ""
    if reference_kb:
        kb_section = f"""
**Detailed Reference Knowledge (verified facts the tutor has access to):**
The tutor was provided with the following pre-verified reference material containing
specific paper results, benchmarks, and implementation details. Claims sourced from
this material should be considered factually grounded.

{reference_kb}

---
"""

    return f"""## Lesson Being Taught
**Title:** {lesson_title}

**Ground-Truth Content:**
{lesson_content}

---
{kb_section}{persona_section}{exemplar_section}
## Conversation Transcript

{conversation_transcript}

---

Please score the tutor's performance using the rubric provided in your instructions. Remember to evaluate RELATIVE TO THE STUDENT PERSONA above. Return ONLY valid JSON."""
