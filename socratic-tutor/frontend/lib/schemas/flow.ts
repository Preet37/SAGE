export interface FlowNode {
  id: string;
  label: string;
  type?:
    | "data"
    | "compute"
    | "decision"
    | "output"
    | "loss"
    | "activation"
    | "normalization";
  detail?: string;
}

export interface FlowEdge {
  from: string;
  to: string;
  label?: string;
}

export interface FlowStep {
  title: string;
  description: string;
  activeNodes: string[];
  activeEdges: Array<[string, string]>;
}

export interface FlowDiagram {
  title: string;
  layout?: "vertical" | "horizontal";
  nodes: FlowNode[];
  edges: FlowEdge[];
  steps: FlowStep[];
}

const VALID_NODE_TYPES = new Set([
  "data",
  "compute",
  "decision",
  "output",
  "loss",
  "activation",
  "normalization",
]);

/**
 * Parse and validate a raw JSON string into a FlowDiagram.
 * Returns null if the payload is malformed or references invalid node IDs.
 */
export function parseFlowDiagram(raw: string): FlowDiagram | null {
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch {
    return null;
  }

  if (!parsed || typeof parsed !== "object") return null;
  const obj = parsed as Record<string, unknown>;

  if (typeof obj.title !== "string" || !obj.title) return null;
  if (!Array.isArray(obj.nodes) || obj.nodes.length === 0) return null;
  if (!Array.isArray(obj.edges)) return null;
  if (!Array.isArray(obj.steps) || obj.steps.length === 0) return null;

  const nodeIds = new Set<string>();

  for (const node of obj.nodes) {
    if (!node || typeof node !== "object") return null;
    const n = node as Record<string, unknown>;
    if (typeof n.id !== "string" || typeof n.label !== "string") return null;
    if (n.type && !VALID_NODE_TYPES.has(n.type as string)) {
      (n as Record<string, unknown>).type = undefined;
    }
    nodeIds.add(n.id as string);
  }

  for (const edge of obj.edges) {
    if (!edge || typeof edge !== "object") return null;
    const e = edge as Record<string, unknown>;
    if (typeof e.from !== "string" || typeof e.to !== "string") return null;
    if (!nodeIds.has(e.from) || !nodeIds.has(e.to)) return null;
  }

  for (const step of obj.steps) {
    if (!step || typeof step !== "object") return null;
    const s = step as Record<string, unknown>;
    if (typeof s.title !== "string" || typeof s.description !== "string")
      return null;

    if (!Array.isArray(s.activeNodes)) s.activeNodes = [];
    for (const nid of s.activeNodes as unknown[]) {
      if (typeof nid !== "string" || !nodeIds.has(nid)) return null;
    }

    if (!Array.isArray(s.activeEdges)) s.activeEdges = [];
    const normalizedEdges: Array<[string, string]> = [];
    for (const ae of s.activeEdges as unknown[]) {
      if (Array.isArray(ae) && ae.length === 2) {
        if (!nodeIds.has(ae[0] as string) || !nodeIds.has(ae[1] as string))
          return null;
        normalizedEdges.push([ae[0] as string, ae[1] as string]);
      } else if (ae && typeof ae === "object" && !Array.isArray(ae)) {
        const pair = ae as Record<string, unknown>;
        if (
          typeof pair.from === "string" &&
          typeof pair.to === "string" &&
          nodeIds.has(pair.from) &&
          nodeIds.has(pair.to)
        ) {
          normalizedEdges.push([pair.from, pair.to]);
        } else {
          return null;
        }
      } else {
        return null;
      }
    }
    (s as Record<string, unknown>).activeEdges = normalizedEdges;
  }

  return {
    title: obj.title as string,
    layout: obj.layout === "horizontal" ? "horizontal" : "vertical",
    nodes: obj.nodes as FlowNode[],
    edges: obj.edges as FlowEdge[],
    steps: obj.steps as FlowStep[],
  };
}
