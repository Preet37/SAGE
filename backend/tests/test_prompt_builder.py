from app.core.prompt_builder import A11yProfile, ConceptMastery, build_system_prompt


def test_default_prompt_contains_socratic_core():
    p = build_system_prompt(A11yProfile(), [])
    assert "Socratic tutor" in p
    assert "Constraints" not in p  # no a11y or mastery → no constraints block


def test_dyslexia_adds_short_sentence_rule():
    p = build_system_prompt(A11yProfile(dyslexia_font=True), [])
    assert "short sentences" in p.lower()


def test_mastery_scaffolds_weak_concepts():
    mastery = [
        ConceptMastery("derivatives", 0.2),
        ConceptMastery("integrals", 0.9),
    ]
    p = build_system_prompt(A11yProfile(), mastery)
    assert "derivatives" in p
    assert "Scaffold" in p
    assert "integrals" in p
    assert "mastered" in p


def test_sources_included_with_indices():
    p = build_system_prompt(A11yProfile(), [], sources=["alpha", "beta"])
    assert "[0] alpha" in p
    assert "[1] beta" in p


def test_objective_included_when_present():
    p = build_system_prompt(A11yProfile(), [], objective="Understand mitosis stages")
    assert "Understand mitosis stages" in p
