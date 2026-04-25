'use client';
import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

interface Node {
  id: string;
  label: string;
  kind: 'self' | 'tutor' | 'co_learner';
  score?: number;
}

interface Edge {
  source: string;
  target: string;
  weight: number;
}

interface Props {
  nodes: Node[];
  edges: Edge[];
  width?: number;
  height?: number;
}

const KIND_COLOR: Record<Node['kind'], string> = {
  self: '#2dd4a4',
  tutor: '#f5834a',
  co_learner: '#5b9fff',
};

export default function NetworkTopology({ nodes, edges, width = 560, height = 320 }: Props) {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current) return;
    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    if (nodes.length <= 1) {
      svg
        .append('text')
        .attr('x', width / 2)
        .attr('y', height / 2)
        .attr('fill', '#64748b')
        .attr('text-anchor', 'middle')
        .attr('font-size', 12)
        .text('No peers in routing table yet');
      return;
    }

    interface SimNode extends d3.SimulationNodeDatum, Node {}
    interface SimLink extends d3.SimulationLinkDatum<SimNode> {
      weight: number;
    }

    const simNodes: SimNode[] = nodes.map((n) => ({ ...n }));
    const idToNode = new Map(simNodes.map((n) => [n.id, n]));
    const simLinks: SimLink[] = [];
    for (const e of edges) {
      const s = idToNode.get(e.source);
      const t = idToNode.get(e.target);
      if (!s || !t) continue;
      simLinks.push({ source: s, target: t, weight: e.weight });
    }

    const sim = d3
      .forceSimulation(simNodes)
      .force(
        'link',
        d3
          .forceLink<SimNode, SimLink>(simLinks)
          .id((d) => d.id)
          .distance((d) => 60 + (1 - d.weight) * 120)
          .strength((d) => Math.max(0.1, d.weight)),
      )
      .force('charge', d3.forceManyBody<SimNode>().strength(-260))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide<SimNode>().radius(28));

    const link = svg
      .append('g')
      .selectAll('line')
      .data(simLinks)
      .join('line')
      .attr('stroke', '#f5834a')
      .attr('stroke-opacity', (d) => 0.2 + d.weight * 0.6)
      .attr('stroke-width', (d) => 1 + d.weight * 4);

    const linkLabel = svg
      .append('g')
      .selectAll('text')
      .data(simLinks)
      .join('text')
      .attr('font-size', 9)
      .attr('font-family', 'monospace')
      .attr('fill', '#94a3b8')
      .attr('text-anchor', 'middle')
      .text((d) => `srp ${d.weight.toFixed(2)}`);

    const nodeG = svg
      .append('g')
      .selectAll<SVGGElement, SimNode>('g')
      .data(simNodes)
      .join('g')
      .style('cursor', 'pointer');

    nodeG
      .append('circle')
      .attr('r', (d) => (d.kind === 'self' ? 16 : 12))
      .attr('fill', (d) => KIND_COLOR[d.kind])
      .attr('fill-opacity', 0.18)
      .attr('stroke', (d) => KIND_COLOR[d.kind])
      .attr('stroke-width', 1.5);

    nodeG
      .append('text')
      .attr('text-anchor', 'middle')
      .attr('dominant-baseline', 'central')
      .attr('font-size', (d) => (d.kind === 'self' ? 10 : 9))
      .attr('font-weight', 700)
      .attr('fill', (d) => KIND_COLOR[d.kind])
      .text((d) => (d.kind === 'self' ? 'YOU' : d.label.slice(0, 2).toUpperCase()));

    nodeG
      .append('text')
      .attr('text-anchor', 'middle')
      .attr('y', 26)
      .attr('font-size', 9)
      .attr('font-family', 'monospace')
      .attr('fill', '#94a3b8')
      .text((d) => (d.kind === 'self' ? 'self' : d.label.slice(0, 14)));

    nodeG.call(
      d3
        .drag<SVGGElement, SimNode>()
        .on('start', (event, d) => {
          if (!event.active) sim.alphaTarget(0.3).restart();
          d.fx = d.x; d.fy = d.y;
        })
        .on('drag', (event, d) => { d.fx = event.x; d.fy = event.y; })
        .on('end', (event, d) => {
          if (!event.active) sim.alphaTarget(0);
          d.fx = null; d.fy = null;
        }),
    );

    sim.on('tick', () => {
      link
        .attr('x1', (d) => (d.source as SimNode).x ?? 0)
        .attr('y1', (d) => (d.source as SimNode).y ?? 0)
        .attr('x2', (d) => (d.target as SimNode).x ?? 0)
        .attr('y2', (d) => (d.target as SimNode).y ?? 0);
      linkLabel
        .attr('x', (d) => (((d.source as SimNode).x ?? 0) + ((d.target as SimNode).x ?? 0)) / 2)
        .attr('y', (d) => (((d.source as SimNode).y ?? 0) + ((d.target as SimNode).y ?? 0)) / 2 - 4);
      nodeG.attr('transform', (d) => `translate(${d.x ?? 0},${d.y ?? 0})`);
    });

    return () => { sim.stop(); };
  }, [nodes, edges, width, height]);

  return (
    <svg
      ref={svgRef}
      width="100%"
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      className="rounded-xl bg-bg2 border border-ora/15"
      preserveAspectRatio="xMidYMid meet"
    />
  );
}
