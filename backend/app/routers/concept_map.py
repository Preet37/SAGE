import os
import json
from anthropic import AsyncAnthropic
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as OrmSession

from app.db import get_db
from app.models import Concept, User
from app.schemas import ConceptOut
from app.security import get_current_user

anthropic_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

router = APIRouter(prefix="/concept-map", tags=["concept-map"])

@router.get("/{session_id}", response_model=list[ConceptOut])
def get_map(
    session_id: int,
    db: OrmSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return db.query(Concept).filter(Concept.session_id == session_id).all()

@router.post("/generate/{topic}")
async def generate_map(
    topic: str,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    prompt = f"Create an obsidian-style knowledge graph for the topic '{topic}'. Return ONLY valid JSON with 'nodes' (list of objects with 'id' and 'label') and 'edges' (list of objects with 'source' and 'target'). Do not include markdown formatting like ```json."
    
    response = await anthropic_client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    try:
        text = response.content[0].text.strip()
        if text.startswith("```json"):
            text = text[7:-3]
        graph_data = json.loads(text)
    except Exception as e:
        graph_data = {"nodes": [], "edges": [], "error": str(e)}
        
    return {"topic": topic, "graph": graph_data}
