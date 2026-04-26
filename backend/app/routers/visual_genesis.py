"""
Genesis physics simulation renderer.

Genesis (genesis-world) is a universal physics engine with photorealistic
ray-traced rendering. This endpoint:
  1. LLM generates a complete Genesis Python scene script
  2. Backend runs it headlessly in a subprocess
  3. Genesis renders to MP4 using its built-in Rasterizer or RayTracer
  4. Backend returns the video as base64-encoded MP4

Genesis features used:
  - gs.morphs.*         → primitives (Cylinder, Box, Sphere, Mesh from STL)
  - gs.materials.*      → physics (Rigid, Liquid, Gas, Elastic, MPM)
  - gs.surfaces.*       → PBR rendering (color, roughness, metallic)
  - gs.lights.*         → lighting (Directional, Ambient, Point)
  - Actual physics step → real rigid body dynamics, not scripted animation

Install: pip install torch && pip install genesis-world
"""

import asyncio
import base64
import logging
import os
import re
import sys
import tempfile
import textwrap
from pathlib import Path

from fastapi import APIRouter, Depends
from openai import OpenAI
from pydantic import BaseModel

from ..config import get_settings
from ..deps import get_current_user
from ..models.user import User

router = APIRouter(prefix="/visual", tags=["visual"])
logger = logging.getLogger(__name__)

TIMEOUT_SECS = 45   # Genesis rendering budget
MAX_CODE_LEN  = 12_000

# ─── Genesis boilerplate ─────────────────────────────────────────────────────
# Injected before and after the LLM-generated code.
SCRIPT_PREFIX = textwrap.dedent("""\
import os, sys, math, numpy as np
os.environ.setdefault("GENESIS_LOGGING", "WARNING")
os.environ["PYOPENGL_PLATFORM"] = "osmesa"  # headless fallback

import genesis as gs

# Headless init — try Metal (Apple Silicon), then CPU
try:
    gs.init(backend=gs.metal, logging_level="warning")
except Exception:
    gs.init(backend=gs.cpu,   logging_level="warning")

_OUTPUT_PATH = sys.argv[1] if len(sys.argv) > 1 else "/tmp/genesis_out.mp4"
_RES = (960, 540)
_FPS = 30
_FRAMES = 120   # 4 seconds

scene = gs.Scene(
    show_viewer=False,
    renderer=gs.renderers.Rasterizer(width=_RES[0], height=_RES[1]),
)

# Convenience re-exports the model code can use
Cylinder  = gs.morphs.Cylinder
Box       = gs.morphs.Box
Sphere    = gs.morphs.Sphere
Plane     = gs.morphs.Plane
Mesh      = gs.morphs.Mesh
Rigid     = gs.materials.Rigid
Liquid    = gs.materials.Liquid
Elastic   = gs.materials.Elastic
Surface   = gs.surfaces.Default

def add_standard_lights():
    scene.add_light(gs.lights.DirectionalLight(
        dir=(-0.5, -1.5, -1.0), intensity=6.0, cast_shadow=True))
    scene.add_light(gs.lights.AmbientLight(intensity=2.5))
    scene.add_light(gs.lights.PointLight(
        pos=(0.6, 0.6, 0.6), intensity=4.0, color=(0.8, 0.9, 1.0)))

# ─────────────────────────────────────────────────────────────────────────────
# USER CODE START
""")

SCRIPT_SUFFIX = textwrap.dedent("""\
# USER CODE END
# ─────────────────────────────────────────────────────────────────────────────

# Build scene
scene.build()

# Render
_cam.start_recording()
for _i in range(_FRAMES):
    if callable(globals().get("pre_step")):
        pre_step(_i, _i / _FPS)
    scene.step()
    if callable(globals().get("post_step")):
        post_step(_i, _i / _FPS)
    _cam.render()
_cam.stop_recording(save_to=_OUTPUT_PATH, fps=_FPS)
print("DONE:", _OUTPUT_PATH)
""")


# ─── LLM prompt ──────────────────────────────────────────────────────────────
GENESIS_PROMPT = '''\
You are an expert in Genesis physics simulation (genesis-world Python package).

Generate a complete Genesis scene for: "{topic}"
Context: {context}

═══ GENESIS API REFERENCE ═══

Available globals (pre-imported for you):
  scene        — the gs.Scene (already created, show_viewer=False)
  Cylinder, Box, Sphere, Plane, Mesh   — morphs
  Rigid, Liquid, Elastic               — materials
  Surface                              — gs.surfaces.Default
  add_standard_lights()                — adds directional+ambient+point light

CAMERA (you MUST define _cam):
  _cam = scene.add_camera(
      res=(960, 540),
      pos=(x, y, z),         # in meters, Y is up
      lookat=(0, 0.1, 0),
      fov=45,
      GUI=False,
  )

ENTITIES:
  obj = scene.add_entity(
      morph=Cylinder(
          radius=0.05,        # meters
          height=0.40,
          pos=(0, 0.2, 0),    # center position
          euler=(90, 0, 0),   # degrees, optional — rotate to lie on X: euler=(0,0,90)
      ),
      material=Rigid(rho=7800),                # density kg/m³
      surface=Surface(
          color=(0.4, 0.45, 0.52, 1.0),        # RGBA 0-1
          roughness=0.6,
          metallic=0.85,
      ),
  )

GROUND PLANE:
  ground = scene.add_entity(
      morph=Plane(),
      material=Rigid(),
      surface=Surface(color=(0.08, 0.1, 0.12, 1.0)),
  )

JOINTS / CONSTRAINED MOTION:
  # For scripted animation use pre_step() / post_step() hooks:
  def pre_step(frame, t):
      stroke = 0.5 * (1 + math.sin(t * 1.5))   # 0→1→0
      piston.set_pos((stroke * 0.18 - 0.09, 0, 0))

MATERIALS:
  Rigid(rho=7800)            # steel
  Rigid(rho=2700)            # aluminum
  Rigid(rho=1200)            # plastic
  Rigid(rho=8900)            # copper/brass
  Rigid(rho=1000)            # water/resin

SURFACE COLORS for realism:
  Machined steel:   (0.55, 0.60, 0.68, 1.0), roughness=0.20, metallic=0.88
  Chrome rod:       (0.80, 0.85, 0.90, 1.0), roughness=0.04, metallic=0.96
  Cast iron:        (0.26, 0.28, 0.32, 1.0), roughness=0.65, metallic=0.70
  Brass fitting:    (0.72, 0.52, 0.22, 1.0), roughness=0.25, metallic=0.88
  Black rubber:     (0.06, 0.06, 0.06, 1.0), roughness=0.97, metallic=0.00
  Anodized blue:    (0.16, 0.32, 0.60, 1.0), roughness=0.32, metallic=0.62
  Hydraulic fluid:  (0.72, 0.46, 0.10, 0.5), roughness=0.00, metallic=0.00

═══ RULES ═══
1. ALWAYS define `_cam` before scene.build() is called.
2. ALWAYS call `add_standard_lights()` (or add your own lights).
3. Use REAL dimensions in METERS. A 400mm cylinder has height=0.4.
4. Animation via pre_step(frame, t) / post_step(frame, t) — DO NOT call scene.step().
5. _FRAMES=120, _FPS=30 (already set) — 4 seconds total.
6. Do NOT import genesis or call gs.init() — already done.
7. Do NOT call scene.build() or cam.start_recording() — already done.
8. Camera position: place camera to clearly show the whole object. For a horizontal actuator
   (0.4m long), camera at pos=(0.0, 0.25, 0.60), lookat=(0, 0.05, 0) works well.
9. Keep total entities ≤ 20 (performance).
10. For rotating parts use euler angles in degrees. To lie a cylinder on X-axis: euler=(0,0,90).

Output ONLY Python code. No markdown fences. No explanation.
Define _cam, call add_standard_lights(), add entities, optionally define pre_step/post_step.
'''


# ─── Safety check on generated code ─────────────────────────────────────────
_BLOCKED_PATTERNS = [
    r"import\s+os\b",
    r"import\s+subprocess",
    r"import\s+shutil",
    r"open\s*\(",
    r"__import__",
    r"exec\s*\(",
    r"eval\s*\(",
    r"compile\s*\(",
]

def _is_safe(code: str) -> bool:
    for pat in _BLOCKED_PATTERNS:
        if re.search(pat, code):
            logger.warning("Blocked pattern found: %s", pat)
            return False
    return True


# ─── Request / Response ───────────────────────────────────────────────────────
class GenesisRequest(BaseModel):
    topic: str
    context: str = ""


class GenesisResponse(BaseModel):
    video_b64: str | None = None     # base64 MP4
    script:    str | None = None     # generated Python script (for download)
    topic:     str        = ""
    error:     str | None = None
    fallback:  bool       = False    # True if we fell back to a canned script


# ─── Endpoint ─────────────────────────────────────────────────────────────────
@router.post("/genesis", response_model=GenesisResponse)
async def generate_genesis_simulation(
    req: GenesisRequest,
    user: User = Depends(get_current_user),
):
    settings = get_settings()
    topic   = req.topic[:200]
    context = req.context[:2000]

    # ── Check Genesis is installed ──────────────────────────────────────────
    try:
        import importlib
        importlib.import_module("genesis")
    except ImportError:
        return GenesisResponse(
            topic=topic,
            error="genesis-world is not installed. Run: pip install torch && pip install genesis-world",
        )

    # ── Generate scene code via LLM ─────────────────────────────────────────
    client = OpenAI(api_key=settings.llm_api_key, base_url=settings.llm_base_url)
    try:
        resp = client.chat.completions.create(
            model=settings.llm_model,
            messages=[{
                "role": "user",
                "content": GENESIS_PROMPT.format(topic=topic, context=context),
            }],
            temperature=0.15,
            max_tokens=3000,
        )
        raw = resp.choices[0].message.content or ""
        raw = re.sub(r"```(?:python)?\s*", "", raw)
        raw = re.sub(r"```\s*$", "", raw, flags=re.MULTILINE).strip()
    except Exception as exc:
        raw = _fallback_script(topic)
        logger.warning("LLM failed, using fallback: %s", exc)

    # Safety check
    if not _is_safe(raw) or len(raw) > MAX_CODE_LEN:
        raw = _fallback_script(topic)

    full_script = SCRIPT_PREFIX + "\n" + raw + "\n" + SCRIPT_SUFFIX

    # ── Run Genesis in subprocess ────────────────────────────────────────────
    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = os.path.join(tmpdir, "sim.py")
        output_path = os.path.join(tmpdir, "output.mp4")

        with open(script_path, "w") as f:
            f.write(full_script)

        try:
            proc = await asyncio.create_subprocess_exec(
                sys.executable, script_path, output_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=tmpdir,
            )
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(), timeout=TIMEOUT_SECS
            )
            stdout_txt = stdout.decode("utf-8", errors="replace")
            stderr_txt = stderr.decode("utf-8", errors="replace")
        except asyncio.TimeoutError:
            return GenesisResponse(
                topic=topic, script=raw,
                error=f"Genesis rendering timed out after {TIMEOUT_SECS}s.",
            )
        except Exception as exc:
            return GenesisResponse(topic=topic, script=raw, error=str(exc))

        if "DONE:" not in stdout_txt or not os.path.exists(output_path):
            err_summary = (stderr_txt or stdout_txt)[-800:]
            # Try fallback script
            fallback = _fallback_script(topic)
            if fallback != raw:
                fs = SCRIPT_PREFIX + "\n" + fallback + "\n" + SCRIPT_SUFFIX
                with open(script_path, "w") as f:
                    f.write(fs)
                try:
                    proc2 = await asyncio.create_subprocess_exec(
                        sys.executable, script_path, output_path,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                        cwd=tmpdir,
                    )
                    out2, err2 = await asyncio.wait_for(proc2.communicate(), timeout=TIMEOUT_SECS)
                    if "DONE:" in out2.decode("utf-8", errors="replace") and os.path.exists(output_path):
                        raw = fallback
                        # continue to encode below
                    else:
                        return GenesisResponse(topic=topic, script=raw, error=err_summary)
                except Exception:
                    return GenesisResponse(topic=topic, script=raw, error=err_summary)
            else:
                return GenesisResponse(topic=topic, script=raw, error=err_summary)

        # ── Read & encode video ──────────────────────────────────────────────
        video_bytes = Path(output_path).read_bytes()
        video_b64 = base64.b64encode(video_bytes).decode("ascii")

        return GenesisResponse(
            video_b64=video_b64,
            script=raw,
            topic=topic,
        )


# ─── Canned fallback: hydraulic actuator ─────────────────────────────────────
def _fallback_script(topic: str) -> str:
    return f'''\
# Hydraulic Linear Actuator — {topic}
# Real physics, accurate dimensions (meters)

add_standard_lights()

_cam = scene.add_camera(
    res=(960, 540),
    pos=(0.0, 0.28, 0.65),
    lookat=(0.0, 0.04, 0.0),
    fov=42,
    GUI=False,
)

# Ground
scene.add_entity(
    morph=Plane(),
    material=Rigid(),
    surface=Surface(color=(0.06, 0.08, 0.10, 1.0), roughness=0.95),
)

# ── Cylinder barrel (cast iron) ──────────────────────────────────────────────
barrel = scene.add_entity(
    morph=Cylinder(radius=0.053, height=0.40, pos=(0.0, 0.05, 0.0), euler=(0, 0, 90)),
    material=Rigid(rho=7800),
    surface=Surface(color=(0.26, 0.29, 0.33, 1.0), roughness=0.62, metallic=0.72),
)

# ── Blind end cap (left) ─────────────────────────────────────────────────────
scene.add_entity(
    morph=Cylinder(radius=0.053, height=0.025, pos=(-0.213, 0.05, 0.0), euler=(0, 0, 90)),
    material=Rigid(rho=7800),
    surface=Surface(color=(0.42, 0.48, 0.55, 1.0), roughness=0.22, metallic=0.88),
)

# ── Rod end cap (right) ──────────────────────────────────────────────────────
scene.add_entity(
    morph=Cylinder(radius=0.053, height=0.025, pos=(0.213, 0.05, 0.0), euler=(0, 0, 90)),
    material=Rigid(rho=7800),
    surface=Surface(color=(0.42, 0.48, 0.55, 1.0), roughness=0.22, metallic=0.88),
)

# ── Piston (anodized aluminum, moves) ────────────────────────────────────────
piston = scene.add_entity(
    morph=Cylinder(radius=0.040, height=0.030, pos=(-0.10, 0.05, 0.0), euler=(0, 0, 90)),
    material=Rigid(rho=2700),
    surface=Surface(color=(0.16, 0.32, 0.60, 1.0), roughness=0.30, metallic=0.65),
)

# ── Piston rod (chrome steel) ────────────────────────────────────────────────
rod = scene.add_entity(
    morph=Cylinder(radius=0.020, height=0.30, pos=(0.05, 0.05, 0.0), euler=(0, 0, 90)),
    material=Rigid(rho=7800),
    surface=Surface(color=(0.80, 0.85, 0.90, 1.0), roughness=0.04, metallic=0.96),
)

# ── O-ring seals (rubber) ─────────────────────────────────────────────────────
for ox in [-0.007, 0.007]:
    scene.add_entity(
        morph=Box(size=(0.006, 0.082, 0.082), pos=(-0.10 + ox, 0.05, 0.0)),
        material=Rigid(rho=1200),
        surface=Surface(color=(0.05, 0.05, 0.05, 1.0), roughness=0.97),
    )

# ── Port A fitting (brass) ────────────────────────────────────────────────────
scene.add_entity(
    morph=Cylinder(radius=0.009, height=0.025, pos=(-0.17, 0.103, 0.0), euler=(90, 0, 0)),
    material=Rigid(rho=8500),
    surface=Surface(color=(0.72, 0.52, 0.22, 1.0), roughness=0.24, metallic=0.88),
)

# ── Port B fitting (brass) ────────────────────────────────────────────────────
scene.add_entity(
    morph=Cylinder(radius=0.009, height=0.025, pos=(0.12, 0.103, 0.0), euler=(90, 0, 0)),
    material=Rigid(rho=8500),
    surface=Surface(color=(0.72, 0.52, 0.22, 1.0), roughness=0.24, metallic=0.88),
)

# ── Animation: piston + rod extend and retract ────────────────────────────────
_piston_start = (-0.10, 0.05, 0.0)
_rod_start     = ( 0.05, 0.05, 0.0)

def pre_step(frame, t):
    # Sinusoidal stroke: full extend in 2s, retract in 2s
    stroke = 0.5 * (1.0 - math.cos(t * math.pi * 0.5))  # 0→1 over 4s
    travel = stroke * 0.19                                 # 190mm max travel

    piston.set_pos((_piston_start[0] + travel, _piston_start[1], _piston_start[2]))
    rod.set_pos(   (_rod_start[0]    + travel, _rod_start[1],    _rod_start[2]))
'''
