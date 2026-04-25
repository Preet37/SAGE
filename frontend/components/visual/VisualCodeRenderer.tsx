"use client";
import { useEffect, useRef, useState } from "react";

export interface VisualCode {
  code: string;
  title: string;
  concept: string;
  lines?: number;
}

interface Props {
  data: VisualCode;
  onClose?: () => void;
  compact?: boolean;
}

// The iframe HTML template — Three.js r128 loaded from CDN
// All boilerplate (scene, camera, renderer, lights, controls, grid, stars)
// is pre-set so the LLM only writes the object-specific code
function buildHTML(code: string): string {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:100%; height:100%; background:#060c18; overflow:hidden; }
canvas { display:block; width:100%!important; height:100%!important; }
#labels { position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; overflow:hidden; }
.lbl {
  position:absolute; transform:translate(-50%,-50%);
  font:500 11px/1 system-ui,sans-serif; color:#94a3b8;
  white-space:nowrap; text-shadow:0 1px 5px #000c;
  background:rgba(6,12,24,0.55); padding:2px 6px; border-radius:4px;
}
#err {
  position:fixed; bottom:8px; left:8px; right:8px;
  background:#1a0000cc; border:1px solid #7f1d1d;
  color:#fca5a5; font:11px/1.5 monospace; padding:8px 12px;
  border-radius:6px; display:none; z-index:99;
}
</style>
</head>
<body>
<div id="labels"></div>
<div id="err"></div>

<!-- Three.js r134 UMD (stable, includes OrbitControls in examples/js) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/gh/mrdoob/three.js@r134/examples/js/controls/OrbitControls.js"></script>

<script>
// ─── Boilerplate setup ────────────────────────────────────────────────────────
const W = () => window.innerWidth;
const H = () => window.innerHeight;

const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(W(), H());
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
renderer.setClearColor(0x060c18);
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x060c18, 0.028);

const camera = new THREE.PerspectiveCamera(50, W() / H(), 0.05, 200);
camera.position.set(6, 5, 10);
camera.lookAt(0, 0, 0);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.minDistance = 1.5;
controls.maxDistance = 40;

// Lights
const hemi = new THREE.HemisphereLight(0x1a2a4a, 0x0a0814, 0.65);
scene.add(hemi);

const sun = new THREE.DirectionalLight(0xffffff, 1.5);
sun.position.set(8, 16, 7);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.near = 0.1;
sun.shadow.camera.far = 60;
sun.shadow.camera.left = sun.shadow.camera.bottom = -14;
sun.shadow.camera.right = sun.shadow.camera.top = 14;
sun.shadow.bias = -0.0005;
scene.add(sun);

const fill = new THREE.DirectionalLight(0x8899ff, 0.45);
fill.position.set(-7, 4, -5);
scene.add(fill);

const rim1 = new THREE.PointLight(0x6366f1, 0.6, 22);
rim1.position.set(-6, 7, -6);
scene.add(rim1);

const rim2 = new THREE.PointLight(0x06b6d4, 0.4, 16);
rim2.position.set(6, -2, 7);
scene.add(rim2);

// Grid
const grid = new THREE.GridHelper(26, 26, 0x1e293b, 0x0f172a);
grid.position.y = 0;
grid.material.transparent = true;
grid.material.opacity = 0.42;
scene.add(grid);

// Stars
const sGeo = new THREE.BufferGeometry();
const sArr = new Float32Array(4200);
for (let i = 0; i < 4200; i++) sArr[i] = (Math.random() - 0.5) * 180;
sGeo.setAttribute('position', new THREE.BufferAttribute(sArr, 3));
scene.add(new THREE.Points(sGeo, new THREE.PointsMaterial({ color: 0xffffff, size: 0.06, transparent: true, opacity: 0.5 })));

// Label helper: addLabel(text, x, y, z, color)
const labelsEl = document.getElementById('labels');
const _labels = [];
window.addLabel = function(text, x, y, z, color) {
  const el = document.createElement('div');
  el.className = 'lbl';
  el.textContent = text;
  if (color) el.style.color = color;
  labelsEl.appendChild(el);
  _labels.push({ el, pos: new THREE.Vector3(x, y, z) });
};
const _tmpV = new THREE.Vector3();
function updateLabels() {
  _labels.forEach(({ el, pos }) => {
    _tmpV.copy(pos).project(camera);
    const sx = ((_tmpV.x + 1) / 2) * W();
    const sy = ((-_tmpV.y + 1) / 2) * H();
    el.style.left = sx + 'px';
    el.style.top = sy + 'px';
    el.style.display = _tmpV.z < 1 ? 'block' : 'none';
  });
}

window.addEventListener('resize', () => {
  renderer.setSize(W(), H());
  camera.aspect = W() / H();
  camera.updateProjectionMatrix();
});

// Clock (available to generated code)
const clock = new THREE.Clock();

// ─── LLM GENERATED CODE (runs in global scope) ───────────────────────────────
window._sceneReady = false;
window.onerror = function(msg, src, line, col, err) {
  const errEl = document.getElementById('err');
  errEl.style.display = 'block';
  errEl.textContent = 'Scene error (line ' + line + '): ' + msg;
  // Start minimal fallback loop so page isn't frozen
  if (!window._sceneReady) {
    (function fb() { requestAnimationFrame(fb); controls.update(); renderer.render(scene, camera); })();
    window._sceneReady = true;
  }
  return true; // suppress console error
};

${code}

window._sceneReady = true;
// ─── END GENERATED CODE ──────────────────────────────────────────────────────

// Ensure labels update every frame
setInterval(updateLabels, 16);
</script>
</body>
</html>`;
}

export default function VisualCodeRenderer({ data, onClose, compact = false }: Props) {
  const [fullscreen, setFullscreen] = useState(false);
  const [showCode, setShowCode] = useState(false);
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const height = fullscreen ? "90vh" : compact ? "300px" : "520px";

  const html = buildHTML(data.code);

  return (
    <div
      className={`relative rounded-xl overflow-hidden border border-slate-700/40 bg-[#060c18] ${fullscreen ? "fixed inset-3 z-50" : ""}`}
      style={{ height }}
    >
      {/* Header */}
      <div className="absolute top-0 left-0 right-0 z-10 px-4 py-2.5 flex items-center justify-between bg-gradient-to-b from-[#060c18f0] via-[#060c18aa] to-transparent pointer-events-none">
        <div className="min-w-0">
          <h3 className="text-sm font-semibold text-white truncate">{data.title}</h3>
          <p className="text-[10px] text-slate-500 mt-0.5">{data.lines ?? "?"} lines · Three.js r134 · drag to orbit · scroll to zoom</p>
        </div>
        <div className="flex items-center gap-1.5 pointer-events-auto flex-shrink-0 ml-3">
          <button
            onClick={() => setShowCode(s => !s)}
            className="text-[10px] px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors border border-slate-700/50"
            title="View generated code"
          >
            {"</>"}
          </button>
          <button
            onClick={() => setFullscreen(f => !f)}
            className="text-slate-400 hover:text-white p-1.5 rounded-lg hover:bg-white/5 transition-colors"
          >
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {fullscreen
                ? <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 9L4 4m0 0v4m0-4h4M15 15l5 5m0 0v-4m0 4h-4M9 15l-5 5m0 0v-4m0 4h4M15 9l5-5m0 0v4m0-4h-4" />
                : <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-5h-4m4 0v4m0-4l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
              }
            </svg>
          </button>
          {onClose && (
            <button onClick={onClose} className="text-slate-400 hover:text-white p-1.5 rounded-lg hover:bg-white/5 transition-colors">
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
      </div>

      {/* Code viewer overlay */}
      {showCode && (
        <div className="absolute inset-0 z-20 bg-[#060c18f8] overflow-auto">
          <div className="flex items-center justify-between px-4 py-3 border-b border-slate-700/50">
            <span className="text-xs font-semibold text-slate-300">Generated Three.js code ({data.lines} lines)</span>
            <button onClick={() => setShowCode(false)} className="text-slate-400 hover:text-white text-xs px-3 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 transition-colors">
              ← Back to 3D
            </button>
          </div>
          <pre className="p-4 text-[11px] leading-relaxed text-slate-300 font-mono overflow-x-auto whitespace-pre-wrap">
            {data.code}
          </pre>
        </div>
      )}

      {/* Three.js iframe */}
      <iframe
        ref={iframeRef}
        srcDoc={html}
        className="w-full h-full border-0"
        sandbox="allow-scripts"
        title={`3D visualization: ${data.title}`}
      />
    </div>
  );
}
