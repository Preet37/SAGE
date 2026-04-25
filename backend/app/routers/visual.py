"""
Visual generation endpoint.
LLM generates a VIZCONFIG JSON → frontend Three.js scenes consume it.
Same pattern as Loomin's SIMCONFIG: LLM as programmer, not pixel generator.
"""
import json
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
from app.agents.base import asi1_complete

router = APIRouter(prefix="/visual", tags=["visual"])

# Supported viz types and what params they expect
VIZ_SCHEMA = {
    "mechanical": {
        "description": "High-quality 3D mechanical/physics object with real geometry — wind turbine, pendulum, atom, orbital mechanics, spring-mass, gear system",
        "params": {
            "subtype": "wind_turbine | pendulum | atom | orbital | spring | gears",
            "animated": "bool — animate the system",
            "rpm": "(wind_turbine) float — rotor RPM",
            "length": "(pendulum) float — arm length",
            "angle": "(pendulum) float — initial angle degrees",
            "protons": "(atom) int — proton count",
            "electrons": "(atom) int — electron count",
            "shells": "(atom) array of ints — electrons per shell e.g. [2,8,6]",
            "element": "(atom) string — element name",
            "bodies": "(orbital) int — number of planets",
            "springConstant": "(spring) float — k value N/m",
            "mass": "(spring) float — mass kg",
            "amplitude": "(spring) float — displacement m",
            "gears": "(gears) int — number of gears",
        }
    },
    "neural_network": {
        "description": "3D neural network with layers, nodes, animated forward pass",
        "params": {
            "layers": "array of ints e.g. [2,4,4,1] — neurons per layer",
            "activations": "array of strings e.g. ['relu','relu','sigmoid']",
            "highlightLayer": "int — which layer to highlight (0-indexed)",
            "showWeights": "bool — show weight edges",
            "animated": "bool — animate forward pass",
            "title": "string",
            "description": "string"
        }
    },
    "gradient_descent": {
        "description": "3D loss landscape with gradient descent path",
        "params": {
            "lossType": "bowl|saddle|ravine|noisy",
            "learningRate": "float 0.01-1.0",
            "steps": "int 5-30",
            "startPos": "[x, y] float array",
            "title": "string",
            "description": "string"
        }
    },
    "attention": {
        "description": "Transformer attention mechanism — Q K V matrices animated",
        "params": {
            "tokens": "array of strings e.g. ['The','cat','sat']",
            "highlightToken": "int — which token is querying",
            "attentionWeights": "2D array of floats (NxN) — attention scores",
            "title": "string",
            "description": "string"
        }
    },
    "data_flow": {
        "description": "Data flowing through a pipeline with transformation nodes",
        "params": {
            "stages": "array of {label, type, color} objects",
            "animated": "bool",
            "title": "string",
            "description": "string"
        }
    },
    "convolution": {
        "description": "2D convolution filter sliding over an input matrix",
        "params": {
            "inputSize": "int e.g. 6",
            "kernelSize": "int e.g. 3",
            "stride": "int e.g. 1",
            "featureMaps": "int e.g. 2",
            "animated": "bool",
            "title": "string",
            "description": "string"
        }
    },
    "embedding_space": {
        "description": "3D vector embedding space with concept clusters",
        "params": {
            "points": "array of {label, x, y, z, cluster} — up to 20 points",
            "clusters": "array of {name, color} — cluster legend",
            "title": "string",
            "description": "string"
        }
    },
    "decision_tree": {
        "description": "Interactive 3D decision tree with branches and leaf nodes",
        "params": {
            "tree": "recursive {question, left, right} or {label, value} for leaves",
            "title": "string",
            "description": "string"
        }
    },
    "custom_geometry": {
        "description": "Procedural 3D scene from a list of geometric primitives",
        "params": {
            "objects": "array of {type:'box|sphere|cylinder|cone|torus', position:[x,y,z], size:[w,h,d], color:'#hex', label, opacity}",
            "connections": "array of {from:int, to:int, color:'#hex'} — index-based connections",
            "animated": "bool",
            "title": "string",
            "description": "string"
        }
    }
}


class VisualRequest(BaseModel):
    concept: str
    context: str = ""
    lesson_id: Optional[int] = None
    force_type: Optional[str] = None  # pin a specific vizType


@router.post("/generate")
async def generate_visual(
    req: VisualRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate a VIZCONFIG JSON for a concept. Frontend Three.js scenes render it."""

    lesson_context = ""
    if req.lesson_id:
        lesson_result = await db.execute(select(Lesson).where(Lesson.id == req.lesson_id))
        lesson = lesson_result.scalar_one_or_none()
        if lesson:
            course_result = await db.execute(select(Course).where(Course.id == lesson.course_id))
            course = course_result.scalar_one_or_none()
            lesson_context = f"Course: {course.title if course else ''}\nLesson: {lesson.title}"

    schema_str = json.dumps(VIZ_SCHEMA, indent=2)

    force_hint = ""
    if req.force_type and req.force_type in VIZ_SCHEMA:
        force_hint = f'\nYou MUST use vizType: "{req.force_type}"'

    prompt = f"""You are the SAGE Visualization Agent. Your job is to generate a VIZCONFIG JSON rendered as a real-time interactive 3D Three.js scene.

The student asked for a visual explanation of: {req.concept}
{lesson_context}
Additional context: {req.context[:500] if req.context else "none"}
{force_hint}

Available visualization types and their params:
{schema_str}

ROUTING RULES — pick the MOST specific type available:
- Wind turbines, pendulums, atoms, orbits, springs, gears → mechanical (with correct subtype)
- Neural networks, MLPs, backprop, perceptrons → neural_network
- Loss landscape, gradient descent, optimization → gradient_descent
- Attention, transformers, Q/K/V, BERT, GPT attention heads → attention
- Data pipelines, preprocessing flows, ETL → data_flow
- CNNs, filters, feature maps, convolution → convolution
- Word2Vec, embeddings, latent space, vectors → embedding_space
- Anything physics/mechanical/science that has a mechanical subtype → mechanical
- LAST RESORT ONLY: custom_geometry for abstract concepts with NO mechanical subtype

For custom_geometry — use RICH params:
- type options: box | sphere | cylinder | cone | torus | octahedron | lathe
- For lathe: include "radiusPoints": [[radius, height], ...] for tapered/cylindrical shapes
- Include metalness (0-1) and roughness (0-1) per object for PBR realism
- Include "animate": {{"type":"rotate","axis":"y","speed":0.015}} for moving parts
- Use "connections" with tube-based bezier paths between objects
- Colors should be varied and meaningful, not all the same

Fill ALL params with real, accurate, concept-specific values. Not placeholders.
Make it EDUCATIONAL — the visualization should make the concept visually intuitive.

Return ONLY a valid JSON object:

{{
  "vizType": "...",
  "title": "...",
  "description": "...",
  "params": {{ ... }}
}}"""

    raw = await asi1_complete(prompt, max_tokens=1024)

    # Extract JSON — try progressively more aggressive extraction strategies
    vizconfig = None
    match = re.search(r'\{[\s\S]*\}', raw)
    if match:
        raw_json = match.group(0)
        # Strategy 1: parse as-is
        try:
            vizconfig = json.loads(raw_json)
        except json.JSONDecodeError:
            # Strategy 2: strip trailing commas before } or ]
            cleaned = re.sub(r',\s*([}\]])', r'\1', raw_json)
            # Strategy 3: strip // comments
            cleaned = re.sub(r'//[^\n]*', '', cleaned)
            # Strategy 4: strip /* */ comments
            cleaned = re.sub(r'/\*[\s\S]*?\*/', '', cleaned)
            try:
                vizconfig = json.loads(cleaned)
            except json.JSONDecodeError:
                # Strategy 5: try to find the outermost complete JSON object
                depth = 0
                start = raw_json.find('{')
                end = start
                for i, c in enumerate(raw_json[start:], start):
                    if c == '{': depth += 1
                    elif c == '}':
                        depth -= 1
                        if depth == 0:
                            end = i; break
                try:
                    vizconfig = json.loads(raw_json[start:end + 1])
                except Exception:
                    pass

    if not vizconfig:
        raise HTTPException(status_code=422, detail="Could not generate valid VIZCONFIG")

    if "vizType" not in vizconfig or vizconfig["vizType"] not in VIZ_SCHEMA:
        # Fall back to custom_geometry rather than erroring
        vizconfig["vizType"] = "custom_geometry"
        if "params" not in vizconfig or not isinstance(vizconfig.get("params"), dict):
            vizconfig["params"] = {}
        if "objects" not in vizconfig["params"]:
            vizconfig["params"]["objects"] = [
                {"type": "sphere", "position": [-2, 0, 0], "size": [0.8, 0.8, 0.8], "color": "#60a5fa", "label": "Input"},
                {"type": "box", "position": [0, 0, 0], "size": [1.2, 0.8, 0.4], "color": "#8b5cf6", "label": req.concept[:20]},
                {"type": "cone", "position": [2, 0, 0], "size": [0.8, 1, 0.8], "color": "#34d399", "label": "Output"},
            ]
            vizconfig["params"]["connections"] = [{"from": 0, "to": 1}, {"from": 1, "to": 2}]

    return vizconfig


@router.get("/types")
async def get_viz_types():
    """Return supported visualization types."""
    return {k: v["description"] for k, v in VIZ_SCHEMA.items()}
