"""
Interactive animated 2D Plot Generation.

Architecture:
  - HTML_TEMPLATE: hardcoded framework (sliders, tabs, animation loop, Plotly lifecycle)
  - LLM writes ONLY physics: PARAMS, TABS, LIVE_KEYS, compute(), getTraces(), getLayout()
  - Framework injects a live animated cursor + play/pause + live value readout
  - Sliders guaranteed to update P correctly (framework owns the oninput handlers)
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

router = APIRouter(prefix="/visual", tags=["visual"])
settings = get_settings()
yaml_cfg = load_yaml_config()

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"/>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
html,body{width:100%;height:100%;background:#060c18;color:#e2e8f0;
  font-family:system-ui,-apple-system,sans-serif;overflow:hidden;display:flex;flex-direction:column;}

/* ── CONTENT ROW ──────────────────────────────────────────────────────────── */
#content{flex:1;display:flex;min-height:0;}

/* ── SIDEBAR ──────────────────────────────────────────────────────────────── */
#sidebar{
  width:224px;min-width:224px;height:100%;
  background:#07111f;border-right:1px solid #1a2540;
  overflow-y:auto;overflow-x:hidden;display:flex;flex-direction:column;
  scrollbar-width:thin;scrollbar-color:#1e293b transparent;
}
#sidebar::-webkit-scrollbar{width:4px;}
#sidebar::-webkit-scrollbar-thumb{background:#1e293b;border-radius:2px;}
#sidebar-title{
  padding:13px 16px 11px;font-size:14px;font-weight:700;
  color:#e2e8f0;border-bottom:1px solid #1a2540;flex-shrink:0;
}
.section-header{
  padding:14px 16px 5px;font-size:9px;font-weight:800;
  text-transform:uppercase;letter-spacing:0.14em;color:#6366f1;
}
.param-block{padding:1px 16px 11px;}
.param-label{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:5px;}
.param-name{font-size:11.5px;color:#94a3b8;}
.param-val{font-size:11.5px;color:#e2e8f0;font-weight:700;font-variant-numeric:tabular-nums;}
input[type=range]{
  width:100%;height:4px;cursor:pointer;
  appearance:none;-webkit-appearance:none;
  background:linear-gradient(to right,#6366f1 var(--pct,50%),#1e293b var(--pct,50%));
  border-radius:2px;outline:none;
}
input[type=range]::-webkit-slider-thumb{
  -webkit-appearance:none;width:13px;height:13px;border-radius:50%;
  background:#6366f1;cursor:pointer;
  box-shadow:0 0 0 3px rgba(99,102,241,0.2);transition:box-shadow .12s;
}
input[type=range]::-webkit-slider-thumb:hover{box-shadow:0 0 0 5px rgba(99,102,241,0.3);}
input[type=range]::-moz-range-thumb{
  width:13px;height:13px;border-radius:50%;background:#6366f1;cursor:pointer;border:none;
}

/* LIVE VALUES */
#live-vals{
  margin-top:auto;padding:12px 16px 14px;
  border-top:1px solid #1a2540;
}
.live-header{font-size:9px;font-weight:800;text-transform:uppercase;letter-spacing:.14em;
  color:#0ea5e9;margin-bottom:9px;}
.live-row{display:flex;justify-content:space-between;align-items:baseline;
  margin-bottom:5px;font-size:11.5px;}
.live-label{color:#64748b;}
.live-value{color:#e2e8f0;font-weight:700;font-variant-numeric:tabular-nums;}

/* ── MAIN ─────────────────────────────────────────────────────────────────── */
#main{flex:1;display:flex;flex-direction:column;min-width:0;height:100%;}
#tab-bar{
  display:flex;gap:4px;align-items:center;padding:8px 12px;
  border-bottom:1px solid #1a2540;flex-wrap:wrap;flex-shrink:0;background:#07111f;
}
.tab-btn{
  padding:4px 13px;border-radius:6px;cursor:pointer;
  font-size:11px;font-weight:600;border:1px solid #1e293b;
  transition:all .15s;background:#0f172a;color:#64748b;
}
.tab-btn:hover:not(.active){background:#1e293b;color:#94a3b8;border-color:#334155;}
.tab-btn.active{background:#6366f1;color:#fff;border-color:#6366f1;}
#plot{flex:1;min-height:0;min-width:0;}

/* ── ANIMATION BAR ────────────────────────────────────────────────────────── */
#anim-bar{
  display:flex;align-items:center;gap:8px;padding:7px 14px;
  border-top:1px solid #1a2540;background:#07111f;flex-shrink:0;
}
.anim-btn{
  width:28px;height:28px;border-radius:7px;border:1px solid #1e293b;
  background:#0f172a;color:#94a3b8;cursor:pointer;display:flex;
  align-items:center;justify-content:center;font-size:12px;
  transition:all .15s;flex-shrink:0;
}
.anim-btn:hover{background:#1e293b;color:#e2e8f0;}
.anim-btn.active{background:#6366f1;color:#fff;border-color:#6366f1;}
#time-scrub{
  flex:1;height:4px;cursor:pointer;appearance:none;-webkit-appearance:none;
  background:#1e293b;border-radius:2px;outline:none;
}
#time-scrub::-webkit-slider-thumb{
  -webkit-appearance:none;width:12px;height:12px;border-radius:50%;
  background:#f59e0b;cursor:pointer;box-shadow:0 0 0 3px rgba(245,158,11,.2);
}
#time-scrub::-moz-range-thumb{
  width:12px;height:12px;border-radius:50%;background:#f59e0b;cursor:pointer;border:none;
}
#time-display{font-size:11px;color:#94a3b8;font-variant-numeric:tabular-nums;white-space:nowrap;min-width:70px;}
#speed-select{
  background:#0f172a;color:#94a3b8;border:1px solid #1e293b;
  border-radius:5px;padding:2px 4px;font-size:11px;cursor:pointer;
}
</style>
</head>
<body>
<div id="content">
  <div id="sidebar">
    <div id="sidebar-title">Parameters</div>
    <div id="sidebar-content"></div>
    <div id="live-vals">
      <div class="live-header">Live Values</div>
      <div id="live-rows"></div>
    </div>
  </div>
  <div id="main">
    <div id="tab-bar"></div>
    <div id="plot"></div>
    <div id="anim-bar">
      <button class="anim-btn" id="btn-reset" title="Reset">&#8635;</button>
      <button class="anim-btn" id="btn-play" title="Play">&#9654;</button>
      <input type="range" id="time-scrub" min="0" max="100" step="0.1" value="0">
      <span id="time-display">t = 0.00 s</span>
      <select id="speed-select">
        <option value="0.25">0.25×</option>
        <option value="0.5">0.5×</option>
        <option value="1" selected>1×</option>
        <option value="2">2×</option>
        <option value="5">5×</option>
      </select>
    </div>
  </div>
</div>

<script src="https://cdn.plot.ly/plotly-2.35.2.min.js" charset="utf-8"></script>
<script>
/* ════════════════════════════════════════════════════════════════════════════
   FRAMEWORK — never changes, always works
════════════════════════════════════════════════════════════════════════════ */
window.P = {};
window.activeTab = null;
let _data = null;
let _plotReady = false;
let _cursorTraceIdx = 0; // index of the animated cursor trace in Plotly
let _tIdx = 0;
let _playing = false;
let _lastTs = null;
let _speed = 1.0;
let _animId = null;
let _TABS = [], _LIVE_KEYS = [], _PARAMS = [];

window.DARK = {
  paper_bgcolor:'#0a0f1e', plot_bgcolor:'#060c18',
  font:{color:'#94a3b8',family:'system-ui,sans-serif',size:11},
  title:{font:{color:'#e2e8f0',size:13},x:0.5,xanchor:'center'},
  xaxis:{gridcolor:'#1a2540',zerolinecolor:'#334155',linecolor:'#1a2540',tickfont:{color:'#64748b'}},
  yaxis:{gridcolor:'#1a2540',zerolinecolor:'#334155',linecolor:'#1a2540',tickfont:{color:'#64748b'}},
  legend:{bgcolor:'rgba(0,0,0,0)',font:{color:'#94a3b8'}},
  margin:{l:64,r:20,t:48,b:50},
  hovermode:'x unified',
  hoverlabel:{bgcolor:'#0f172a',bordercolor:'#334155',font:{color:'#e2e8f0'}},
  autosize:true,
};
window.darkLayout = (extra) => {
  function merge(a,b){const o=Object.assign({},a);for(const k in b){o[k]=(b[k]&&typeof b[k]==='object'&&!Array.isArray(b[k]))?merge(a[k]||{},b[k]):b[k];}return o;}
  return merge(window.DARK, extra||{});
};

/* ── Slider fill gradient update ── */
function _updateSliderFill(el) {
  const pct = ((el.value - el.min) / (el.max - el.min)) * 100;
  el.style.setProperty('--pct', pct + '%');
}

/* ── Build sidebar ── */
function _buildSidebar(PARAMS) {
  let html = '';
  let lastSection = null;
  PARAMS.forEach(p => {
    const section = p.section || 'Parameters';
    if (section !== lastSection) {
      html += `<div class="section-header">${section}</div>`;
      lastSection = section;
    }
    const dec = p.decimals !== undefined ? p.decimals : (p.step < 1 ? 2 : (p.step < 10 ? 1 : 0));
    const pct = ((p.value - p.min) / (p.max - p.min)) * 100;
    html += `<div class="param-block">
  <div class="param-label">
    <span class="param-name">${p.label}</span>
    <span class="param-val" id="pv-${p.key}">${Number(p.value).toFixed(dec)}</span>
  </div>
  <input type="range" min="${p.min}" max="${p.max}" step="${p.step}" value="${p.value}"
    style="--pct:${pct}%"
    oninput="window.P['${p.key}']=parseFloat(this.value);_updateSliderFill(this);document.getElementById('pv-${p.key}').textContent=parseFloat(this.value).toFixed(${dec});_onParamChange()">
</div>`;
  });
  document.getElementById('sidebar-content').innerHTML = html;
  if (PARAMS[0]?.sidebarTitle) document.getElementById('sidebar-title').textContent = PARAMS[0].sidebarTitle;
}

/* ── Build live value rows ── */
function _buildLiveValues(LIVE_KEYS) {
  document.getElementById('live-rows').innerHTML = LIVE_KEYS.map(lk =>
    `<div class="live-row"><span class="live-label">${lk.label}</span><span class="live-value" id="lv-${lk.key}">—</span></div>`
  ).join('');
}

/* ── Build tabs ── */
function _buildTabs(TABS) {
  document.getElementById('tab-bar').innerHTML = TABS.map(t =>
    `<button class="tab-btn${t.key===window.activeTab?' active':''}" onclick="window._switchTab('${t.key}',this)">${t.label}</button>`
  ).join('');
}

/* ── Render plot (full re-render, called on param change or tab switch) ── */
function _renderPlot() {
  if (!_data) return;
  try {
    const bgTraces = window._getTraces(window.activeTab, _data, window.P);
    const tab = _TABS.find(t => t.key === window.activeTab) || _TABS[0];

    // Animated cursor trace
    const xKey = tab.xKey || 't';
    const yKey = tab.yKey || (Object.keys(_data).find(k => k !== 't') || 't');
    const cursorX = _data[xKey] ? [_data[xKey][_tIdx]] : [0];
    const cursorY = _data[yKey] ? [_data[yKey][_tIdx]] : [0];
    const cursorTrace = {
      x: cursorX, y: cursorY,
      mode: 'markers', type: 'scatter',
      marker: { size: 11, color: '#f59e0b', symbol: 'circle',
                line: { color: '#fbbf24', width: 2 } },
      name: 'Now', showlegend: false, hoverinfo: 'skip',
    };
    _cursorTraceIdx = bgTraces.length;

    // Vertical time-line shape (only for time-axis tabs)
    const isTimeBased = xKey === 't';
    const baseLayout = window._getLayout(window.activeTab, _data, window.P);
    if (isTimeBased && _data.t) {
      baseLayout.shapes = (baseLayout.shapes || []).concat([{
        type: 'line', xref: 'x', yref: 'paper',
        x0: _data.t[_tIdx], x1: _data.t[_tIdx],
        y0: 0, y1: 1,
        line: { color: 'rgba(245,158,11,0.55)', width: 1.5, dash: 'dot' },
      }]);
    }

    const allTraces = [...bgTraces, cursorTrace];
    if (!_plotReady) {
      Plotly.newPlot('plot', allTraces, baseLayout,
        { responsive:true, displayModeBar:true, displaylogo:false,
          modeBarButtonsToRemove:['toImage','sendDataToCloud','lasso2d','select2d','autoScale2d'] });
      _plotReady = true;
    } else {
      Plotly.react('plot', allTraces, baseLayout);
    }
  } catch(e) { console.error('Plot render error:', e); }
}

/* ── Fast cursor-only update (called every animation frame) ── */
function _updateCursor(i) {
  if (!_data || !_plotReady) return;
  const tab = _TABS.find(t => t.key === window.activeTab) || _TABS[0];
  const xKey = tab.xKey || 't';
  const yKey = tab.yKey || 't';
  const xArr = _data[xKey];
  const yArr = _data[yKey];
  if (!xArr || !yArr) return;

  // Restyle only the cursor trace (fast)
  Plotly.restyle('plot', { x: [[xArr[i]]], y: [[yArr[i]]] }, [_cursorTraceIdx]);

  // Update vertical line shape position
  if (xKey === 't' && _data.t) {
    Plotly.relayout('plot', { 'shapes[0].x0': _data.t[i], 'shapes[0].x1': _data.t[i] });
  }

  // Live value readout
  _LIVE_KEYS.forEach(lk => {
    const el = document.getElementById('lv-' + lk.key);
    if (el && _data[lk.key]) {
      const v = _data[lk.key][i];
      el.textContent = (v !== undefined ? Number(v).toFixed(lk.decimals !== undefined ? lk.decimals : 3) : '—') + (lk.unit || '');
    }
  });

  // Time scrubber + display
  const pct = xArr.length > 1 ? (i / (xArr.length - 1)) * 100 : 0;
  const scrub = document.getElementById('time-scrub');
  scrub.value = pct;
  _updateSliderFill(scrub);
  if (_data.t) {
    document.getElementById('time-display').textContent = 't = ' + (_data.t[i] || 0).toFixed(2) + ' s';
  }
}

/* ── Animation loop ── */
function _animLoop(ts) {
  if (!_playing) { _lastTs = null; return; }
  if (_lastTs !== null) {
    const elapsed = (ts - _lastTs) / 1000 * _speed;
    const dt = _data.t && _data.t.length > 1 ? (_data.t[1] - _data.t[0]) : 0.02;
    const steps = Math.max(1, Math.round(elapsed / dt));
    _tIdx = Math.min(_tIdx + steps, (_data.t || [0]).length - 1);
    if (_tIdx >= (_data.t || [0]).length - 1) {
      _playing = false;
      document.getElementById('btn-play').innerHTML = '&#9654;';
      document.getElementById('btn-play').classList.remove('active');
    }
  }
  _lastTs = ts;
  _updateCursor(_tIdx);
  if (_playing) _animId = requestAnimationFrame(_animLoop);
}

function _startAnim() {
  _playing = true;
  _lastTs = null;
  document.getElementById('btn-play').innerHTML = '&#9646;&#9646;';
  document.getElementById('btn-play').classList.add('active');
  _animId = requestAnimationFrame(_animLoop);
}
function _pauseAnim() {
  _playing = false;
  if (_animId) cancelAnimationFrame(_animId);
  document.getElementById('btn-play').innerHTML = '&#9654;';
  document.getElementById('btn-play').classList.remove('active');
}

/* ── Param change: recompute + re-render ── */
window._onParamChange = function() {
  _pauseAnim();
  _tIdx = 0;
  _data = window._compute(window.P);
  _renderPlot();
  _updateCursor(0);
};

/* ── Tab switch ── */
window._switchTab = function(key, btn) {
  window.activeTab = key;
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  _renderPlot();
  _updateCursor(_tIdx);
};

/* ── Controls ── */
document.getElementById('btn-play').addEventListener('click', () => {
  if (_playing) _pauseAnim();
  else {
    if (_tIdx >= (_data?.t?.length || 1) - 1) _tIdx = 0;
    _startAnim();
  }
});
document.getElementById('btn-reset').addEventListener('click', () => {
  _pauseAnim(); _tIdx = 0; _updateCursor(0);
});
document.getElementById('time-scrub').addEventListener('input', function() {
  _pauseAnim();
  const pct = parseFloat(this.value) / 100;
  _tIdx = Math.round(pct * ((_data?.t?.length || 1) - 1));
  _updateSliderFill(this);
  _updateCursor(_tIdx);
});
document.getElementById('speed-select').addEventListener('change', function() {
  _speed = parseFloat(this.value);
});

/* ── Main entry point called by generated code ── */
window._setupFramework = function(PARAMS, TABS, LIVE_KEYS, computeFn, tracesFn, layoutFn) {
  _PARAMS = PARAMS; _TABS = TABS; _LIVE_KEYS = LIVE_KEYS;
  window._compute = computeFn;
  window._getTraces = tracesFn;
  window._getLayout = layoutFn;

  PARAMS.forEach(p => { window.P[p.key] = p.value; });
  window.activeTab = TABS[0].key;

  _buildSidebar(PARAMS);
  _buildLiveValues(LIVE_KEYS);
  _buildTabs(TABS);

  _data = window._compute(window.P);
  _renderPlot();
  _updateCursor(0);

  // Auto-play after short delay
  setTimeout(() => _startAnim(), 600);
};

window.addEventListener('resize', () => { if (_plotReady) Plotly.relayout('plot', {autosize:true}); });
/* ════════════════════════════════════════════════════════════════════════════
   END FRAMEWORK
════════════════════════════════════════════════════════════════════════════ */

/* ════════════════════════════════════════════════════════════════════════════
   GENERATED PHYSICS CODE
════════════════════════════════════════════════════════════════════════════ */
{USER_CODE}
/* ════════════════════════════════════════════════════════════════════════════
   END GENERATED CODE
════════════════════════════════════════════════════════════════════════════ */
</script>
</body>
</html>"""


PHYSICS_PROMPT = """\
You are an expert scientific computing engineer. Write JavaScript code to create a real-time \
interactive animated physics/math visualization for:

CONCEPT: {concept}
CONTEXT: {context}

════════════════════════════════════════════════════════════════════════════
ENVIRONMENT — already set up, do NOT redeclare:
  • Plotly.js 2.35 loaded
  • window.DARK — dark layout base object
  • window.darkLayout(extra) — merges extra keys on top of DARK
  • window._setupFramework(PARAMS, TABS, LIVE_KEYS, compute, getTraces, getLayout)
    → call this as your LAST line

The framework already handles:
  ✓ Sliders that correctly update window.P[key] before calling _onParamChange()
  ✓ Play/Pause/Reset/Scrub animation controls
  ✓ A moving amber cursor dot that follows the simulation in real-time
  ✓ A dashed vertical time line on time-based plots
  ✓ Live value readout (from LIVE_KEYS array + data arrays)
  ✓ Tab switching
════════════════════════════════════════════════════════════════════════════

WRITE THESE 6 THINGS:

━━ 1. PARAMS array (6–10 sliders) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const PARAMS = [
  {{
    key: 'L',              // JS identifier
    label: 'Length (m)',   // shown in sidebar with units
    section: 'Pendulum',   // section header (group related params)
    min: 0.1, max: 5.0, step: 0.05, value: 1.0,
    decimals: 2,           // displayed decimal places
    sidebarTitle: 'Pendulum Parameters',  // optional, first param only → sets sidebar title
  }},
  ...
];
Rules: real physical/mathematical ranges, cover full interesting domain, at least 2 sections.

━━ 2. TABS array (4–6 tabs) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const TABS = [
  {{ key: 'theta',  label: 'Angle',         xKey: 't',     yKey: 'theta'  }},
  {{ key: 'omega',  label: 'Velocity',       xKey: 't',     yKey: 'omega'  }},
  {{ key: 'phase',  label: 'Phase Space',    xKey: 'theta', yKey: 'omega'  }},
  {{ key: 'energy', label: 'Energy',         xKey: 't',     yKey: 'E'      }},
  {{ key: 'xy',     label: '2D Position',    xKey: 'x',     yKey: 'y'      }},
];
xKey/yKey tell the framework where to place the animated cursor dot.
Make each tab a genuinely different physical insight (not just rescaled).

━━ 3. LIVE_KEYS array (3–6 live readouts) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const LIVE_KEYS = [
  {{ key: 'theta', label: 'θ',      unit: ' °',     decimals: 2 }},
  {{ key: 'omega', label: 'ω',      unit: ' rad/s', decimals: 3 }},
  {{ key: 'E',     label: 'Energy', unit: ' J',     decimals: 4 }},
];
key must match a field in the object returned by compute(P).

━━ 4. compute(P) function ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function compute(P) {{
  // Use RK4 for ODEs. dt = 0.02 (or smaller). n = ceil(P.tmax / dt).
  // Return an object with arrays for every key used in TABS xKey/yKey and LIVE_KEYS.
  // Example return: {{ t, theta, omega, x, y, KE, PE, E }}
}}

RK4 template (second-order ODE: d²q/dt² = acc(q, dq)):
  const dt=0.02, n=Math.ceil(P.tmax/dt);
  let q=q0, dq=dq0;
  const t=[],Q=[],DQ=[];
  for(let i=0;i<=n;i++){{
    t.push(i*dt); Q.push(q); DQ.push(dq);
    const a=(q,dq)=> /* equation */;
    const k1=a(q,dq)*dt,     h1=dq*dt;
    const k2=a(q+h1/2,dq+k1/2)*dt, h2=(dq+k1/2)*dt;
    const k3=a(q+h2/2,dq+k2/2)*dt, h3=(dq+k2/2)*dt;
    const k4=a(q+h3,dq+k3)*dt,     h4=(dq+k3)*dt;
    dq+=(k1+2*k2+2*k3+k4)/6; q+=(h1+2*h2+2*h3+h4)/6;
  }}

━━ 5. getTraces(tab, data, P) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Return Plotly trace array. These are the BACKGROUND traces (full path).
The animated cursor dot is added automatically by the framework — do NOT add it here.

VISUAL RULES — make it look beautiful:
  a) Time-series plots (xKey='t'): Use semi-transparent lines so the animated cursor stands out:
       line: {{ color: 'rgba(99,102,241,0.7)', width: 2 }}

  b) Phase portraits (e.g. theta vs omega): Use gradient coloring by time:
       {{
         x: data.theta, y: data.omega, mode: 'markers', type: 'scattergl',
         marker: {{ color: data.t, colorscale: 'Plasma', size: 3, opacity: 0.8,
                    showscale: true, colorbar: {{ title: 't (s)', thickness: 8, len: 0.7 }} }},
         name: 'Phase Path', showlegend: false
       }}

  c) 2D position plots (x vs y): Draw position snapshot lines at N evenly-spaced times:
       const N=12, step=Math.floor(data.t.length/N);
       const traces=[];
       for(let j=0;j<N;j++){{
         const i=j*step;
         traces.push({{ x:[0, data.x[i]], y:[0, data.y[i]],
           mode:'lines+markers', line:{{color:`hsl(${{200+j*12}},80%,55%)`,width:2}},
           marker:{{size:[4,9],color:`hsl(${{200+j*12}},80%,65%)`}},
           name:`t=${{data.t[i].toFixed(1)}}s`, showlegend:true }});
       }}
       return traces;

  d) Energy plots: Multiple traces (KE, PE, Total), distinct colors:
       [
         {{x:data.t, y:data.KE, mode:'lines', name:'KE', line:{{color:'#f59e0b',width:2}}}},
         {{x:data.t, y:data.PE, mode:'lines', name:'PE', line:{{color:'#10b981',width:2}}}},
         {{x:data.t, y:data.E,  mode:'lines', name:'Total', line:{{color:'#e2e8f0',width:2,dash:'dot'}}}},
       ]

  Always set hovertemplate with units: `%{{y:.3f}} m<extra></extra>`

━━ 6. getLayout(tab, data, P) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function getLayout(tab, data, P) {{
  const axes = {{
    theta: {{ title:'Angle vs Time',   x:'Time (s)',   y:'θ (degrees)' }},
    omega: {{ title:'Velocity vs Time', x:'Time (s)',   y:'ω (rad/s)'  }},
    phase: {{ title:'Phase Portrait',   x:'θ (degrees)',y:'ω (rad/s)'  }},
    energy:{{ title:'Energy vs Time',   x:'Time (s)',   y:'Energy (J)' }},
    xy:    {{ title:'2D Position',       x:'x (m)',      y:'y (m)'      }},
  }};
  const ax = axes[tab] || axes.theta;
  return window.darkLayout({{
    title: {{ text: ax.title }},
    xaxis: Object.assign({{}}, window.DARK.xaxis, {{ title: ax.x }}),
    yaxis: Object.assign({{}}, window.DARK.yaxis, {{ title: ax.y,
      ...(tab==='xy' ? {{scaleanchor:'x', scaleratio:1}} : {{}}) }}),
  }});
}}

════════════════════════════════════════════════════════════════════════════
CRITICAL: Output ONLY raw JavaScript. No markdown. No HTML. No explanation.
  • First line: const PARAMS = [
  • Last line:  _setupFramework(PARAMS, TABS, LIVE_KEYS, compute, getTraces, getLayout);
  • Do NOT redeclare: Plotly, window, P, DARK, darkLayout, _setupFramework
"""


async def _call_groq(prompt: str) -> str:
    from openai import AsyncOpenAI
    groq_base = yaml_cfg["llm"]["groq_base"]
    model = yaml_cfg.get("models", {}).get("tutor", {}).get("groq", "llama-3.3-70b-versatile")
    client = AsyncOpenAI(base_url=groq_base, api_key=settings.llm_api_key)
    resp = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
        temperature=0.1,
        stream=False,
    )
    return resp.choices[0].message.content or ""


def _extract_js(raw: str) -> str:
    match = re.search(r"```(?:javascript|js)?\s*\n([\s\S]*?)```", raw, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    stripped = raw.strip()
    for marker in ["const PARAMS", "var PARAMS", "let PARAMS"]:
        idx = stripped.find(marker)
        if idx != -1:
            return stripped[idx:].strip()
    return stripped


class VisualPlotRequest(BaseModel):
    concept: str
    context: str = ""
    lesson_id: Optional[int] = None


@router.post("/plot")
async def generate_visual_plot(
    req: VisualPlotRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
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

    prompt = PHYSICS_PROMPT.format(
        concept=req.concept,
        context=context_str or "General educational scientific visualization",
    )

    raw = await _call_groq(prompt)
    user_code = _extract_js(raw)

    if len(user_code) < 100 or "_setupFramework" not in user_code:
        raise HTTPException(status_code=422, detail="LLM did not generate valid visualization code")

    html = HTML_TEMPLATE.replace("{USER_CODE}", user_code)
    return {
        "html": html,
        "title": title,
        "concept": req.concept,
        "chars": len(html),
        "user_code_lines": len(user_code.splitlines()),
    }
