export interface ArchPort {
  name: string;
  shape?: string;
}

export interface ArchComponent {
  id: string;
  label: string;
  type?: "block" | "operation" | "data" | "io" | "memory" | "control";
  detail?: string;
  inputs?: ArchPort[];
  outputs?: ArchPort[];
  children?: ArchComponent[];
}

export interface ArchConnection {
  from: string;
  to: string;
  label?: string;
}

export interface ArchitectureDiagram {
  title: string;
  components: ArchComponent[];
  connections: ArchConnection[];
}

const VALID_COMPONENT_TYPES = new Set([
  "block",
  "operation",
  "data",
  "io",
  "memory",
  "control",
]);

function collectComponentIds(
  components: ArchComponent[],
  ids: Set<string>
): boolean {
  for (const comp of components) {
    if (!comp || typeof comp !== "object") return false;
    if (typeof comp.id !== "string" || typeof comp.label !== "string")
      return false;
    if (ids.has(comp.id)) return false;
    ids.add(comp.id);

    if (comp.type && !VALID_COMPONENT_TYPES.has(comp.type)) {
      comp.type = undefined;
    }

    if (comp.inputs && !Array.isArray(comp.inputs)) return false;
    if (comp.outputs && !Array.isArray(comp.outputs)) return false;

    if (comp.inputs) {
      for (const p of comp.inputs) {
        if (!p || typeof p !== "object" || typeof p.name !== "string")
          return false;
      }
    }
    if (comp.outputs) {
      for (const p of comp.outputs) {
        if (!p || typeof p !== "object" || typeof p.name !== "string")
          return false;
      }
    }

    if (comp.children) {
      if (!Array.isArray(comp.children)) return false;
      if (!collectComponentIds(comp.children, ids)) return false;
    }
  }
  return true;
}

/**
 * Parse and validate a raw JSON string into an ArchitectureDiagram.
 * Returns null if the payload is malformed or references invalid component IDs.
 */
export function parseArchitectureDiagram(
  raw: string
): ArchitectureDiagram | null {
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch {
    return null;
  }

  if (!parsed || typeof parsed !== "object") return null;
  const obj = parsed as Record<string, unknown>;

  if (typeof obj.title !== "string" || !obj.title) return null;
  if (!Array.isArray(obj.components) || obj.components.length === 0)
    return null;
  if (!Array.isArray(obj.connections)) return null;

  const componentIds = new Set<string>();
  if (!collectComponentIds(obj.components as ArchComponent[], componentIds))
    return null;

  for (const conn of obj.connections) {
    if (!conn || typeof conn !== "object") return null;
    const c = conn as Record<string, unknown>;
    if (typeof c.from !== "string" || typeof c.to !== "string") return null;
    if (!componentIds.has(c.from) || !componentIds.has(c.to)) return null;
  }

  return {
    title: obj.title as string,
    components: obj.components as ArchComponent[],
    connections: obj.connections as ArchConnection[],
  };
}
