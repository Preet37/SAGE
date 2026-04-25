"use client";

import { useState, useMemo, useCallback, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  ChevronLeft,
  ChevronRight,
  Play,
  Pause,
  RotateCcw,
} from "lucide-react";
import type { FlowDiagram, FlowNode, FlowEdge } from "@/lib/schemas/flow";

const NODE_W = 200;
const NODE_H = 50;
const GAP_X = 60;
const GAP_Y = 48;
const PAD = 32;
const MIN_VIEWBOX_W = 500;

const NODE_COLORS: Record<string, { bg: string; border: string; glow: string }> = {
  data:          { bg: "#1e3a5f", border: "#3b82f6", glow: "0 0 12px rgba(59,130,246,0.5)" },
  compute:       { bg: "#1e3a2f", border: "#22c55e", glow: "0 0 12px rgba(34,197,94,0.5)" },
  decision:      { bg: "#3b2f1e", border: "#f59e0b", glow: "0 0 12px rgba(245,158,11,0.5)" },
  output:        { bg: "#2d1e3a", border: "#a855f7", glow: "0 0 12px rgba(168,85,247,0.5)" },
  loss:          { bg: "#3a1e1e", border: "#ef4444", glow: "0 0 12px rgba(239,68,68,0.5)" },
  activation:    { bg: "#1e3a3a", border: "#06b6d4", glow: "0 0 12px rgba(6,182,212,0.5)" },
  normalization: { bg: "#2a2a1e", border: "#eab308", glow: "0 0 12px rgba(234,179,8,0.5)" },
  default:       { bg: "#1e293b", border: "#64748b", glow: "0 0 12px rgba(100,116,139,0.5)" },
};

interface LayoutNode {
  id: string;
  x: number;
  y: number;
  node: FlowNode;
}

interface LayoutEdge {
  from: LayoutNode;
  to: LayoutNode;
  edge: FlowEdge;
}

function computeLayout(
  diagram: FlowDiagram
): { layoutNodes: LayoutNode[]; layoutEdges: LayoutEdge[]; width: number; height: number } {
  const isHorizontal = diagram.layout === "horizontal";
  const nodeMap = new Map<string, FlowNode>();
  for (const n of diagram.nodes) nodeMap.set(n.id, n);

  const inDegree = new Map<string, number>();
  const children = new Map<string, string[]>();
  for (const n of diagram.nodes) {
    inDegree.set(n.id, 0);
    children.set(n.id, []);
  }
  for (const e of diagram.edges) {
    inDegree.set(e.to, (inDegree.get(e.to) ?? 0) + 1);
    children.get(e.from)?.push(e.to);
  }

  // Topological sort into layers (BFS / Kahn's algorithm)
  const layers: string[][] = [];
  const assigned = new Set<string>();
  let queue = diagram.nodes
    .filter((n) => (inDegree.get(n.id) ?? 0) === 0)
    .map((n) => n.id);

  while (queue.length > 0) {
    layers.push(queue);
    for (const id of queue) assigned.add(id);
    const next: string[] = [];
    for (const id of queue) {
      for (const child of children.get(id) ?? []) {
        const remaining = (inDegree.get(child) ?? 1) - 1;
        inDegree.set(child, remaining);
        if (remaining === 0 && !assigned.has(child)) {
          next.push(child);
        }
      }
    }
    queue = next;
  }

  // Catch any nodes not reached (cycles or isolated)
  for (const n of diagram.nodes) {
    if (!assigned.has(n.id)) {
      layers.push([n.id]);
      assigned.add(n.id);
    }
  }

  const layoutNodes: LayoutNode[] = [];
  const nodePositions = new Map<string, LayoutNode>();

  for (let li = 0; li < layers.length; li++) {
    const layer = layers[li];
    for (let ni = 0; ni < layer.length; ni++) {
      const id = layer[ni];
      const node = nodeMap.get(id)!;
      const offset = (ni - (layer.length - 1) / 2);

      const x = isHorizontal
        ? PAD + li * (NODE_W + GAP_X)
        : PAD + offset * (NODE_W + GAP_X) + (layers.reduce((m, l) => Math.max(m, l.length), 0) - 1) / 2 * (NODE_W + GAP_X);
      const y = isHorizontal
        ? PAD + offset * (NODE_H + GAP_Y) + (layers.reduce((m, l) => Math.max(m, l.length), 0) - 1) / 2 * (NODE_H + GAP_Y)
        : PAD + li * (NODE_H + GAP_Y);

      const ln: LayoutNode = { id, x, y, node };
      layoutNodes.push(ln);
      nodePositions.set(id, ln);
    }
  }

  const layoutEdges: LayoutEdge[] = diagram.edges
    .map((e) => {
      const from = nodePositions.get(e.from);
      const to = nodePositions.get(e.to);
      if (!from || !to) return null;
      return { from, to, edge: e };
    })
    .filter(Boolean) as LayoutEdge[];

  const naturalW = Math.max(...layoutNodes.map((n) => n.x)) + NODE_W + PAD;
  const maxY = Math.max(...layoutNodes.map((n) => n.y)) + NODE_H + PAD;

  const viewW = Math.max(naturalW, MIN_VIEWBOX_W);
  const offsetX = (viewW - naturalW) / 2;
  if (offsetX > 0) {
    for (const ln of layoutNodes) ln.x += offsetX;
  }

  return { layoutNodes, layoutEdges, width: viewW, height: maxY };
}

function edgeKey(from: string, to: string) {
  return `${from}:${to}`;
}

interface AnimatedFlowBlockProps {
  diagram: FlowDiagram;
}

export function AnimatedFlowBlock({ diagram }: AnimatedFlowBlockProps) {
  const [stepIdx, setStepIdx] = useState(0);
  const [playing, setPlaying] = useState(false);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const step = diagram.steps[stepIdx];
  const activeNodeSet = useMemo(() => new Set(step?.activeNodes ?? []), [step]);
  const activeEdgeSet = useMemo(() => {
    const s = new Set<string>();
    for (const pair of step?.activeEdges ?? []) s.add(edgeKey(pair[0], pair[1]));
    return s;
  }, [step]);

  const { layoutNodes, layoutEdges, width, height } = useMemo(
    () => computeLayout(diagram),
    [diagram]
  );

  const prev = useCallback(() => {
    setStepIdx((i) => Math.max(0, i - 1));
  }, []);
  const next = useCallback(() => {
    setStepIdx((i) => Math.min(diagram.steps.length - 1, i + 1));
  }, [diagram.steps.length]);
  const reset = useCallback(() => {
    setStepIdx(0);
    setPlaying(false);
  }, []);

  useEffect(() => {
    if (playing) {
      intervalRef.current = setInterval(() => {
        setStepIdx((i) => {
          if (i >= diagram.steps.length - 1) {
            setPlaying(false);
            return i;
          }
          return i + 1;
        });
      }, 2000);
    }
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [playing, diagram.steps.length]);

  const isHorizontal = diagram.layout === "horizontal";

  return (
    <div className="my-3 rounded-lg border border-border bg-muted/20 overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-border bg-muted/30">
        <span className="text-xs font-semibold text-primary uppercase tracking-wider">
          {diagram.title}
        </span>
        <div className="flex items-center gap-1">
          <span className="text-xs text-muted-foreground mr-2">
            {stepIdx + 1} / {diagram.steps.length}
          </span>
          <button
            onClick={reset}
            className="p-1 rounded hover:bg-accent transition-colors text-muted-foreground hover:text-foreground"
            aria-label="Reset"
          >
            <RotateCcw className="h-3.5 w-3.5" />
          </button>
          <button
            onClick={prev}
            disabled={stepIdx === 0}
            className="p-1 rounded hover:bg-accent transition-colors text-muted-foreground hover:text-foreground disabled:opacity-30"
            aria-label="Previous step"
          >
            <ChevronLeft className="h-4 w-4" />
          </button>
          <button
            onClick={() => setPlaying((p) => !p)}
            className="p-1 rounded hover:bg-accent transition-colors text-muted-foreground hover:text-foreground"
            aria-label={playing ? "Pause" : "Play"}
          >
            {playing ? (
              <Pause className="h-3.5 w-3.5" />
            ) : (
              <Play className="h-3.5 w-3.5" />
            )}
          </button>
          <button
            onClick={next}
            disabled={stepIdx === diagram.steps.length - 1}
            className="p-1 rounded hover:bg-accent transition-colors text-muted-foreground hover:text-foreground disabled:opacity-30"
            aria-label="Next step"
          >
            <ChevronRight className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Diagram SVG */}
      <div className="overflow-x-auto">
        <svg
          viewBox={`0 0 ${width} ${height}`}
          className="w-full"
          style={{ minWidth: Math.min(width, 400), maxHeight: 500 }}
        >
          <defs>
            <marker
              id="arrow-dim"
              viewBox="0 0 10 7"
              refX="10"
              refY="3.5"
              markerWidth="8"
              markerHeight="6"
              orient="auto-start-reverse"
            >
              <path d="M 0 0 L 10 3.5 L 0 7 z" fill="#475569" />
            </marker>
            <marker
              id="arrow-active"
              viewBox="0 0 10 7"
              refX="10"
              refY="3.5"
              markerWidth="8"
              markerHeight="6"
              orient="auto-start-reverse"
            >
              <path d="M 0 0 L 10 3.5 L 0 7 z" fill="#3b82f6" />
            </marker>
          </defs>

          {/* Edges */}
          {layoutEdges.map((le) => {
            const key = edgeKey(le.from.id, le.to.id);
            const active = activeEdgeSet.has(key);

            const x1 = le.from.x + NODE_W / 2;
            const y1 = le.from.y + NODE_H / 2;
            const x2 = le.to.x + NODE_W / 2;
            const y2 = le.to.y + NODE_H / 2;

            let startX: number, startY: number, endX: number, endY: number;
            if (isHorizontal) {
              startX = le.from.x + NODE_W;
              startY = y1;
              endX = le.to.x;
              endY = y2;
            } else {
              startX = x1;
              startY = le.from.y + NODE_H;
              endX = x2;
              endY = le.to.y;
            }

            const midX = (startX + endX) / 2;
            const midY = (startY + endY) / 2;

            return (
              <g key={key}>
                <motion.line
                  x1={startX}
                  y1={startY}
                  x2={endX}
                  y2={endY}
                  strokeWidth={active ? 2.5 : 1.5}
                  markerEnd={active ? "url(#arrow-active)" : "url(#arrow-dim)"}
                  animate={{
                    stroke: active ? "#3b82f6" : "#475569",
                    opacity: active ? 1 : 0.4,
                  }}
                  transition={{ duration: 0.4 }}
                />
                {active && (
                  <motion.circle
                    r={3}
                    fill="#3b82f6"
                    initial={{ opacity: 0 }}
                    animate={{
                      opacity: [0, 1, 1, 0],
                      cx: [startX, midX, endX, endX],
                      cy: [startY, midY, endY, endY],
                    }}
                    transition={{
                      duration: 1.5,
                      repeat: Infinity,
                      ease: "easeInOut",
                    }}
                  />
                )}
                {le.edge.label && (
                  <motion.text
                    x={midX}
                    y={midY - 8}
                    textAnchor="middle"
                    fontSize={11}
                    className="fill-muted-foreground"
                    animate={{ opacity: active ? 1 : 0.3 }}
                    transition={{ duration: 0.3 }}
                  >
                    {le.edge.label}
                  </motion.text>
                )}
              </g>
            );
          })}

          {/* Nodes */}
          {layoutNodes.map((ln) => {
            const active = activeNodeSet.has(ln.id);
            const colors = NODE_COLORS[ln.node.type ?? "default"] ?? NODE_COLORS.default;

            return (
              <motion.g key={ln.id}>
                <motion.rect
                  x={ln.x}
                  y={ln.y}
                  width={NODE_W}
                  height={NODE_H}
                  rx={10}
                  ry={10}
                  strokeWidth={active ? 2 : 1.5}
                  animate={{
                    fill: active ? colors.bg : "#0f172a",
                    stroke: active ? colors.border : "#334155",
                    opacity: active ? 1 : 0.5,
                  }}
                  transition={{ duration: 0.4 }}
                  style={{
                    filter: active ? `drop-shadow(${colors.glow})` : "none",
                  }}
                />
                <motion.text
                  x={ln.x + NODE_W / 2}
                  y={ln.y + NODE_H / 2 + 1}
                  textAnchor="middle"
                  dominantBaseline="central"
                  fontSize={13}
                  fontWeight={500}
                  className="pointer-events-none"
                  animate={{
                    fill: active ? "#f1f5f9" : "#94a3b8",
                  }}
                  transition={{ duration: 0.3 }}
                >
                  {ln.node.label}
                </motion.text>
                {active && ln.node.detail && (
                  <motion.text
                    x={ln.x + NODE_W / 2}
                    y={ln.y + NODE_H + 16}
                    textAnchor="middle"
                    fontSize={11}
                    className="fill-primary"
                    initial={{ opacity: 0, y: ln.y + NODE_H + 10 }}
                    animate={{ opacity: 0.8, y: ln.y + NODE_H + 16 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    {ln.node.detail}
                  </motion.text>
                )}
              </motion.g>
            );
          })}
        </svg>
      </div>

      {/* Step info panel */}
      <AnimatePresence mode="wait">
        {step && (
          <motion.div
            key={stepIdx}
            className="px-4 py-3 border-t border-border bg-muted/30"
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -4 }}
            transition={{ duration: 0.25 }}
          >
            <p className="text-sm font-medium text-foreground">{step.title}</p>
            <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
              {step.description}
            </p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Step dots */}
      <div className="flex justify-center gap-1.5 pb-3 pt-1">
        {diagram.steps.map((_, i) => (
          <button
            key={i}
            onClick={() => setStepIdx(i)}
            className={`w-1.5 h-1.5 rounded-full transition-all duration-300 ${
              i === stepIdx
                ? "bg-primary w-4"
                : i < stepIdx
                  ? "bg-primary/40"
                  : "bg-muted-foreground/30"
            }`}
            aria-label={`Go to step ${i + 1}`}
          />
        ))}
      </div>
    </div>
  );
}
