"use client";

import * as d3 from "d3";
import { useEffect, useMemo, useRef } from "react";

export type ConceptNode = {
  id: string;
  label: string;
  mastery: number; // 0..1
};
export type ConceptEdge = { source: string; target: string };

interface ConceptMapProps {
  nodes: ConceptNode[];
  edges: ConceptEdge[];
  topic?: string;
}

const MASTERY_THRESHOLD = 0.8;

export default function ConceptMap({ nodes, edges, topic }: ConceptMapProps) {
  const svgRef = useRef<SVGSVGElement | null>(null);

  const masteryById = useMemo(() => {
    const m = new Map<string, number>();
    nodes.forEach((n) => m.set(n.id, n.mastery));
    return m;
  }, [nodes]);

  useEffect(() => {
    const svgEl = svgRef.current;
    if (!svgEl) return;
    const svg = d3.select(svgEl);
    const { width, height } = svgEl.getBoundingClientRect();

    svg.selectAll("*").remove();

    // Filter: glow for mastered links/nodes
    const defs = svg.append("defs");
    const glow = defs.append("filter").attr("id", "node-glow").attr("x", "-50%").attr("y", "-50%")
      .attr("width", "200%").attr("height", "200%");
    glow.append("feGaussianBlur").attr("stdDeviation", "4").attr("result", "blur");
    const merge = glow.append("feMerge");
    merge.append("feMergeNode").attr("in", "blur");
    merge.append("feMergeNode").attr("in", "SourceGraphic");

    const grad = defs.append("radialGradient").attr("id", "node-grad");
    grad.append("stop").attr("offset", "0%").attr("stop-color", "white").attr("stop-opacity", 0.85);
    grad.append("stop").attr("offset", "100%").attr("stop-color", "white").attr("stop-opacity", 0);

    const g = svg.append("g");

    type LinkRef = { source: ConceptNode | string; target: ConceptNode | string; mastered: boolean };
    const links: LinkRef[] = edges.map((e) => ({
      ...e,
      mastered:
        (masteryById.get(e.source) ?? 0) >= MASTERY_THRESHOLD &&
        (masteryById.get(e.target) ?? 0) >= MASTERY_THRESHOLD,
    }));

    const sim = d3
      .forceSimulation<ConceptNode>(nodes)
      .force("link", d3.forceLink<ConceptNode, LinkRef>(links).id((d) => d.id).distance(110))
      .force("charge", d3.forceManyBody().strength(-260))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collide", d3.forceCollide(38));

    const link = g
      .append("g")
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("stroke-width", (d) => (d.mastered ? 2.5 : 1.5))
      .attr("stroke-linecap", "round")
      .attr("stroke", (d) =>
        d.mastered ? "var(--color-secondary)" : "rgba(31,27,51,0.15)",
      )
      .attr("class", (d) => (d.mastered ? "glow-edge" : ""));

    const node = g
      .append("g")
      .selectAll("g")
      .data(nodes)
      .join("g")
      .style("cursor", "grab")
      .call(
        d3
          .drag<SVGGElement, ConceptNode>()
          .on("start", (event, d) => {
            if (!event.active) sim.alphaTarget(0.3).restart();
            d.fx = d.x; d.fy = d.y;
          })
          .on("drag", (event, d) => { d.fx = event.x; d.fy = event.y; })
          .on("end", (event, d) => {
            if (!event.active) sim.alphaTarget(0);
            d.fx = null; d.fy = null;
          }),
      );

    // Outer halo for mastered nodes
    node
      .append("circle")
      .attr("r", (d) => 22 + d.mastery * 16)
      .attr("fill", "url(#node-grad)")
      .attr("opacity", (d) => (d.mastery >= MASTERY_THRESHOLD ? 1 : 0));

    node
      .append("circle")
      .attr("r", (d) => 18 + d.mastery * 14)
      .attr("fill", (d) =>
        d.mastery >= MASTERY_THRESHOLD ? "var(--color-secondary)"
          : d.mastery >= 0.5 ? "var(--color-ring)"
          : "var(--color-accent)",
      )
      .attr("stroke", "white")
      .attr("stroke-width", 2.5)
      .attr("class", (d) => (d.mastery >= MASTERY_THRESHOLD ? "glow-strong" : ""));

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

    return () => { sim.stop(); };
  }, [nodes, edges, masteryById]);

  return (
    <div className="card flex h-full flex-col p-5">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h2 className="text-lg">Knowledge Graph</h2>
          <p className="text-sm" style={{ opacity: 0.6 }}>
            {topic ? <>Topic: <span style={{ fontWeight: 600 }}>{topic}</span></> : "Drag nodes · size = mastery"}
          </p>
        </div>
        <Legend />
      </div>
      <svg ref={svgRef} className="mt-3 flex-1 w-full" role="img" aria-label="Knowledge graph" />
    </div>
  );
}

function Legend() {
  const items: { color: string; label: string; glow?: boolean }[] = [
    { color: "var(--color-secondary)", label: "Mastered", glow: true },
    { color: "var(--color-ring)",      label: "Learning" },
    { color: "var(--color-accent)",    label: "Weak" },
  ];
  return (
    <ul className="flex flex-wrap gap-2 text-xs">
      {items.map((it) => (
        <li
          key={it.label}
          className="flex items-center gap-1.5 rounded-full px-2.5 py-1"
          style={{ background: "rgba(255,255,255,0.6)", border: "1px solid var(--glass-border)" }}
        >
          <span
            aria-hidden
            className={`inline-block h-2.5 w-2.5 rounded-full ${it.glow ? "glow-strong" : ""}`}
            style={{ background: it.color }}
          />
          {it.label}
        </li>
      ))}
    </ul>
  );
}
