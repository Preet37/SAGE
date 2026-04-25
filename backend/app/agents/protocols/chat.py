"""Chat Protocol message models for Agentverse Chat Protocol."""
from uagents import Model


class ChatMessage(Model):
    """Incoming message from ASI:One or any Agentverse agent."""
    content: str
    session_id: str = ""
    lesson_id: int = 1
    teaching_mode: str = "default"


class ChatResponse(Model):
    """Response sent back to the caller."""
    content: str
    agent_trace: dict = {}
    confidence_score: int = 75
