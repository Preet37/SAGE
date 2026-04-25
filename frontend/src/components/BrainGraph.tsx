"use client";

import * as d3 from "d3";
import { useEffect, useRef } from "react";

import { MasteredTopic, brainScale } from "@/lib/mastery";

interface BrainGraphProps {
  mastered: MasteredTopic[];
  highlightId?: string | null;
}

interface SimNode extends d3.SimulationNodeDatum {
  id: string;
  label: string;
  isBrain: boolean;
  scale?: number;
  highlight?: boolean;
}

interface SimLink extends d3.SimulationLinkDatum<SimNode> {
  source: string | SimNode;
  target: string | SimNode;
}

export default function BrainGraph({ mastered, highlightId }: BrainGraphProps) {
  const svgRef = useRef<SVGSVGElement | null>(null);

  useEffect(() => {
    const svgEl = svgRef.current;
    if (!svgEl) return;
    const svg = d3.select(svgEl);
    const { width, height } = svgEl.getBoundingClientRect();
    if (!width || !height) return;
    svg.selectAll("*").remove();

    const scale = brainScale(mastered.length);

    const defs = svg.append("defs");

    const glow = defs.append("filter").attr("id", "brain-glow")
      .attr("x", "-50%").attr("y", "-50%").attr("width", "200%").attr("height", "200%");
    glow.append("feGaussianBlur").attr("stdDeviation", 6).attr("result", "blur");
    const merge = glow.append("feMerge");
    merge.append("feMergeNode").attr("in", "blur");
    merge.append("feMergeNode").attr("in", "SourceGraphic");

    const grad = defs.append("radialGradient").attr("id", "brain-grad");
    grad.append("stop").attr("offset", "0%").attr("stop-color", "#A78BFA").attr("stop-opacity", 0.95);
    grad.append("stop").attr("offset", "60%").attr("stop-color", "#6C5CE7").attr("stop-opacity", 0.85);
    grad.append("stop").attr("offset", "100%").attr("stop-color", "#4C3FAA").attr("stop-opacity", 0.9);

    const nodeGrad = defs.append("radialGradient").attr("id", "node-grad-2");
    nodeGrad.append("stop").attr("offset", "0%").attr("stop-color", "white").attr("stop-opacity", 0.85);
    nodeGrad.append("stop").attr("offset", "100%").attr("stop-color", "white").attr("stop-opacity", 0);

    const nodes: SimNode[] = [
      { id: "__brain__", label: "BRAIN", isBrain: true, scale, fx: width / 2, fy: height / 2 },
      ...mastered.map<SimNode>((t) => ({
        id: t.id,
        label: t.label,
        isBrain: false,
        highlight: t.id === highlightId,
      })),
    ];
    const links: SimLink[] = mastered.map((t) => ({ source: "__brain__", target: t.id }));

    const sim = d3.forceSimulation<SimNode>(nodes)
      .force("link", d3.forceLink<SimNode, SimLink>(links).id((d) => d.id).distance(140 + scale * 20))
      .force("charge", d3.forceManyBody().strength(-340))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collide", d3.forceCollide(48));

    const g = svg.append("g");

    const link = g.append("g")
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("stroke", "#6C5CE7")
      .attr("stroke-opacity", 0.45)
      .attr("stroke-width", 2);

    const node = g.append("g")
      .selectAll<SVGGElement, SimNode>("g")
      .data(nodes)
      .join("g")
      .style("cursor", (d) => (d.isBrain ? "default" : "grab"))
      .call(
        d3.drag<SVGGElement, SimNode>()
          .filter((_, d) => !d.isBrain)
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

    // Brain
    const brain = node.filter((d) => d.isBrain);
    const baseR = 56;
    brain.append("circle")
      .attr("r", baseR * scale + 18)
      .attr("fill", "url(#node-grad-2)");
    brain.append("circle")
      .attr("r", baseR * scale)
      .attr("fill", "url(#brain-grad)")
      .attr("stroke", "white")
      .attr("stroke-width", 3)
      .attr("filter", "url(#brain-glow)");
    brain.append("text")
      .text("🧠")
      .attr("text-anchor", "middle")
      .attr("dy", baseR * scale * 0.32)
      .attr("font-size", baseR * scale * 0.95)
      .attr("pointer-events", "none");
    brain.append("text")
      .text(`${mastered.length} mastered`)
      .attr("text-anchor", "middle")
      .attr("dy", baseR * scale + 20)
      .attr("fill", "var(--color-foreground)")
      .attr("font-family", "var(--font-heading)")
      .attr("font-weight", 700)
      .attr("font-size", 11)
      .attr("opacity", 0.7)
      .attr("pointer-events", "none");

    // Mastered topics
    const topic = node.filter((d) => !d.isBrain);
    topic.append("circle")
      .attr("r", 30)
      .attr("fill", "url(#node-grad-2)")
      .attr("opacity", (d) => (d.highlight ? 1 : 0.35));
    topic.append("circle")
      .attr("r", 22)
      .attr("fill", (d) => (d.highlight ? "#F59E0B" : "#6C5CE7"))
      .attr("stroke", "white")
      .attr("stroke-width", 2.5)
      .attr("class", (d) => (d.highlight ? "glow-strong" : ""));
    topic.append("text")
      .text((d) => (d.label.length > 14 ? d.label.slice(0, 13) + "…" : d.label))
      .attr("text-anchor", "middle")
      .attr("dy", 4)
      .attr("fill", "white")
      .attr("font-family", "var(--font-heading)")
      .attr("font-weight", 600)
      .attr("font-size", 10)
      .attr("pointer-events", "none");

    sim.on("tick", () => {
      link
        .attr("x1", (d) => (d.source as SimNode).x ?? 0)
        .attr("y1", (d) => (d.source as SimNode).y ?? 0)
        .attr("x2", (d) => (d.target as SimNode).x ?? 0)
        .attr("y2", (d) => (d.target as SimNode).y ?? 0);
      node.attr("transform", (d) => `translate(${d.x ?? 0},${d.y ?? 0})`);
    });

    return () => { sim.stop(); };
  }, [mastered, highlightId]);

  return (
    <div className="card flex h-full flex-col p-5">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h2 className="text-lg" style={{ fontFamily: "var(--font-heading)" }}>Knowledge Graph</h2>
          <p className="text-sm" style={{ opacity: 0.6 }}>
            {mastered.length === 0
              ? "Master your first topic to grow your brain."
              : `Brain expands every 15 mastered topics — ${mastered.length}/${(Math.floor(mastered.length / 15) + 1) * 15} to next stage.`}
          </p>
        </div>
      </div>
      <svg ref={svgRef} className="mt-3 flex-1 w-full" role="img" aria-label="Brain knowledge graph" />
    </div>
  );
}
