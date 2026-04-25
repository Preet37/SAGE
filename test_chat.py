import asyncio
from app.db import SessionLocal
from app.models import User, Session as TutorSession, Lesson
from app.agents.orchestrator import Orchestrator
from app.agents.base import AgentContext

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

async def test_chat():
    db = SessionLocal()
    # Ensure a user exists
    user = db.query(User).first()
    if not user:
        user = User(email="test@example.com", hashed_password="stub")
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Ensure a lesson exists
    lesson = db.query(Lesson).first()
    if not lesson:
        lesson = Lesson(title="Capacitors", objective="Learn about capacitors and capacitance.", owner_id=user.id)
        db.add(lesson)
        db.commit()
        db.refresh(lesson)

    # Create a session
    session = TutorSession(user_id=user.id, lesson_id=lesson.id)
    db.add(session)
    db.commit()
    db.refresh(session)

    print(f"Testing chat for session {session.id}...")
    
    ctx = AgentContext(
        session_id=session.id,
        user_id=user.id,
        user_message="I want to learn about capacitors",
        sources=["Capacitors store electrical energy in an electric field."],
    )
    
    orchestrator = Orchestrator()
    ctx = await orchestrator.run_turn(ctx)
    
    print("\n--- SAGE RESPONSE ---")
    print(ctx.answer)
    print("----------------------\n")
    
    if "Module 1" in ctx.answer and "lecture" in ctx.answer.lower():
        print("SUCCESS: Response followed the Expert Teacher format!")
    else:
        print("FAILURE: Response did not follow the requested format.")

if __name__ == "__main__":
    import os
    # Ensure keys are set for testing (they should be in .env)
    from dotenv import load_dotenv
    load_dotenv()
    
    asyncio.run(test_chat())
