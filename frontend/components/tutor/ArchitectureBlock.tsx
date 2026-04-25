"use client";

import { useState, useMemo, useCallback } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  Handle,
  Position,
  BackgroundVariant,
  type Node,
  type Edge,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { AnimatePresence, motion } from "framer-motion";
import type {
  ArchitectureDiagram,
  ArchComponent,
} from "@/lib/schemas/architecture";

const NODE_W = 220;
const NODE_H = 64;
const GAP_X = 80;
const GAP_Y = 72;
const PAD = 40;
const MAX_COLS = 4;
const ROW_GAP = 60;

const TYPE_COLORS: Record<
  string,
  { bg: string; border: string; accent: string }
> = {
  block: { bg: "#1e3a5f", border: "#3b82f6", accent: "#60a5fa" },
  operation: { bg: "#1e3a2f", border: "#22c55e", accent: "#4ade80" },
  data: { bg: "#2d1e3a", border: "#a855f7", accent: "#c084fc" },
  io: { bg: "#3b2f1e", border: "#f59e0b", accent: "#fbbf24" },
  memory: { bg: "#3a1e1e", border: "#ef4444", accent: "#f87171" },
  control: { bg: "#2a2a1e", border: "#eab308", accent: "#facc15" },
  default: { bg: "#1e293b", border: "#64748b", accent: "#94a3b8" },
};

interface ArchNodeData {
  label: string;
  componentType: string;
  detail?: string;
  inputLine?: string;
  outputLine?: string;
  hasChildren: boolean;
  isSelected: boolean;
  [key: string]: unknown;
}

const handleStyle = (color: string) => ({
  background: color,
  width: 8,
  height: 8,
  border: "none",
});

function ArchNodeComponent({ data }: { data: ArchNodeData }) {
  const colors = TYPE_COLORS[data.componentType] ?? TYPE_COLORS.default;

  return (
    <div
      style={{
        background: colors.bg,
        border: `2px solid ${data.isSelected ? colors.accent : colors.border}`,
        borderRadius: 10,
        padding: "10px 14px",
        minWidth: NODE_W,
        maxWidth: NODE_W + 60,
        cursor: "pointer",
        boxShadow: data.isSelected
          ? `0 0 16px ${colors.accent}40`
          : "0 2px 8px rgba(0,0,0,0.3)",
        transition: "border-color 0.2s, box-shadow 0.2s",
      }}
    >
      <Handle type="target" position={Position.Left} id="left" style={handleStyle(colors.border)} />
      <Handle type="target" position={Position.Top} id="top" style={handleStyle(colors.border)} />
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <span
          style={{
            display: "inline-block",
            width: 8,
            height: 8,
            borderRadius: "50%",
            background: colors.accent,
            flexShrink: 0,
          }}
        />
        <span
          style={{
            color: "#f1f5f9",
            fontSize: 13,
            fontWeight: 600,
            lineHeight: 1.3,
          }}
        >
          {data.label}
        </span>
        {data.hasChildren && (
          <span
            style={{
              color: colors.accent,
              fontSize: 11,
              marginLeft: "auto",
              fontWeight: 700,
            }}
          >
            {data.isSelected ? "▾" : "▸"}
          </span>
        )}
      </div>
      {(data.inputLine || data.outputLine) && (
        <div style={{ marginTop: 4, fontSize: 10, color: "#94a3b8", lineHeight: 1.5 }}>
          {data.inputLine && <div>in: {data.inputLine}</div>}
          {data.outputLine && <div>out: {data.outputLine}</div>}
        </div>
      )}
      <Handle type="source" position={Position.Right} id="right" style={handleStyle(colors.border)} />
      <Handle type="source" position={Position.Bottom} id="bottom" style={handleStyle(colors.border)} />
    </div>
  );
}

const nodeTypes = { archNode: ArchNodeComponent };

function buildGraph(
  diagram: ArchitectureDiagram,
  selectedId: string | null
): { nodes: Node[]; edges: Edge[] } {
  const topIds = new Set(diagram.components.map((c) => c.id));

  const inDegree = new Map<string, number>();
  const adj = new Map<string, string[]>();
  for (const c of diagram.components) {
    inDegree.set(c.id, 0);
    adj.set(c.id, []);
  }
  for (const conn of diagram.connections) {
    if (!topIds.has(conn.from) || !topIds.has(conn.to)) continue;
    inDegree.set(conn.to, (inDegree.get(conn.to) ?? 0) + 1);
    adj.get(conn.from)?.push(conn.to);
  }

  const layers: string[][] = [];
  const assigned = new Set<string>();
  let queue = diagram.components
    .filter((c) => (inDegree.get(c.id) ?? 0) === 0)
    .map((c) => c.id);

  while (queue.length > 0) {
    layers.push(queue);
    for (const id of queue) assigned.add(id);
    const next: string[] = [];
    for (const id of queue) {
      for (const child of adj.get(id) ?? []) {
        const remaining = (inDegree.get(child) ?? 1) - 1;
        inDegree.set(child, remaining);
        if (remaining === 0 && !assigned.has(child)) next.push(child);
      }
    }
    queue = next;
  }

  for (const c of diagram.components) {
    if (!assigned.has(c.id)) {
      layers.push([c.id]);
      assigned.add(c.id);
    }
  }

  const compMap = new Map(diagram.components.map((c) => [c.id, c]));
  const maxLayerSize = Math.max(...layers.map((l) => l.length), 1);
  const needsWrap = layers.length > MAX_COLS;
  const rowHeight = maxLayerSize * (NODE_H + GAP_Y) + ROW_GAP;

  const nodes: Node[] = [];
  const nodeGridRow = new Map<string, number>();

  for (let li = 0; li < layers.length; li++) {
    const layer = layers[li];
    const gridCol = needsWrap ? li % MAX_COLS : li;
    const gridRow = needsWrap ? Math.floor(li / MAX_COLS) : 0;

    for (let ni = 0; ni < layer.length; ni++) {
      const id = layer[ni];
      const comp = compMap.get(id)!;
      const offset = ni - (layer.length - 1) / 2;

      const x = PAD + gridCol * (NODE_W + GAP_X);
      const y =
        PAD +
        gridRow * rowHeight +
        offset * (NODE_H + GAP_Y) +
        ((maxLayerSize - 1) / 2) * (NODE_H + GAP_Y);

      nodeGridRow.set(id, gridRow);

      const inputLine = comp.inputs
        ?.map((p) => (p.shape ? `${p.name}: ${p.shape}` : p.name))
        .join(" · ");
      const outputLine = comp.outputs
        ?.map((p) => (p.shape ? `${p.name}: ${p.shape}` : p.name))
        .join(" · ");

      nodes.push({
        id,
        type: "archNode",
        position: { x, y },
        data: {
          label: comp.label,
          componentType: comp.type ?? "default",
          detail: comp.detail,
          inputLine,
          outputLine,
          hasChildren: !!(comp.children && comp.children.length > 0),
          isSelected: selectedId === id,
        } satisfies ArchNodeData,
      });
    }
  }

  const edges: Edge[] = diagram.connections
    .filter((c) => topIds.has(c.from) && topIds.has(c.to))
    .map((c) => {
      const srcRow = nodeGridRow.get(c.from) ?? 0;
      const tgtRow = nodeGridRow.get(c.to) ?? 0;
      const crossRow = srcRow !== tgtRow;

      return {
        id: `${c.from}->${c.to}`,
        source: c.from,
        target: c.to,
        label: c.label,
        type: "smoothstep",
        sourceHandle: crossRow ? "bottom" : "right",
        targetHandle: crossRow ? "top" : "left",
        style: { stroke: "#475569", strokeWidth: 2 },
        labelStyle: { fill: "#94a3b8", fontSize: 11, fontWeight: 500 },
        labelBgStyle: { fill: "#0f172a", fillOpacity: 0.8 },
        labelBgPadding: [6, 4] as [number, number],
        labelBgBorderRadius: 4,
      };
    });

  return { nodes, edges };
}

function findComponent(
  comps: ArchComponent[],
  id: string
): ArchComponent | null {
  for (const c of comps) {
    if (c.id === id) return c;
    if (c.children) {
      const found = findComponent(c.children, id);
      if (found) return found;
    }
  }
  return null;
}

function findParentId(
  comps: ArchComponent[],
  targetId: string,
  parentId: string | null = null
): string | null {
  for (const c of comps) {
    if (c.id === targetId) return parentId;
    if (c.children) {
      const found = findParentId(c.children, targetId, c.id);
      if (found !== null) return found;
    }
  }
  return null;
}

interface ArchitectureBlockProps {
  diagram: ArchitectureDiagram;
}

export function ArchitectureBlock({ diagram }: ArchitectureBlockProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [drillId, setDrillId] = useState<string | null>(null);

  const topIds = useMemo(
    () => new Set(diagram.components.map((c) => c.id)),
    [diagram]
  );

  const { nodes, edges } = useMemo(
    () => buildGraph(diagram, selectedId),
    [diagram, selectedId]
  );

  const displayId = drillId ?? selectedId;
  const displayComp = useMemo(
    () => (displayId ? findComponent(diagram.components, displayId) : null),
    [displayId, diagram]
  );

  const parentId = useMemo(
    () =>
      drillId ? findParentId(diagram.components, drillId) : null,
    [drillId, diagram]
  );

  const handleNodeClick = useCallback(
    (_: React.MouseEvent, node: Node) => {
      setSelectedId((prev) => (prev === node.id ? null : node.id));
      setDrillId(null);
    },
    []
  );

  const handlePaneClick = useCallback(() => {
    setSelectedId(null);
    setDrillId(null);
  }, []);

  const handleChildClick = useCallback(
    (childId: string) => {
      if (topIds.has(childId)) {
        setSelectedId(childId);
        setDrillId(null);
      } else {
        setDrillId(childId);
      }
    },
    [topIds]
  );

  const handleBack = useCallback(() => {
    if (parentId) {
      if (topIds.has(parentId)) {
        setSelectedId(parentId);
        setDrillId(null);
      } else {
        setDrillId(parentId);
      }
    }
  }, [parentId, topIds]);

  return (
    <div className="my-3 rounded-lg border border-border bg-muted/20 overflow-hidden">
      <div className="flex items-center px-4 py-2 border-b border-border bg-muted/30">
        <span className="text-xs font-semibold text-primary uppercase tracking-wider">
          {diagram.title}
        </span>
        <span className="ml-auto text-[10px] text-muted-foreground">
          Click to explore · Scroll to zoom
        </span>
      </div>

      <div style={{ height: 400 }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          nodeTypes={nodeTypes}
          onNodeClick={handleNodeClick}
          onPaneClick={handlePaneClick}
          fitView
          colorMode="dark"
          proOptions={{ hideAttribution: true }}
          minZoom={0.3}
          maxZoom={2}
          nodesDraggable={false}
          nodesConnectable={false}
          elementsSelectable={false}
        >
          <Background variant={BackgroundVariant.Dots} gap={20} size={1} />
          <Controls showInteractive={false} position="bottom-right" />
        </ReactFlow>
      </div>

      <AnimatePresence mode="wait">
        {displayComp && (
          <motion.div
            key={displayId}
            className="px-4 py-3 border-t border-border bg-muted/30"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.25 }}
          >
            <DetailPanel
              component={displayComp}
              showBack={!!drillId && !!parentId}
              onBack={handleBack}
              onSelectChild={handleChildClick}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function DetailPanel({
  component,
  showBack,
  onBack,
  onSelectChild,
}: {
  component: ArchComponent;
  showBack: boolean;
  onBack: () => void;
  onSelectChild: (id: string) => void;
}) {
  const colors =
    TYPE_COLORS[component.type ?? "default"] ?? TYPE_COLORS.default;

  return (
    <div>
      {showBack && (
        <button
          onClick={onBack}
          className="text-[11px] text-primary hover:underline mb-1.5 flex items-center gap-1"
        >
          ← Back
        </button>
      )}

      <div className="flex items-center gap-2 mb-2">
        <span
          className="inline-block w-2.5 h-2.5 rounded-full flex-shrink-0"
          style={{ background: colors.accent }}
        />
        <span className="text-sm font-semibold text-foreground">
          {component.label}
        </span>
        {component.type && (
          <span
            className="text-[10px] px-1.5 py-0.5 rounded font-medium"
            style={{
              background: colors.bg,
              color: colors.accent,
              border: `1px solid ${colors.border}`,
            }}
          >
            {component.type}
          </span>
        )}
      </div>

      {component.detail && (
        <p className="text-xs text-muted-foreground leading-relaxed mb-2">
          {component.detail}
        </p>
      )}

      <div className="flex flex-wrap gap-x-6 gap-y-2 mb-2">
        {component.inputs && component.inputs.length > 0 && (
          <div>
            <span className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider">
              Inputs
            </span>
            <div className="mt-0.5 space-y-0.5">
              {component.inputs.map((p, i) => (
                <div key={i} className="text-xs text-foreground">
                  <span className="font-medium">{p.name}</span>
                  {p.shape && (
                    <span className="text-muted-foreground ml-1.5">
                      {p.shape}
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
        {component.outputs && component.outputs.length > 0 && (
          <div>
            <span className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider">
              Outputs
            </span>
            <div className="mt-0.5 space-y-0.5">
              {component.outputs.map((p, i) => (
                <div key={i} className="text-xs text-foreground">
                  <span className="font-medium">{p.name}</span>
                  {p.shape && (
                    <span className="text-muted-foreground ml-1.5">
                      {p.shape}
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {component.children && component.children.length > 0 && (
        <div>
          <span className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider">
            Sub-components
          </span>
          <div className="mt-1 flex flex-wrap gap-1.5">
            {component.children.map((child) => {
              const cc =
                TYPE_COLORS[child.type ?? "default"] ?? TYPE_COLORS.default;
              return (
                <button
                  key={child.id}
                  onClick={() => onSelectChild(child.id)}
                  className="text-xs px-2.5 py-1 rounded-md transition-all hover:brightness-125"
                  style={{
                    background: cc.bg,
                    color: cc.accent,
                    border: `1px solid ${cc.border}`,
                  }}
                >
                  {child.label}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
