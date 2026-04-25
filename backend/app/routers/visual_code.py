"""
Visual Code Generation endpoint.
LLM writes actual Three.js JavaScript code (150-400 lines).
Frontend runs it in a sandboxed iframe. Works for ANY concept.
"""
import re
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from app.database import get_db
from app.models.user import User
from app.models.lesson import Lesson, Course
from app.routers.auth import get_current_user
from app.config import get_settings, load_yaml_config
import httpx

router = APIRouter(prefix="/visual", tags=["visual"])
settings = get_settings()
yaml_cfg = load_yaml_config()

THREEJS_PROMPT = """\
You are an elite Three.js 3D graphics programmer and educational visualizer.

Your task: Write complete, production-quality Three.js r128 JavaScript code that creates a \
stunning, scientifically accurate 3D visualization of: {concept}

CONTEXT: {context}

═══════════════════════════════════════════════════════
ENVIRONMENT ALREADY PROVIDED (DO NOT RE-DECLARE):
  • THREE     — three.js r128 global
  • scene     — THREE.Scene (fog, dark background)
  • camera    — THREE.PerspectiveCamera at (6, 5, 10)
  • renderer  — WebGLRenderer (shadows ON, ACES tonemapping)
  • controls  — OrbitControls with damping
  • Lights already added: HemisphereLight + DirectionalLight + 2 PointLights
  • GridHelper at y=0 already added
  • Stars already added

YOUR OUTPUT: Write ONLY the object-specific Three.js code. 150–400 lines.
             End with: function animate() {{ ... }} animate();
═══════════════════════════════════════════════════════

GEOMETRY RULES — use the RIGHT geometry, not lazy boxes:

  Tapered/cylindrical objects (towers, columns, bottles, vases):
    const pts = [new THREE.Vector2(r0,y0), ...];
    const geo = new THREE.LatheGeometry(pts, 64);

  Complex cross-section shapes (blades, fins, brackets, wings):
    const shape = new THREE.Shape();
    shape.moveTo(x, y); shape.bezierCurveTo(...); shape.closePath();
    const geo = new THREE.ExtrudeGeometry(shape, {{depth:d, bevelEnabled:true, bevelSize:0.02}});

  Wires, cables, springs, DNA, coils:
    const curve = new THREE.CatmullRomCurve3([new THREE.Vector3(x,y,z), ...]);
    const geo = new THREE.TubeGeometry(curve, 80, radius, 12, false);

  Spheres with detail: new THREE.SphereGeometry(r, 64, 64)
  Smooth cylinders: new THREE.CylinderGeometry(rt, rb, h, 48, 1, false)
  Tori, coils: new THREE.TorusGeometry(R, r, 20, 64)

MATERIAL RULES — ALWAYS use MeshStandardMaterial or MeshPhysicalMaterial:

  Metals (steel, chrome, copper):
    new THREE.MeshStandardMaterial({{color:0xcccccc, metalness:0.85, roughness:0.15}})

  Painted surfaces (nacelle, housings):
    new THREE.MeshStandardMaterial({{color:0xe8e8e8, metalness:0.1, roughness:0.35}})

  Glass / transparent:
    new THREE.MeshPhysicalMaterial({{color:0x88ccff, transmission:0.92, roughness:0.05, metalness:0, ior:1.5}})

  Emissive / glowing:
    new THREE.MeshStandardMaterial({{color:0xff4400, emissive:0xff2200, emissiveIntensity:0.6}})

  Rubber / matte:
    new THREE.MeshStandardMaterial({{color:0x222222, metalness:0, roughness:0.95}})

SHADOW RULES:
  Every major mesh: mesh.castShadow = true; mesh.receiveShadow = true;
  Ground plane: ground.receiveShadow = true; (castShadow = false)

ANIMATION RULES:
  - Rotating parts: use a THREE.Group, set group.rotation.axis += speed each frame
  - Oscillating: use Math.sin(clock.getElapsedTime() * freq) * amplitude
  - ALWAYS declare: const clock = new THREE.Clock();
  - ALWAYS end with function animate() and animate(); call

SCALE: Objects should fit roughly within -6 to +6 on each axis.

QUALITY CHECKLIST — before finishing, verify:
  ✓ At least 8–15 distinct named parts
  ✓ Every part has correct real-world proportions
  ✓ Materials differentiated (metal vs painted vs glass vs rubber)
  ✓ At least one animated component
  ✓ Shadows cast and received
  ✓ Labels or structural detail lines where helpful

CRITICAL OUTPUT FORMAT RULES:
- Output ONLY raw JavaScript. No markdown. No ``` fences. No explanations.
- Start immediately with your first const/let/var declaration.
- End with function animate() {{ ... }} and the call animate();
- No TypeScript. Pure JavaScript only.
- Do not re-declare: THREE, scene, camera, renderer, controls, clock, W, H, grid, hemi, sun
"""

class VisualCodeRequest(BaseModel):
    concept: str
    context: str = ""
    lesson_id: Optional[int] = None


async def _call_groq_code(prompt: str) -> str:
    """Call Groq with high token budget for code generation."""
    from openai import AsyncOpenAI
    groq_base = yaml_cfg["llm"]["groq_base"]
    model = yaml_cfg.get("models", {}).get("tutor", {}).get("groq", "llama-3.3-70b-versatile")

    client = AsyncOpenAI(base_url=groq_base, api_key=settings.llm_api_key)
    resp = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
        temperature=0.2,  # low temp for reliable code
        stream=False,
    )
    return resp.choices[0].message.content or ""


def _extract_code(raw: str) -> str:
    """Extract JavaScript from LLM output — strip markdown fences if present."""
    # Strip ```javascript ... ``` or ``` ... ``` wrappers
    match = re.search(r"```(?:javascript|js|threejs)?\s*\n([\s\S]*?)```", raw, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # If no fences, return raw (already raw JS)
    return raw.strip()


@router.post("/code")
async def generate_visual_code(
    req: VisualCodeRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    LLM writes full Three.js JavaScript code for any concept.
    Frontend runs it in a sandboxed iframe. No pre-built scenes needed.
    """
    lesson_context = ""
    title = req.concept.title()

    if req.lesson_id:
        lesson_result = await db.execute(select(Lesson).where(Lesson.id == req.lesson_id))
        lesson = lesson_result.scalar_one_or_none()
        if lesson:
            course_result = await db.execute(select(Course).where(Course.id == lesson.course_id))
            course = course_result.scalar_one_or_none()
            lesson_context = f"Course: {course.title if course else ''} | Lesson: {lesson.title}"
            title = lesson.title

    context_str = f"{lesson_context}. {req.context[:300]}" if lesson_context else req.context[:400]

    prompt = THREEJS_PROMPT.format(
        concept=req.concept,
        context=context_str or "General educational visualization",
    )

    raw = await _call_groq_code(prompt)
    code = _extract_code(raw)

    if len(code) < 100:
        raise HTTPException(status_code=422, detail="LLM did not generate valid Three.js code")

    return {
        "code": code,
        "title": title,
        "concept": req.concept,
        "lines": len(code.splitlines()),
    }
