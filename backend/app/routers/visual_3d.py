"""
3D Simulation — OpenJSCAD (@jscad/modeling) + Three.js renderer.

The LLM generates OpenJSCAD-style JavaScript:
  - PARTS_META: per-part display metadata (material, color, label, animation)
  - PARAMS_META: interactive sliders
  - buildParts(P, jscad): uses @jscad/modeling CSG operations to build
    geometrically accurate parts (subtract for hollows, union, intersect)
  - Optional tick() / onParam() for complex animations

The browser template loads @jscad/modeling from esm.sh CDN, runs buildParts(),
converts the resulting polygon data to Three.js BufferGeometry, and renders
with PBR materials, directional shadows, and OrbitControls.

Why this beats raw Three.js:
  - subtract(outer_cylinder, inner_bore)  → real hollow barrel
  - subtract(piston, torus_grooves)       → machined O-ring grooves
  - union(head, flange, boss)             → accurate composite part
  All impossible with Three.js primitives alone.
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
<html><head><meta charset="utf-8"/><style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#08090e;color:#e6edf3;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;display:flex;height:100vh;overflow:hidden}
#sidebar{width:230px;background:#0d1117;border-right:1px solid #1e2530;display:flex;flex-direction:column;flex-shrink:0;overflow:hidden}
#sb-head{padding:10px 14px 4px;font-size:11px;font-weight:700;color:#58a6ff;letter-spacing:.5px;text-transform:uppercase}
#sb-obj{padding:2px 14px 8px;font-size:9.5px;color:#8b949e;border-bottom:1px solid #1e2530;line-height:1.5}
#params{padding:10px 14px;overflow-y:auto;flex:1}
#legend{padding:6px 14px 10px;border-top:1px solid #1e2530}
.leg{display:flex;align-items:center;gap:6px;margin:2px 0;color:#8b949e;font-size:9px}
.leg-c{width:9px;height:9px;border-radius:2px;flex-shrink:0}
#canvas-wrap{flex:1;position:relative}
canvas{display:block;width:100%;height:100%}
#lbl-layer{position:absolute;inset:0;pointer-events:none}
.lbl{position:absolute;transform:translate(-50%,-100%);background:rgba(10,12,18,.88);border:1px solid #30363d;color:#e6edf3;font-size:9px;padding:2px 7px;border-radius:4px;white-space:nowrap}
.lbl::after{content:'';position:absolute;left:50%;bottom:-5px;transform:translateX(-50%);border:4px solid transparent;border-top-color:#30363d}
.pg{margin-bottom:10px}
.pl{display:flex;justify-content:space-between;font-size:9.5px;color:#8b949e;letter-spacing:.4px;margin-bottom:3px}
.pv{color:#58a6ff;font-weight:700}
input[type=range]{width:100%;height:3px;accent-color:#58a6ff;cursor:pointer;display:block}
#loading{position:absolute;inset:0;background:#08090e;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:12px;z-index:10}
.sp{width:28px;height:28px;border:2px solid #1e2530;border-top-color:#58a6ff;border-radius:50%;animation:spin .8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
#ltxt{font-size:10px;color:#8b949e;text-align:center;max-width:180px;line-height:1.5}
#fps{position:absolute;bottom:6px;right:8px;font-size:9px;color:#2a3040;pointer-events:none}
#err{display:none;position:absolute;inset:0;background:rgba(8,9,14,.96);padding:20px;color:#f85149;font-size:10.5px;white-space:pre-wrap;z-index:99;overflow:auto;font-family:monospace;line-height:1.6}
</style></head><body>
<div id="sidebar">
  <div id="sb-head">▲ 3D Simulation</div>
  <div id="sb-obj">Initializing…</div>
  <div id="params"></div>
  <div id="legend"></div>
</div>
<div id="canvas-wrap">
  <canvas id="c"></canvas>
  <div id="lbl-layer"></div>
  <div id="loading">
    <div class="sp"></div>
    <div id="ltxt">Loading JSCAD modeling engine…<br/><span style="color:#3d4a5a;font-size:9px">(OpenJSCAD — first load ~2s)</span></div>
  </div>
  <div id="fps"></div>
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

// ── Error display ────────────────────────────────────────────────────────────
function showErr(msg) {
  document.getElementById('loading').style.display = 'none';
  const el = document.getElementById('err');
  el.style.display = 'block';
  el.textContent = String(msg);
}
window.onerror = (m,s,l,_,e) => showErr(`${m}\n@ ${s}:${l}\n${e?.stack||''}`);
window.addEventListener('unhandledrejection', e => showErr(String(e.reason)));

// ── Three.js setup ───────────────────────────────────────────────────────────
const canvas = document.getElementById('c');
const wrap = document.getElementById('canvas-wrap');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.35;
renderer.outputColorSpace = THREE.SRGBColorSpace;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x08090e);
const camera = new THREE.PerspectiveCamera(48, 1, 0.0001, 500);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.07;

new ResizeObserver(() => {
  const w = wrap.clientWidth, h = wrap.clientHeight;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h, false);
}).observe(wrap);
setTimeout(() => {
  const w = wrap.clientWidth, h = wrap.clientHeight;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h, false);
}, 0);

// ── Material presets ─────────────────────────────────────────────────────────
function getMaterial(meta) {
  const t = (meta.material || 'brushed_metal').replace(/-/g, '_');
  const c = new THREE.Color(meta.color || '#7a8fa6');
  const presets = {
    brushed_metal:  { metalness:.88, roughness:.18 },
    polished_metal: { metalness:.96, roughness:.04 },
    chrome:         { metalness:.99, roughness:.02 },
    cast_iron:      { metalness:.7,  roughness:.65 },
    rubber:         { metalness:0,   roughness:.97 },
    hydraulic_fluid:{ metalness:0,   roughness:0,  transparent:true, opacity:.42 },
    glass:          { metalness:0,   roughness:0,  transparent:true, opacity:.25 },
    brass:          { metalness:.88, roughness:.22 },
    anodized:       { metalness:.62, roughness:.32 },
    ceramic:        { metalness:0,   roughness:.42 },
    plastic:        { metalness:0,   roughness:.75 },
    copper:         { metalness:.92, roughness:.28 },
    carbon_fiber:   { metalness:.2,  roughness:.28 },
    titanium:       { metalness:.9,  roughness:.15 },
    wood:           { metalness:0,   roughness:.88 },
  };
  const p = presets[t] || presets.brushed_metal;
  const overrides = {};
  if (meta.metalness != null) overrides.metalness = meta.metalness;
  if (meta.roughness != null) overrides.roughness = meta.roughness;
  if (meta.opacity   != null) { overrides.transparent = true; overrides.opacity = meta.opacity; }
  const props = { color: c, side: THREE.DoubleSide, ...p, ...overrides };
  if (t === 'glass') {
    return new THREE.MeshPhysicalMaterial({ ...props, transmission: 0.88, thickness: 0.3 });
  }
  return new THREE.MeshStandardMaterial(props);
}

// ── JSCAD → Three.js BufferGeometry ─────────────────────────────────────────
// @jscad/modeling returns geom3 objects whose .polygons array contains Poly3s.
// Each Poly3 has .vertices = [[x,y,z], [x,y,z], ...].
// We fan-triangulate and compute vertex normals.
function jscadToThree(geom) {
  if (!geom) { console.warn('null geom'); return new THREE.BufferGeometry(); }
  // Support arrays of geometries (union returns single geom, but just in case)
  const polys = Array.isArray(geom) ? geom.flatMap(g => g.polygons || []) : (geom.polygons || []);
  if (!polys.length) { console.warn('no polygons'); return new THREE.BufferGeometry(); }
  const pos = [];
  for (const poly of polys) {
    const verts = poly.vertices;
    if (!verts || verts.length < 3) continue;
    for (let i = 1; i < verts.length - 1; i++) {
      const v0=verts[0], v1=verts[i], v2=verts[i+1];
      pos.push(v0[0],v0[1],v0[2], v1[0],v1[1],v1[2], v2[0],v2[1],v2[2]);
    }
  }
  if (!pos.length) return new THREE.BufferGeometry();
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  geo.computeVertexNormals();
  return geo;
}

// ── Labels ───────────────────────────────────────────────────────────────────
const _lbls = [];
function addLabel(text, pos, offset) {
  const el = document.createElement('div');
  el.className = 'lbl';
  el.textContent = text;
  document.getElementById('lbl-layer').appendChild(el);
  const o = offset || [0,0,0];
  _lbls.push({ el, pos: new THREE.Vector3(pos[0]+o[0], pos[1]+o[1], pos[2]+o[2]) });
}
function updateLabels() {
  const ww = wrap.clientWidth, wh = wrap.clientHeight;
  for (const lb of _lbls) {
    const v = lb.pos.clone().project(camera);
    if (v.z > 1) { lb.el.style.display = 'none'; continue; }
    lb.el.style.display = 'block';
    lb.el.style.left = ((v.x * .5 + .5) * ww) + 'px';
    lb.el.style.top  = ((-.5 * v.y + .5) * wh - 10) + 'px';
  }
}

// ── Param UI ─────────────────────────────────────────────────────────────────
const P = {};
function buildUI(params) {
  const c = document.getElementById('params');
  c.innerHTML = '';
  for (const p of (params || [])) {
    P[p.key] = p.default ?? p.min ?? 0;
    const w = document.createElement('div'); w.className = 'pg';
    const l = document.createElement('div'); l.className = 'pl';
    const n = document.createElement('span');
    n.textContent = (p.label || p.key) + (p.unit ? ` (${p.unit})` : '');
    const v = document.createElement('span'); v.className = 'pv'; v.id = 'pv_' + p.key;
    v.textContent = P[p.key].toFixed(p.decimals ?? 2);
    l.append(n, v);
    const s = document.createElement('input'); s.type = 'range';
    s.min = p.min ?? 0; s.max = p.max ?? 1;
    s.step = p.step ?? ((p.max - p.min) / 100) || 0.01;
    s.value = P[p.key];
    s.oninput = () => {
      P[p.key] = parseFloat(s.value);
      document.getElementById('pv_' + p.key).textContent = P[p.key].toFixed(p.decimals ?? 2);
      if (typeof onParam === 'function') try { onParam(p.key, P[p.key], P, window._meshMap || {}); } catch(e) { console.warn(e); }
    };
    w.append(l, s); c.append(w);
  }
}
function buildLegend(items) {
  const c = document.getElementById('legend'); c.innerHTML = '';
  for (const it of (items || [])) {
    const r = document.createElement('div'); r.className = 'leg';
    const d = document.createElement('div'); d.className = 'leg-c'; d.style.background = it.color || '#888';
    const t = document.createElement('span'); t.textContent = it.label || '';
    r.append(d, t); c.append(r);
  }
}

// ── Mesh animation helper ────────────────────────────────────────────────────
function animateMesh(mesh, anim, t, dt) {
  if (!anim) return;
  if (anim.type === 'translate_param') {
    const v = Math.max(0, Math.min(1, P[anim.param] ?? 0.5));
    mesh.position[anim.axis || 'x'] = (anim.from ?? -0.1) + v * ((anim.to ?? 0.1) - (anim.from ?? -0.1));
  } else if (anim.type === 'oscillate') {
    mesh.position[anim.axis || 'y'] = (anim.center ?? 0) + (anim.amplitude ?? 0.05) * Math.sin(t * (anim.freq ?? 1) * Math.PI * 2);
  } else if (anim.type === 'rotate_continuous') {
    const rpm = P[anim.param_speed ?? 'rpm'] ?? (anim.rpm ?? 60);
    mesh.rotation[anim.axis || 'y'] += dt * rpm / 60 * Math.PI * 2;
  } else if (anim.type === 'rotate_param') {
    const v = P[anim.param] ?? 0.5;
    mesh.rotation[anim.axis || 'z'] = THREE.MathUtils.degToRad((anim.min_deg ?? -45) + v * ((anim.max_deg ?? 45) - (anim.min_deg ?? -45)));
  } else if (anim.type === 'scale_param') {
    const v = P[anim.param] ?? 0.5;
    mesh.scale[anim.axis || 'x'] = (anim.from ?? 0.1) + v * ((anim.to ?? 1) - (anim.from ?? 0.1));
  }
}

// ── Lighting ─────────────────────────────────────────────────────────────────
function setupLighting() {
  const sun = new THREE.DirectionalLight(0xfff8e0, 2.6);
  sun.position.set(5, 8, 4);
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  sun.shadow.camera.near = 0.01; sun.shadow.camera.far = 50;
  sun.shadow.camera.left = -3; sun.shadow.camera.right = 3;
  sun.shadow.camera.top = 3; sun.shadow.camera.bottom = -3;
  sun.shadow.bias = -0.001;
  scene.add(sun);
  scene.add(new THREE.HemisphereLight(0x1a2f4a, 0x080c10, 0.9));
  const rim = new THREE.PointLight(0x3a7dff, 1.4, 30);
  rim.position.set(-4, 3, -2);
  scene.add(rim);
}

// ── Ground ───────────────────────────────────────────────────────────────────
function addGround(y) {
  y = y ?? -0.30;
  const g = new THREE.Mesh(
    new THREE.PlaneGeometry(10, 10),
    new THREE.MeshStandardMaterial({ color: 0x0c1016, roughness: .95 })
  );
  g.rotation.x = -Math.PI / 2; g.position.y = y; g.receiveShadow = true;
  scene.add(g);
  const grid = new THREE.GridHelper(8, 32, 0x1a2535, 0x0f1828);
  grid.position.y = y + 0.001;
  scene.add(grid);
}

// ════════════════════════════════════════════════════════════════════════════
// GENERATED JSCAD MODEL CODE (injected by backend)
// ════════════════════════════════════════════════════════════════════════════
${GENERATED_CODE}
// ════════════════════════════════════════════════════════════════════════════

// ── Main initialization ───────────────────────────────────────────────────────
async function init() {
  try {
    // Load @jscad/modeling from esm.sh (converts npm CJS package to ES module)
    document.getElementById('ltxt').innerHTML =
      'Loading JSCAD modeling engine…<br/><span style="color:#3d4a5a;font-size:9px">(OpenJSCAD — first load ~2s)</span>';
    let jscadModule;
    try {
      jscadModule = await import('https://esm.sh/@jscad/modeling@2');
    } catch (e) {
      showErr('Failed to load @jscad/modeling from esm.sh.\nCheck your internet connection.\n\n' + e);
      return;
    }
    // esm.sh may wrap in a .default object
    const jscad = jscadModule.default || jscadModule;

    document.getElementById('ltxt').textContent = 'Building CSG geometry…';

    // Build param UI
    if (typeof PARAMS_META !== 'undefined') buildUI(PARAMS_META);

    // Set header text
    if (typeof MODEL_NAME !== 'undefined') {
      document.getElementById('sb-obj').textContent =
        MODEL_NAME + (typeof MODEL_DESC !== 'undefined' ? ' — ' + MODEL_DESC : '');
    }

    // Build all geometry via JSCAD CSG
    const rawGeoms = buildParts(P, jscad);

    const meshMap = window._meshMap = {};
    const animParts = [];
    const allMeta = typeof PARTS_META !== 'undefined' ? PARTS_META : [];

    for (const [id, result] of Object.entries(rawGeoms)) {
      const fromMeta = allMeta.find(p => p.id === id) || {};

      // Accept: raw JSCAD geom, or { geom, ...inlineMeta }
      let jscadGeom, partMeta;
      if (result && result.polygons) {
        jscadGeom = result;
        partMeta = fromMeta;
      } else if (result && result.geom && result.geom.polygons) {
        jscadGeom = result.geom;
        const { geom: _g, ...rest } = result;
        partMeta = { ...fromMeta, ...rest };
      } else {
        console.warn('Unknown geometry for part:', id, result);
        continue;
      }

      const threeGeo = jscadToThree(jscadGeom);
      if (threeGeo.attributes.position?.count === 0) continue;

      const mat = getMaterial(partMeta);
      const mesh = new THREE.Mesh(threeGeo, mat);
      mesh.castShadow = true;
      mesh.receiveShadow = true;

      const p = partMeta.position || [0, 0, 0];
      mesh.position.set(p[0], p[1], p[2]);
      const r = partMeta.rotation || [0, 0, 0];
      mesh.rotation.set(r[0], r[1], r[2]);

      scene.add(mesh);
      meshMap[id] = mesh;

      if (partMeta.label) {
        const off = partMeta.label_offset || [0, 0.08, 0];
        addLabel(partMeta.label, [p[0], p[1], p[2]], off);
      }
      if (partMeta.animate) animParts.push({ mesh, anim: partMeta.animate });
    }

    // Camera
    if (typeof CAMERA_SETUP === 'function') {
      CAMERA_SETUP(camera, controls);
    } else {
      camera.position.set(0.28, 0.18, 0.60);
      controls.target.set(0, 0, 0);
    }
    controls.update();

    // Lighting + ground
    setupLighting();
    addGround(typeof GROUND_Y !== 'undefined' ? GROUND_Y : undefined);

    // Legend
    buildLegend(allMeta.filter(p => p.name).map(p => ({ color: p.color || '#888', label: p.name })));

    // Done loading
    document.getElementById('loading').style.display = 'none';

    // Render loop
    const clock = new THREE.Clock();
    let fc = 0;
    (function loop() {
      requestAnimationFrame(loop);
      const dt = Math.min(clock.getDelta(), 0.05);
      const t = clock.getElapsedTime();
      fc++;
      controls.update();
      for (const { mesh, anim } of animParts) animateMesh(mesh, anim, t, dt);
      if (typeof tick === 'function') try { tick(t, dt, P, meshMap); } catch (e) { console.error(e); }
      renderer.render(scene, camera);
      updateLabels();
      if (fc % 90 === 0) document.getElementById('fps').textContent = Math.round(1 / (dt || 0.016)) + ' fps';
    })();

  } catch (e) {
    showErr('Init error:\n' + e + '\n' + (e.stack || ''));
  }
}

init();
</script>
</body></html>"""


# ─── LLM prompt ──────────────────────────────────────────────────────────────
JSCAD_PROMPT = '''You are an expert mechanical engineer and 3D modeler using OpenJSCAD (@jscad/modeling v2).
Generate a complete, accurate 3D model for: "{topic}"
Context: {context}

═══ THE JSCAD API (all units in METERS) ═══
The `jscad` argument to buildParts() contains the entire @jscad/modeling library:

  const {{ primitives, booleans, transforms, extrusions }} = jscad
  const {{ cylinder, sphere, cuboid, torus, polygon, circle }} = primitives
  const {{ union, subtract, intersect }} = booleans
  const {{ translate, rotate, scale, mirror }} = transforms
  const {{ extrudeLinear, extrudeRotate }} = extrusions

Primitives — all centered at origin:
  cylinder({{ radius: r, height: h, segments: 64 }})      // along Y-axis by default
  sphere({{ radius: r, segments: 32 }})
  cuboid({{ size: [w, h, d] }})
  torus({{ outerRadius: R, innerRadius: r }})              // ring in XZ plane, hole along Y
  polygon({{ points: [[x,y],...] }})                       // 2D
  circle({{ radius: r, segments: 32 }})                    // 2D

Boolean CSG — THIS IS THE CRITICAL ADVANTAGE OVER THREE.JS:
  subtract(base, ...tools)    → drill holes, create bores, machine grooves
  union(a, b, ...)            → merge parts
  intersect(a, b)             → keep only overlap

Transforms:
  translate([dx,dy,dz], geom)
  rotate([rx,ry,rz], geom)    // RADIANS. 90°=Math.PI/2, 180°=Math.PI
  scale([sx,sy,sz], geom)

To orient a cylinder along X-axis: rotate([0,0,Math.PI/2], cylinder({{...}}))
To orient a cylinder along Z-axis: rotate([Math.PI/2,0,0], cylinder({{...}}))

═══ EXAMPLES ═══
// Hollow barrel (cylinder bore — NEVER use solid cylinder for this):
const barrel = subtract(
  rotate([0,0,Math.PI/2], cylinder({{ radius:0.053, height:0.40, segments:64 }})),
  rotate([0,0,Math.PI/2], cylinder({{ radius:0.041, height:0.41, segments:64 }})) // slightly longer
)

// Piston with O-ring grooves:
const piston_body = rotate([0,0,Math.PI/2], cylinder({{ radius:0.0398, height:0.028, segments:48 }}))
const groove1 = translate([0.007,0,0],  torus({{ outerRadius:0.038, innerRadius:0.0025 }}))
const groove2 = translate([-0.007,0,0], torus({{ outerRadius:0.038, innerRadius:0.0025 }}))
const piston = subtract(piston_body, groove1, groove2)

// Extruded cross-section profile (for complex swept shapes):
const profile = polygon({{ points: [[0.04,-0.2],[0.053,-0.19],[0.053,0.19],[0.04,0.2]] }})
const shell = extrudeRotate({{ segments:64 }}, profile)

═══ WHAT YOU MUST DEFINE ═══

const MODEL_NAME = "Exact Technical Name";          // shown in header
const MODEL_DESC = "One-line function description"; // shown in subheader

const PARTS_META = [
  {{
    id: "part_id",            // MUST match key returned by buildParts()
    name: "Display Name",     // shown in legend
    material: "brushed_metal",// preset: brushed_metal|polished_metal|chrome|cast_iron|rubber|
                              //         hydraulic_fluid|glass|brass|anodized|ceramic|plastic|
                              //         copper|carbon_fiber|titanium|wood
    color: "#7a8fa6",         // hex color
    metalness: 0.88,          // optional override
    roughness: 0.18,          // optional override
    opacity: 0.4,             // optional, auto-enables transparency
    position: [x, y, z],     // initial world position in meters
    rotation: [rx, ry, rz],  // initial rotation in radians (applied AFTER JSCAD geometry rotation)
    label: "Part Name",       // null = no label
    label_offset: [0,0.08,0], // offset from position for label placement
    animate: {{               // null = no animation
      type: "translate_param",
      axis: "x",
      param: "stroke",        // key from PARAMS_META
      from: -0.12,            // position when param=0
      to:    0.10,            // position when param=1
    }},
    // Other animate types:
    // {{ type:"oscillate", axis:"y", center:0, amplitude:0.05, freq:1.5 }}
    // {{ type:"rotate_continuous", axis:"y", rpm:300, param_speed:"rpm" }}
    // {{ type:"rotate_param", axis:"z", param:"angle", min_deg:-30, max_deg:30 }}
    // {{ type:"scale_param", axis:"x", param:"extension", from:0.1, to:1.0 }}
  }}
];

const PARAMS_META = [
  {{ key:"stroke", label:"Stroke", min:0, max:1, default:0.3, unit:"", decimals:2 }},
  {{ key:"pressure", label:"Pressure", min:50, max:350, default:180, unit:"bar", decimals:0 }},
];

function buildParts(P, jscad) {{
  const {{ primitives, booleans, transforms, extrusions }} = jscad;
  // ... build geometry using CSG ...
  return {{
    barrel: barrel_geom,    // raw JSCAD geometry
    piston: piston_geom,    // keys must match PARTS_META ids
  }};
}}

// Optional: complex per-frame animation (runs every frame)
function tick(t, dt, P, meshMap) {{
  // t = elapsed seconds, dt = delta, P = current param values, meshMap = {{ id: THREE.Mesh }}
}}

// Optional: called when a param slider changes
function onParam(key, val, P, meshMap) {{ }}

// Optional: camera setup
function CAMERA_SETUP(camera, controls) {{
  camera.position.set(0.3, 0.2, 0.6);
  controls.target.set(0, 0, 0);
}}

const GROUND_Y = -0.28; // Y position of ground plane

═══ CRITICAL RULES ═══
1. HOLLOW PARTS: Always use subtract() for bores, cavities, holes. A hydraulic barrel IS a
   subtract(outer_cylinder, inner_bore). A gear blank has subtracted tooth gaps. A pipe is hollow.
   NEVER represent a tube as a solid cylinder — that is wrong.

2. DIMENSIONS: Use real engineering measurements in METERS.
   - Hydraulic cylinder: bore=80mm=0.08, barrel OD=106mm=0.106, stroke=200-300mm
   - Bearing: OD=80mm, bore=40mm, width=18mm
   - Gear (module 2, 20 teeth): PCD=40mm, OD=44mm, bore=12mm
   - Engine cylinder: bore=86mm, stroke=86mm, wall thickness=8mm

3. SINGLE FOCUSED MODEL: 6-16 parts representing ONE mechanism accurately.
   Parts must have correct spatial relationships and fit together.

4. TOOL OVERLAP: When subtracting, make the cutting tool 1-2% longer than the base to avoid
   zero-thickness artifacts: subtract(cyl(h:0.40), cyl(h:0.41))

5. JSCAD COORDINATE CONVENTION: Y is up. Cylinder/torus default along Y.
   For X-axis mechanisms: rotate([0,0,Math.PI/2], ...) to lay cylinder on X.

6. ANIMATION: Link main moving part to 'stroke' (0-1 range). Parts that move together
   (piston + rod + seals) should all have the same animation type with offset `from`/`to` values.

7. O-RINGS / SEALS: Use torus() for visible O-rings. Use subtract(piston, torus) for grooves.
   The torus() is in XZ plane (ring around Y). When the piston lies on X-axis, the groove
   is already correct (torus ring encircles the X-axis cylinder).

Output ONLY JavaScript code. No markdown fences. No explanations.
Define MODEL_NAME, MODEL_DESC, PARTS_META, PARAMS_META, buildParts().
Optionally define tick(), onParam(), CAMERA_SETUP(), GROUND_Y.
'''


# ─── Request / Response models ────────────────────────────────────────────────
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

    try:
        resp = client.chat.completions.create(
            model=settings.llm_model,
            messages=[{
                "role": "user",
                "content": JSCAD_PROMPT.format(topic=topic, context=context)
            }],
            temperature=0.15,
            max_tokens=4096,
        )
        raw = resp.choices[0].message.content or ""
        # Strip any markdown fences the model adds
        raw = re.sub(r"```(?:javascript|js)?\s*", "", raw)
        raw = re.sub(r"```\s*$", "", raw, flags=re.MULTILINE).strip()

        # Extract object name from generated code for the response
        name_match = re.search(r'MODEL_NAME\s*=\s*["\']([^"\']+)["\']', raw)
        object_name = name_match.group(1) if name_match else topic

        html = HTML_3D_TEMPLATE.replace("${GENERATED_CODE}", raw)
        return Visual3DResponse(html=html, topic=topic, object_name=object_name)

    except Exception as exc:
        logger.exception("3D generation failed: %s", exc)
        html = HTML_3D_TEMPLATE.replace("${GENERATED_CODE}", _fallback_jscad(topic))
        return Visual3DResponse(html=html, topic=topic, object_name=topic, error=str(exc))


# ─── Fallback: hardcoded JSCAD hydraulic actuator ────────────────────────────
def _fallback_jscad(topic: str) -> str:
    """
    Geometrically accurate hydraulic linear actuator using real CSG operations.
    All dimensions in meters, matching a typical 80mm bore x 300mm stroke actuator.
    """
    desc = topic.replace("'", "\\'")
    return f"""
const MODEL_NAME = 'Hydraulic Linear Actuator';
const MODEL_DESC = '{desc}';
const GROUND_Y = -0.28;

const PARTS_META = [
  // Static structural parts
  {{ id:'barrel',    name:'Cylinder Barrel',   material:'cast_iron',      color:'#3d4757' }},
  {{ id:'cap_blind', name:'Blind End Cap',      material:'brushed_metal',  color:'#6a7a8a',
     label:'Blind End', label_offset:[0,0.08,0] }},
  {{ id:'cap_rod',   name:'Rod End Cap',        material:'brushed_metal',  color:'#6a7a8a',
     label:'Rod End',   label_offset:[0,0.08,0] }},
  // Moving parts — all driven by 'stroke' slider
  {{ id:'piston',   name:'Piston',             material:'anodized',       color:'#2a5298',
     label:'Piston', label_offset:[0,0.07,0],
     animate:{{ type:'translate_param', axis:'x', param:'stroke', from:-0.11, to:0.09 }} }},
  {{ id:'rod',      name:'Piston Rod',         material:'chrome',         color:'#ccd8e8',
     label:'Piston Rod (Ø40mm)', label_offset:[0.14,0.06,0],
     animate:{{ type:'translate_param', axis:'x', param:'stroke', from:-0.11, to:0.09 }} }},
  {{ id:'seal_1',   name:'Piston Seal A',      material:'rubber',         color:'#0d0d0d',
     animate:{{ type:'translate_param', axis:'x', param:'stroke', from:-0.117, to:0.083 }} }},
  {{ id:'seal_2',   name:'Piston Seal B',      material:'rubber',         color:'#0d0d0d',
     animate:{{ type:'translate_param', axis:'x', param:'stroke', from:-0.103, to:0.097 }} }},
  {{ id:'rod_seal', name:'Rod Wiper Seal',     material:'rubber',         color:'#111' }},
  // Ports
  {{ id:'port_a',   name:'Port A (Pressure)',  material:'brass',          color:'#c08030',
     label:'Port A', label_offset:[0,0.04,0] }},
  {{ id:'port_b',   name:'Port B (Return)',    material:'brass',          color:'#c08030',
     label:'Port B', label_offset:[0,0.04,0] }},
  // Fluid (transparent)
  {{ id:'fluid',    name:'Hydraulic Fluid',    material:'hydraulic_fluid',color:'#c07820', opacity:0.38,
     animate:{{ type:'translate_param', axis:'x', param:'stroke', from:-0.11, to:0.09 }} }},
];

const PARAMS_META = [
  {{ key:'stroke',   label:'Stroke Position', min:0,   max:1,   default:0.3, unit:'',    decimals:2 }},
  {{ key:'speed',    label:'Cycle Speed',     min:0.1, max:4,   default:1,   unit:'×',   decimals:1 }},
  {{ key:'pressure', label:'System Pressure', min:50,  max:350, default:180, unit:'bar', decimals:0 }},
];

function buildParts(P, jscad) {{
  const {{ primitives, booleans, transforms }} = jscad;
  const {{ cylinder, torus }}             = primitives;
  const {{ subtract }}                    = booleans;
  const {{ translate, rotate }}           = transforms;
  const R90z = [0, 0, Math.PI / 2];       // rotate to lie along X-axis
  const cxz  = g => rotate(R90z, g);      // shorthand

  // ── Cylinder barrel: hollow cast iron tube, 400 mm long ──────────────
  // Bore = 82 mm diameter (r=41mm), OD = 106 mm (r=53mm)
  const barrel = subtract(
    cxz(cylinder({{ radius:0.053, height:0.400, segments:72 }})),
    cxz(cylinder({{ radius:0.041, height:0.408, segments:72 }}))   // slightly longer → clean ends
  );

  // ── Blind end cap: solid disk with central port hole ──────────────────
  const cap_blind = translate([-0.220, 0, 0], subtract(
    cxz(cylinder({{ radius:0.053, height:0.040, segments:48 }})),
    cxz(cylinder({{ radius:0.008, height:0.041, segments:16 }}))   // port bore
  ));

  // ── Rod end cap: disk with larger rod bore + rod-seal groove ──────────
  const cap_rod = translate([0.220, 0, 0], subtract(
    cxz(cylinder({{ radius:0.053, height:0.040, segments:48 }})),
    cxz(cylinder({{ radius:0.022, height:0.041, segments:32 }})),  // rod bore (Ø44mm)
    translate([0, 0, 0], torus({{ outerRadius:0.025, innerRadius:0.003 }}))  // wiper groove
  ));

  // ── Piston: disk with two O-ring grooves machined in ─────────────────
  const piston_body = cxz(cylinder({{ radius:0.0398, height:0.030, segments:52 }}));
  const groove_a    = translate([ 0.007, 0, 0], torus({{ outerRadius:0.0388, innerRadius:0.0025 }}));
  const groove_b    = translate([-0.007, 0, 0], torus({{ outerRadius:0.0388, innerRadius:0.0025 }}));
  const piston      = subtract(piston_body, groove_a, groove_b);

  // ── Piston rod: polished chrome steel, Ø40mm, 320 mm long ────────────
  // Geometry centered at origin; PARTS_META animation offsets place it correctly.
  // Rod extends from piston center (+0 m) to rod end (+0.32 m), so center = +0.16 m.
  const rod = translate([0.160, 0, 0],
    cxz(cylinder({{ radius:0.020, height:0.320, segments:36 }}))
  );

  // ── O-ring seals (visible, sitting in grooves) ────────────────────────
  // torus() creates a ring in XZ plane (encircles Y-axis).
  // When the piston lies on X, the ring correctly encircles it.
  const seal_1 = translate([ 0.007, 0, 0], torus({{ outerRadius:0.040, innerRadius:0.0022 }}));
  const seal_2 = translate([-0.007, 0, 0], torus({{ outerRadius:0.040, innerRadius:0.0022 }}));

  // ── Rod wiper seal (fixed at rod end cap) ─────────────────────────────
  const rod_seal = translate([0.218, 0, 0], torus({{ outerRadius:0.023, innerRadius:0.0022 }}));

  // ── Hydraulic ports (brass fittings extending upward from caps) ───────
  const port_a = translate([-0.200, 0.054, 0],
    cylinder({{ radius:0.0085, height:0.020, segments:16 }})
  );
  const port_b = translate([0.120, 0.054, 0],
    cylinder({{ radius:0.0085, height:0.020, segments:16 }})
  );

  // ── Fluid volume: fills the blind-end chamber (pressure side) ─────────
  // This is a translucent cylinder that represents fluid volume.
  // tick() will scale it dynamically with stroke position.
  const fluid = translate([-0.110, 0, 0],
    cxz(cylinder({{ radius:0.0405, height:0.200, segments:32 }}))
  );

  return {{ barrel, cap_blind, cap_rod, piston, rod, seal_1, seal_2, rod_seal, port_a, port_b, fluid }};
}}

function CAMERA_SETUP(camera, controls) {{
  camera.position.set(0.35, 0.22, 0.60);
  controls.target.set(0.05, 0, 0);
}}

// ── Auto-cycle + dynamic fluid volume ────────────────────────────────────────
let _dir = 1, _auto = true, _pauseTimer = 0;

function tick(t, dt, P, meshMap) {{
  // Auto-cycle stroke when user isn't adjusting
  if (_auto) {{
    P.stroke += dt * (P.speed || 1) * 0.38 * _dir;
    if (P.stroke >= 0.96) {{ _dir = -1; P.stroke = 0.96; }}
    if (P.stroke <= 0.04) {{ _dir =  1; P.stroke = 0.04; }}
    // Sync slider display
    const sv = document.getElementById('pv_stroke');
    if (sv) sv.textContent = P.stroke.toFixed(2);
    for (const s of document.querySelectorAll('input[type=range]')) {{
      if (+s.min === 0 && +s.max === 1) s.value = P.stroke;
    }}
  }}

  // Scale fluid cylinder to represent actual fluid volume in pressure chamber.
  // As piston extends (stroke→1), pressure-side fluid shrinks, rod-side grows.
  const fluid = meshMap['fluid'];
  if (fluid) {{
    const s = P.stroke;
    // Scale x to represent fluid length (piston travel 200mm, fluid goes from 200mm down to ~20mm)
    const fluidLen = 0.02 + (1 - s) * 0.18;   // 200mm at stroke=0, 20mm at stroke=1
    fluid.scale.x = fluidLen / 0.200;          // normalize to geometry height
    // Reposition so left face stays at blind cap
    fluid.position.x = -0.220 + fluidLen / 2 + 0.020;
  }}
}}

function onParam(key, val, P, meshMap) {{
  if (key === 'stroke') {{
    _auto = false;
    clearTimeout(_pauseTimer);
    _pauseTimer = setTimeout(() => {{ _auto = true; }}, 4000);
  }}
}}
"""
