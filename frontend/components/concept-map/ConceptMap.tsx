'use client';
import { useEffect, useRef, useState } from 'react';
import { useAuthStore } from '@/lib/store';
import { getConceptMap, updateMastery } from '@/lib/api';

interface Node { id: number; label: string; description: string; node_type: string; mastery_score: number; is_mastered: boolean; lesson_id?: number; x?: number; y?: number; fx?: number | null; fy?: number | null; vx?: number; vy?: number }
interface Edge { id: number; source_id: number; target_id: number; edge_type: string; weight: number }

interface Props { data: { nodes: unknown[]; edges: unknown[] } | null; courseId: number }

const TYPE_COLOR: Record<string, string> = { concept: '#5b9fff', skill: '#2dd4a4', prereq: '#9d78f5' };

function getMasteryColor(node: Node) {
  if (node.is_mastered) return '#2dd4a4';
  if (node.mastery_score > 0.4) return '#5b9fff';
  return '#566880';
}

export default function ConceptMap({ data, courseId }: Props) {
  const svgRef = useRef<SVGSVGElement>(null);
  const { token } = useAuthStore();
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [selected, setSelected] = useState<Node | null>(null);
  const [loading, setLoading] = useState(!data);
  const simRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const nodesRef = useRef<Node[]>([]);

  useEffect(() => {
    if (data) {
      initGraph(data.nodes as Node[], data.edges as Edge[]);
    } else if (token) {
      getConceptMap(token, courseId).then(d => {
        initGraph(d.nodes as Node[], d.edges as Edge[]);
        setLoading(false);
      });
    }
  }, [data, courseId, token]);

  function initGraph(rawNodes: Node[], rawEdges: Edge[]) {
    const svg = svgRef.current;
    if (!svg) return;
    const W = svg.clientWidth || 700;
    const H = svg.clientHeight || 500;

    const ns = rawNodes.map((n, i) => ({
      ...n,
      x: n.x ?? (W / 2 + (Math.random() - 0.5) * 400),
      y: n.y ?? (H / 2 + (Math.random() - 0.5) * 300),
      vx: 0, vy: 0, fx: null, fy: null,
    }));

    nodesRef.current = ns;
    setNodes([...ns]);
    setEdges(rawEdges);
    setLoading(false);
    runSimulation(ns, rawEdges, W, H);
  }

  function runSimulation(ns: Node[], es: Edge[], W: number, H: number) {
    const nodeById = new Map(ns.map(n => [n.id, n]));
    const alpha = { v: 0.3 };

    if (simRef.current) clearInterval(simRef.current);

    simRef.current = setInterval(() => {
      if (alpha.v < 0.005) { clearInterval(simRef.current!); return; }
      alpha.v *= 0.95;

      // repulsion
      for (let i = 0; i < ns.length; i++) {
        for (let j = i + 1; j < ns.length; j++) {
          const a = ns[i], b = ns[j];
          const dx = (b.x ?? 0) - (a.x ?? 0);
          const dy = (b.y ?? 0) - (a.y ?? 0);
          const d = Math.max(1, Math.sqrt(dx * dx + dy * dy));
          const force = (alpha.v * 2400) / (d * d);
          a.vx = (a.vx ?? 0) - (dx / d) * force;
          a.vy = (a.vy ?? 0) - (dy / d) * force;
          b.vx = (b.vx ?? 0) + (dx / d) * force;
          b.vy = (b.vy ?? 0) + (dy / d) * force;
        }
      }

      // attraction
      for (const e of es) {
        const src = nodeById.get(e.source_id);
        const tgt = nodeById.get(e.target_id);
        if (!src || !tgt) continue;
        const dx = (tgt.x ?? 0) - (src.x ?? 0);
        const dy = (tgt.y ?? 0) - (src.y ?? 0);
        const d = Math.max(1, Math.sqrt(dx * dx + dy * dy));
        const target_dist = 120;
        const force = ((d - target_dist) / d) * alpha.v * 0.4;
        src.vx = (src.vx ?? 0) + dx * force;
        src.vy = (src.vy ?? 0) + dy * force;
        tgt.vx = (tgt.vx ?? 0) - dx * force;
        tgt.vy = (tgt.vy ?? 0) - dy * force;
      }

      // center pull
      for (const n of ns) {
        n.vx = (n.vx ?? 0) + (W / 2 - (n.x ?? 0)) * 0.005 * alpha.v;
        n.vy = (n.vy ?? 0) + (H / 2 - (n.y ?? 0)) * 0.005 * alpha.v;
      }

      // integrate
      for (const n of ns) {
        if (n.fx != null) { n.x = n.fx; n.vx = 0; continue; }
        n.vx = (n.vx ?? 0) * 0.8;
        n.vy = (n.vy ?? 0) * 0.8;
        n.x = Math.max(30, Math.min(W - 30, (n.x ?? 0) + (n.vx ?? 0)));
        n.y = Math.max(30, Math.min(H - 30, (n.y ?? 0) + (n.vy ?? 0)));
      }

      nodesRef.current = [...ns];
      setNodes([...ns]);
    }, 30);
  }

  async function handleNodeClick(node: Node) {
    setSelected(node);
    if (!token) return;
    const newScore = Math.min(1, node.mastery_score + 0.15);
    await updateMastery(token, node.id, newScore);
    setNodes(prev => prev.map(n => n.id === node.id ? { ...n, mastery_score: newScore, is_mastered: newScore >= 0.8 } : n));
  }

  useEffect(() => () => { if (simRef.current) clearInterval(simRef.current); }, []);

  if (loading) return (
    <div className="h-full flex items-center justify-center">
      <div className="w-8 h-8 border-2 border-white/10 border-t-acc rounded-full animate-spin-slow" />
    </div>
  );

  const nodeById = new Map(nodes.map(n => [n.id, n]));

  return (
    <div className="h-full flex overflow-hidden relative">
      <svg ref={svgRef} className="flex-1 h-full">
        <defs>
          <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
            <polygon points="0 0, 8 3, 0 6" fill="rgba(255,255,255,0.15)" />
          </marker>
        </defs>

        {/* Edges */}
        {edges.map(e => {
          const src = nodeById.get(e.source_id);
          const tgt = nodeById.get(e.target_id);
          if (!src || !tgt) return null;
          return (
            <line key={e.id}
              x1={src.x} y1={src.y} x2={tgt.x} y2={tgt.y}
              stroke="rgba(255,255,255,0.08)" strokeWidth={1.5}
              markerEnd="url(#arrowhead)"
            />
          );
        })}

        {/* Nodes */}
        {nodes.map(n => {
          const color = getMasteryColor(n);
          const r = n.node_type === 'concept' ? 22 : 16;
          return (
            <g key={n.id} transform={`translate(${n.x ?? 0},${n.y ?? 0})`}
              style={{ cursor: 'pointer' }}
              onClick={() => handleNodeClick(n)}
            >
              {n.is_mastered && <circle r={r + 8} fill="none" stroke="#2dd4a4" strokeWidth={1} opacity={0.2} />}
              <circle r={r} fill={color + '22'} stroke={color} strokeWidth={n.id === selected?.id ? 2.5 : 1.5}
                style={{ filter: n.id === selected?.id ? `drop-shadow(0 0 8px ${color})` : undefined }}
              />
              <text textAnchor="middle" dy={r + 14} fill="rgba(255,255,255,0.65)"
                fontSize={9} fontFamily="Inter, sans-serif" fontWeight="500"
              >
                {n.label.length > 14 ? n.label.slice(0, 12) + '…' : n.label}
              </text>
              {n.mastery_score > 0 && (
                <text textAnchor="middle" dy={5} fill={color} fontSize={8} fontFamily="Inter, sans-serif" fontWeight="700">
                  {Math.round(n.mastery_score * 100)}%
                </text>
              )}
            </g>
          );
        })}
      </svg>

      {/* Legend */}
      <div className="absolute top-3 left-3 bg-bg1/85 border border-white/5 rounded-xl px-3 py-2.5 backdrop-blur-sm">
        <div className="text-[9px] font-bold uppercase tracking-widest text-t3 mb-2">Mastery</div>
        {[['#2dd4a4', 'Mastered ≥ 80%'], ['#5b9fff', 'In Progress'], ['#566880', 'Not Started']].map(([c, l]) => (
          <div key={l} className="flex items-center gap-2 text-[10px] text-t1 mb-1">
            <div className="w-2 h-2 rounded-full" style={{ background: c }} />
            {l}
          </div>
        ))}
        <div className="text-[9px] text-t3 mt-2">Click nodes to mark progress</div>
      </div>

      {/* Selected node detail */}
      {selected && (
        <div className="absolute right-0 top-0 h-full w-64 bg-bg1 border-l border-white/5 p-4 overflow-y-auto">
          <button onClick={() => setSelected(null)} className="text-t2 hover:text-t0 text-xs mb-4 block">← Close</button>
          <div className="w-8 h-8 rounded-lg mb-3 flex items-center justify-center text-sm" style={{ background: getMasteryColor(selected) + '22', color: getMasteryColor(selected) }}>
            {selected.is_mastered ? '✓' : '○'}
          </div>
          <h3 className="font-bold text-sm text-t0 mb-1">{selected.label}</h3>
          <div className="text-[10px] font-semibold uppercase tracking-widest text-t3 mb-3">{selected.node_type}</div>
          <p className="text-xs text-t1 leading-relaxed mb-4">{selected.description}</p>

          <div className="text-[10px] font-bold uppercase tracking-widest text-t3 mb-1.5">Mastery</div>
          <div className="h-1.5 bg-bg3 rounded-full overflow-hidden mb-1">
            <div className="h-full rounded-full transition-all" style={{ width: `${selected.mastery_score * 100}%`, background: getMasteryColor(selected) }} />
          </div>
          <div className="text-[10px] text-t2">{Math.round(selected.mastery_score * 100)}% mastered</div>
        </div>
      )}
    </div>
  );
}
