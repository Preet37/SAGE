import os
from google import genai
import cloudinary
import cloudinary.uploader
import cloudinary.api
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session as OrmSession

from app.db import get_db
from app.models import Session as TutorSession
from app.models import User
from app.security import get_current_user

# Initialize Cloudinary (Uses CLOUDINARY_URL env var automatically if set, but we can explicitly call it)
cloudinary.config()

# Initialize Gemini client lazily so missing GEMINI_API_KEY does not crash boot.
_client = None
def client():
    global _client
    if _client is None:
        _client = genai.Client()
    return _client

router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("/{session_id}")
def get_notes(
    session_id: int,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    s = db.query(TutorSession).filter(
        TutorSession.id == session_id, TutorSession.user_id == user.id
    ).first()
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": s.id, "markdown": "(notes synthesis stub)"}

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), user: User = Depends(get_current_user)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    result = cloudinary.uploader.upload(
        file.file,
        resource_type="image",
        use_filename=True,
        unique_filename=True
    )
    return {"url": result.get("secure_url"), "public_id": result.get("public_id")}

@router.post("/{session_id}/lesson-plan")
async def generate_lesson_plan(
    session_id: int,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    s = db.query(TutorSession).filter(
        TutorSession.id == session_id, TutorSession.user_id == user.id
    ).first()
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
        
    # Get topic from session history or metadata (assuming s.topic or similar exists, or just use s.id)
    # For now, we'll try to extract the main topic from the session history
    topic = "the current subject" # Default fallback
    
    prompt = f"""Act as an expert teacher. I want to learn about {topic}.

Please teach me by following these rules:

Structure: Break the topic into 5-7 logical modules, from foundational to advanced.

Method: For each module, start with a concise lecture (theory + concrete example), followed by 2 check-for-understanding questions. 
Include LaTeX formulas for any mathematical or scientific concepts (e.g., $E=mc^2$).
Include relevant image placeholders from Google Search in markdown format, e.g., ![Diagram of {topic}](https://source.unsplash.com/featured/?{topic}).

Interaction: Do not proceed to the next module until the check-for-understanding questions are correctly answered.

Tone: Clear, patient, and engaging.

Start with Module 1."""

    response = client().models.generate_content(
        model='gemini-2.0-flash', # Upgrade to 2.0 as suggested by deprecation banner check
        contents=prompt
    )
    
    return {"session_id": s.id, "lesson_plan": response.text}

@router.post("/fetch-crop")
async def fetch_and_crop(
    public_id: str, 
    topic: str,
    user: User = Depends(get_current_user)
):
    prompt = f"The user is learning about '{topic}'. Which page number (1-5) of a standard textbook is most likely to contain this? Return just the number."
    response = client().models.generate_content(
        model='gemini-1.5-flash',
        contents=prompt
    )
    try:
        page = int(response.text.strip())
    except:
        page = 1
        
    cropped_url, _ = cloudinary.utils.cloudinary_url(
        f"{public_id}.jpg",
        page=page,
        transformation=[
            {"width": 800, "crop": "limit"},
            {"effect": "enhance"}
        ]
    )
    
    return {"cropped_url": cropped_url, "page": page, "topic": topic}
