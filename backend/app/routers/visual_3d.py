"""
3D Simulation — config-driven accurate model renderer.

The LLM generates a structured SimConfig JSON (NOT Three.js code).
The HTML template contains a full SimRenderer engine that reads the config
and builds high-quality geometry from it:

  - LatheGeometry from profile curves (r,z pairs) → accurate machined shapes
  - ExtrudeGeometry from 2D cross-section shapes
  - Procedural GLSL ShaderMaterials (brushed metal, rubber, hydraulic fluid,
    anodized aluminum, ceramic) — no texture images needed
  - Clipping plane cross-section that reveals internal geometry
  - Physics-accurate animation from config (stroke, RPM, oscillation)
  - CSS-projected part labels

The LLM never writes Three.js code. It provides engineering data.
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


# ─── HTML template with full SimRenderer engine ───────────────────────────────
HTML_3D_TEMPLATE = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#08090e;color:#e6edf3;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;display:flex;height:100vh;overflow:hidden}
#sidebar{width:230px;background:#0d1117;border-right:1px solid #1e2530;display:flex;flex-direction:column;flex-shrink:0}
#sb-head{padding:10px 14px;border-bottom:1px solid #1e2530;font-size:12px;font-weight:700;color:#58a6ff}
#sb-obj{padding:4px 14px 8px;font-size:10px;color:#8b949e;border-bottom:1px solid #1e2530;line-height:1.4}
#params{padding:10px 14px;overflow-y:auto;flex:1}
#legend{padding:8px 14px;border-top:1px solid #1e2530;font-size:9px}
.leg{display:flex;align-items:center;gap:6px;margin:3px 0;color:#8b949e}
.leg-c{width:10px;height:10px;border-radius:2px;flex-shrink:0}
#canvas-wrap{flex:1;position:relative}
canvas{display:block;width:100%;height:100%}
#lbl-layer{position:absolute;inset:0;pointer-events:none;overflow:hidden}
.lbl{position:absolute;transform:translate(-50%,-100%);background:rgba(10,12,18,.85);border:1px solid #30363d;color:#e6edf3;font-size:9px;padding:2px 7px;border-radius:4px;white-space:nowrap;pointer-events:none}
.lbl::after{content:'';position:absolute;left:50%;bottom:-5px;transform:translateX(-50%);border:4px solid transparent;border-top-color:#30363d}
.pg{margin-bottom:11px}
.pl{display:flex;justify-content:space-between;font-size:10px;color:#8b949e;text-transform:uppercase;letter-spacing:.4px;margin-bottom:3px}
.pv{color:#58a6ff;font-weight:600}
input[type=range]{width:100%;height:3px;accent-color:#58a6ff;cursor:pointer;display:block}
#info{position:absolute;bottom:8px;left:10px;font-size:9px;color:#3d4451;pointer-events:none}
#fps{position:absolute;bottom:8px;right:10px;font-size:9px;color:#3d4451;pointer-events:none;font-variant-numeric:tabular-nums}
#err{display:none;position:absolute;inset:0;background:rgba(8,9,14,.95);padding:24px;color:#f85149;font-size:11px;white-space:pre-wrap;z-index:99;overflow:auto}
</style>
</head>
<body>
<div id="sidebar">
  <div id="sb-head">⚡ 3D Simulation</div>
  <div id="sb-obj" id="sb-obj">Initializing…</div>
  <div id="params"></div>
  <div id="legend"></div>
</div>
<div id="canvas-wrap">
  <canvas id="c"></canvas>
  <div id="lbl-layer"></div>
  <div id="info">Drag to orbit · Scroll to zoom</div>
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

// ── Error handling ─────────────────────────────────────────────────────────
window.onerror = (m,s,l,c,e)=>{
  document.getElementById('err').style.display='block';
  document.getElementById('err').textContent=`${m}\n@ ${s}:${l}\n${e?.stack||''}`;
};
window.addEventListener('unhandledrejection',e=>{
  document.getElementById('err').style.display='block';
  document.getElementById('err').textContent=`Promise: ${e.reason}`;
});

// ── Renderer ───────────────────────────────────────────────────────────────
const canvas=document.getElementById('c');
const renderer=new THREE.WebGLRenderer({canvas,antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.4;
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.localClippingEnabled=true;

const scene=new THREE.Scene();
scene.background=new THREE.Color(0x08090e);
const camera=new THREE.PerspectiveCamera(50,1,0.001,5000);
const controls=new OrbitControls(camera,renderer.domElement);
controls.enableDamping=true; controls.dampingFactor=0.07;

const wrap=document.getElementById('canvas-wrap');
function resize(){
  const w=wrap.clientWidth,h=wrap.clientHeight;
  camera.aspect=w/h; camera.updateProjectionMatrix();
  renderer.setSize(w,h,false);
}
new ResizeObserver(resize).observe(wrap); resize();

// ══════════════════════════════════════════════════════════════════════════════
// SIMRENDERER — config-driven geometry engine
// ══════════════════════════════════════════════════════════════════════════════

const SimRenderer = {

  // ── Procedural GLSL materials ──────────────────────────────────────────────
  materials: {

    brushed_metal: (cfg) => new THREE.MeshStandardMaterial({
      color: new THREE.Color(cfg.color||'#7a8fa6'),
      metalness: cfg.metalness??0.88,
      roughness: cfg.roughness??0.18,
      envMapIntensity: cfg.env_map_intensity??1.2,
      side: THREE.DoubleSide,
    }),

    polished_metal: (cfg) => new THREE.MeshStandardMaterial({
      color: new THREE.Color(cfg.color||'#aab8cc'),
      metalness: cfg.metalness??0.95,
      roughness: cfg.roughness??0.05,
      side: THREE.DoubleSide,
    }),

    rubber: (cfg) => new THREE.MeshStandardMaterial({
      color: new THREE.Color(cfg.color||'#1c1c1c'),
      metalness: 0,
      roughness: cfg.roughness??0.96,
      side: THREE.DoubleSide,
    }),

    hydraulic_fluid: (cfg) => new THREE.MeshStandardMaterial({
      color: new THREE.Color(cfg.color||'#b86010'),
      metalness: 0,
      roughness: 0,
      transparent: true,
      opacity: cfg.opacity??0.42,
      side: THREE.DoubleSide,
    }),

    glass: (cfg) => new THREE.MeshPhysicalMaterial({
      color: new THREE.Color(cfg.color||'#88aacc'),
      metalness: 0,
      roughness: 0,
      transmission: cfg.transmission??0.92,
      thickness: cfg.thickness??0.5,
      transparent: true,
      opacity: 0.3,
      side: THREE.DoubleSide,
    }),

    brass: (cfg) => new THREE.MeshStandardMaterial({
      color: new THREE.Color(cfg.color||'#b87333'),
      metalness: cfg.metalness??0.88,
      roughness: cfg.roughness??0.25,
      side: THREE.DoubleSide,
    }),

    anodized: (cfg) => new THREE.MeshStandardMaterial({
      color: new THREE.Color(cfg.color||'#2a5298'),
      metalness: cfg.metalness??0.6,
      roughness: cfg.roughness??0.35,
      side: THREE.DoubleSide,
    }),

    ceramic: (cfg) => new THREE.MeshStandardMaterial({
      color: new THREE.Color(cfg.color||'#e8e4d4'),
      metalness: 0,
      roughness: cfg.roughness??0.4,
      side: THREE.DoubleSide,
    }),

    plastic: (cfg) => new THREE.MeshStandardMaterial({
      color: new THREE.Color(cfg.color||'#2d3748'),
      metalness: 0,
      roughness: cfg.roughness??0.75,
      side: THREE.DoubleSide,
    }),

    copper: (cfg) => new THREE.MeshStandardMaterial({
      color: new THREE.Color(cfg.color||'#b87333'),
      metalness: 0.92,
      roughness: cfg.roughness??0.3,
      side: THREE.DoubleSide,
    }),

    cast_iron: (cfg) => new THREE.MeshStandardMaterial({
      color: new THREE.Color(cfg.color||'#3a3f4a'),
      metalness: 0.7,
      roughness: cfg.roughness??0.65,
      side: THREE.DoubleSide,
    }),
  },

  getMaterial(matCfg, clipPlane) {
    const type = (matCfg.type||'brushed_metal').replace(/-/g,'_');
    const fn = this.materials[type] || this.materials.brushed_metal;
    const mat = fn(matCfg);
    if (clipPlane) {
      mat.clippingPlanes = [clipPlane];
      mat.clipShadows = true;
    }
    return mat;
  },

  // ── Build LatheGeometry from (r, z) profile points ─────────────────────────
  // axis: 'x' rotates around X (horizontal cylinder), 'y' rotates around Y (vertical)
  buildLathe(profilePoints, segments, axis, scaleFactor) {
    const sf = scaleFactor || 1;
    // Three.js LatheGeometry takes Vector2 (x=radius, y=height) and rotates around Y
    // We'll build it in Y orientation then rotate
    const pts = profilePoints.map(p => new THREE.Vector2(
      Math.abs(p.r * sf),
      p.z * sf
    ));
    const geo = new THREE.LatheGeometry(pts, segments||64);
    if (axis === 'x') geo.rotateZ(Math.PI / 2);
    return geo;
  },

  // ── Build tube from centerline path + radius ────────────────────────────────
  buildTube(pathPoints, radius, segments, scaleFactor) {
    const sf = scaleFactor || 1;
    const pts = pathPoints.map(p => new THREE.Vector3(p.x*sf, p.y*sf, p.z*sf));
    const path = new THREE.CatmullRomCurve3(pts);
    return new THREE.TubeGeometry(path, pathPoints.length*3, radius*sf, 12, false);
  },

  // ── Build box with optional chamfer ─────────────────────────────────────────
  buildBox(dims, scaleFactor) {
    const sf = scaleFactor || 1;
    return new THREE.BoxGeometry(dims.w*sf, dims.h*sf, dims.d*sf);
  },

  // ── Build cylinder (axis-aligned) ──────────────────────────────────────────
  buildCylinder(cfg, scaleFactor) {
    const sf = scaleFactor || 1;
    const geo = new THREE.CylinderGeometry(
      (cfg.r_top??cfg.r)*sf, (cfg.r_bottom??cfg.r)*sf,
      cfg.length*sf, cfg.segments||48, 1, cfg.open||false
    );
    if ((cfg.axis||'y') === 'x') geo.rotateZ(Math.PI/2);
    if (cfg.axis === 'z') geo.rotateX(Math.PI/2);
    return geo;
  },

  // ── Build sphere ────────────────────────────────────────────────────────────
  buildSphere(cfg, scaleFactor) {
    const sf = scaleFactor || 1;
    return new THREE.SphereGeometry(cfg.r*sf, cfg.w_seg||48, cfg.h_seg||32);
  },

  // ── Build torus (ring / O-ring / seal) ─────────────────────────────────────
  buildTorus(cfg, scaleFactor) {
    const sf = scaleFactor || 1;
    const geo = new THREE.TorusGeometry(cfg.r*sf, cfg.tube*sf, cfg.radial_seg||16, cfg.tubular_seg||64);
    if ((cfg.axis||'y') === 'x') geo.rotateZ(Math.PI/2);
    if (cfg.axis === 'z') geo.rotateY(Math.PI/2);
    return geo;
  },

  // ── Main entry: build a part from config ────────────────────────────────────
  buildPart(partCfg, scaleFactor, clipPlane) {
    let geo;
    const sf = scaleFactor || 1;
    const t = partCfg.type;

    if (t === 'lathe' && partCfg.profile) {
      geo = this.buildLathe(partCfg.profile, partCfg.segments, partCfg.axis||'y', sf);
    } else if (t === 'lathe_shell' && partCfg.outer_profile && partCfg.inner_profile) {
      // Build two lathe surfaces for hollow parts
      const outerGeo = this.buildLathe(partCfg.outer_profile, partCfg.segments, partCfg.axis||'y', sf);
      const innerGeo = this.buildLathe(partCfg.inner_profile, partCfg.segments, partCfg.axis||'y', sf);
      // Merge
      geo = THREE.BufferGeometryUtils ? 
        THREE.BufferGeometryUtils.mergeGeometries([outerGeo, innerGeo]) : outerGeo;
    } else if (t === 'cylinder') {
      geo = this.buildCylinder(partCfg, sf);
    } else if (t === 'tube' && partCfg.path) {
      geo = this.buildTube(partCfg.path, partCfg.r, partCfg.segments, sf);
    } else if (t === 'sphere') {
      geo = this.buildSphere(partCfg, sf);
    } else if (t === 'torus') {
      geo = this.buildTorus(partCfg, sf);
    } else if (t === 'box') {
      geo = this.buildBox(partCfg.dims || {w:partCfg.w||1,h:partCfg.h||1,d:partCfg.d||1}, sf);
    } else {
      // Default: cylinder
      geo = new THREE.CylinderGeometry((partCfg.r||0.5)*sf, (partCfg.r||0.5)*sf, (partCfg.length||1)*sf, 32);
    }

    geo.computeVertexNormals();
    const mat = this.getMaterial(partCfg.material||{type:'brushed_metal'}, clipPlane);
    const mesh = new THREE.Mesh(geo, mat);

    // Position
    const pos = partCfg.position||{};
    mesh.position.set((pos.x||0)*sf, (pos.y||0)*sf, (pos.z||0)*sf);

    // Rotation (degrees → radians)
    const rot = partCfg.rotation||{};
    mesh.rotation.set(
      THREE.MathUtils.degToRad(rot.x||0),
      THREE.MathUtils.degToRad(rot.y||0),
      THREE.MathUtils.degToRad(rot.z||0)
    );

    mesh.castShadow = true;
    mesh.receiveShadow = true;
    mesh.userData = { id: partCfg.id, animation: partCfg.animation||null };
    return mesh;
  },

  // ── Animate a mesh from its animation config ─────────────────────────────────
  animatePart(mesh, t, P, scaleFactor) {
    const anim = mesh.userData.animation;
    if (!anim) return;
    const sf = scaleFactor || 1;
    const driven = anim.driven_by ? (P[anim.driven_by]??anim.default_value??0.5) : 0.5;
    const speed = anim.speed_driven_by ? (P[anim.speed_driven_by]??1) : (anim.speed||1);

    if (anim.type === 'translate_linear') {
      const axis = anim.axis||'x';
      const from = (anim.from||0)*sf, to = (anim.to||1)*sf;
      // driven 0–1 maps to from–to
      mesh.position[axis] = from + driven*(to-from);
    } else if (anim.type === 'oscillate') {
      const axis = anim.axis||'y';
      const amp = (anim.amplitude||0.5)*sf;
      const center = (anim.center||0)*sf;
      mesh.position[axis] = center + amp*Math.sin(t*speed*(anim.freq||1)*Math.PI*2);
    } else if (anim.type === 'rotate_continuous') {
      const axis = anim.axis||'y';
      mesh.rotation[axis] = t * speed * (anim.rpm||60) / 60 * Math.PI*2;
    } else if (anim.type === 'rotate_oscillate') {
      const axis = anim.axis||'y';
      const amp = THREE.MathUtils.degToRad(anim.amplitude_deg||45);
      mesh.rotation[axis] = amp*Math.sin(t*speed*(anim.freq||1)*Math.PI*2);
    } else if (anim.type === 'scale_pulse') {
      const s = 1 + (anim.amplitude||0.05)*Math.sin(t*speed*Math.PI*2*(anim.freq||1));
      mesh.scale.setScalar(s);
    }
  },
};

// ── Lighting helper ─────────────────────────────────────────────────────────
function applyLighting(lightCfg) {
  // Always add a strong directional light for shadows
  const sun = new THREE.DirectionalLight(
    new THREE.Color(lightCfg?.key?.color||'#fff8e8'),
    lightCfg?.key?.intensity??2.8
  );
  const angle = lightCfg?.key?.position||[6, 9, 5];
  sun.position.set(angle[0], angle[1], angle[2]);
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  sun.shadow.camera.near = 0.1; sun.shadow.camera.far = 60;
  sun.shadow.camera.left = -8; sun.shadow.camera.right = 8;
  sun.shadow.camera.top = 6; sun.shadow.camera.bottom = -6;
  sun.shadow.bias = -0.001;
  scene.add(sun);

  const fill = lightCfg?.fill;
  scene.add(new THREE.HemisphereLight(
    new THREE.Color(fill?.sky_color||'#1a2f4a'),
    new THREE.Color(fill?.ground_color||'#0a0c12'),
    fill?.intensity??0.9
  ));

  const rim = lightCfg?.rim;
  if (rim !== false) {
    const rimLight = new THREE.PointLight(
      new THREE.Color(rim?.color||'#3a7dff'),
      rim?.intensity??1.4,
      rim?.distance??40
    );
    rimLight.position.set(
      rim?.position?.[0]??-5,
      rim?.position?.[1]??4,
      rim?.position?.[2]??-3
    );
    scene.add(rimLight);
  }
}

// ── Camera setup ──────────────────────────────────────────────────────────
function applyCamera(camCfg, sf) {
  const p = camCfg?.position;
  if (p) camera.position.set(p[0]*sf, p[1]*sf, p[2]*sf);
  else camera.position.set(0, (camCfg?.height||3)*sf, (camCfg?.distance||7)*sf);
  const t = camCfg?.target;
  controls.target.set((t?.[0]||0)*sf, (t?.[1]||0)*sf, (t?.[2]||0)*sf);
}

// ── Ground plane ──────────────────────────────────────────────────────────
function addGround(groundCfg, sf) {
  if (groundCfg === false) return;
  const y = (groundCfg?.y??-1)*sf;
  const size = (groundCfg?.size??20)*sf;
  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(size, size),
    new THREE.MeshStandardMaterial({color:0x0f1318,roughness:0.95})
  );
  ground.rotation.x = -Math.PI/2;
  ground.position.y = y;
  ground.receiveShadow = true;
  scene.add(ground);
  const grid = new THREE.GridHelper(size, Math.round(size*2/(sf||1)), 0x1a2535, 0x0f1828);
  grid.position.y = y + 0.001;
  scene.add(grid);
}

// ── Labels ────────────────────────────────────────────────────────────────
const _lbls = [];
function addLabel(text, worldPos) {
  const el = document.createElement('div');
  el.className = 'lbl';
  el.textContent = text;
  document.getElementById('lbl-layer').append(el);
  _lbls.push({ el, pos: worldPos.clone() });
}
function updateLabels() {
  const ww = wrap.clientWidth, wh = wrap.clientHeight;
  for (const lb of _lbls) {
    const v = lb.pos.clone().project(camera);
    if (v.z > 1) { lb.el.style.display='none'; continue; }
    lb.el.style.display = 'block';
    lb.el.style.left = ((v.x*.5+.5)*ww)+'px';
    lb.el.style.top  = ((-.5*v.y+.5)*wh - 10)+'px';
  }
}

// ── Param UI ──────────────────────────────────────────────────────────────
const P = {};
function buildUI(params) {
  const c = document.getElementById('params'); c.innerHTML='';
  for (const p of params) {
    P[p.key] = p.default??p.min;
    const w = document.createElement('div'); w.className='pg';
    const l = document.createElement('div'); l.className='pl';
    const n = document.createElement('span'); n.textContent=p.label+(p.unit?` (${p.unit})`:'');
    const v = document.createElement('span'); v.className='pv'; v.id='v_'+p.key;
    v.textContent=(+P[p.key]).toFixed(p.decimals??2);
    l.append(n,v);
    const s = document.createElement('input'); s.type='range';
    s.min=p.min; s.max=p.max; s.step=p.step??((p.max-p.min)/200); s.value=P[p.key];
    s.oninput=()=>{
      P[p.key]=parseFloat(s.value);
      document.getElementById('v_'+p.key).textContent=P[p.key].toFixed(p.decimals??2);
      if(typeof onParam==='function') try{ onParam(p.key,P[p.key],P,meshMap); }catch(e){console.warn(e);}
    };
    w.append(l,s); c.append(w);
  }
}

// ── Legend ────────────────────────────────────────────────────────────────
function buildLegend(items) {
  const c = document.getElementById('legend'); c.innerHTML='';
  for (const it of items) {
    const row = document.createElement('div'); row.className='leg';
    const dot = document.createElement('div'); dot.className='leg-c'; dot.style.background=it.color;
    const txt = document.createElement('span'); txt.textContent=it.label;
    row.append(dot,txt); c.append(row);
  }
}

// ── Parse and render the SimConfig ────────────────────────────────────────
const meshMap = {};
let _animParts = [];
let _sf = 1;
let _clipPlane = null;

function loadConfig(cfg) {
  // Scale factor: config units → Three.js units (meters)
  const units = cfg.meta?.units || 'mm';
  _sf = units==='mm' ? 0.001 : units==='cm' ? 0.01 : units==='m' ? 1 : 0.001;
  // Override scale factor if explicitly set
  if (cfg.meta?.scale_factor) _sf = cfg.meta.scale_factor;

  // Set name
  document.getElementById('sb-obj').textContent =
    (cfg.meta?.object||'3D Model') + (cfg.meta?.description ? ' — '+cfg.meta.description : '');

  // Clipping plane for cross-section
  const xsAxis = cfg.cross_section?.axis;
  if (xsAxis && xsAxis !== 'none') {
    const normals = {x:[0,-1,0], y:[0,0,-1], z:[-1,0,0]};
    const n = normals[xsAxis]||[0,-1,0];
    _clipPlane = new THREE.Plane(new THREE.Vector3(...n), cfg.cross_section?.offset??0.002);
  }

  // Lighting
  applyLighting(cfg.lighting);

  // Camera
  applyCamera(cfg.camera, _sf);

  // Ground
  addGround(cfg.ground, _sf);

  // Build all parts
  for (const partCfg of (cfg.parts||[])) {
    try {
      const mesh = SimRenderer.buildPart(partCfg, _sf, _clipPlane);
      scene.add(mesh);
      meshMap[partCfg.id] = mesh;
      if (mesh.userData.animation) _animParts.push(mesh);

      // Add label if specified
      if (partCfg.label) {
        const lp = partCfg.label_position||partCfg.position||{};
        const lo = partCfg.label_offset||{};
        addLabel(partCfg.label, new THREE.Vector3(
          ((lp.x||0)+(lo.x||0))*_sf,
          ((lp.y||0)+(lo.y||0))*_sf,
          ((lp.z||0)+(lo.z||0))*_sf
        ));
      }
    } catch(e) {
      console.error('Part build error ('+partCfg.id+'):', e);
    }
  }

  // UI parameters
  if (cfg.parameters) buildUI(cfg.parameters);

  // Legend
  if (cfg.legend) buildLegend(cfg.legend);
  else {
    // Auto-generate legend from part materials
    const seen = new Set();
    const items = [];
    for (const p of (cfg.parts||[])) {
      const mat = p.material||{};
      const key = (mat.color||'#888')+'_'+(mat.type||'');
      if (!seen.has(key) && p.name) {
        seen.add(key);
        items.push({color: mat.color||'#888888', label: p.name});
      }
    }
    buildLegend(items);
  }
}

// ── Animation loop ────────────────────────────────────────────────────────
const clock = new THREE.Clock();
let fc = 0;

(function loop() {
  requestAnimationFrame(loop);
  const dt = Math.min(clock.getDelta(), 0.05);
  const t = clock.getElapsedTime();
  fc++;
  controls.update();

  // Animate parts from config
  for (const m of _animParts) {
    SimRenderer.animatePart(m, t, P, _sf);
  }

  // User tick function
  try { if(typeof tick==='function') tick(t, dt, P, meshMap, scene, THREE); } catch(e) { console.error(e); }

  renderer.render(scene, camera);
  updateLabels();
  if (fc%60===0) document.getElementById('fps').textContent = Math.round(1/(dt||.016))+' fps';
})();

// ════════════════════════════════════════════════════════════════════════════
// CONFIG DATA (generated by LLM — pure JSON, no Three.js code)
// ════════════════════════════════════════════════════════════════════════════
try {
const SIM_CONFIG = ${SIM_CONFIG_JSON};
loadConfig(SIM_CONFIG);
} catch(e) {
  document.getElementById('err').style.display='block';
  document.getElementById('err').textContent='Config parse error:\n'+e;
}

// Optional: user-defined tick/onParam functions injected after config
${EXTRA_JS}
// ════════════════════════════════════════════════════════════════════════════

</script>
</body>
</html>"""


# ─── LLM prompt: generate SimConfig JSON ────────────────────────────────────
CONFIG_PROMPT = """You are a mechanical/physical engineering simulation expert who also knows Three.js geometry.

Generate a detailed SimConfig JSON for a 3D simulation of: "{topic}"

Context: {context}

The SimConfig drives a renderer that builds LatheGeometry, CylinderGeometry, TorusGeometry,
SphereGeometry, and TubeGeometry from your data — you do NOT write Three.js code.
You provide the geometric data; the renderer builds the model.

Output ONLY a valid JSON object. No markdown. No explanation. No ```json fences.

Required JSON structure:
{{
  "meta": {{
    "object": "exact technical name",
    "description": "one-line function description",
    "units": "mm",
    "scale_factor": 0.001
  }},
  "cross_section": {{
    "axis": "x",
    "offset": 0.002
  }},
  "camera": {{
    "position": [x, y, z],
    "target": [0, 0, 0]
  }},
  "lighting": {{
    "key": {{ "color": "#fff8e8", "intensity": 2.8, "position": [6, 9, 5] }},
    "fill": {{ "sky_color": "#1a2f4a", "ground_color": "#0a0c12", "intensity": 0.9 }},
    "rim": {{ "color": "#3a7dff", "intensity": 1.4, "position": [-5, 4, -3] }}
  }},
  "ground": {{ "y": -1, "size": 20 }},
  "parts": [
    {{
      "id": "part_id",
      "name": "Human readable name",
      "type": "lathe",
      "axis": "x",
      "segments": 64,
      "profile": [
        {{"r": radius_mm, "z": position_along_axis_mm}},
        ...minimum 15-25 points to capture chamfers, grooves, flanges...
      ],
      "position": {{"x": 0, "y": 0, "z": 0}},
      "material": {{
        "type": "brushed_metal",
        "color": "#7a8fa6",
        "metalness": 0.88,
        "roughness": 0.18
      }},
      "label": "Part Name",
      "label_offset": {{"x": 0, "y": 20, "z": 0}},
      "animation": {{
        "type": "translate_linear",
        "axis": "x",
        "from": -120,
        "to": 120,
        "driven_by": "stroke"
      }}
    }}
  ],
  "parameters": [
    {{
      "key": "stroke",
      "label": "Stroke Position",
      "min": 0,
      "max": 1,
      "default": 0.3,
      "step": 0.005,
      "decimals": 2,
      "unit": ""
    }}
  ],
  "legend": [
    {{"color": "#7a8fa6", "label": "Machined steel"}}
  ]
}}

CRITICAL REQUIREMENTS:

1. MODEL only the most important single mechanism (e.g. "hydraulic actuator" → the actuator itself).
   Do NOT generate decorative extras or multiple unrelated objects.

2. GEOMETRY ACCURACY:
   - Use real-world proportions in mm (e.g. hydraulic cylinder bore = 80mm, length = 400mm)
   - LatheGeometry profiles need 15-30 (r, z) pairs to capture: chamfers (2-3mm), O-ring grooves (width 5mm, depth 2.5mm), flanges, wall thickness
   - Parts must have correct spatial relationships (piston inside barrel, etc.)
   - "lathe" type: profile rotated 360° around the axis → creates solid of revolution (cylinder, piston, etc.)
   - "torus" type: for O-rings, seals, rings — specify r (center radius) and tube (tube radius)
   - "cylinder" type: for simple uniform-radius parts — specify r, length, axis
   - "sphere" type: ball joints, end caps
   - Cross-section AXIS must match the primary axis of the mechanism

3. MATERIALS — use accurate real-world values:
   - Machined steel: type="brushed_metal", metalness=0.88, roughness=0.18, color="#7a8fa6"
   - Polished rod: type="polished_metal", metalness=0.95, roughness=0.04, color="#b0bfcc"
   - Rubber O-ring: type="rubber", roughness=0.96, color="#1c1c1c"
   - Hydraulic fluid: type="hydraulic_fluid", color="#b86010", opacity=0.42
   - Brass port fittings: type="brass", metalness=0.88, roughness=0.22, color="#b87333"
   - Anodized piston: type="anodized", metalness=0.62, roughness=0.32, color="#2a5298"
   - Cast iron housing: type="cast_iron", metalness=0.7, roughness=0.65, color="#3a3f4a"

4. ANIMATION — describe the actual physical function:
   - Linear actuator: piston translates along axis, driven by "stroke" slider
   - Rotary: rotation driven by "rpm" or "angle" slider
   - Spring: oscillate type, frequency = natural frequency
   - Gear: rotate_continuous with speed driven by "rpm"
   - Include 3-6 animated parts where physically correct

5. PARAMETERS — 4-8 sliders that control real physical parameters:
   - Use real units: mm, bar, rpm, N, Hz, °C
   - Default values should be typical operating values
   - Range should span realistic operating range

6. PROFILE CURVE TIPS for LatheGeometry (axis="x", rotating around X-axis):
   - z goes along the primary axis (e.g., -200 to +200 for 400mm long part)
   - r is the radius at each z position
   - To model a cylinder barrel with bore: use two separate parts —
     outer barrel (r from wall_outer to wall_outer) and inner fluid area (r from 0 to bore_inner)
   - Chamfer at edge: z=-200 → r=wall_outer, z=-197 → r=wall_outer, z=-195 → r=wall_outer-2 (chamfer)
   - O-ring groove: ...add points like: r=outer, then dip to r=outer-2.5 for 5mm, then back to r=outer...

7. The JSON must be valid — no trailing commas, no comments.
"""


# ─── Optional extra JS prompt (for complex animations needing math) ──────────
EXTRA_JS_PROMPT = """Given this SimConfig for "{object_name}", write a MINIMAL JavaScript tick function
for complex behavior that cannot be expressed in the animation config fields alone.

Only write this if needed for:
- Fluid level that changes based on piston position
- Multiple parts whose positions are mathematically linked
- A parameter that affects the scale/geometry of another part

If no extra JS is needed, output exactly: // no extra js

Otherwise output ONLY raw JavaScript defining:
function tick(t, dt, P, meshMap, scene, THREE) {{ ... }}
function onParam(key, val, P, meshMap) {{ ... }}

No markdown. No explanation. Access parts via meshMap['part_id'].
"""


class Visual3DRequest(BaseModel):
    topic: str
    context: str = ""


class Visual3DResponse(BaseModel):
    html: str
    topic: str
    object_name: str = ""
    error: str | None = None


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
        # ── Step 1: Generate SimConfig JSON ──────────────────────────────────
        cfg_resp = client.chat.completions.create(
            model=settings.llm_model,
            messages=[{"role": "user", "content": CONFIG_PROMPT.format(topic=topic, context=context)}],
            temperature=0.15,
            max_tokens=4000,
        )
        raw_cfg = cfg_resp.choices[0].message.content or ""
        raw_cfg = re.sub(r"```(?:json)?\s*", "", raw_cfg)
        raw_cfg = re.sub(r"```\s*$", "", raw_cfg, flags=re.MULTILINE).strip()

        # Validate JSON
        try:
            cfg_obj = json.loads(raw_cfg)
            object_name = cfg_obj.get("meta", {}).get("object", topic)
        except json.JSONDecodeError as je:
            # Try to extract JSON block
            m = re.search(r'\{[\s\S]*\}', raw_cfg)
            if m:
                cfg_obj = json.loads(m.group())
                object_name = cfg_obj.get("meta", {}).get("object", topic)
                raw_cfg = m.group()
            else:
                raise ValueError(f"LLM returned invalid JSON: {je}") from je

        # ── Step 2: Optional extra JS for complex animations ──────────────────
        extra_js = "// no extra js"
        try:
            js_resp = client.chat.completions.create(
                model=settings.llm_model,
                messages=[{
                    "role": "user",
                    "content": EXTRA_JS_PROMPT.format(
                        object_name=object_name,
                    ) + "\n\nSimConfig summary:\n" + json.dumps({
                        "object": object_name,
                        "parts": [{"id": p["id"], "animation": p.get("animation")} for p in cfg_obj.get("parts", [])],
                        "parameters": [p["key"] for p in cfg_obj.get("parameters", [])],
                    })
                }],
                temperature=0.1,
                max_tokens=800,
            )
            js_raw = js_resp.choices[0].message.content or ""
            js_raw = re.sub(r"```(?:javascript|js)?\s*", "", js_raw)
            js_raw = re.sub(r"```\s*$", "", js_raw, flags=re.MULTILINE).strip()
            if js_raw and "no extra js" not in js_raw.lower():
                extra_js = js_raw
        except Exception:
            pass  # Extra JS is optional

        html = (HTML_3D_TEMPLATE
                .replace("${SIM_CONFIG_JSON}", raw_cfg)
                .replace("${EXTRA_JS}", extra_js))

        return Visual3DResponse(html=html, topic=topic, object_name=object_name)

    except Exception as exc:
        logger.exception("3D simulation generation failed: %s", exc)
        html = (HTML_3D_TEMPLATE
                .replace("${SIM_CONFIG_JSON}", json.dumps(_fallback_config(topic)))
                .replace("${EXTRA_JS}", _fallback_extra_js()))
        return Visual3DResponse(html=html, topic=topic, object_name=topic, error=str(exc))


def _fallback_config(topic: str) -> dict:
    """Geometrically accurate hydraulic actuator fallback config."""
    return {
        "meta": {"object": "Hydraulic Linear Actuator", "description": topic, "units": "mm", "scale_factor": 0.001},
        "cross_section": {"axis": "x", "offset": 0.002},
        "camera": {"position": [0.4, 0.25, 0.6], "target": [0, 0, 0]},
        "lighting": {
            "key": {"color": "#fff8e8", "intensity": 2.8, "position": [6, 9, 5]},
            "fill": {"sky_color": "#1a2f4a", "ground_color": "#0a0c12", "intensity": 0.9},
            "rim": {"color": "#3a7dff", "intensity": 1.4, "position": [-5, 4, -3]},
        },
        "ground": {"y": -65, "size": 0.8},
        "parts": [
            # Outer barrel
            {
                "id": "barrel",
                "name": "Cylinder Barrel",
                "type": "lathe",
                "axis": "x",
                "segments": 72,
                "profile": [
                    {"r": 40, "z": -200}, {"r": 40, "z": -196}, {"r": 43, "z": -196},
                    {"r": 53, "z": -186}, {"r": 53, "z": -180}, {"r": 53, "z": 180},
                    {"r": 53, "z": 186}, {"r": 43, "z": 196}, {"r": 40, "z": 196}, {"r": 40, "z": 200},
                ],
                "material": {"type": "cast_iron", "color": "#4a5060", "metalness": 0.72, "roughness": 0.6},
                "label": "Cylinder Barrel",
                "label_offset": {"x": 0, "y": 70, "z": 0},
            },
            # Inner bore (machined)
            {
                "id": "bore",
                "name": "Bore Wall",
                "type": "lathe",
                "axis": "x",
                "segments": 64,
                "profile": [
                    {"r": 37, "z": -198}, {"r": 37, "z": -190},
                    {"r": 40, "z": -186}, {"r": 40, "z": 180},
                    {"r": 37, "z": -190},
                ],
                "material": {"type": "brushed_metal", "color": "#8898a8", "metalness": 0.88, "roughness": 0.12},
            },
            # Piston
            {
                "id": "piston",
                "name": "Piston",
                "type": "lathe",
                "axis": "x",
                "segments": 48,
                "profile": [
                    {"r": 0, "z": -14}, {"r": 36, "z": -14},
                    {"r": 38, "z": -11}, {"r": 38, "z": -8},
                    {"r": 35.5, "z": -5}, {"r": 35.5, "z": -2},
                    {"r": 38, "z": 0}, {"r": 38, "z": 3},
                    {"r": 35.5, "z": 6}, {"r": 35.5, "z": 9},
                    {"r": 38, "z": 11}, {"r": 38, "z": 14},
                    {"r": 36, "z": 14}, {"r": 0, "z": 14},
                ],
                "position": {"x": -100, "y": 0, "z": 0},
                "material": {"type": "anodized", "color": "#2a5298", "metalness": 0.65, "roughness": 0.3},
                "label": "Piston",
                "label_offset": {"x": 0, "y": 55, "z": 0},
                "animation": {"type": "translate_linear", "axis": "x", "from": -140, "to": 60, "driven_by": "stroke"},
            },
            # O-ring 1 (piston seal)
            {
                "id": "seal1",
                "name": "Piston Seal",
                "type": "torus",
                "r": 37, "tube": 3,
                "axis": "x",
                "position": {"x": -100, "y": 0, "z": 0},
                "material": {"type": "rubber", "color": "#111111"},
                "animation": {"type": "translate_linear", "axis": "x", "from": -140, "to": 60, "driven_by": "stroke"},
            },
            # O-ring 2 (piston second seal)
            {
                "id": "seal2",
                "name": "Piston Seal 2",
                "type": "torus",
                "r": 37, "tube": 3,
                "axis": "x",
                "position": {"x": -92, "y": 0, "z": 0},
                "material": {"type": "rubber", "color": "#111111"},
                "animation": {"type": "translate_linear", "axis": "x", "from": -132, "to": 68, "driven_by": "stroke"},
            },
            # Piston rod
            {
                "id": "rod",
                "name": "Piston Rod",
                "type": "lathe",
                "axis": "x",
                "segments": 36,
                "profile": [
                    {"r": 0, "z": -14}, {"r": 18, "z": -14},
                    {"r": 18, "z": -10}, {"r": 20, "z": -8},
                    {"r": 20, "z": 280}, {"r": 18, "z": 282},
                    {"r": 18, "z": 286}, {"r": 0, "z": 286},
                ],
                "position": {"x": -100, "y": 0, "z": 0},
                "material": {"type": "polished_metal", "color": "#c0ccd8", "metalness": 0.95, "roughness": 0.04},
                "label": "Piston Rod (Ø40mm)",
                "label_offset": {"x": 200, "y": 35, "z": 0},
                "animation": {"type": "translate_linear", "axis": "x", "from": -140, "to": 60, "driven_by": "stroke"},
            },
            # Rod-end cap
            {
                "id": "cap_rod",
                "name": "Rod End Cap",
                "type": "lathe",
                "axis": "x",
                "segments": 48,
                "profile": [
                    {"r": 20, "z": -30}, {"r": 20, "z": -26},
                    {"r": 22, "z": -24}, {"r": 42, "z": -24},
                    {"r": 53, "z": -16}, {"r": 53, "z": 16},
                    {"r": 42, "z": 24}, {"r": 22, "z": 24},
                    {"r": 20, "z": 26}, {"r": 20, "z": 30},
                ],
                "position": {"x": 180, "y": 0, "z": 0},
                "material": {"type": "brushed_metal", "color": "#6a7a8a", "metalness": 0.85, "roughness": 0.22},
                "label": "Rod End Cap",
                "label_offset": {"x": 0, "y": 70, "z": 0},
            },
            # Rod seal at cap
            {
                "id": "rod_seal",
                "name": "Rod Wiper Seal",
                "type": "torus",
                "r": 21, "tube": 2.5,
                "axis": "x",
                "position": {"x": 180, "y": 0, "z": 0},
                "material": {"type": "rubber", "color": "#1a1a1a"},
            },
            # Blind end cap
            {
                "id": "cap_blind",
                "name": "Blind End Cap",
                "type": "lathe",
                "axis": "x",
                "segments": 48,
                "profile": [
                    {"r": 0, "z": -30}, {"r": 42, "z": -30},
                    {"r": 53, "z": -20}, {"r": 53, "z": 20},
                    {"r": 42, "z": 30}, {"r": 0, "z": 30},
                ],
                "position": {"x": -200, "y": 0, "z": 0},
                "material": {"type": "brushed_metal", "color": "#6a7a8a", "metalness": 0.85, "roughness": 0.22},
                "label": "Blind End Cap",
                "label_offset": {"x": 0, "y": 70, "z": 0},
            },
            # Hydraulic port (blind end)
            {
                "id": "port_a",
                "name": "Port A (High Pressure)",
                "type": "cylinder",
                "r": 8, "length": 25, "axis": "y",
                "position": {"x": -200, "y": 53, "z": 0},
                "material": {"type": "brass", "color": "#b87333", "metalness": 0.88, "roughness": 0.22},
                "label": "Port A",
                "label_offset": {"x": 0, "y": 35, "z": 0},
            },
            # Hydraulic port (rod end)
            {
                "id": "port_b",
                "name": "Port B (Return)",
                "type": "cylinder",
                "r": 8, "length": 25, "axis": "y",
                "position": {"x": 120, "y": 53, "z": 0},
                "material": {"type": "brass", "color": "#b87333", "metalness": 0.88, "roughness": 0.22},
                "label": "Port B",
                "label_offset": {"x": 0, "y": 35, "z": 0},
            },
            # Hydraulic fluid (left chamber)
            {
                "id": "fluid_a",
                "name": "Hydraulic Fluid (Pressure Side)",
                "type": "cylinder",
                "r": 36, "length": 100, "axis": "x",
                "position": {"x": -170, "y": 0, "z": 0},
                "material": {"type": "hydraulic_fluid", "color": "#c07820", "opacity": 0.4},
            },
        ],
        "parameters": [
            {"key": "stroke", "label": "Stroke Position", "min": 0, "max": 1, "default": 0.3, "step": 0.005, "decimals": 2, "unit": ""},
            {"key": "speed", "label": "Cycle Speed", "min": 0.1, "max": 3, "default": 0.8, "step": 0.05, "decimals": 2, "unit": "×"},
            {"key": "pressure", "label": "System Pressure", "min": 50, "max": 350, "default": 180, "step": 5, "decimals": 0, "unit": "bar"},
        ],
        "legend": [
            {"color": "#4a5060", "label": "Cast iron barrel"},
            {"color": "#2a5298", "label": "Anodized piston"},
            {"color": "#c0ccd8", "label": "Polished steel rod"},
            {"color": "#b87333", "label": "Brass port fittings"},
            {"color": "#111111", "label": "Rubber seals"},
            {"color": "#c07820", "label": "Hydraulic fluid"},
        ],
    }


def _fallback_extra_js() -> str:
    return """
// Auto-cycle stroke when not manually adjusted
let _autoCycle = true;
let _cycleDir = 1;
let _manualTimer = 0;

function tick(t, dt, P, meshMap) {
  // Auto-cycle
  if (_autoCycle) {
    P.stroke = (P.stroke||0) + dt * (P.speed||0.8) * 0.35 * _cycleDir;
    if (P.stroke >= 0.98) { _cycleDir = -1; P.stroke = 0.98; }
    if (P.stroke <= 0.02) { _cycleDir = 1; P.stroke = 0.02; }
    // Sync slider UI
    const el = document.getElementById('v_stroke');
    if (el) el.textContent = P.stroke.toFixed(2);
    const sliders = document.querySelectorAll('input[type=range]');
    for (const s of sliders) {
      if (s.min == 0 && s.max == 1) s.value = P.stroke;
    }
  }

  // Fluid volume changes with piston position
  const fluid = meshMap['fluid_a'];
  if (fluid) {
    const s = P.stroke||0.3;
    // fluid fills the back chamber proportionally
    fluid.scale.set(s*1.4+0.1, 1, 1);
    fluid.position.x = (-0.17 + (-0.2 + s*(-0.14+0.2)) * 0.5) ;
  }
}

function onParam(key, val, P, meshMap) {
  if (key === 'stroke') {
    _autoCycle = false;
    clearTimeout(_manualTimer);
    _manualTimer = setTimeout(() => { _autoCycle = true; }, 3000);
  }
}
"""
