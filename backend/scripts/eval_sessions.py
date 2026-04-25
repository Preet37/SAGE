#!/usr/bin/env python3
"""Production session analyzer — detect dead-ends, tool usage patterns, modalities.

Analyzes real user sessions from the database to surface quality issues that
synthetic evals can't catch.

Usage:
    python -m scripts.eval_sessions                    # Analyze all sessions (last 7 days)
    python -m scripts.eval_sessions --days 30          # Last 30 days
    python -m scripts.eval_sessions --session-id abc   # Specific session
    python -m scripts.eval_sessions --json             # Output as JSON
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select
from app.db import engine
from app.models.progress import ChatMessage, TutorSession
from app.models.exploration import ExplorationMessage, ExplorationSession


@dataclass
class SessionAnalysis:
    """Analysis results for a single session."""
    session_id: str
    session_type: str  # "tutor" | "explore"
    message_count: int
    user_message_count: int
    assistant_message_count: int
    tools_used: list[str] = field(default_factory=list)
    modalities_used: list[str] = field(default_factory=list)
    is_dead_end: bool = False
    dead_end_reason: str = ""
    avg_response_length: float = 0.0
    created_at: Optional[datetime] = None
    duration_minutes: float = 0.0

    def as_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "session_type": self.session_type,
            "message_count": self.message_count,
            "user_message_count": self.user_message_count,
            "assistant_message_count": self.assistant_message_count,
            "tools_used": self.tools_used,
            "modalities_used": self.modalities_used,
            "is_dead_end": self.is_dead_end,
            "dead_end_reason": self.dead_end_reason,
            "avg_response_length": self.avg_response_length,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "duration_minutes": self.duration_minutes,
        }


@dataclass
class AggregateAnalysis:
    """Aggregate analysis across all sessions."""
    total_sessions: int = 0
    total_messages: int = 0
    dead_end_count: int = 0
    dead_end_rate: float = 0.0
    tool_usage: Counter = field(default_factory=Counter)
    modality_usage: Counter = field(default_factory=Counter)
    sessions_with_no_tools: int = 0
    no_tool_rate: float = 0.0
    avg_messages_per_session: float = 0.0
    avg_response_length: float = 0.0
    dead_end_sessions: list[SessionAnalysis] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "total_sessions": self.total_sessions,
            "total_messages": self.total_messages,
            "dead_end_count": self.dead_end_count,
            "dead_end_rate": self.dead_end_rate,
            "tool_usage": dict(self.tool_usage),
            "modality_usage": dict(self.modality_usage),
            "sessions_with_no_tools": self.sessions_with_no_tools,
            "no_tool_rate": self.no_tool_rate,
            "avg_messages_per_session": self.avg_messages_per_session,
            "avg_response_length": self.avg_response_length,
            "dead_end_sessions": [s.as_dict() for s in self.dead_end_sessions[:10]],
        }


def _detect_dead_end(messages: list[dict]) -> tuple[bool, str]:
    """Detect if a conversation ended in a dead-end.
    
    Dead-end patterns:
    - Single exchange (user asked, tutor answered, user left)
    - User's last message indicates confusion/frustration
    - Very short final assistant response
    - Repeated similar questions (user didn't get it)
    """
    if len(messages) < 2:
        return False, ""
    
    user_messages = [m for m in messages if m["role"] == "user"]
    assistant_messages = [m for m in messages if m["role"] == "assistant"]
    
    if not user_messages or not assistant_messages:
        return False, ""
    
    # Single exchange — user didn't continue
    if len(user_messages) == 1 and len(assistant_messages) == 1:
        return True, "single_exchange"
    
    # Check last user message for frustration signals
    last_user = user_messages[-1]["content"].lower() if user_messages else ""
    frustration_signals = [
        "i don't understand", "confused", "what do you mean",
        "that doesn't make sense", "still don't get", "help",
        "??" , "not helpful", "try again",
    ]
    if any(sig in last_user for sig in frustration_signals):
        return True, "user_frustration"
    
    # Very short final response (tutor gave up or errored)
    last_assistant = assistant_messages[-1]["content"] if assistant_messages else ""
    if len(last_assistant) < 50:
        return True, "short_final_response"
    
    # Repeated questions (user asked same thing multiple times)
    if len(user_messages) >= 3:
        last_three = [m["content"].lower()[:100] for m in user_messages[-3:]]
        if len(set(last_three)) == 1:
            return True, "repeated_question"
    
    return False, ""


def analyze_tutor_session(session_id: str, db: Session) -> Optional[SessionAnalysis]:
    """Analyze a tutor session."""
    tutor_session = db.get(TutorSession, session_id)
    if not tutor_session:
        return None
    
    messages = db.exec(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
    ).all()
    
    if not messages:
        return None
    
    tools_used = []
    modalities_used = []
    response_lengths = []
    
    for msg in messages:
        if msg.role == "assistant":
            response_lengths.append(len(msg.content))
            if msg.message_meta:
                try:
                    meta = json.loads(msg.message_meta)
                    tools_used.extend(meta.get("tools_used", []))
                    modalities_used.extend(meta.get("modalities", []))
                except (json.JSONDecodeError, TypeError):
                    pass
    
    msg_dicts = [{"role": m.role, "content": m.content} for m in messages]
    is_dead_end, reason = _detect_dead_end(msg_dicts)
    
    user_count = sum(1 for m in messages if m.role == "user")
    assistant_count = sum(1 for m in messages if m.role == "assistant")
    
    duration = 0.0
    if len(messages) >= 2:
        duration = (messages[-1].created_at - messages[0].created_at).total_seconds() / 60
    
    return SessionAnalysis(
        session_id=session_id,
        session_type="tutor",
        message_count=len(messages),
        user_message_count=user_count,
        assistant_message_count=assistant_count,
        tools_used=list(set(tools_used)),
        modalities_used=list(set(modalities_used)),
        is_dead_end=is_dead_end,
        dead_end_reason=reason,
        avg_response_length=sum(response_lengths) / len(response_lengths) if response_lengths else 0,
        created_at=tutor_session.created_at,
        duration_minutes=duration,
    )


def analyze_explore_session(session_id: str, db: Session) -> Optional[SessionAnalysis]:
    """Analyze an explore session."""
    explore_session = db.get(ExplorationSession, session_id)
    if not explore_session:
        return None
    
    messages = db.exec(
        select(ExplorationMessage)
        .where(ExplorationMessage.session_id == session_id)
        .order_by(ExplorationMessage.created_at)
    ).all()
    
    if not messages:
        return None
    
    tools_used = []
    modalities_used = []
    response_lengths = []
    
    for msg in messages:
        if msg.role == "assistant":
            response_lengths.append(len(msg.content))
            if msg.message_meta:
                try:
                    meta = json.loads(msg.message_meta)
                    tools_used.extend(meta.get("tools_used", []))
                    modalities_used.extend(meta.get("modalities", []))
                except (json.JSONDecodeError, TypeError):
                    pass
    
    msg_dicts = [{"role": m.role, "content": m.content} for m in messages]
    is_dead_end, reason = _detect_dead_end(msg_dicts)
    
    user_count = sum(1 for m in messages if m.role == "user")
    assistant_count = sum(1 for m in messages if m.role == "assistant")
    
    duration = 0.0
    if len(messages) >= 2:
        duration = (messages[-1].created_at - messages[0].created_at).total_seconds() / 60
    
    return SessionAnalysis(
        session_id=session_id,
        session_type="explore",
        message_count=len(messages),
        user_message_count=user_count,
        assistant_message_count=assistant_count,
        tools_used=list(set(tools_used)),
        modalities_used=list(set(modalities_used)),
        is_dead_end=is_dead_end,
        dead_end_reason=reason,
        avg_response_length=sum(response_lengths) / len(response_lengths) if response_lengths else 0,
        created_at=explore_session.created_at,
        duration_minutes=duration,
    )


def analyze_all_sessions(days: int = 7) -> AggregateAnalysis:
    """Analyze all sessions from the last N days."""
    cutoff = datetime.utcnow() - timedelta(days=days)
    
    with Session(engine) as db:
        # Get tutor sessions
        tutor_sessions = db.exec(
            select(TutorSession)
            .where(TutorSession.created_at >= cutoff)
        ).all()
        
        # Get explore sessions
        explore_sessions = db.exec(
            select(ExplorationSession)
            .where(ExplorationSession.created_at >= cutoff)
        ).all()
        
        analyses: list[SessionAnalysis] = []
        
        for ts in tutor_sessions:
            analysis = analyze_tutor_session(ts.id, db)
            if analysis:
                analyses.append(analysis)
        
        for es in explore_sessions:
            analysis = analyze_explore_session(es.id, db)
            if analysis:
                analyses.append(analysis)
    
    if not analyses:
        return AggregateAnalysis()
    
    agg = AggregateAnalysis()
    agg.total_sessions = len(analyses)
    agg.total_messages = sum(a.message_count for a in analyses)
    
    dead_ends = [a for a in analyses if a.is_dead_end]
    agg.dead_end_count = len(dead_ends)
    agg.dead_end_rate = len(dead_ends) / len(analyses) if analyses else 0
    agg.dead_end_sessions = sorted(dead_ends, key=lambda a: a.created_at or datetime.min, reverse=True)
    
    for a in analyses:
        for tool in a.tools_used:
            agg.tool_usage[tool] += 1
        for mod in a.modalities_used:
            agg.modality_usage[mod] += 1
        if not a.tools_used:
            agg.sessions_with_no_tools += 1
    
    agg.no_tool_rate = agg.sessions_with_no_tools / len(analyses) if analyses else 0
    agg.avg_messages_per_session = agg.total_messages / len(analyses) if analyses else 0
    agg.avg_response_length = sum(a.avg_response_length for a in analyses) / len(analyses) if analyses else 0
    
    return agg


def print_report(agg: AggregateAnalysis) -> None:
    """Print a human-readable report."""
    print("\n" + "=" * 60)
    print("  PRODUCTION SESSION ANALYSIS")
    print("=" * 60)
    
    print(f"\n  Total Sessions:        {agg.total_sessions}")
    print(f"  Total Messages:        {agg.total_messages}")
    print(f"  Avg Messages/Session:  {agg.avg_messages_per_session:.1f}")
    print(f"  Avg Response Length:   {agg.avg_response_length:.0f} chars")
    
    print(f"\n  --- Dead-End Detection ---")
    print(f"  Dead-End Sessions:     {agg.dead_end_count} ({agg.dead_end_rate:.1%})")
    
    if agg.dead_end_sessions:
        print(f"\n  Recent Dead-Ends:")
        for s in agg.dead_end_sessions[:5]:
            print(f"    - {s.session_id[:8]}... ({s.session_type}) — {s.dead_end_reason}")
    
    print(f"\n  --- Tool Usage ---")
    print(f"  Sessions with NO tools: {agg.sessions_with_no_tools} ({agg.no_tool_rate:.1%})")
    
    if agg.tool_usage:
        print(f"\n  Tool Usage (sessions):")
        for tool, count in agg.tool_usage.most_common(10):
            print(f"    {tool:<25} {count:>5} ({count/agg.total_sessions:.1%})")
    
    print(f"\n  --- Modality Usage ---")
    if agg.modality_usage:
        for mod, count in agg.modality_usage.most_common(10):
            print(f"    {mod:<25} {count:>5} ({count/agg.total_sessions:.1%})")
    
    print()


def main():
    parser = argparse.ArgumentParser(description="Analyze production sessions")
    parser.add_argument("--days", type=int, default=7, help="Look back N days (default: 7)")
    parser.add_argument("--session-id", help="Analyze a specific session")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    if args.session_id:
        with Session(engine) as db:
            # Try tutor session first
            analysis = analyze_tutor_session(args.session_id, db)
            if not analysis:
                analysis = analyze_explore_session(args.session_id, db)
            
            if not analysis:
                print(f"Session not found: {args.session_id}")
                return
            
            if args.json:
                print(json.dumps(analysis.as_dict(), indent=2))
            else:
                print(f"\nSession: {analysis.session_id}")
                print(f"Type: {analysis.session_type}")
                print(f"Messages: {analysis.message_count}")
                print(f"Tools: {', '.join(analysis.tools_used) or 'none'}")
                print(f"Modalities: {', '.join(analysis.modalities_used) or 'none'}")
                print(f"Dead-end: {analysis.is_dead_end} ({analysis.dead_end_reason})")
    else:
        agg = analyze_all_sessions(days=args.days)
        
        if args.json:
            print(json.dumps(agg.as_dict(), indent=2))
        else:
            print_report(agg)


if __name__ == "__main__":
    main()
