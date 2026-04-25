'use client';
import { useEffect, useRef, useState } from 'react';
import { useAuthStore } from '@/lib/store';

interface NetworkNode {
  id: string;
  label: string;
  mastery: number;
  status: 'active' | 'waiting';
}

interface NetworkLink {
  source: string;
  target: string;
  type: 'active' | 'pending';
}

interface TopologyData {
  nodes: NetworkNode[];
  links: NetworkLink[];
  health: { active_peers: number; total_waiting: number; active_sessions: number };
}

export default function NetworkTopology() {
  const svgRef = useRef<SVGSVGElement>(null);
  const { token } = useAuthStore();
  const [topology, setTopology] = useState<TopologyData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) return;

    async function fetchTopology() {
      try {
        const res = await fetch('/api/network/analytics', {
          headers: { Authorization: `Bearer ${token}` },
        });
        const data = await res.json();

        const nodes: NetworkNode[] = data.routing_table
          .filter((r: { peers_available: number }) => r.peers_available > 0)
          .slice(0, 12)
          .map(
            (r: { concept_id: number; concept: string; peers_available: number }, i: number) => ({
              id: `concept_${r.concept_id}`,
              label: r.concept,
              mastery: 0.6 + (i % 4) * 0.1,
              status: r.peers_available > 2 ? 'active' : 'waiting',
            }),
          );

        const links: NetworkLink[] = [];
        for (let i = 0; i < Math.min(nodes.length - 1, 8); i++) {
          links.push({
            source: nodes[i].id,
            target: nodes[i + 1].id,
            type: i % 3 === 0 ? 'active' : 'pending',
          });
        }

        setTopology({ nodes, links, health: data.network_health });
      } catch {
        // network fetch failed silently
      } finally {
        setLoading(false);
      }
    }

    fetchTopology();
    const interval = setInterval(fetchTopology, 5000);
    return () => clearInterval(interval);
  }, [token]);

  useEffect(() => {
    if (!topology || !svgRef.current) return;

    import('d3').then((d3) => {
      const svg = d3.select(svgRef.current!);
      svg.selectAll('*').remove();

      const width = svgRef.current!.clientWidth || 480;
      const height = 280;

      type SimNode = NetworkNode & d3.SimulationNodeDatum;
      const simNodes: SimNode[] = topology.nodes.map((n) => ({ ...n }));
      const nodeById = new Map(simNodes.map((n) => [n.id, n]));

      type SimLink = { source: SimNode; target: SimNode; type: string };
      const simLinks: SimLink[] = topology.links
        .map((l) => ({
          source: nodeById.get(l.source)!,
          target: nodeById.get(l.target)!,
          type: l.type,
        }))
        .filter((l) => l.source && l.target);

      const simulation = d3
        .forceSimulation<SimNode>(simNodes)
        .force('link', d3.forceLink<SimNode, SimLink>(simLinks).id((d) => d.id).distance(80))
        .force('charge', d3.forceManyBody().strength(-100))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide(28));

      const link = svg
        .append('g')
        .selectAll<SVGLineElement, SimLink>('line')
        .data(simLinks)
        .join('line')
        .attr('stroke', (d) => (d.type === 'active' ? '#4ade80' : '#fbbf24'))
        .attr('stroke-width', (d) => (d.type === 'active' ? 2 : 1))
        .attr('stroke-dasharray', (d) => (d.type === 'pending' ? '4,4' : null))
        .attr('opacity', 0.6);

      const nodeG = svg
        .append('g')
        .selectAll<SVGGElement, SimNode>('g')
        .data(simNodes)
        .join('g');

      nodeG
        .append('circle')
        .attr('r', (d) => 10 + d.mastery * 8)
        .attr('fill', (d) =>
          d.status === 'active' ? 'rgba(74,222,128,0.2)' : 'rgba(251,191,36,0.2)',
        )
        .attr('stroke', (d) => (d.status === 'active' ? '#4ade80' : '#fbbf24'))
        .attr('stroke-width', 1.5);

      nodeG
        .append('text')
        .text((d) => d.label.slice(0, 14))
        .attr('text-anchor', 'middle')
        .attr('dy', '0.35em')
        .attr('font-size', '9px')
        .attr('fill', '#e5e7eb');

      simulation.on('tick', () => {
        link
          .attr('x1', (d) => (d.source as SimNode).x ?? 0)
          .attr('y1', (d) => (d.source as SimNode).y ?? 0)
          .attr('x2', (d) => (d.target as SimNode).x ?? 0)
          .attr('y2', (d) => (d.target as SimNode).y ?? 0);
        nodeG.attr('transform', (d) => `translate(${d.x ?? 0},${d.y ?? 0})`);
      });

      return () => simulation.stop();
    });
  }, [topology]);

  return (
    <div className="rounded-xl border border-green-500/20 bg-green-500/5 p-3">
      <div className="flex items-center justify-between mb-3">
        <span className="text-[10px] font-bold uppercase tracking-widest text-green-400">
          Live Network Topology
        </span>
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1">
            <div className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
            <span className="text-[9px] text-green-400">LIVE</span>
          </div>
          <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-green-500/15 text-green-400 border border-green-500/20">
            arista ↗
          </span>
        </div>
      </div>

      {loading ? (
        <div className="h-[280px] flex items-center justify-center text-t3 text-xs">
          Loading topology…
        </div>
      ) : (
        <svg ref={svgRef} className="w-full" height={280} />
      )}

      <div className="flex items-center gap-4 mt-2 text-[9px] text-t3">
        <div className="flex items-center gap-1">
          <div className="w-4 bg-green-400" style={{ height: 1 }} />
          <span>Active session</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-4 border-t border-dashed border-yellow-400" />
          <span>Pending match</span>
        </div>
      </div>

      {topology?.health && (
        <div className="flex gap-4 mt-3 pt-3 border-t border-white/5 text-[10px] text-t2">
          <span>
            Active:{' '}
            <span className="text-green-400 font-semibold">{topology.health.active_peers}</span>
          </span>
          <span>
            Queue:{' '}
            <span className="text-yellow-400 font-semibold">{topology.health.total_waiting}</span>
          </span>
          <span>
            Sessions:{' '}
            <span className="text-blue-400 font-semibold">{topology.health.active_sessions}</span>
          </span>
        </div>
      )}
    </div>
  );
}
