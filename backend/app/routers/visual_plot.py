"""Interactive 2D Plotly visualization endpoint.

The LLM generates only the physics/math JavaScript functions;
the rest of the UI framework (sidebar, tabs, Plotly lifecycle,
slider wiring, animation loop) is a hardcoded template injected
around the LLM code so sliders always work.
"""
import re
import logging
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from openai import OpenAI

from ..config import get_settings
from ..deps import get_current_user
from ..models.user import User

router = APIRouter(prefix="/visual", tags=["visual"])
logger = logging.getLogger(__name__)

# ─── HTML template ──────────────────────────────────────────────────────────
# The template is self-contained and robust:
#   - window.onerror shows a visible red error box instead of silent failure
#   - normalizeParams() handles both flat AND nested LLM output formats
#   - every call to compute/getTraces/getLayout is wrapped in try/catch
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#141009;color:#f0e9d6;display:flex;height:100vh;overflow:hidden}
#sidebar{width:240px;min-width:180px;background:#1a1612;border-right:1px solid rgba(240,233,214,0.08);padding:10px;overflow-y:auto;flex-shrink:0}
#main{flex:1;display:flex;flex-direction:column;overflow:hidden;min-width:0}
#tabs{display:flex;gap:4px;padding:7px 10px;background:#1a1612;border-bottom:1px solid rgba(240,233,214,0.08);flex-shrink:0;flex-wrap:wrap}
.tab-btn{padding:4px 11px;border-radius:3px;border:1px solid rgba(240,233,214,0.12);background:transparent;color:rgba(240,233,214,0.45);cursor:pointer;font-size:11px;letter-spacing:.04em;transition:all .15s}
.tab-btn.active{background:rgba(196,152,90,0.15);border-color:rgba(196,152,90,0.6);color:#c4985a}
.tab-btn:not(.active):hover{border-color:rgba(240,233,214,0.25);color:rgba(240,233,214,0.75)}
#plot-area{flex:1;overflow:hidden;min-height:0}
#plot{width:100%;height:100%}
#playbar{display:flex;align-items:center;gap:8px;padding:5px 10px;background:#1a1612;border-top:1px solid rgba(240,233,214,0.08);flex-shrink:0}
#playbar button{padding:4px 9px;border-radius:3px;border:1px solid rgba(240,233,214,0.15);background:transparent;color:rgba(240,233,214,0.75);cursor:pointer;font-size:11px;letter-spacing:.03em;transition:background .15s,border-color .15s}
#playbar button:hover{background:rgba(240,233,214,0.06);border-color:rgba(240,233,214,0.3)}
#time-display{font-size:11px;color:rgba(240,233,214,0.4);margin-left:4px;font-variant-numeric:tabular-nums}
.grp-label{font-size:9px;font-weight:700;color:rgba(240,233,214,0.35);text-transform:uppercase;letter-spacing:.1em;margin:10px 0 5px;border-bottom:1px solid rgba(240,233,214,0.07);padding-bottom:3px}
.grp-label:first-child{margin-top:0}
.slider-row{margin-bottom:7px}
.slider-label{display:flex;justify-content:space-between;font-size:11px;color:rgba(240,233,214,0.7);margin-bottom:3px;gap:4px}
.slider-name{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1;min-width:0}
.slider-val{color:#c4985a;font-weight:700;font-variant-numeric:tabular-nums;flex-shrink:0;min-width:40px;text-align:right}
input[type=range]{width:100%;accent-color:#c4985a;cursor:pointer}
#errbox{display:none;position:absolute;inset:8px;background:rgba(80,20,20,0.95);border:1px solid rgba(220,80,80,0.4);border-radius:6px;padding:12px;overflow:auto;z-index:99;font-size:11px;color:#f0a0a0;white-space:pre-wrap}
</style>
</head>
<body>
<div id="sidebar"></div>
<div id="main">
  <div id="tabs"></div>
  <div id="plot-area" style="position:relative">
    <div id="plot"></div>
    <div id="errbox"></div>
  </div>
  <div id="playbar">
    <button id="btn-play">&#9654; Play</button>
    <button id="btn-reset">&#8635; Reset</button>
    <span id="time-display"></span>
  </div>
</div>
<script>
/* ── Error display ────────────────────────────────────────────────────── */
window.onerror = function(msg,src,line,col,err){
  var box=document.getElementById('errbox');
  box.style.display='block';
  box.textContent='JS Error: '+msg+'\n('+src+':'+line+':'+col+')\n'+(err&&err.stack||'');
  return false;
};
function showErr(label, e){
  var box=document.getElementById('errbox');
  box.style.display='block';
  box.textContent=(box.textContent||'')+(label+': '+e+'\n'+(e&&e.stack||'')+'\n');
}

/* ── Injected LLM code ────────────────────────────────────────────────── */
__PHYSICS_CODE__
/* ────────────────────────────────────────────────────────────────────── */

(function(){
  /* ── Normalize PARAMS ─────────────────────────────────────────────── */
  /* Handles two LLM output formats:
     FLAT (correct):   { mass: { default:1, min:0.1, max:10, ... }, ... }
     NESTED (wrong):   { "Group": { mass: { default:1, ... }, ... }, ... }
  */
  function normalizeParams(raw){
    var flat = {};
    if(!raw || typeof raw !== 'object') return flat;
    Object.entries(raw).forEach(function([k,v]){
      if(v !== null && typeof v === 'object' && typeof v.default === 'undefined'){
        // Could be a nested group — check if its children look like param defs
        var isGroup = Object.values(v).every(function(child){
          return child !== null && typeof child === 'object' && typeof child.default !== 'undefined';
        });
        if(isGroup){
          Object.entries(v).forEach(function([pk,pv]){
            flat[pk] = Object.assign({group: k}, pv);
          });
          return;
        }
      }
      // Leaf that has no numeric default — treat whole value as default scalar
      if(v !== null && typeof v === 'object' && typeof v.default === 'undefined'){
        flat[k] = {default: 0, min:0, max:1, step:0.1, label:k, group:'Parameters'};
      } else {
        flat[k] = (typeof v === 'object') ? v : {default: v, min: v*0.1||0, max: v*10||100, step:Math.abs(v)*0.05||0.1, label:k};
      }
    });
    return flat;
  }

  var rawParams;
  try { rawParams = (typeof PARAMS==='function') ? PARAMS() : {}; }
  catch(e){ showErr('PARAMS()', e); rawParams={}; }

  var paramDefs = normalizeParams(rawParams);
  var P = {};
  Object.entries(paramDefs).forEach(function([k,v]){ P[k] = (v.default !== undefined ? v.default : 0); });

  /* ── Build sidebar ────────────────────────────────────────────────── */
  var sidebar = document.getElementById('sidebar');
  var groups = {};
  Object.entries(paramDefs).forEach(function([k,v]){
    var g = (v && v.group) || 'Parameters';
    if(!groups[g]) groups[g]=[];
    groups[g].push([k,v]);
  });
  Object.entries(groups).forEach(function([gname,items]){
    var h = document.createElement('div'); h.className='grp-label'; h.textContent=gname; sidebar.appendChild(h);
    items.forEach(function([k,v]){
      var def = v.default !== undefined ? v.default : 0;
      var mn  = v.min  !== undefined ? v.min  : 0;
      var mx  = v.max  !== undefined ? v.max  : Math.max(def*10, 100);
      var st  = v.step !== undefined ? v.step : ((mx-mn)/200 || 0.01);
      var row = document.createElement('div'); row.className='slider-row';
      var lbl = document.createElement('div'); lbl.className='slider-label';
      var nm  = document.createElement('span'); nm.className='slider-name';
      nm.textContent = (v.label||k) + (v.unit ? ' ('+v.unit+')' : '');
      var decimals = st < 0.01 ? 3 : st < 0.1 ? 2 : st < 1 ? 1 : 0;
      var val = document.createElement('span'); val.className='slider-val';
      val.id='val-'+k; val.textContent=parseFloat(def).toFixed(decimals);
      lbl.appendChild(nm); lbl.appendChild(val); row.appendChild(lbl);
      var sl = document.createElement('input'); sl.type='range';
      sl.min=mn; sl.max=mx; sl.step=st; sl.value=def;
      sl.addEventListener('input',function(){
        P[k]=parseFloat(sl.value);
        document.getElementById('val-'+k).textContent=parseFloat(sl.value).toFixed(decimals);
        renderPlot(tAnim);
      });
      row.appendChild(sl); sidebar.appendChild(row);
    });
  });

  /* ── Tabs ─────────────────────────────────────────────────────────── */
  var tabs;
  try { tabs = (typeof TABS==='function') ? TABS() : ['Plot']; }
  catch(e){ showErr('TABS()', e); tabs=['Plot']; }
  if(!Array.isArray(tabs)||tabs.length===0) tabs=['Plot'];

  var activeTab = tabs[0];
  var tabsEl = document.getElementById('tabs');
  tabs.forEach(function(t){
    var btn=document.createElement('button'); btn.className='tab-btn'+(t===activeTab?' active':'');
    btn.textContent=t;
    btn.onclick=function(){
      activeTab=t;
      document.querySelectorAll('.tab-btn').forEach(function(b){b.classList.remove('active');});
      btn.classList.add('active');
      renderPlot(tAnim);
    };
    tabsEl.appendChild(btn);
  });

  /* ── Animation state ──────────────────────────────────────────────── */
  var tAnim=0, playing=false, animId=null;
  var tMaxKey = Object.keys(paramDefs).find(function(k){ return k==='t_max'||k==='T'||k==='duration'||k==='time'; }) || null;
  var dtKey   = Object.keys(paramDefs).find(function(k){ return k==='dt'||k==='time_step'; }) || null;

  /* ── Speed control ─────────────────────────────────────────────────── */
  var speedMult = 1.0;
  var speedRow = document.createElement('div');
  speedRow.style.cssText='padding:6px 10px;background:#141009;border-top:1px solid rgba(240,233,214,0.07);display:flex;align-items:center;gap:8px;flex-shrink:0';
  speedRow.innerHTML='<span style="font-size:10px;color:rgba(240,233,214,0.35);white-space:nowrap;text-transform:uppercase;letter-spacing:.07em">Speed</span>'
    +'<input type="range" id="speed-sl" min="0.1" max="5" step="0.1" value="1" style="flex:1;accent-color:#c4985a">'
    +'<span id="speed-val" style="font-size:11px;color:#c4985a;min-width:30px;text-align:right;font-weight:700">1×</span>';
  document.getElementById('playbar').parentNode.insertBefore(speedRow, document.getElementById('playbar').nextSibling);
  document.getElementById('speed-sl').addEventListener('input', function(){
    speedMult = parseFloat(this.value);
    document.getElementById('speed-val').textContent = speedMult.toFixed(1)+'×';
  });

  document.getElementById('btn-play').onclick=function(){
    playing=!playing;
    document.getElementById('btn-play').textContent=playing?'\u23F8 Pause':'\u25B6 Play';
    if(playing) { lastRaf=performance.now(); animLoop(); } else{ cancelAnimationFrame(animId); animId=null; }
  };
  document.getElementById('btn-reset').onclick=function(){
    playing=false; tAnim=0;
    document.getElementById('btn-play').textContent='\u25B6 Play';
    cancelAnimationFrame(animId); animId=null;
    document.getElementById('time-display').textContent='';
    renderPlot(0);
  };
  var lastRaf = 0;
  function animLoop(ts){
    if(!playing) return;
    var now = ts || performance.now();
    var elapsed = (now - lastRaf) / 1000; // seconds since last frame
    lastRaf = now;
    var tMax = (tMaxKey ? P[tMaxKey] : null) || 10;
    var dt   = (dtKey   ? P[dtKey]   : null) || 0.05;
    // advance by wall-clock time × speed multiplier, not by dt steps
    tAnim += elapsed * speedMult * (tMax / 8); // full sweep in ~8s at 1×
    if(tAnim > tMax) tAnim = 0;
    document.getElementById('time-display').textContent='t = '+tAnim.toFixed(2)+' s';
    renderPlot(tAnim);
    animId = requestAnimationFrame(animLoop);
  }

  /* ── Render ───────────────────────────────────────────────────────── */
  var plotInited=false;
  var BASE_LAYOUT = {
    paper_bgcolor:'#141009', plot_bgcolor:'#141009',
    font:{color:'#f0e9d6',size:11,family:'-apple-system,BlinkMacSystemFont,sans-serif'},
    margin:{l:52,r:18,t:38,b:48},
    xaxis:{gridcolor:'rgba(240,233,214,0.06)',zerolinecolor:'rgba(240,233,214,0.15)',zerolinewidth:1,linecolor:'rgba(240,233,214,0.12)',tickfont:{color:'rgba(240,233,214,0.55)'}},
    yaxis:{gridcolor:'rgba(240,233,214,0.06)',zerolinecolor:'rgba(240,233,214,0.15)',zerolinewidth:1,linecolor:'rgba(240,233,214,0.12)',tickfont:{color:'rgba(240,233,214,0.55)'}},
    legend:{bgcolor:'rgba(20,16,9,0.88)',bordercolor:'rgba(240,233,214,0.1)',borderwidth:1,font:{size:10,color:'rgba(240,233,214,0.75)'}}
  };

  function renderPlot(t){
    var errbox=document.getElementById('errbox');
    var data_computed;
    try {
      data_computed = (typeof compute==='function') ? compute(P, t||0) : {x:[0],y:[0]};
    } catch(e){ showErr('compute()', e); data_computed={x:[0],y:[0]}; }

    var traces;
    try {
      traces = (typeof getTraces==='function') ? getTraces(activeTab, data_computed, P) : [];
    } catch(e){ showErr('getTraces()', e); traces=[]; }
    if(!Array.isArray(traces)) traces=[];

    var userLayout;
    try {
      userLayout = (typeof getLayout==='function') ? getLayout(activeTab, data_computed, P) : {};
    } catch(e){ showErr('getLayout()', e); userLayout={}; }
    if(!userLayout || typeof userLayout!=='object') userLayout={};

    var merged = Object.assign({}, BASE_LAYOUT, userLayout, {
      xaxis: Object.assign({}, BASE_LAYOUT.xaxis, userLayout.xaxis||{}),
      yaxis: Object.assign({}, BASE_LAYOUT.yaxis, userLayout.yaxis||{}),
    });

    try {
      if(!plotInited){
        Plotly.newPlot('plot', traces, merged, {responsive:true,displayModeBar:false,scrollZoom:true});
        plotInited=true;
        // Clear any stale error from earlier bad render
        if(errbox.textContent.indexOf('compute()')===-1 && errbox.textContent.indexOf('getTraces()')===-1){
          errbox.style.display='none';
        }
      } else {
        Plotly.react('plot', traces, merged);
      }
    } catch(e){ showErr('Plotly', e); }
  }

  renderPlot(0);
  // Auto-start animation
  setTimeout(function(){
    playing = true;
    document.getElementById('btn-play').textContent='\u23F8 Pause';
    lastRaf = performance.now();
    animLoop();
  }, 400);
})();
</script>
</body>
</html>"""

# ─── LLM prompt ────────────────────────────────────────────────────────────
PHYSICS_PROMPT = """You are an expert at creating interactive scientific visualizations with Plotly.js.

Topic: {topic}
Context: {context}

Generate ONLY 5 plain JavaScript function definitions (no HTML, no module syntax, no imports, no export).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REQUIRED FORMAT — copy this pattern EXACTLY:

function PARAMS() {{
  return {{
    mass:     {{ default:1.0,  min:0.1, max:10,  step:0.1,  label:'Mass',     unit:'kg', group:'System' }},
    k_spring: {{ default:5.0,  min:0.5, max:50,  step:0.5,  label:'Stiffness', unit:'N/m', group:'System' }},
    x0:       {{ default:1.0,  min:-3,  max:3,   step:0.1,  label:'x₀',       unit:'m',  group:'Initial Conditions' }},
    v0:       {{ default:0.0,  min:-5,  max:5,   step:0.1,  label:'v₀',       unit:'m/s',group:'Initial Conditions' }},
    t_max:    {{ default:10,   min:2,   max:30,  step:1,    label:'Duration',  unit:'s',  group:'Simulation' }},
    dt:       {{ default:0.05, min:0.01,max:0.2, step:0.01, label:'Time step', unit:'s',  group:'Simulation' }},
  }};
}}

⚠️  CRITICAL: PARAMS() MUST return a FLAT object where every key is a
    parameter name and its value has a numeric `default` field.
    DO NOT nest parameters inside group names like {{ "Group": {{ param: ... }} }}.
    Use the `group` field inside each parameter to set its group label.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function TABS() {{
  return ['Phase Space', 'Time Series', 'Energy', 'Poincaré Map'];
  // 2–5 meaningful tabs for this topic
}}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function LIVE_KEYS() {{
  return ['mass', 'k_spring'];  // params that feel good to update live
}}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// RK4 or analytical; t is the current playhead time (float)
// Return an object with numeric arrays — at least {{ t, x, y }} or
// whatever is needed by getTraces.
function compute(P, t) {{
  // example: cache-based RK4 for spring-mass
  var steps = Math.round(P.t_max / P.dt);
  var arr_t=[], arr_x=[], arr_v=[], arr_E=[];
  var x=P.x0, v=P.v0;
  for(var i=0;i<=steps;i++){{
    arr_t.push(i*P.dt); arr_x.push(x); arr_v.push(v);
    arr_E.push(0.5*P.mass*v*v + 0.5*P.k_spring*x*x);
    // RK4 step
    var k1x=v,             k1v=-P.k_spring/P.mass*x;
    var k2x=v+0.5*P.dt*k1v, k2v=-P.k_spring/P.mass*(x+0.5*P.dt*k1x);
    var k3x=v+0.5*P.dt*k2v, k3v=-P.k_spring/P.mass*(x+0.5*P.dt*k2x);
    var k4x=v+P.dt*k3v,    k4v=-P.k_spring/P.mass*(x+P.dt*k3x);
    x+=P.dt/6*(k1x+2*k2x+2*k3x+k4x);
    v+=P.dt/6*(k1v+2*k2v+2*k3v+k4v);
  }}
  // cursor index for the animated dot
  var ci = Math.min(Math.round(t/P.t_max * steps), steps);
  return {{ t:arr_t, x:arr_x, v:arr_v, E:arr_E, ci:ci }};
}}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// CRITICAL: Use data.ci to slice arrays so lines GROW as time advances.
// NEVER return the full array — always slice to data.ci+1 for animated reveals.
// Add a ghost (faded full trajectory) behind the live line for context.
function getTraces(tab, data, P) {{
  var ci = data.ci || 0;
  if(tab === 'Phase Space') {{
    return [
      // ghost trajectory (faded)
      {{ x:data.x, y:data.v, mode:'lines', name:'full path',
         line:{{color:'rgba(88,166,255,0.15)',width:1}}, showlegend:false }},
      // live growing trajectory
      {{ x:data.x.slice(0,ci+1), y:data.v.slice(0,ci+1), mode:'lines', name:'trajectory',
         line:{{color:'#58a6ff',width:2}} }},
      // current state dot (large, pulsing via size)
      {{ x:[data.x[ci]], y:[data.v[ci]], mode:'markers',
         marker:{{size:12,color:'#f78166',symbol:'circle',
           line:{{color:'#ffb3a3',width:2}}}}, name:'now', showlegend:false }},
    ];
  }}
  if(tab === 'Time Series') {{
    // Ghost full lines
    var traces = [
      {{ x:data.t, y:data.x, mode:'lines', name:'', line:{{color:'rgba(121,192,255,0.12)',width:1}}, showlegend:false }},
      {{ x:data.t, y:data.v, mode:'lines', name:'', line:{{color:'rgba(86,211,100,0.12)',width:1}}, showlegend:false }},
    ];
    // Live growing lines
    traces.push({{ x:data.t.slice(0,ci+1), y:data.x.slice(0,ci+1), mode:'lines', name:'position', line:{{color:'#79c0ff',width:2}} }});
    traces.push({{ x:data.t.slice(0,ci+1), y:data.v.slice(0,ci+1), mode:'lines', name:'velocity',  line:{{color:'#56d364',width:2}} }});
    // Current moment markers
    traces.push({{ x:[data.t[ci]], y:[data.x[ci]], mode:'markers', marker:{{size:8,color:'#79c0ff'}}, showlegend:false }});
    traces.push({{ x:[data.t[ci]], y:[data.v[ci]], mode:'markers', marker:{{size:8,color:'#56d364'}}, showlegend:false }});
    return traces;
  }}
  // … handle other tabs using the same slice(0,ci+1) pattern …
  return [];
}}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function getLayout(tab, data, P) {{
  if(tab === 'Phase Space') return {{
    title:'Phase Space (x vs v)', xaxis:{{title:'Position (m)'}}, yaxis:{{title:'Velocity (m/s)'}}
  }};
  if(tab === 'Time Series') return {{
    title:'Motion over time', xaxis:{{title:'Time (s)'}}, yaxis:{{title:'Value'}}
  }};
  return {{ title:tab }};
}}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Now implement the SAME 5 functions for the ACTUAL topic: "{topic}"

Rules:
- Use real equations relevant to this topic (with inline comments)
- 6–10 parameters total covering the interesting dimensions
- If the topic is conceptual (agents, transformers, etc.) model a relevant
  mathematical process (e.g., attention score softmax, reward accumulation,
  gradient descent loss surface, etc.)
- At least 3 tabs, each showing a genuinely different view
- CRITICAL: ALL time-series traces MUST slice to data.ci: data.x.slice(0, data.ci+1)
  Also add a ghost full-range trace at rgba opacity 0.12 behind the live one
- Always add a current-state marker dot at index data.ci on every tab
- Use vivid colors: position=#79c0ff, velocity=#56d364, energy=#f0883e, current=#f78166
- Gradient: interpolate trace color from blue (#1f6feb) to red (#f78166) across time
- NEVER show full static traces — always use data.ci as the reveal cursor
- Output ONLY the 5 function definitions, nothing else"""


class PlotRequest(BaseModel):
    topic: str
    context: str = ""


@router.post("/plot")
async def generate_plot(
    req: PlotRequest,
    current_user: User = Depends(get_current_user),
):
    settings = get_settings()
    client = OpenAI(api_key=settings.llm_api_key, base_url=settings.llm_base_url)

    prompt = PHYSICS_PROMPT.format(topic=req.topic, context=req.context[:1500])

    try:
        completion = client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a scientific visualization expert. "
                        "Output ONLY the 5 raw JavaScript function definitions requested — "
                        "no HTML, no markdown fences, no explanatory text, no export/import."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=3500,
            temperature=0.15,
        )
        js_code = completion.choices[0].message.content or ""

        # Strip markdown code fences if LLM added them anyway
        js_code = re.sub(r"^```(?:javascript|js)?\s*\n?", "", js_code.strip(), flags=re.MULTILINE)
        js_code = re.sub(r"\n?```\s*$", "", js_code.strip())

        html = HTML_TEMPLATE.replace("__PHYSICS_CODE__", js_code)
        return {"html": html, "topic": req.topic}

    except Exception as e:
        logger.error("Visual plot generation failed: %s", e)
        return {"error": str(e)}
