"use client";

import * as d3 from "d3";
import { useEffect, useRef } from "react";

export interface ConceptNode extends d3.SimulationNodeDatum {
  id: string;
  label: string;
  mastery: number; // 0..1
  conceptId?: number;
}
export interface ConceptEdge {
  source: string;
  target: string;
}

interface ConceptMapProps {
  nodes: ConceptNode[];
  edges: ConceptEdge[];
  onNodeClick?: (node: ConceptNode) => void;
}

export default function ConceptMap({ nodes, edges, onNodeClick }: ConceptMapProps) {
  const svgRef = useRef<SVGSVGElement | null>(null);
  // Hold the latest click handler so the d3 callback always sees the freshest one.
  const clickRef = useRef(onNodeClick);
  useEffect(() => {
    clickRef.current = onNodeClick;
  }, [onNodeClick]);

  useEffect(() => {
    if (!svgRef.current) return;
    const svg = d3.select(svgRef.current);
    const { width, height } = svgRef.current.getBoundingClientRect();

    svg.selectAll("*").remove();
    const g = svg.append("g");

    type LinkRef = { source: ConceptNode | string; target: ConceptNode | string };
    const links: LinkRef[] = edges.map((e) => ({ ...e }));
    const data: ConceptNode[] = nodes.map((n) => ({ ...n }));

    const sim = d3
      .forceSimulation<ConceptNode>(data)
      .force("link", d3.forceLink<ConceptNode, LinkRef>(links).id((d) => d.id).distance(90))
      .force("charge", d3.forceManyBody().strength(-220))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collide", d3.forceCollide(34));

    const link = g
      .append("g")
      .attr("stroke", "var(--color-border)")
      .attr("stroke-width", 2)
      .selectAll("line")
      .data(links)
      .join("line");

    const node = g
      .append("g")
      .selectAll<SVGGElement, ConceptNode>("g")
      .data(data)
      .join("g")
      .style("cursor", "pointer")
      .on("click", (_event, d) => clickRef.current?.(d))
      .call(
        d3
          .drag<SVGGElement, ConceptNode>()
          .on("start", (event, d) => {
            if (!event.active) sim.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on("end", (event, d) => {
            if (!event.active) sim.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          }),
      );

    node
      .append("circle")
      .attr("r", (d) => 16 + d.mastery * 14)
      .attr("fill", (d) =>
        d.mastery >= 0.8
          ? "var(--color-secondary)"
          : d.mastery >= 0.5
            ? "var(--color-primary)"
            : "var(--color-accent)",
      )
      .attr("stroke", "white")
      .attr("stroke-width", 3);

    node
      .append("text")
      .text((d) => d.label)
      .attr("text-anchor", "middle")
      .attr("dy", 4)
      .attr("fill", "white")
      .attr("font-family", "var(--font-heading)")
      .attr("font-weight", 600)
      .attr("font-size", 11)
      .attr("pointer-events", "none");

    sim.on("tick", () => {
      link
        .attr("x1", (d) => (d.source as ConceptNode).x ?? 0)
        .attr("y1", (d) => (d.source as ConceptNode).y ?? 0)
        .attr("x2", (d) => (d.target as ConceptNode).x ?? 0)
        .attr("y2", (d) => (d.target as ConceptNode).y ?? 0);
      node.attr("transform", (d) => `translate(${d.x ?? 0},${d.y ?? 0})`);
    });

    return () => {
      sim.stop();
    };
  }, [edges, nodes]);

  return (
    <div className="card flex h-full flex-col p-5">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h2 className="text-lg" style={{ fontFamily: "var(--font-heading)" }}>
            Concept Map
          </h2>
          <p className="text-sm opacity-60">
            Drag to rearrange. Click a node to mark progress.
          </p>
        </div>
        <Legend />
      </div>
      <svg ref={svgRef} className="mt-3 flex-1 w-full" role="img" aria-label="Concept map" />
    </div>
  );
}

function Legend() {
  const items: { color: string; label: string }[] = [
    { color: "var(--color-secondary)", label: "Mastered" },
    { color: "var(--color-primary)", label: "Learning" },
    { color: "var(--color-accent)", label: "Weak" },
  ];
  return (
    <ul className="flex flex-wrap gap-2 text-xs">
      {items.map((it) => (
        <li
          key={it.label}
          className="flex items-center gap-1.5 rounded-full px-2.5 py-1"
          style={{ background: "var(--color-muted)", border: "1px solid var(--color-border)" }}
        >
          <span aria-hidden className="inline-block h-2.5 w-2.5 rounded-full" style={{ background: it.color }} />
          {it.label}
        </li>
      ))}
    </ul>
  );
}
