import pytest

from app.agents.base import AgentContext, LLM, StubProvider
from app.agents.orchestrator import Orchestrator


def _ctx(**kw) -> AgentContext:
    base = dict(
        session_id=1,
        user_id=1,
        user_message="What is photosynthesis?",
        sources=["Photosynthesis converts light into chemical energy in plants."],
        mastery=[
            {"label": "Chlorophyll", "mastery": 0.3},
            {"label": "Mitochondria", "mastery": 0.85},
        ],
    )
    base.update(kw)
    return AgentContext(**base)


@pytest.fixture
def orch() -> Orchestrator:
    return Orchestrator(llm=LLM(StubProvider()))


async def test_run_turn_populates_all_fields(orch):
    ctx = await orch.run_turn(_ctx())
    assert ctx.plan and ctx.plan["strategy"] in {"scaffold", "extend", "socratic"}
    assert ctx.answer.startswith("[stub:")
    assert "score" in ctx.verification
    assert isinstance(ctx.concept_map_delta, list)
    assert "skip" in ctx.assessment
    assert isinstance(ctx.peers, list)
    assert "by_concept" in ctx.progress_delta


async def test_pedagogy_picks_scaffold_when_weak(orch):
    ctx = await orch.run_turn(_ctx(mastery=[{"label": "X", "mastery": 0.1}]))
    assert ctx.plan["strategy"] == "scaffold"
    assert "X" in ctx.plan["weak_concepts"]


async def test_pedagogy_picks_extend_when_strong(orch):
    ctx = await orch.run_turn(_ctx(mastery=[{"label": "Y", "mastery": 0.9}]))
    assert ctx.plan["strategy"] == "extend"


async def test_trace_records_each_agent(orch):
    ctx = await orch.run_turn(_ctx())
    senders = {m.sender for m in ctx.trace}
    assert {"pedagogy", "content", "concept_map", "assessment", "peer_match", "progress"} <= senders


async def test_stream_turn_yields_expected_events(orch):
    events = [name async for name, _ in orch.stream_turn(_ctx())]
    # Must end with `done` and contain a verification event.
    assert events[0] == "agent_event"
    assert "verification" in events
    assert events[-1] == "done"


async def test_llm_falls_back_on_primary_failure():
    class Boom:
        name = "boom"

        async def complete(self, *a, **k):
            raise RuntimeError("nope")

    fb = StubProvider()
    fb.name = "fallback-stub"
    llm = LLM(primary=Boom(), fallback=fb)
    out = await llm.complete("sys", "hi")
    assert out.startswith("[stub:")
