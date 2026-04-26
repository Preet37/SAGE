"""
3D Simulation — accurate, topic-specific mechanical/physical model.

Two-step LLM pipeline:
  1. Extract: identify the exact physical object to model, its components,
     materials, dimensions, and motion type.
  2. Generate: produce Three.js code for ONE accurate cross-section model
     with labeled parts, correct PBR materials, and physics-accurate animation.

The output is always a single focused object — not a random shape showcase.
"""

import json
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
HTML_3D_TEMPLATE = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0c12;color:#e6edf3;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;display:flex;height:100vh;overflow:hidden}
#sidebar{width:220px;background:#0d1117;border-right:1px solid #1e2530;display:flex;flex-direction:column;flex-shrink:0;min-width:0}
#sb-head{padding:10px 12px;border-bottom:1px solid #1e2530}
#sb-title{font-size:12px;font-weight:700;color:#e6edf3;letter-spacing:.03em}
#sb-object{font-size:10px;color:#58a6ff;margin-top:2px;word-wrap:break-word}
#params{padding:10px 12px;overflow-y:auto;flex:1}
#canvas-wrap{flex:1;position:relative;min-width:0;overflow:hidden}
canvas{display:block;width:100%;height:100%}
.pg{margin-bottom:12px}
.pl{font-size:10px;color:#8b949e;text-transform:uppercase;letter-spacing:.4px;margin-bottom:3px;display:flex;justify-content:space-between}
.pv{color:#58a6ff;font-weight:600;font-size:10px}
input[type=range]{width:100%;height:3px;accent-color:#58a6ff;cursor:pointer;display:block;margin-top:2px}
#legend{padding:10px 12px;border-top:1px solid #1e2530;font-size:9px;color:#8b949e}
.leg-item{display:flex;align-items:center;gap:6px;margin-bottom:4px}
.leg-dot{width:8px;height:8px;border-radius:2px;flex-shrink:0}
#fps{position:absolute;top:8px;right:10px;font-size:9px;color:#484f58;pointer-events:none;font-variant-numeric:tabular-nums}
#hint{position:absolute;bottom:8px;left:10px;font-size:9px;color:#484f58;pointer-events:none}
#label-layer{position:absolute;inset:0;pointer-events:none}
.label3d{position:absolute;transform:translate(-50%,-50%);white-space:nowrap;font-size:10px;color:#e6edf3;background:rgba(13,17,23,.82);border:1px solid #30363d;border-radius:4px;padding:2px 6px;pointer-events:none;line-height:1.4}
.label3d::before{content:'';position:absolute;left:50%;top:100%;transform:translateX(-50%);border:4px solid transparent;border-top-color:#30363d}
#err{display:none;position:absolute;inset:0;background:rgba(10,12,18,.93);padding:20px;color:#f85149;font-size:11px;white-space:pre-wrap;z-index:99;overflow:auto}
</style>
</head>
<body>
<div id="sidebar">
  <div id="sb-head">
    <div id="sb-title">⚡ 3D Simulation</div>
    <div id="sb-object">Loading…</div>
  </div>
  <div id="params"></div>
  <div id="legend"></div>
</div>
<div id="canvas-wrap">
  <canvas id="c"></canvas>
  <div id="label-layer"></div>
  <div id="fps"></div>
  <div id="hint">Drag · scroll · right-drag to pan</div>
  <div id="err"></div>
</div>

<script type="importmap">
{"imports":{
  "three":"https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.module.js",
  "three/addons/":"https://cdn.jsdelivr.net/npm/three@0.169.0/examples/jsm/"
}}
</script>

<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

window.onerror = (m,s,l,c,e) => {
  document.getElementById('err').style.display='block';
  document.getElementById('err').textContent=`Error: ${m}\n@ ${s}:${l}\n${e?.stack||''}`;
};
window.addEventListener('unhandledrejection', e => {
  document.getElementById('err').style.display='block';
  document.getElementById('err').textContent=`Promise error:\n${e.reason}`;
});

// ── Renderer ─────────────────────────────────────────────────────────────────
const canvas = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.4;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.localClippingEnabled = true;  // needed for cross-section cut

// ── Scene ─────────────────────────────────────────────────────────────────────
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0c12);

// ── Camera ────────────────────────────────────────────────────────────────────
const camera = new THREE.PerspectiveCamera(50, 1, 0.001, 5000);
camera.position.set(0, 3, 8);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.07;
controls.target.set(0, 0, 0);

// ── Resize ────────────────────────────────────────────────────────────────────
const wrap = document.getElementById('canvas-wrap');
function resize(){
  const w=wrap.clientWidth, h=wrap.clientHeight;
  camera.aspect = w/h;
  camera.updateProjectionMatrix();
  renderer.setSize(w,h,false);
}
new ResizeObserver(resize).observe(wrap);
resize();

// ── Param system ──────────────────────────────────────────────────────────────
const P = {};
function buildUI(params){
  const c=document.getElementById('params');
  c.innerHTML='';
  for(const p of params){
    P[p.key]=p.default??p.min;
    const w=document.createElement('div'); w.className='pg';
    const l=document.createElement('div'); l.className='pl';
    const n=document.createElement('span'); n.textContent=p.label;
    const v=document.createElement('span'); v.className='pv'; v.id='v_'+p.key;
    v.textContent=(+P[p.key]).toFixed(p.decimals??2);
    l.append(n,v);
    const s=document.createElement('input'); s.type='range';
    s.min=p.min; s.max=p.max;
    s.step=p.step??((p.max-p.min)/200);
    s.value=P[p.key];
    s.oninput=()=>{
      P[p.key]=parseFloat(s.value);
      document.getElementById('v_'+p.key).textContent=P[p.key].toFixed(p.decimals??2);
      try{ if(typeof onParam==='function') onParam(p.key,P[p.key],P); }catch(e){console.warn(e);}
    };
    w.append(l,s); c.append(w);
  }
}

// ── Legend ────────────────────────────────────────────────────────────────────
function buildLegend(items){
  const l=document.getElementById('legend'); l.innerHTML='';
  for(const it of items){
    const row=document.createElement('div'); row.className='leg-item';
    const dot=document.createElement('div'); dot.className='leg-dot';
    dot.style.background=it.color;
    const txt=document.createElement('span'); txt.textContent=it.label;
    row.append(dot,txt); l.append(row);
  }
}

// ── 3D Labels ────────────────────────────────────────────────────────────────
const _labels=[];
function addLabel(text, worldPos){
  const el=document.createElement('div'); el.className='label3d';
  el.textContent=text;
  document.getElementById('label-layer').append(el);
  _labels.push({el, pos: worldPos.clone()});
}
function updateLabels(){
  const ww=wrap.clientWidth, wh=wrap.clientHeight;
  for(const lb of _labels){
    const v=lb.pos.clone().project(camera);
    const x=(v.x*.5+.5)*ww, y=(-.5*v.y+.5)*wh;
    if(v.z>1){ lb.el.style.display='none'; continue; }
    lb.el.style.display='block';
    lb.el.style.left=x+'px'; lb.el.style.top=y+'px';
  }
}

// ════════════════════════════════════════════════════════════════════════════
// LLM-GENERATED CODE
// ════════════════════════════════════════════════════════════════════════════
${GENERATED_CODE}
// ════════════════════════════════════════════════════════════════════════════

// ── Animation loop ────────────────────────────────────────────────────────────
const clock=new THREE.Clock();
let fc=0;
(function loop(){
  requestAnimationFrame(loop);
  const dt=Math.min(clock.getDelta(),.05);
  const t=clock.getElapsedTime();
  fc++;
  controls.update();
  try{ if(typeof tick==='function') tick(t,dt,P); }catch(e){ console.error('tick error',e); }
  renderer.render(scene,camera);
  updateLabels();
  if(fc%60===0) document.getElementById('fps').textContent=Math.round(1/(dt||.016))+' fps';
})();
</script>
</body>
</html>"""


# ─── Step 1: Extract exact model spec ────────────────────────────────────────
EXTRACT_PROMPT = """You are a mechanical/physical engineering expert.

Given this topic and context, identify the SINGLE most important physical mechanism or component to model in 3D.

Topic: {topic}
Context: {context}

Respond with a JSON object ONLY (no markdown):
{{
  "object_name": "exact technical name of the component",
  "description": "1-sentence description of what it does",
  "components": [
    {{"name": "component name", "shape": "cylinder|box|sphere|torus|custom", "material": "steel|rubber|glass|plastic|fluid|copper|ceramic", "color_hex": "#rrggbb", "role": "brief functional role"}}
  ],
  "motion_type": "linear|rotational|oscillating|expanding|none",
  "motion_description": "describe the exact motion to animate (e.g. 'piston rod extends 40mm then retracts')",
  "cross_section_axis": "x|y|z",
  "key_parameters": [
    {{"key": "param_key", "label": "Human Label", "min": 0, "max": 100, "default": 50, "unit": "unit", "effect": "what changing this does to the animation"}}
  ]
}}
"""

# ─── Step 2: Generate Three.js from spec ─────────────────────────────────────
GEN_PROMPT = """You are an expert Three.js engineer. Generate JavaScript code for an accurate 3D model.

MODEL SPEC:
{spec_json}

CRITICAL RULES — read every one:

1. MODEL ONLY the object named above. ONE focused, anatomically accurate model.
   NO random floating shapes. NO decorative extras. NO generic "physics sandbox."

2. GEOMETRY must be accurate:
   - Use real-world proportions. A hydraulic cylinder is 5-10x longer than its diameter.
   - CylinderGeometry for shafts, rods, barrels. TorusGeometry for O-rings/seals.
   - LatheGeometry or ExtrudeGeometry for complex profiles.
   - Use clipping planes (renderer.localClippingEnabled=true is set) to cut a
     cross-section that reveals internal components.
   - Arrange parts in correct spatial relationships (piston INSIDE cylinder, etc.)

3. MATERIALS must be realistic:
   - Steel/aluminum: MeshStandardMaterial, metalness:0.85, roughness:0.15, color:#8a9bb0
   - Rubber seals: MeshStandardMaterial, metalness:0, roughness:0.9, color:#1a1a1a
   - Hydraulic fluid: MeshStandardMaterial, metalness:0, roughness:0, color:#c07020, transparent:true, opacity:0.5
   - Glass/viewport: MeshPhysicalMaterial, transmission:0.9, roughness:0, thickness:0.5
   - Copper/brass: MeshStandardMaterial, metalness:0.9, roughness:0.2, color:#b87333

4. LIGHTING must be high quality:
   - One DirectionalLight (intensity 2.5, castShadow true, shadow map 2048x2048)
   - One HemisphereLight for ambient (skyColor:#1a2f4a, groundColor:#0a0c12, intensity 0.8)
   - One or two PointLights for dramatic highlights on metal surfaces
   - Camera aimed at the object, not at origin unless object is centered there

5. ANIMATION must show the ACTUAL FUNCTION of this specific object:
   - Use the motion_type and motion_description from the spec
   - Sliders control physically meaningful parameters (speed, stroke, pressure)
   - The motion must make physical sense (piston moves axially, gear rotates, spring oscillates)
   - Use smooth sinusoidal or physics-based motion, NOT random spinning

6. LABELS: Call addLabel('Component Name', worldPos) for every major component.
   worldPos must be a THREE.Vector3 positioned at the label's target.

7. LEGEND: Call buildLegend([{{label:'...', color:'#hex'}},...]) with material colors.

8. Call document.getElementById('sb-object').textContent = 'ObjectName';
   to show the object name in the sidebar header.

9. Expose EXACTLY these named symbols (no other names):
   - buildUI(PARAMS) called ONCE with your param array
   - function tick(t, dt, P) — animation update, t=elapsed, dt=delta, P=param values
   - function onParam(key, val, P) — optional, handle slider changes

10. All mesh objects must set castShadow=true, receiveShadow=true.

11. Add a ground/floor plane with receiveShadow=true and a subtle grid.

Output ONLY raw JavaScript. No markdown. No ```js. No explanation.
"""


# ─── Request/Response ────────────────────────────────────────────────────────
class Visual3DRequest(BaseModel):
    topic: str
    context: str = ""


class Visual3DResponse(BaseModel):
    html: str
    topic: str
    object_name: str = ""
    error: str | None = None


# ─── Endpoint ─────────────────────────────────────────────────────────────────
@router.post("/3d", response_model=Visual3DResponse)
async def generate_3d_simulation(
    req: Visual3DRequest,
    user: User = Depends(get_current_user),
):
    settings = get_settings()
    client = OpenAI(api_key=settings.llm_api_key, base_url=settings.llm_base_url)
    topic = req.topic[:200]
    context = req.context[:2000]

    object_name = topic

    try:
        # ── Step 1: Extract model spec ────────────────────────────────────────
        extract_resp = client.chat.completions.create(
            model=settings.llm_model,
            messages=[{
                "role": "user",
                "content": EXTRACT_PROMPT.format(topic=topic, context=context)
            }],
            temperature=0.1,
            max_tokens=800,
        )
        raw_spec = extract_resp.choices[0].message.content or ""
        # Strip markdown fences
        raw_spec = re.sub(r"```(?:json)?\s*", "", raw_spec)
        raw_spec = re.sub(r"```\s*$", "", raw_spec, flags=re.MULTILINE).strip()

        # Parse spec
        try:
            spec = json.loads(raw_spec)
            object_name = spec.get("object_name", topic)
        except json.JSONDecodeError:
            # Try extracting JSON from the response
            m = re.search(r'\{.*\}', raw_spec, re.DOTALL)
            if m:
                spec = json.loads(m.group())
                object_name = spec.get("object_name", topic)
            else:
                spec = {"object_name": topic, "description": "", "components": [], "motion_type": "none"}
                object_name = topic

        spec_json = json.dumps(spec, indent=2)

        # ── Step 2: Generate Three.js code ────────────────────────────────────
        gen_resp = client.chat.completions.create(
            model=settings.llm_model,
            messages=[{
                "role": "user",
                "content": GEN_PROMPT.format(spec_json=spec_json)
            }],
            temperature=0.2,
            max_tokens=4000,
        )
        generated = gen_resp.choices[0].message.content or ""
        generated = re.sub(r"```(?:javascript|js)?\s*", "", generated)
        generated = re.sub(r"```\s*$", "", generated, flags=re.MULTILINE).strip()

        html = HTML_3D_TEMPLATE.replace("${GENERATED_CODE}", generated)
        return Visual3DResponse(html=html, topic=topic, object_name=object_name)

    except Exception as exc:
        logger.exception("3D simulation generation failed: %s", exc)
        fallback = _fallback_hydraulic(topic)
        html = HTML_3D_TEMPLATE.replace("${GENERATED_CODE}", fallback)
        return Visual3DResponse(html=html, topic=topic, object_name=topic, error=str(exc))


def _fallback_hydraulic(topic: str) -> str:
    """Accurate fallback: a hydraulic linear actuator cross-section."""
    return r"""
// ── Fallback: Hydraulic Linear Actuator ──────────────────────────────────────
document.getElementById('sb-object').textContent = 'Hydraulic Linear Actuator';

const PARAMS = [
  { key:'stroke', label:'Stroke Position', min:0, max:1, default:0.3, step:0.005, decimals:2 },
  { key:'speed',  label:'Cycle Speed',     min:0.1, max:3, default:0.8, step:0.05, decimals:2 },
  { key:'bore',   label:'Bore Diameter',   min:0.3, max:1.2, default:0.7, step:0.01, decimals:2 },
];
buildUI(PARAMS);

// Materials
const matSteel  = new THREE.MeshStandardMaterial({ color:0x7a8fa6, metalness:0.85, roughness:0.2 });
const matDkSteel = new THREE.MeshStandardMaterial({ color:0x4a5568, metalness:0.9, roughness:0.15 });
const matRubber = new THREE.MeshStandardMaterial({ color:0x1a1a1a, metalness:0, roughness:0.95 });
const matFluid  = new THREE.MeshStandardMaterial({ color:0xc07020, metalness:0, roughness:0, transparent:true, opacity:0.45 });
const matBrass  = new THREE.MeshStandardMaterial({ color:0xb87333, metalness:0.9, roughness:0.2 });
const matGround = new THREE.MeshStandardMaterial({ color:0x0f131a, roughness:0.9 });

// Clipping plane for cross-section (cut along +Y half)
const clipPlane = new THREE.Plane(new THREE.Vector3(0, -1, 0), 0.01);

function makeSec(mat) {
  const m = mat.clone();
  m.clippingPlanes = [clipPlane];
  m.clipShadows = true;
  m.side = THREE.DoubleSide;
  return m;
}

// ── Geometry ──────────────────────────────────────────────────────────────────
const CYL_LEN = 4.0;
const CYL_R   = 0.35;
const ROD_R   = 0.12;

// Outer cylinder barrel
const barrel = new THREE.Mesh(
  new THREE.CylinderGeometry(CYL_R, CYL_R, CYL_LEN, 48, 1, true),
  makeSec(matDkSteel)
);
barrel.rotation.z = Math.PI/2;
barrel.castShadow = barrel.receiveShadow = true;
scene.add(barrel);

// Cylinder end cap (rod side)
const capRod = new THREE.Mesh(
  new THREE.CylinderGeometry(CYL_R, CYL_R, 0.12, 32),
  makeSec(matSteel)
);
capRod.rotation.z = Math.PI/2;
capRod.position.x = CYL_LEN/2 + 0.06;
capRod.castShadow = capRod.receiveShadow = true;
scene.add(capRod);

// Cylinder end cap (blind end)
const capBlind = capRod.clone();
capBlind.position.x = -(CYL_LEN/2 + 0.06);
scene.add(capBlind);

// Piston
const piston = new THREE.Mesh(
  new THREE.CylinderGeometry(CYL_R*0.92, CYL_R*0.92, 0.22, 40),
  makeSec(matBrass)
);
piston.rotation.z = Math.PI/2;
piston.castShadow = piston.receiveShadow = true;
scene.add(piston);

// Piston O-ring seal
const pistonSeal = new THREE.Mesh(
  new THREE.TorusGeometry(CYL_R*0.92, 0.035, 12, 36),
  makeSec(matRubber)
);
pistonSeal.rotation.x = Math.PI/2;
pistonSeal.castShadow = true;
scene.add(pistonSeal);

// Piston rod
const rod = new THREE.Mesh(
  new THREE.CylinderGeometry(ROD_R, ROD_R, CYL_LEN*1.3, 24),
  makeSec(matSteel)
);
rod.rotation.z = Math.PI/2;
rod.castShadow = rod.receiveShadow = true;
scene.add(rod);

// Rod seal (at rod-side cap)
const rodSeal = new THREE.Mesh(
  new THREE.TorusGeometry(ROD_R*1.4, 0.04, 10, 32),
  makeSec(matRubber)
);
rodSeal.rotation.x = Math.PI/2;
rodSeal.position.x = CYL_LEN/2 + 0.06;
rodSeal.castShadow = true;
scene.add(rodSeal);

// Hydraulic fluid (pressurized side — behind piston)
const fluid = new THREE.Mesh(
  new THREE.CylinderGeometry(CYL_R*0.88, CYL_R*0.88, CYL_LEN, 32),
  makeSec(matFluid)
);
fluid.rotation.z = Math.PI/2;
scene.add(fluid);

// Port fittings (hydraulic inlet/outlet)
for(const xPos of [-CYL_LEN/2+0.3, CYL_LEN/2-0.3]) {
  const port = new THREE.Mesh(
    new THREE.CylinderGeometry(0.06, 0.06, 0.28, 10),
    matBrass.clone()
  );
  port.position.set(xPos, CYL_R+0.1, 0);
  port.castShadow = true;
  scene.add(port);
}

// ── Lights ────────────────────────────────────────────────────────────────────
const sun = new THREE.DirectionalLight(0xfff4e0, 2.8);
sun.position.set(6, 8, 5);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.near = 0.1;
sun.shadow.camera.far = 30;
sun.shadow.camera.left = -6;
sun.shadow.camera.right = 6;
sun.shadow.camera.top = 4;
sun.shadow.camera.bottom = -4;
scene.add(sun);
scene.add(new THREE.HemisphereLight(0x1a2f4a, 0x0a0c12, 0.9));
const rim = new THREE.PointLight(0x4488ff, 1.5, 20);
rim.position.set(-5, 3, -3);
scene.add(rim);

// ── Ground ────────────────────────────────────────────────────────────────────
const ground = new THREE.Mesh(new THREE.PlaneGeometry(20, 20), matGround);
ground.rotation.x = -Math.PI/2;
ground.position.y = -0.65;
ground.receiveShadow = true;
scene.add(ground);
scene.add(new THREE.GridHelper(16, 24, 0x1a2030, 0x111820));

// ── Camera ────────────────────────────────────────────────────────────────────
camera.position.set(3, 2.5, 5);
controls.target.set(0, 0, 0);

// ── Labels ────────────────────────────────────────────────────────────────────
addLabel('Piston', new THREE.Vector3(0, CYL_R+0.4, 0));
addLabel('Piston Rod', new THREE.Vector3(CYL_LEN*0.6, 0.3, 0));
addLabel('Cylinder Barrel', new THREE.Vector3(-0.5, -CYL_R-0.35, 0));
addLabel('End Cap', new THREE.Vector3(-(CYL_LEN/2+0.1), -0.4, 0));
addLabel('Rod Seal', new THREE.Vector3(CYL_LEN/2+0.15, 0.4, 0));

buildLegend([
  { label:'Steel barrel / rod', color:'#7a8fa6' },
  { label:'Brass piston', color:'#b87333' },
  { label:'Rubber O-ring seals', color:'#333' },
  { label:'Hydraulic fluid', color:'#c07020' },
]);

// ── Animation ─────────────────────────────────────────────────────────────────
let autoStroke = 0.3;
let strokeDir = 1;

function tick(t, dt, P) {
  const spd = P.speed ?? 0.8;
  const boreScale = (P.bore ?? 0.7) / 0.7;

  // Auto-cycle stroke with adjustable speed
  autoStroke += dt * spd * strokeDir * 0.6;
  if(autoStroke > 0.98) strokeDir = -1;
  if(autoStroke < 0.02) strokeDir = 1;

  const s = P.stroke !== undefined
    ? P.stroke
    : autoStroke;

  // Piston position: from -CYL_LEN/2+0.11 to +CYL_LEN/2-0.11
  const minX = -CYL_LEN/2 + 0.25;
  const maxX =  CYL_LEN/2 - 0.25;
  const pistonX = minX + s * (maxX - minX);

  piston.position.x = pistonX;
  pistonSeal.position.x = pistonX;

  // Rod moves with piston (rod center extends right)
  const rodOffset = CYL_LEN*0.65 + pistonX * 0.5;
  rod.position.x = rodOffset * 0.5;

  // Fluid fills left chamber (behind piston)
  const fluidLen = pistonX + CYL_LEN/2 - 0.12;
  if(fluidLen > 0.05) {
    fluid.scale.set(fluidLen / CYL_LEN, boreScale, boreScale);
    fluid.position.x = pistonX/2 - CYL_LEN/4 + 0.06;
  }

  // Scale bore visually
  barrel.scale.set(1, boreScale, boreScale);
  piston.scale.set(1, boreScale*0.92, boreScale*0.92);
  pistonSeal.scale.set(1, boreScale, boreScale);
}

function onParam(key, val, P) {
  if(key === 'stroke') {
    // Manual override from slider — disable auto advance temporarily
    strokeDir = 0;
    setTimeout(() => { strokeDir = 1; }, 2000);
  }
}
""";
