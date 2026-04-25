"""
SAGE Agent Bureau — starts all 7 uAgents in a background thread.
Called from FastAPI lifespan. Daemon thread stops with the process.
"""
import threading
import logging
from uagents import Bureau

log = logging.getLogger("sage.bureau")


def start_bureau() -> threading.Thread:
    """Start Bureau with all 7 SAGE agents. Returns the daemon thread."""
    from app.agents.director import director_agent
    from app.agents.uagents_runner import (
        pedagogy_agent,
        content_agent,
        concept_map_agent,
        assessment_agent,
        peer_match_agent,
        progress_agent,
    )

    bureau = Bureau()
    bureau.add(director_agent)
    bureau.add(pedagogy_agent)
    bureau.add(content_agent)
    bureau.add(concept_map_agent)
    bureau.add(assessment_agent)
    bureau.add(peer_match_agent)
    bureau.add(progress_agent)

    thread = threading.Thread(target=bureau.run, daemon=True, name="sage-bureau")
    thread.start()

    log.info("Bureau started — 7 agents running")
    log.info(f"  Director:    {director_agent.address}")
    log.info(f"  Pedagogy:    {pedagogy_agent.address}")
    log.info(f"  Content:     {content_agent.address}")
    log.info(f"  ConceptMap:  {concept_map_agent.address}")
    log.info(f"  Assessment:  {assessment_agent.address}")
    log.info(f"  PeerMatch:   {peer_match_agent.address}")
    log.info(f"  Progress:    {progress_agent.address}")

    return thread
