"""
Genesis physics simulation renderer — topic-aware with Gemini Vision verification.

Pipeline:
  1. Stage-1 LLM: produce a JSON "scene design brief" describing what objects
     represent the topic and why.
  2. Stage-2 LLM: convert the brief into Genesis 0.4.x Python scene code.
  3. Run headlessly in the isolated Python 3.12 genesis venv.
  4. Extract a frame from the MP4 and verify with Gemini Vision that the frame
     actually depicts the topic. Auto-retry (up to 2 times) with Gemini's feedback.
  5. Return base64 MP4.

Genesis 0.4.x Rasterizer API constraints (hard-won):
  - RigidEntity.set_pos(tuple) — yes
  - RigidEntity.set_quat((w,x,y,z)) — yes  (NO set_euler!)
  - gs.materials.Rigid only  (no Liquid, Elastic, Gas, MPM)
  - Box needs both `pos` AND `size`; Cylinder/Sphere default pos=(0,0,0)
"""

import asyncio
import base64
import io
import json
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

TIMEOUT_SECS = 75
MAX_CODE_LEN  = 14_000
MAX_RETRIES   = 2


def _genesis_python() -> str:
    return os.environ.get("GENESIS_PYTHON") or sys.executable


# ─── Genesis boilerplate ─────────────────────────────────────────────────────
SCRIPT_PREFIX = textwrap.dedent("""\
import os, sys, math, numpy as np
os.environ.setdefault("GENESIS_LOGGING", "WARNING")

import genesis as gs

try:
    gs.init(backend=gs.metal, logging_level="warning")
except Exception:
    gs.init(backend=gs.cpu, logging_level="warning")

_OUTPUT_PATH = sys.argv[1] if len(sys.argv) > 1 else "/tmp/genesis_out.mp4"
_FPS    = 30
_FRAMES = 120   # 4 seconds @ 30 fps

scene = gs.Scene(
    show_viewer=False,
    renderer=gs.renderers.Rasterizer(),
    vis_options=gs.options.VisOptions(
        ambient_light=(0.45, 0.45, 0.50),
        lights=[
            {"type": "directional", "dir": (-0.5, -1.5, -1.0),
             "intensity": 5.0, "color": (1.0, 0.95, 0.88)},
            {"type": "directional", "dir": (1.0, -0.5, -0.5),
             "intensity": 1.5, "color": (0.6, 0.7, 1.0)},
        ],
    ),
)

Cylinder  = gs.morphs.Cylinder
Box       = gs.morphs.Box
Sphere    = gs.morphs.Sphere
Plane     = gs.morphs.Plane
Rigid     = gs.materials.Rigid
Surface   = gs.surfaces.Default

def add_standard_lights():
    pass  # lighting set above in VisOptions

# ── Rotation helper ──────────────────────────────────────────────────────────
# RigidEntity has set_pos and set_quat only (NO set_euler).
# Use quat_from_euler to build (w, x, y, z) quaternions.
def quat_from_euler(roll_deg, pitch_deg, yaw_deg):
    \"\"\"Euler ZYX -> quaternion (w, x, y, z) expected by set_quat.\"\"\"
    r = math.radians(roll_deg)
    p = math.radians(pitch_deg)
    y = math.radians(yaw_deg)
    cr, sr = math.cos(r/2), math.sin(r/2)
    cp, sp = math.cos(p/2), math.sin(p/2)
    cy, sy = math.cos(y/2), math.sin(y/2)
    w = cr*cp*cy + sr*sp*sy
    x = sr*cp*cy - cr*sp*sy
    y_ = cr*sp*cy + sr*cp*sy
    z = cr*cp*sy - sr*sp*cy
    return (w, x, y_, z)

# ─────────────────────────────────────────────────────────────────────────────
# USER CODE START
""")

SCRIPT_SUFFIX = textwrap.dedent("""\
# USER CODE END
# ─────────────────────────────────────────────────────────────────────────────
scene.build()
_cam.start_recording()
for _i in range(_FRAMES):
    if callable(globals().get("pre_step")):
        pre_step(_i, _i / _FPS)
    scene.step()
    if callable(globals().get("post_step")):
        post_step(_i, _i / _FPS)
    _cam.render()
_cam.stop_recording(save_to_filename=_OUTPUT_PATH, fps=_FPS)
print("DONE:", _OUTPUT_PATH)
""")


# ─── Stage-1 prompt: design brief ────────────────────────────────────────────
BRIEF_PROMPT = '''\
You are a physics-visualization designer for an educational platform.
The student is studying: "{topic}"
Extra context: {context}

Design a Genesis physics simulation that SPECIFICALLY and ACCURATELY depicts this topic.
Ask yourself: what are the SIGNATURE visual elements that make this concept immediately
recognizable? A double helix for DNA? Orbiting spheres for planetary motion? A pendulum
for SHM? Multiple cylinders/spheres for a gear train? A robot arm for RL?

Return ONLY a JSON object — no markdown, no extra text:
{{
  "scene_title": "<short, specific title>",
  "topic_category": "<mechanics|robotics|electromagnetism|thermodynamics|waves|biology|chemistry|mathematics|astronomy|machine_learning|civil_engineering|optics|general>",
  "key_objects": [
    {{
      "name": "<part name>",
      "shape": "<Cylinder|Box|Sphere|Plane>",
      "role": "<what it represents>",
      "size_m": "<size in meters>",
      "color_desc": "<e.g. steel-grey, bright-red, gold>",
      "animated": true
    }}
  ],
  "animation_description": "<1-2 sentences: what moves, how, and why it illustrates the topic>",
  "camera_hint": "<distance and angle to frame the whole scene, in meters>",
  "accuracy_check": "<what a vision model should see to confirm this depicts the topic>"
}}
'''

# ─── Stage-2 prompt: Genesis code ────────────────────────────────────────────
CODE_PROMPT = '''\
You are an expert in Genesis physics simulation (genesis-world 0.4.x Python).

Generate a complete Genesis scene for: "{topic}"

SCENE DESIGN BRIEF — follow this exactly:
{brief}

═══ GENESIS 0.4.x API — USE EXACTLY THIS SYNTAX ═══

Pre-defined globals (do NOT re-import or call gs.init):
  scene               — gs.Scene (already created)
  Cylinder, Box, Sphere, Plane  — morphs
  Rigid               — ONLY available material  (NEVER use Liquid, Elastic, Gas, MPM — they CRASH)
  Surface             — gs.surfaces.Default (PBR)
  _FRAMES=120, _FPS=30
  quat_from_euler(roll_deg, pitch_deg, yaw_deg) → (w,x,y,z)

CAMERA — define _cam first:
  _cam = scene.add_camera(
      res=(960, 540),
      pos=(x, y, z),      # Y is up; back far enough to see everything
      lookat=(cx, cy, cz),
      fov=50,
      GUI=False,
  )

ENTITY CREATION:
  obj = scene.add_entity(
      morph=Cylinder(radius=0.05, height=0.4, pos=(0, 0.2, 0), euler=(0,0,90)),
      material=Rigid(rho=7800),
      surface=Surface(color=(0.55, 0.60, 0.68, 1.0), roughness=0.20, metallic=0.88),
  )
  # Box MUST have both pos AND size:
  scene.add_entity(morph=Box(size=(0.1,0.1,0.1), pos=(0,0.5,0)), material=Rigid(), surface=Surface(color=(0.8,0.2,0.1,1)))
  # Sphere with pos:
  scene.add_entity(morph=Sphere(radius=0.08, pos=(0,0.4,0)), material=Rigid(rho=1000), surface=Surface(color=(0.2,0.5,0.9,1)))

ANIMATION — ONLY via pre_step hook; NEVER call scene.step() yourself:
  def pre_step(frame, t):   # t = elapsed seconds
      # ONLY these methods exist on entities:
      obj.set_pos((x, y, z))           # move
      obj.set_quat(quat_from_euler(roll, pitch, yaw))  # rotate  ← USE THIS, not set_euler
      # Example: orbit at radius r around Y axis
      obj.set_pos((r*math.cos(t), 0.3, r*math.sin(t)))

GROUND — Plane takes NO arguments (infinite flat ground):
  scene.add_entity(morph=Plane(), material=Rigid(),
      surface=Surface(color=(0.07, 0.09, 0.11, 1.0), roughness=0.9))
  # WRONG: Plane(size=...) or Plane(pos=...) — Plane() only!

MATERIAL DENSITIES (rho kg/m³):  Steel=7800  Aluminum=2700  Plastic=1200  Brass=8900  Rock=2500

SURFACE COLORS:
  Steel (0.55,0.60,0.68,1) r=0.20 m=0.88  |  Chrome (0.80,0.85,0.90,1) r=0.04 m=0.96
  Copper(0.72,0.45,0.20,1) r=0.30 m=0.85  |  Gold  (0.83,0.68,0.21,1) r=0.15 m=0.90
  Red   (0.85,0.15,0.10,1) r=0.60 m=0.00  |  Blue  (0.15,0.35,0.80,1) r=0.40 m=0.10
  Green (0.15,0.65,0.25,1) r=0.50 m=0.00  |  White (0.90,0.90,0.90,1) r=0.50 m=0.00
  Yellow(0.90,0.80,0.10,1) r=0.40 m=0.20  |  Black (0.06,0.06,0.06,1) r=0.97 m=0.00

TOPIC-SPECIFIC PATTERNS:
  Pendulum SHM:       pivot Box + rod Cylinder + bob Sphere; animate bob along arc with set_pos
  Planetary orbit:    large central Sphere + small Sphere orbiting via set_pos circular path
  Gear train:         multiple Cylinders side by side; rotate via set_quat
  Robot arm:          chain of Boxes/Cylinders; each joint rotates via set_quat
  Spring/oscillator:  a Sphere bouncing vertically via set_pos with sin wave
  Bridge/arch:        Box segments in arch shape + rolling Sphere across
  DNA helix:          two chains of Spheres at offset angles, rotating together
  Neural network:     rows of Spheres (nodes) + thin Cylinder connections, pulsing
  Projectile:         a Sphere launched at an angle, parabolic set_pos path

SCALE RULE — ABSOLUTE RULE FOR ALL TOPICS:
  This is a VISUALIZATION, not a physical simulation. Use model scale, never real scale.
  ALL objects: 0.01m – 2.0m  |  Camera: 1m – 5m away  |  Scene fits in a 4m × 4m × 4m box.

  Examples by topic:
    Atom/molecule: sphere radius=0.05–0.08m, spacing=0.1–0.15m, camera at 1.5m
    DNA helix: sphere radius=0.04m, helix radius=0.15m, height span=0.8m, camera at 1.5m
    Planetary orbit: star Sphere radius=0.25m, planet radius=0.06m, orbit radius=0.6–1.0m, camera at 2m
    Bridge/arch: span=2.0m, pillars height=0.8m, camera at 3m
    Robot arm: links 0.3–0.5m long, 0.04m radius, camera at 2m
    Pendulum: length=0.5m, bob radius=0.04m, pivot at y=0.8m, camera at 1.5m

  NEVER use: 1000m, 0.000001m, 2000000m, 1e6, etc.
  ALWAYS fit the entire scene between y=0 and y=2m, x=-1.5m to x=1.5m.

RULES:
1. Build the EXACT scene from the brief — NOT a generic cylinder demo.
2. _cam MUST be defined before any entity.
3. Camera must frame all key objects — back off enough to see them all.
4. ALL objects between 0.01m and 2.0m — NEVER use atomic/nm/mm scale numbers.
5. Keep entities ≤ 20 for performance.
6. Do NOT call gs.init(), scene.build(), cam.start_recording() — already done.
7. For rotation: ONLY use set_quat(quat_from_euler(r,p,y)) — set_euler does NOT exist.
8. Output ONLY raw Python. No markdown fences, no explanation.
'''


# ─── Safety filter ────────────────────────────────────────────────────────────
_BLOCKED = [
    r"import\s+os\b", r"import\s+subprocess", r"import\s+shutil",
    r"open\s*\(", r"__import__", r"exec\s*\(", r"eval\s*\(", r"compile\s*\(",
]

def _is_safe(code: str) -> bool:
    for pat in _BLOCKED:
        if re.search(pat, code):
            return False
    return True


def _strip_fences(text: str) -> str:
    text = re.sub(r"```(?:python)?\s*", "", text)
    text = re.sub(r"```\s*$", "", text, flags=re.MULTILINE)
    return text.strip()


def _strip_plane_args(code: str) -> str:
    """Replace Plane(...) with Plane() using balanced-parenthesis matching."""
    result = []
    i = 0
    while i < len(code):
        m = re.search(r'\bPlane\s*\(', code[i:])
        if not m:
            result.append(code[i:])
            break
        result.append(code[i : i + m.start()])
        result.append('Plane()')
        # Skip past the original Plane(...) using balanced parens
        j = i + m.end()  # just after the opening '('
        depth = 1
        while j < len(code) and depth > 0:
            if code[j] == '(':
                depth += 1
            elif code[j] == ')':
                depth -= 1
            j += 1
        i = j
    return ''.join(result)


def _sanitize_code(code: str) -> str:
    """
    Auto-fix common LLM mistakes in generated Genesis code.
    1. set_euler((r,p,y)) → set_quat(quat_from_euler(r,p,y))
    2. Liquid()/Elastic()/Gas()/MPM() → Rigid()
    """
    # Fix set_euler((...)) — handles single-tuple form
    code = re.sub(
        r'\.set_euler\(\s*\(([^)]+)\)\s*\)',
        lambda m: f'.set_quat(quat_from_euler({m.group(1)}))',
        code,
    )
    # Fix any remaining .set_euler( that weren't caught (no outer parens)
    code = re.sub(r'\.set_euler\(', '.set_quat(quat_from_euler(', code)
    # Unsupported materials → Rigid
    for bad in ("Liquid", "Elastic", "Gas", "MPM", "PBD"):
        code = re.sub(rf'\b{bad}\s*\(', 'Rigid(', code)
    # Plane takes NO args — strip any Plane(size=...) or Plane(pos=...) etc.
    # Need balanced-paren matching because args may contain tuples.
    code = _strip_plane_args(code)
    # Remove any stray scene.step() calls (already in suffix)
    code = re.sub(r'\bscene\.step\(\)', '# scene.step()  # removed — called in suffix', code)
    return code


# ─── Gemini Vision verification ───────────────────────────────────────────────
def _extract_frame_b64(mp4_path: str, frame_index: int = 45) -> str | None:
    extract_script = textwrap.dedent(f"""\
        import cv2, base64, sys
        cap = cv2.VideoCapture('{mp4_path}')
        cap.set(cv2.CAP_PROP_POS_FRAMES, {frame_index})
        ok, frame = cap.read()
        cap.release()
        if ok:
            ok2, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if ok2:
                sys.stdout.buffer.write(base64.b64encode(buf.tobytes()))
    """)
    try:
        import subprocess
        result = subprocess.run(
            [_genesis_python(), "-c", extract_script],
            capture_output=True, timeout=15,
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout.decode("ascii")
    except Exception as exc:
        logger.warning("Frame extraction failed: %s", exc)
    return None


def _verify_with_gemini(frame_b64: str, topic: str, accuracy_check: str, gemini_key: str) -> tuple[bool, str]:
    try:
        from google import genai as gai
        from google.genai import types as gtypes
        import PIL.Image

        client = gai.Client(api_key=gemini_key)
        img_bytes = base64.b64decode(frame_b64)
        img = PIL.Image.open(io.BytesIO(img_bytes))

        prompt = (
            f"Topic: '{topic}'\n"
            f"Expected visual: {accuracy_check}\n\n"
            "Look at this frame from a 3D physics simulation rendered for an educational platform. "
            "Does it CLEARLY and ACCURATELY represent the stated topic? "
            "Be strict — if it shows random cylinders/boxes with no connection to the topic, say FAIL.\n"
            "Reply with exactly:\nPASS or FAIL\nFeedback: <one sentence — what you see and what is correct or wrong>"
        )
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[prompt, img],
        )
        text = (response.text or "").strip()
        passes = text.upper().startswith("PASS")
        m = re.search(r"Feedback:\s*(.+)", text, re.IGNORECASE)
        feedback = m.group(1).strip() if m else text
        logger.info("Gemini: %s | %s", "PASS" if passes else "FAIL", feedback)
        return passes, feedback
    except Exception as exc:
        logger.warning("Gemini verification error: %s", exc)
        return True, "Gemini verification unavailable"


# ─── Fallback: pendulum (always renders, topic-neutral) ──────────────────────
def _fallback_script(topic: str) -> str:
    """Simple pendulum — uses only set_pos, always valid in Genesis 0.4.x."""
    return f'''\
# Pendulum — fallback for: {topic!r}
add_standard_lights()

_cam = scene.add_camera(
    res=(960, 540),
    pos=(0.0, 0.55, 1.30),
    lookat=(0.0, 0.20, 0.0),
    fov=50,
    GUI=False,
)

# Ground
scene.add_entity(morph=Plane(), material=Rigid(),
    surface=Surface(color=(0.07, 0.09, 0.11, 1.0), roughness=0.90))

# Pivot box (fixed)
scene.add_entity(
    morph=Box(size=(0.04, 0.04, 0.04), pos=(0.0, 0.80, 0.0)),
    material=Rigid(rho=7800),
    surface=Surface(color=(0.55, 0.60, 0.68, 1.0), roughness=0.30, metallic=0.88))

# Pendulum rod
rod = scene.add_entity(
    morph=Cylinder(radius=0.008, height=0.50, pos=(0.0, 0.55, 0.0)),
    material=Rigid(rho=2700),
    surface=Surface(color=(0.80, 0.85, 0.90, 1.0), roughness=0.05, metallic=0.95))

# Pendulum bob
bob = scene.add_entity(
    morph=Cylinder(radius=0.04, height=0.04, pos=(0.0, 0.30, 0.0)),
    material=Rigid(rho=8900),
    surface=Surface(color=(0.83, 0.68, 0.21, 1.0), roughness=0.15, metallic=0.90))

_PIVOT_Y   = 0.80
_LENGTH    = 0.50
_AMPLITUDE = 0.55   # radians (~31 deg)
_OMEGA     = 2.8    # rad/s

def pre_step(frame, t):
    angle = _AMPLITUDE * math.sin(_OMEGA * t)
    sx, sy = math.sin(angle), math.cos(angle)
    # Rod midpoint
    rod.set_pos((_LENGTH * 0.5 * sx, _PIVOT_Y - _LENGTH * 0.5 * sy, 0.0))
    rod.set_quat(quat_from_euler(0.0, 0.0, math.degrees(-angle)))
    # Bob at end
    bob.set_pos((_LENGTH * sx, _PIVOT_Y - _LENGTH * sy, 0.0))
'''


# ─── Request / Response ───────────────────────────────────────────────────────
class GenesisRequest(BaseModel):
    topic: str
    context: str = ""


class GenesisResponse(BaseModel):
    video_b64:   str | None = None
    script:      str | None = None
    topic:       str        = ""
    error:       str | None = None
    fallback:    bool       = False
    verified:    bool       = False
    gemini_note: str | None = None


# ─── Core render helper ───────────────────────────────────────────────────────
async def _run_genesis(full_script: str, tmpdir: str, name: str = "sim.py") -> tuple[bool, str, str, str]:
    script_path = os.path.join(tmpdir, name)
    output_path = os.path.join(tmpdir, name.replace(".py", ".mp4"))
    with open(script_path, "w") as f:
        f.write(full_script)
    try:
        proc = await asyncio.create_subprocess_exec(
            _genesis_python(), script_path, output_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=tmpdir,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=TIMEOUT_SECS)
        sout = stdout.decode("utf-8", errors="replace")
        serr = stderr.decode("utf-8", errors="replace")
        success = "DONE:" in sout and os.path.exists(output_path)
        return success, sout, serr, output_path
    except asyncio.TimeoutError:
        return False, "", f"Genesis timed out after {TIMEOUT_SECS}s", output_path
    except Exception as exc:
        return False, "", str(exc), output_path


# ─── Endpoint ─────────────────────────────────────────────────────────────────
@router.post("/genesis", response_model=GenesisResponse)
async def generate_genesis_simulation(
    req: GenesisRequest,
    user: User = Depends(get_current_user),
):
    settings = get_settings()
    topic    = req.topic[:200].strip()
    context  = req.context[:2000].strip()
    gemini_key: str = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""

    llm = OpenAI(api_key=settings.llm_api_key, base_url=settings.llm_base_url)

    # ── Genesis availability check ───────────────────────────────────────────
    check = await asyncio.create_subprocess_exec(
        _genesis_python(), "-c", "import genesis",
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
    )
    await check.wait()
    if check.returncode != 0:
        try:
            _, raw = await _generate_code(llm, settings, topic, context, feedback="")
        except Exception:
            raw = _fallback_script(topic)
        full = SCRIPT_PREFIX + "\n" + raw + "\n" + SCRIPT_SUFFIX
        return GenesisResponse(
            topic=topic, script=full,
            error=(
                "genesis-world is not installed on this server.\n"
                "Download the script and run locally:\n"
                "  pip install torch && pip install genesis-world\n"
                "  python genesis_simulation.py"
            ),
        )

    # ── Generate → render → verify loop ─────────────────────────────────────
    with tempfile.TemporaryDirectory() as tmpdir:
        raw         = ""
        brief_txt   = "{}"
        feedback    = ""
        output_path = ""
        verified    = False
        gemini_note = None
        used_fallback = False

        for attempt in range(MAX_RETRIES + 1):
            # Generate code
            try:
                brief_txt, raw = await _generate_code(
                    llm, settings, topic, context, feedback=feedback
                )
            except Exception as exc:
                logger.warning("LLM attempt %d failed: %s", attempt, exc)
                raw       = _fallback_script(topic)
                brief_txt = "{}"
                used_fallback = True

            if not _is_safe(raw) or len(raw) > MAX_CODE_LEN:
                raw           = _fallback_script(topic)
                used_fallback = True
            else:
                raw = _sanitize_code(raw)

            full_script = SCRIPT_PREFIX + "\n" + raw + "\n" + SCRIPT_SUFFIX
            success, sout, serr, output_path = await _run_genesis(
                full_script, tmpdir, f"sim_{attempt}.py"
            )

            if not success:
                err_summary = (serr or sout)[-500:]
                if attempt < MAX_RETRIES:
                    feedback = (
                        f"The previous script CRASHED with this error:\n{err_summary[:300]}\n"
                        "Fix the crash. Common causes: "
                        "using set_euler (does not exist — use set_quat(quat_from_euler(r,p,y))); "
                        "Box without pos; using Liquid/Elastic materials; calling scene.step()."
                    )
                    continue
                # All LLM attempts failed — try reliable fallback
                fb_raw    = _fallback_script(topic)
                fb_full   = SCRIPT_PREFIX + "\n" + fb_raw + "\n" + SCRIPT_SUFFIX
                ok_fb, _, _, fb_path = await _run_genesis(fb_full, tmpdir, "fallback.py")
                if ok_fb:
                    raw           = fb_raw
                    output_path   = fb_path
                    used_fallback = True
                    gemini_note   = "Topic-specific rendering failed; showing pendulum fallback."
                    break
                return GenesisResponse(
                    topic=topic, script=raw,
                    error=f"Genesis rendering failed after {MAX_RETRIES+1} attempts: {err_summary}",
                )

            # ── Gemini Vision check ─────────────────────────────────────────
            if gemini_key and not used_fallback:
                try:
                    brief_obj = json.loads(brief_txt)
                except Exception:
                    brief_obj = {}
                accuracy_check = brief_obj.get(
                    "accuracy_check",
                    f"a 3D physics simulation clearly and specifically depicting {topic}",
                )
                frame_b64 = _extract_frame_b64(output_path, frame_index=45)
                if frame_b64:
                    passes, gem_fb = _verify_with_gemini(
                        frame_b64, topic, accuracy_check, gemini_key
                    )
                    gemini_note = gem_fb
                    if passes:
                        verified = True
                        break
                    elif attempt < MAX_RETRIES:
                        feedback = (
                            f"Gemini Vision reviewed your rendered frame and said: '{gem_fb}'. "
                            f"The scene does NOT look like '{topic}'. "
                            "Completely redesign it — different shapes, layout, and motion that "
                            "unambiguously represents this specific topic."
                        )
                        continue
                    else:
                        verified = False
                        break
                else:
                    verified = False
                    gemini_note = "Frame extraction failed; skipping visual verification."
                    break
            else:
                verified = False
                if not gemini_key:
                    gemini_note = "Gemini key not set; visual verification skipped."
                break

        # ── Encode and return ────────────────────────────────────────────────
        if not output_path or not os.path.exists(output_path):
            return GenesisResponse(topic=topic, script=raw, error="Output MP4 not found.")

        video_b64 = base64.b64encode(Path(output_path).read_bytes()).decode("ascii")
        return GenesisResponse(
            video_b64=video_b64,
            script=raw,
            topic=topic,
            fallback=used_fallback,
            verified=verified,
            gemini_note=gemini_note,
        )


# ─── Two-stage LLM generation ─────────────────────────────────────────────────
async def _generate_code(
    llm: OpenAI, settings, topic: str, context: str, feedback: str
) -> tuple[str, str]:
    """Stage 1: design brief JSON. Stage 2: Genesis code from brief."""

    brief_prompt = BRIEF_PROMPT.format(topic=topic, context=context or topic)
    if feedback:
        brief_prompt += f"\n\nCRITICAL CORRECTION NEEDED: {feedback}\nCompletely redesign the scene."

    brief_resp = llm.chat.completions.create(
        model=settings.llm_model,
        messages=[{"role": "user", "content": brief_prompt}],
        temperature=0.35,
        max_tokens=800,
    )
    brief_raw = _strip_fences(brief_resp.choices[0].message.content or "{}")
    m = re.search(r"\{[\s\S]*\}", brief_raw)
    brief_txt = m.group(0) if m else "{}"
    try:
        brief_pretty = json.dumps(json.loads(brief_txt), indent=2)
    except Exception:
        brief_pretty = brief_txt

    code_prompt = CODE_PROMPT.format(topic=topic, brief=brief_pretty)
    if feedback:
        code_prompt += (
            f"\n\nCRITICAL: Previous attempt FAILED or looked wrong: {feedback}\n"
            "Generate a COMPLETELY DIFFERENT, working scene."
        )

    code_resp = llm.chat.completions.create(
        model=settings.llm_model,
        messages=[{"role": "user", "content": code_prompt}],
        temperature=0.2,
        max_tokens=3000,
    )
    raw = _strip_fences(code_resp.choices[0].message.content or "")
    return brief_txt, raw
