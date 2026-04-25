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

# ─── HTML template ─────────────────────────────────────────────────────────
HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#0f1117;color:#e0e0e0;display:flex;height:100vh;overflow:hidden}
#sidebar{width:260px;min-width:200px;background:#161b22;border-right:1px solid #30363d;padding:12px;overflow-y:auto;flex-shrink:0}
#main{flex:1;display:flex;flex-direction:column;overflow:hidden}
#tabs{display:flex;gap:4px;padding:8px 12px;background:#161b22;border-bottom:1px solid #30363d;flex-shrink:0;flex-wrap:wrap}
.tab-btn{padding:5px 12px;border-radius:6px;border:1px solid #30363d;background:#0f1117;color:#8b949e;cursor:pointer;font-size:12px;transition:all .15s}
.tab-btn.active{background:#1f6feb;border-color:#1f6feb;color:#fff}
#plot-area{flex:1;overflow:hidden;position:relative}
#plot{width:100%;height:100%}
#playbar{display:flex;align-items:center;gap:8px;padding:6px 12px;background:#161b22;border-top:1px solid #30363d;flex-shrink:0}
#playbar button{padding:4px 10px;border-radius:5px;border:1px solid #30363d;background:#21262d;color:#e0e0e0;cursor:pointer;font-size:12px}
#playbar button:hover{background:#30363d}
#time-display{font-size:11px;color:#8b949e;margin-left:4px}
h3{font-size:11px;font-weight:600;color:#8b949e;text-transform:uppercase;letter-spacing:.06em;margin:10px 0 6px}
h3:first-child{margin-top:0}
.slider-row{margin-bottom:8px}
.slider-label{display:flex;justify-content:space-between;font-size:11px;color:#c9d1d9;margin-bottom:3px}
.slider-val{color:#58a6ff;font-weight:600;font-variant-numeric:tabular-nums}
input[type=range]{width:100%;accent-color:#1f6feb;height:4px;border-radius:2px}
</style>
</head>
<body>
<div id="sidebar"></div>
<div id="main">
  <div id="tabs"></div>
  <div id="plot-area"><div id="plot"></div></div>
  <div id="playbar">
    <button id="btn-play">▶ Play</button>
    <button id="btn-reset">⟳ Reset</button>
    <span id="time-display"></span>
  </div>
</div>
<script>
// ── Injected LLM physics code ─────────────────────────────────────────────
__PHYSICS_CODE__
// ─────────────────────────────────────────────────────────────────────────

(function(){
  // Build sidebar from PARAMS
  const paramDefs = typeof PARAMS === 'function' ? PARAMS() : {};
  const P = {};
  Object.entries(paramDefs).forEach(([k,v]) => P[k] = v.default ?? v);

  const sidebar = document.getElementById('sidebar');
  const groups = {};
  Object.entries(paramDefs).forEach(([k,v]) => {
    const g = v.group || 'Parameters';
    if(!groups[g]) groups[g]=[];
    groups[g].push([k,v]);
  });
  Object.entries(groups).forEach(([gname,items])=>{
    const h = document.createElement('h3'); h.textContent=gname; sidebar.appendChild(h);
    items.forEach(([k,v])=>{
      const row = document.createElement('div'); row.className='slider-row';
      const label = document.createElement('div'); label.className='slider-label';
      const nm = document.createElement('span'); nm.textContent = (v.label||k)+(v.unit?' ('+v.unit+')':'');
      const val = document.createElement('span'); val.className='slider-val'; val.id='val-'+k; val.textContent=P[k];
      label.appendChild(nm); label.appendChild(val); row.appendChild(label);
      const sl = document.createElement('input'); sl.type='range';
      sl.min=v.min??0; sl.max=v.max??100; sl.step=v.step??((v.max-v.min)/200||0.01);
      sl.value=P[k];
      sl.addEventListener('input',()=>{
        P[k]=parseFloat(sl.value);
        document.getElementById('val-'+k).textContent=parseFloat(sl.value).toFixed(
          sl.step<0.1?2:sl.step<1?1:0
        );
        if(typeof LIVE_KEYS==='function'&&LIVE_KEYS().includes(k)) renderPlot();
        else renderPlot();
      });
      row.appendChild(sl); sidebar.appendChild(row);
    });
  });

  // Tabs
  const tabs = typeof TABS === 'function' ? TABS() : ['Plot'];
  let activeTab = tabs[0];
  const tabsEl = document.getElementById('tabs');
  tabs.forEach(t=>{
    const btn=document.createElement('button'); btn.className='tab-btn'+(t===activeTab?' active':'');
    btn.textContent=t;
    btn.onclick=()=>{
      activeTab=t;
      document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
      btn.classList.add('active');
      renderPlot();
    };
    tabsEl.appendChild(btn);
  });

  // Animation state
  let tAnim=0, playing=false, animId=null;
  const tMaxKey = Object.keys(paramDefs).find(k=>k==='t_max'||k==='T'||k==='duration')||null;
  const dtKey   = Object.keys(paramDefs).find(k=>k==='dt')||null;

  document.getElementById('btn-play').onclick=()=>{
    playing=!playing;
    document.getElementById('btn-play').textContent=playing?'⏸ Pause':'▶ Play';
    if(playing) animLoop();
    else{cancelAnimationFrame(animId); animId=null;}
  };
  document.getElementById('btn-reset').onclick=()=>{
    playing=false; tAnim=0;
    document.getElementById('btn-play').textContent='▶ Play';
    cancelAnimationFrame(animId); animId=null;
    renderPlot();
  };

  function animLoop(){
    if(!playing) return;
    const tMax = tMaxKey ? P[tMaxKey] : 10;
    const dt   = dtKey   ? P[dtKey]   : 0.05;
    tAnim+=dt; if(tAnim>tMax) tAnim=0;
    document.getElementById('time-display').textContent='t = '+tAnim.toFixed(2)+' s';
    renderPlot(tAnim);
    animId=requestAnimationFrame(animLoop);
  }

  // Render
  let plotInited=false;
  function renderPlot(t){
    const data_computed = typeof compute==='function' ? compute(P,t??tAnim) : {t:[]};
    const traces = typeof getTraces==='function' ? getTraces(activeTab, data_computed, P) : [];
    const layout = typeof getLayout==='function' ? getLayout(activeTab, data_computed, P) : {};
    const base={
      paper_bgcolor:'#0f1117', plot_bgcolor:'#0d1117',
      font:{color:'#c9d1d9',size:11},
      margin:{l:50,r:20,t:40,b:50},
      xaxis:{gridcolor:'#21262d',zerolinecolor:'#30363d'},
      yaxis:{gridcolor:'#21262d',zerolinecolor:'#30363d'},
      legend:{bgcolor:'rgba(0,0,0,0)',bordercolor:'#30363d',borderwidth:1}
    };
    const merged={...base,...layout,
      xaxis:{...base.xaxis,...(layout.xaxis||{})},
      yaxis:{...base.yaxis,...(layout.yaxis||{})}
    };
    if(!plotInited){
      Plotly.newPlot('plot', traces, merged, {responsive:true, displayModeBar:false});
      plotInited=true;
    } else {
      Plotly.react('plot', traces, merged);
    }
  }

  renderPlot(0);
})();
</script>
</body>
</html>"""

# ─── LLM prompt ────────────────────────────────────────────────────────────
PHYSICS_PROMPT = """You are a physics/math visualization expert. Generate JavaScript for an interactive Plotly.js simulation.

Topic: {topic}
Context: {context}

Write EXACTLY these 5 JavaScript functions — nothing else, no HTML, no imports:

1. PARAMS() → returns object where each key is a parameter with:
   {{ default, min, max, step, label, unit, group }}
   Groups: use logical sections like "System Parameters", "Initial Conditions", etc.
   Include at least 6-10 sliders total.

2. TABS() → returns array of tab name strings (2-5 tabs showing different aspects)
   e.g. ["Phase Space", "Time Series", "Energy", "Poincaré Map"]

3. LIVE_KEYS() → returns array of param keys that trigger instant re-render

4. compute(P, t) → runs physics simulation using RK4 or analytical solution
   - P: the current param values object
   - t: current animation time (float)
   - Returns an object with arrays of computed values (positions, velocities, energies, etc.)
   - For ODE systems: integrate from 0 to P.t_max (or similar) using ~500-1000 steps
   - Cache results in a closure variable if P hasn't changed for performance

5. getTraces(tab, data, P) → returns Plotly traces array for the given tab name
   - Use meaningful marker colors, line styles, gradient colors
   - Show at least 2-3 traces per tab
   - Include mode: 'lines', 'markers', or 'lines+markers' as appropriate
   - Animate: show current position as a highlighted dot at index Math.floor(t * data.t.length / P.t_max)

6. getLayout(tab, data, P) → returns Plotly layout object
   - Include title, xaxis.title, yaxis.title
   - Set appropriate axis ranges

RULES:
- Use real physics equations (cite them in comments)
- RK4 integration for ODEs
- Each tab must show something genuinely different and insightful
- Gradient colors: use interpolation between blue→red for time evolution
- NO try/catch wrappers, NO external imports
- Make it visually striking and dynamic
- Respond with ONLY the 5 function definitions, no wrapper object"""


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

    prompt = PHYSICS_PROMPT.format(topic=req.topic, context=req.context[:2000])

    try:
        completion = client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": "You write concise, correct JavaScript for physics simulations. Output only the requested function definitions."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=3000,
            temperature=0.2,
        )
        js_code = completion.choices[0].message.content or ""

        # Strip markdown code fences if present
        js_code = re.sub(r"^```(?:javascript|js)?\n?", "", js_code.strip())
        js_code = re.sub(r"\n?```$", "", js_code.strip())

        html = HTML_TEMPLATE.replace("__PHYSICS_CODE__", js_code)
        return {"html": html, "topic": req.topic}

    except Exception as e:
        logger.error("Visual plot generation failed: %s", e)
        return {"error": str(e)}
