"""
3D Simulation endpoint.

LLM generates only three focused functions inside a hardcoded Three.js + cannon-es
template:
  - PARAMS      — array of slider definitions
  - setupScene  — create geometry, materials, lights, camera position
  - updateScene — animation frame callback (t, dt, params)
  - onParamChange (optional) — called when user moves a slider

The template handles: WebGLRenderer, PBR tone-mapping, shadow maps, OrbitControls,
resize observer, slider UI, error overlay, FPS counter, and the RAF loop.
"""

import logging
import re
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from openai import OpenAI

from ..config import get_settings
from ..deps import get_current_user
from ..models.user import User

router = APIRouter(prefix="/visual", tags=["visual"])
logger = logging.getLogger(__name__)


# ─── HTML template ────────────────────────────────────────────────────────────
# Everything except the LLM-generated ${GENERATED_CODE} block is hardcoded so
# the simulation always works regardless of what the LLM produces.

HTML_3D_TEMPLATE = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#08090e;color:#e6edf3;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;display:flex;height:100vh;overflow:hidden}
#sidebar{width:230px;background:#0d1117;border-right:1px solid #21262d;display:flex;flex-direction:column;flex-shrink:0}
#sb-title{padding:12px 14px;border-bottom:1px solid #21262d;font-size:13px;font-weight:700;color:#e6edf3;letter-spacing:.02em}
#sb-subtitle{padding:4px 14px 10px;font-size:10px;color:#8b949e;border-bottom:1px solid #21262d}
#params{padding:12px 14px;overflow-y:auto;flex:1}
#canvas-wrap{flex:1;position:relative;min-width:0}
canvas{display:block;width:100%;height:100%}
.pg{margin-bottom:14px}
.pl{font-size:10px;color:#8b949e;text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px;display:flex;justify-content:space-between;align-items:center}
.pv{color:#58a6ff;font-weight:600}
input[type=range]{width:100%;height:4px;accent-color:#58a6ff;cursor:pointer}
#status{position:absolute;bottom:8px;right:10px;font-size:10px;color:#484f58;pointer-events:none}
#hint{position:absolute;bottom:8px;left:10px;font-size:10px;color:#484f58;pointer-events:none}
#err{display:none;position:absolute;inset:0;background:rgba(8,9,14,.92);padding:20px;color:#f85149;font-size:11px;white-space:pre-wrap;z-index:99;overflow:auto}
.badge{display:inline-block;font-size:9px;padding:2px 6px;border-radius:10px;background:#1f2937;color:#58a6ff;border:1px solid #1e3a5f;margin-top:6px}
</style>
</head>
<body>
<div id="sidebar">
  <div id="sb-title">⚡ 3D Simulation</div>
  <div id="sb-subtitle" id="sb-sub"><!-- topic injected --></div>
  <div id="params"></div>
  <div style="padding:12px 14px;margin-top:auto;border-top:1px solid #21262d">
    <div class="badge">Three.js r169 · WebGL2</div>
    <div class="badge" style="margin-left:4px">cannon-es physics</div>
  </div>
</div>
<div id="canvas-wrap">
  <canvas id="c"></canvas>
  <div id="status"></div>
  <div id="hint">Drag to orbit · scroll to zoom · right-drag to pan</div>
  <div id="err"></div>
</div>

<script type="importmap">
{"imports":{
  "three":"https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.module.js",
  "three/addons/":"https://cdn.jsdelivr.net/npm/three@0.169.0/examples/jsm/",
  "cannon-es":"https://cdn.jsdelivr.net/npm/cannon-es@0.20.0/dist/cannon-es.js"
}}
</script>

<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import * as CANNON from 'cannon-es';

// ── Global error overlay ────────────────────────────────────────────────────
window.onerror = (msg, src, line, col, err) => {
  const box = document.getElementById('err');
  box.style.display = 'block';
  box.textContent = `Runtime error:\n${msg}\n@ ${src}:${line}:${col}\n\n${err?.stack||''}`;
};
window.addEventListener('unhandledrejection', e => {
  const box = document.getElementById('err');
  box.style.display = 'block';
  box.textContent = `Unhandled promise rejection:\n${e.reason}`;
});

// ── Renderer ────────────────────────────────────────────────────────────────
const canvas = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.3;
renderer.outputColorSpace = THREE.SRGBColorSpace;

// ── Scene ───────────────────────────────────────────────────────────────────
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x08090e);

// ── Camera + controls ───────────────────────────────────────────────────────
const camera = new THREE.PerspectiveCamera(55, 1, 0.01, 5000);
camera.position.set(0, 5, 14);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.target.set(0, 1, 0);

// ── Param system ────────────────────────────────────────────────────────────
const paramValues = {};

function buildUI(params) {
  const container = document.getElementById('params');
  container.innerHTML = '';
  for (const p of params) {
    paramValues[p.key] = p.default ?? p.min;
    const wrap = document.createElement('div');
    wrap.className = 'pg';
    const lbl = document.createElement('div');
    lbl.className = 'pl';
    const nameEl = document.createElement('span');
    nameEl.textContent = p.label;
    const valEl = document.createElement('span');
    valEl.className = 'pv';
    valEl.id = 'v_' + p.key;
    valEl.textContent = (+paramValues[p.key]).toFixed(2);
    lbl.appendChild(nameEl);
    lbl.appendChild(valEl);
    const slider = document.createElement('input');
    slider.type = 'range';
    slider.min = p.min;
    slider.max = p.max;
    slider.step = p.step ?? ((p.max - p.min) / 200);
    slider.value = paramValues[p.key];
    slider.addEventListener('input', () => {
      paramValues[p.key] = parseFloat(slider.value);
      document.getElementById('v_' + p.key).textContent = paramValues[p.key].toFixed(2);
      try { if (typeof onParamChange === 'function') onParamChange(p.key, paramValues[p.key], paramValues, scene, THREE, CANNON); }
      catch(e) { console.warn('onParamChange error', e); }
    });
    wrap.appendChild(lbl);
    wrap.appendChild(slider);
    container.appendChild(wrap);
  }
}

// ── Resize ──────────────────────────────────────────────────────────────────
function resize() {
  const wrap = document.getElementById('canvas-wrap');
  const w = wrap.clientWidth, h = wrap.clientHeight;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h, false);
}
new ResizeObserver(resize).observe(document.getElementById('canvas-wrap'));
resize();

// ════════════════════════════════════════════════════════════════════════════
// LLM-GENERATED CODE — scene setup, physics, animation
// ════════════════════════════════════════════════════════════════════════════
${GENERATED_CODE}
// ════════════════════════════════════════════════════════════════════════════

// ── Animation loop ──────────────────────────────────────────────────────────
const clock = new THREE.Clock();
let frameCount = 0;
const fpsEl = document.getElementById('status');

(function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.05);
  const elapsed = clock.getElapsedTime();
  frameCount++;
  controls.update();
  try {
    if (typeof updateScene === 'function') updateScene(elapsed, dt, paramValues, scene, THREE, CANNON);
  } catch(e) { console.error('updateScene error', e); }
  renderer.render(scene, camera);
  if (frameCount % 60 === 0) fpsEl.textContent = Math.round(1 / (dt || 0.016)) + ' fps';
})();
</script>
</body>
</html>"""


# ─── LLM prompt ────────────────────────────────────────────────────────────
SCENE_PROMPT = """You are an expert Three.js + cannon-es physics simulation engineer.
Generate a self-contained JavaScript block for a 3D physics simulation of: "{topic}"

Context: {context}

The block will be injected inside a Three.js r169 module script.
These globals are already defined and available:
  scene        — THREE.Scene
  camera       — THREE.PerspectiveCamera (positioned by you)
  renderer     — THREE.WebGLRenderer (shadows enabled)
  controls     — OrbitControls
  THREE        — the three.js namespace
  CANNON       — cannon-es namespace
  buildUI(params) — call this with your PARAMS array to create sliders
  paramValues  — live object of current slider values

You MUST define these:

1. const PARAMS = [ {{ key, label, min, max, default, step? }}, ... ]
   — 4-8 physically meaningful parameters the user can tweak.

2. (function that runs immediately) — sets up the scene:
   a. Set camera.position and controls.target for a good view
   b. Add meaningful lights:
      - DirectionalLight with castShadow = true, shadow map size 2048
      - AmbientLight or HemisphereLight for fill
      - Optional PointLights for dramatic highlights
   c. Create rich PBR geometry using THREE.MeshStandardMaterial or
      THREE.MeshPhysicalMaterial with realistic metalness, roughness,
      envMapIntensity. Use BufferGeometry for custom meshes where appropriate.
   d. Add a ground plane that receiveShadow = true.
   e. Set up a CANNON.World with gravity if physics applies.
   f. Call buildUI(PARAMS) ONCE.

3. function updateScene(t, dt, params, scene, THREE, CANNON) {{
   }}
   — Called every animation frame. t=elapsed seconds, dt=delta.
   — Advance the cannon physics world: world.step(1/60, dt).
   — Drive geometry from physics body positions/quaternions.
   — Animate non-physics elements (rotation, oscillation, orbits).
   — Make the simulation visually DYNAMIC — things should MOVE.

4. (optional) function onParamChange(key, val, params, scene, THREE, CANNON) {{
   }}
   — If a slider changes, rebuild or rescale relevant objects.

CRITICAL RULES:
- Output ONLY the raw JavaScript. No markdown, no ```js, no explanation.
- Use THREE.MeshStandardMaterial or THREE.MeshPhysicalMaterial — never MeshBasicMaterial.
- Every mesh that should cast/receive shadows must set castShadow/receiveShadow = true.
- Lighting MUST include at least one DirectionalLight with shadows.
- Physics (CANNON.World) is MANDATORY — at minimum one rigid body.
- Camera must be positioned interestingly, not just at default (0,5,14).
- Scene must look like a real simulation — not a static showcase.
- Include at least 3 different geometric shapes (spheres, boxes, cylinders,
  custom BufferGeometry, lathe geometry, etc.).
- Use at least 3 different materials with different colors/metalness/roughness.
- Add fog or environment details for depth: scene.fog = new THREE.FogExp2(...)
- The simulation must AUTO-START and be visually compelling within 1 second.
"""


# ─── Request/Response models ────────────────────────────────────────────────
class Visual3DRequest(BaseModel):
    topic: str
    context: str = ""


class Visual3DResponse(BaseModel):
    html: str
    topic: str
    error: str | None = None


# ─── Endpoint ────────────────────────────────────────────────────────────────
@router.post("/3d", response_model=Visual3DResponse)
async def generate_3d_simulation(
    req: Visual3DRequest,
    user: User = Depends(get_current_user),
):
    settings = get_settings()
    client = OpenAI(api_key=settings.llm_api_key, base_url=settings.llm_base_url)
    topic = req.topic[:200]
    context = req.context[:2000]

    prompt = SCENE_PROMPT.format(topic=topic, context=context)

    try:
        resp = client.chat.completions.create(
            model=settings.llm_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=3500,
        )
        generated = resp.choices[0].message.content or ""

        # Strip any accidental markdown fences
        generated = re.sub(r"```(?:javascript|js)?\s*", "", generated)
        generated = re.sub(r"```\s*$", "", generated, flags=re.MULTILINE)
        generated = generated.strip()

        html = HTML_3D_TEMPLATE.replace("${GENERATED_CODE}", generated)
        return Visual3DResponse(html=html, topic=topic)

    except Exception as exc:
        logger.exception("3D simulation generation failed")
        fallback = _fallback_scene(topic)
        html = HTML_3D_TEMPLATE.replace("${GENERATED_CODE}", fallback)
        return Visual3DResponse(html=html, topic=topic, error=str(exc))


def _fallback_scene(topic: str) -> str:
    """Minimal deterministic scene shown when the LLM call fails."""
    return f"""
// Fallback scene for: {topic}
const PARAMS = [
  {{ key:'speed', label:'Speed', min:0.1, max:5, default:1, step:0.1 }},
  {{ key:'radius', label:'Orbit Radius', min:2, max:10, default:5, step:0.1 }},
  {{ key:'gravity', label:'Gravity', min:0, max:20, default:9.8, step:0.1 }},
];
buildUI(PARAMS);

// Lights
const sun = new THREE.DirectionalLight(0xfff4e0, 2.5);
sun.position.set(8, 12, 6);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
scene.add(sun);
scene.add(new THREE.AmbientLight(0x1a2744, 0.8));
const fill = new THREE.PointLight(0x4488ff, 1.5, 40);
fill.position.set(-8, 4, -4);
scene.add(fill);

// Ground
const ground = new THREE.Mesh(
  new THREE.PlaneGeometry(30, 30),
  new THREE.MeshStandardMaterial({{ color:0x1a1f2e, roughness:0.9, metalness:0.1 }})
);
ground.rotation.x = -Math.PI/2;
ground.receiveShadow = true;
scene.add(ground);

// Grid
const grid = new THREE.GridHelper(30, 30, 0x1f3a5f, 0x0f1f3a);
scene.add(grid);

// Orbiting spheres
const bodies = [];
const colors = [0xff6b6b, 0x4ecdc4, 0xffe66d, 0xa8e6cf, 0xdda0dd];
for (let i=0;i<5;i++) {{
  const r = 0.3+Math.random()*0.6;
  const m = new THREE.Mesh(
    new THREE.SphereGeometry(r,32,32),
    new THREE.MeshStandardMaterial({{ color:colors[i], metalness:0.3, roughness:0.5 }})
  );
  m.castShadow = true;
  scene.add(m);
  bodies.push({{ mesh:m, phase:i*Math.PI*2/5, orbitR:2+i*1.2, height:0.5+i*0.3, speed:0.5+i*0.2 }});
}}

// Central sphere
const core = new THREE.Mesh(
  new THREE.SphereGeometry(1.2,64,64),
  new THREE.MeshStandardMaterial({{ color:0x2a5298, metalness:0.8, roughness:0.2 }})
);
core.castShadow = true;
scene.add(core);

camera.position.set(0, 8, 18);
controls.target.set(0, 2, 0);

function updateScene(t, dt, params) {{
  const spd = params.speed ?? 1;
  const rad = params.radius ?? 5;
  bodies.forEach((b,i) => {{
    const angle = t*b.speed*spd + b.phase;
    b.mesh.position.set(
      Math.cos(angle)*b.orbitR*(rad/5),
      b.height + Math.sin(t*2+i)*0.3,
      Math.sin(angle)*b.orbitR*(rad/5)
    );
    b.mesh.rotation.y = t*2*spd;
  }});
  core.rotation.y = t*0.4*spd;
  core.rotation.x = t*0.15*spd;
}}
"""
