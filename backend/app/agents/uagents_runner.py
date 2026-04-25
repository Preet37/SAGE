"""
Fetch.ai uAgents — all 6 agents registered on Agentverse.
Run this file separately: python -m app.agents.uagents_runner
Each agent registers with Agentverse and implements the Chat Protocol.

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
"""
import asyncio
import json
import os
from app.config import get_settings

settings = get_settings()

try:
    from uagents import Agent, Context, Model
    from uagents.setup import fund_agent_if_low
    UAGENTS_AVAILABLE = True
except ImportError:
    UAGENTS_AVAILABLE = False
    print("uagents not installed. Install with: pip install uagents")


# ─── Message Models ───────────────────────────────────────────────
if UAGENTS_AVAILABLE:
    class TutorRequest(Model):
        user_id: int
        lesson_id: int
        question: str
        session_history: str  # JSON-encoded list

    class TutorResponse(Model):
        agent_name: str
        result: str  # JSON-encoded dict
        timestamp: str

    class ChatRequest(Model):
        content: str

    class ChatResponse(Model):
        content: str


# ─── Agent Definitions ────────────────────────────────────────────
AGENT_SEED_PREFIX = "sage_agent_seed_"


def create_pedagogy_agent():
    if not UAGENTS_AVAILABLE:
        return None

    agent = Agent(
        name="sage_pedagogy_agent",
        seed=AGENT_SEED_PREFIX + "pedagogy",
        port=8001,
        endpoint=["http://localhost:8001/submit"],
        agentverse=settings.agentverse_api_key,
    )

    @agent.on_message(model=TutorRequest)
    async def handle_pedagogy(ctx: Context, sender: str, msg: TutorRequest):
        from app.agents.orchestrator import AgentOrchestrator
        from datetime import datetime
        history = json.loads(msg.session_history or "[]")
        orch = AgentOrchestrator(msg.user_id, msg.lesson_id, msg.question, history)
        result = await orch._run_pedagogy_agent()
        await ctx.send(sender, TutorResponse(
            agent_name="pedagogy",
            result=json.dumps(result),
            timestamp=datetime.utcnow().isoformat(),
        ))

    @agent.on_message(model=ChatRequest)
    async def handle_chat_pedagogy(ctx: Context, sender: str, msg: ChatRequest):
        """ASI:One Chat Protocol handler."""
        from app.agents.base import asi1_complete
        response = await asi1_complete(
            f"As the SAGE Pedagogy Agent, respond to: {msg.content}",
            system="You are the Pedagogy Agent for SAGE, a Socratic AI tutor. Help determine optimal teaching strategies.",
        )
        await ctx.send(sender, ChatResponse(content=response))

    return agent


def create_content_agent():
    if not UAGENTS_AVAILABLE:
        return None

    agent = Agent(
        name="sage_content_agent",
        seed=AGENT_SEED_PREFIX + "content",
        port=8002,
        endpoint=["http://localhost:8002/submit"],
        agentverse=settings.agentverse_api_key,
    )

    @agent.on_message(model=TutorRequest)
    async def handle_content(ctx: Context, sender: str, msg: TutorRequest):
        from app.agents.orchestrator import AgentOrchestrator
        from datetime import datetime
        history = json.loads(msg.session_history or "[]")
        orch = AgentOrchestrator(msg.user_id, msg.lesson_id, msg.question, history)
        result = await orch._run_content_agent()
        await ctx.send(sender, TutorResponse(
            agent_name="content",
            result=json.dumps(result),
            timestamp=datetime.utcnow().isoformat(),
        ))

    @agent.on_message(model=ChatRequest)
    async def handle_chat_content(ctx: Context, sender: str, msg: ChatRequest):
        from app.agents.base import asi1_complete
        response = await asi1_complete(
            msg.content,
            system="You are the Content Agent for SAGE. You retrieve and analyze educational content for Socratic tutoring sessions.",
        )
        await ctx.send(sender, ChatResponse(content=response))

    return agent


def create_concept_map_agent():
    if not UAGENTS_AVAILABLE:
        return None

    agent = Agent(
        name="sage_concept_map_agent",
        seed=AGENT_SEED_PREFIX + "concept_map",
        port=8003,
        endpoint=["http://localhost:8003/submit"],
        agentverse=settings.agentverse_api_key,
    )

    @agent.on_message(model=TutorRequest)
    async def handle_concept_map(ctx: Context, sender: str, msg: TutorRequest):
        from app.agents.orchestrator import AgentOrchestrator
        from datetime import datetime
        history = json.loads(msg.session_history or "[]")
        orch = AgentOrchestrator(msg.user_id, msg.lesson_id, msg.question, history)
        result = await orch._run_concept_map_agent()
        await ctx.send(sender, TutorResponse(
            agent_name="concept_map",
            result=json.dumps(result),
            timestamp=datetime.utcnow().isoformat(),
        ))

    @agent.on_message(model=ChatRequest)
    async def handle_chat_concept(ctx: Context, sender: str, msg: ChatRequest):
        from app.agents.base import asi1_complete
        response = await asi1_complete(
            msg.content,
            system="You are the Concept Map Agent for SAGE. You build and update knowledge graphs of student understanding.",
        )
        await ctx.send(sender, ChatResponse(content=response))

    return agent


def create_assessment_agent():
    if not UAGENTS_AVAILABLE:
        return None

    agent = Agent(
        name="sage_assessment_agent",
        seed=AGENT_SEED_PREFIX + "assessment",
        port=8004,
        endpoint=["http://localhost:8004/submit"],
        agentverse=settings.agentverse_api_key,
    )

    @agent.on_message(model=ChatRequest)
    async def handle_chat_assessment(ctx: Context, sender: str, msg: ChatRequest):
        from app.agents.base import asi1_complete
        response = await asi1_complete(
            msg.content,
            system="You are the Assessment Agent for SAGE. You generate quizzes and evaluate student understanding.",
        )
        await ctx.send(sender, ChatResponse(content=response))

    return agent


def create_peer_match_agent():
    if not UAGENTS_AVAILABLE:
        return None

    agent = Agent(
        name="sage_peer_match_agent",
        seed=AGENT_SEED_PREFIX + "peer_match",
        port=8005,
        endpoint=["http://localhost:8005/submit"],
        agentverse=settings.agentverse_api_key,
    )

    @agent.on_message(model=ChatRequest)
    async def handle_chat_peer(ctx: Context, sender: str, msg: ChatRequest):
        from app.agents.base import asi1_complete
        response = await asi1_complete(
            msg.content,
            system="You are the Peer Match Agent for SAGE. You connect students for collaborative learning using Arista-inspired network routing.",
        )
        await ctx.send(sender, ChatResponse(content=response))

    return agent


def create_progress_agent():
    if not UAGENTS_AVAILABLE:
        return None

    agent = Agent(
        name="sage_progress_agent",
        seed=AGENT_SEED_PREFIX + "progress",
        port=8006,
        endpoint=["http://localhost:8006/submit"],
        agentverse=settings.agentverse_api_key,
    )

    @agent.on_message(model=ChatRequest)
    async def handle_chat_progress(ctx: Context, sender: str, msg: ChatRequest):
        from app.agents.base import asi1_complete
        response = await asi1_complete(
            msg.content,
            system="You are the Progress Agent for SAGE. You track student mastery and recommend personalized learning paths.",
        )
        await ctx.send(sender, ChatResponse(content=response))

    return agent


def run_all_agents():
    """Run all 6 agents. Call from main agent runner script."""
    if not UAGENTS_AVAILABLE:
        print("Cannot run agents: uagents package not installed")
        return

    agents = [
        create_pedagogy_agent(),
        create_content_agent(),
        create_concept_map_agent(),
        create_assessment_agent(),
        create_peer_match_agent(),
        create_progress_agent(),
    ]
    agents = [a for a in agents if a is not None]

    print(f"Starting {len(agents)} SAGE agents on Agentverse...")
    for agent in agents:
        print(f"  → {agent.name}: {agent.address}")

    from uagents import Bureau
    bureau = Bureau()
    for agent in agents:
        bureau.add(agent)
    bureau.run()


if __name__ == "__main__":
    run_all_agents()
