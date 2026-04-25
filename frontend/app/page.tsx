'use client';
import { useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store';
import Link from 'next/link';
import * as d3 from 'd3';

const FEATURES = [
  { num: '01', label: 'Fetch.ai Agents', desc: '6 parallel agents fire on every question' },
  { num: '02', label: 'Live Concept Map', desc: 'D3 knowledge graph updates as you learn' },
  { num: '03', label: 'Voice Interface', desc: 'Speak questions, hear Socratic answers' },
  { num: '04', label: 'Verified Outputs', desc: 'Every response checked for hallucinations' },
  { num: '05', label: 'Peer Matching', desc: 'Arista-style routing to study partners' },
  { num: '06', label: 'Session Replay', desc: 'Every agent decision logged and replayable' },
];

function KnowledgeGraph() {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current) return;

    const W = 920;
    const H = 920;
    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const linkG = svg.append('g').attr('class', 'kg-links');
    const nodeG = svg.append('g').attr('class', 'kg-nodes');

    // Anchor the cluster on the right side of the viewBox
    const CX = W * 0.68;
    const CY = H / 2;

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const nodes: any[] = [
      { id: 'root', x: CX, y: CY, size: 10, color: '#C4985A' },
    ];
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const links: any[] = [];

    const sim = d3
      .forceSimulation(nodes)
      .force('charge', d3.forceManyBody().strength(-95).distanceMax(260))
      .force(
        'link',
        d3
          .forceLink(links)
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          .id((d: any) => d.id)
          .distance(95)
          .strength(0.32)
      )
      // Centering pulls — pinned to the right side of the viewBox
      .force('x', d3.forceX(CX).strength(0.06))
      .force('y', d3.forceY(CY).strength(0.06))
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      .force('collide', d3.forceCollide().radius((d: any) => d.size + 9))
      .alphaDecay(0.006)
      .alphaMin(0)
      .alphaTarget(0.018) // perpetual gentle jiggle
      .velocityDecay(0.6);

    const paint = () => {
      // Links
      const linkSel = linkG
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .selectAll<SVGLineElement, any>('line')
        .data(links);
      linkSel
        .enter()
        .append('line')
        .attr('stroke', '#C4985A')
        .attr('stroke-width', 0.5)
        .attr('stroke-opacity', 0)
        .transition()
        .duration(900)
        .attr('stroke-opacity', 0.22);

      // Nodes
      const nodeSel = nodeG
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .selectAll<SVGCircleElement, any>('circle')
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .data(nodes, (d: any) => d.id);
      nodeSel
        .enter()
        .append('circle')
        .attr('r', 0)
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .attr('fill', (d: any) => d.color)
        .attr('opacity', 0)
        .transition()
        .duration(700)
        .ease(d3.easeBackOut.overshoot(1.4))
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .attr('r', (d: any) => d.size)
        .attr('opacity', 0.9);
    };

    sim.on('tick', () => {
      // Hard wall: bounce nodes back if they reach the edge
      const PAD = 6;
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      nodes.forEach((n: any) => {
        const r = n.size + PAD;
        if (n.x < r) { n.x = r; n.vx = Math.abs(n.vx || 0) * 0.3; }
        if (n.x > W - r) { n.x = W - r; n.vx = -Math.abs(n.vx || 0) * 0.3; }
        if (n.y < r) { n.y = r; n.vy = Math.abs(n.vy || 0) * 0.3; }
        if (n.y > H - r) { n.y = H - r; n.vy = -Math.abs(n.vy || 0) * 0.3; }
      });

      linkG
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .selectAll<SVGLineElement, any>('line')
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .attr('x1', (d: any) => d.source.x)
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .attr('y1', (d: any) => d.source.y)
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .attr('x2', (d: any) => d.target.x)
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .attr('y2', (d: any) => d.target.y);
      nodeG
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .selectAll<SVGCircleElement, any>('circle')
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .attr('cx', (d: any) => d.x)
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .attr('cy', (d: any) => d.y);
    });

    paint();

    let counter = 1;
    let timer: ReturnType<typeof setTimeout> | null = null;
    const HARD_CAP = 54;

    const addNode = () => {
      const parent = nodes[Math.floor(Math.random() * nodes.length)];
      const useGold = Math.random() < 0.62;
      const big = Math.random() < 0.12;
      const angle = Math.random() * Math.PI * 2;

      const newNode = {
        id: `n${counter++}`,
        x: parent.x + Math.cos(angle) * 30,
        y: parent.y + Math.sin(angle) * 30,
        size: big ? 8.5 : 3.5 + Math.random() * 2.5,
        color: useGold ? '#C4985A' : '#7B9E82',
      };

      nodes.push(newNode);
      links.push({ source: parent.id, target: newNode.id });

      if (Math.random() < 0.28 && nodes.length > 5) {
        const other = nodes[Math.floor(Math.random() * (nodes.length - 1))];
        if (other.id !== parent.id && other.id !== newNode.id) {
          links.push({ source: other.id, target: newNode.id });
        }
      }

      sim.nodes(nodes);
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (sim.force('link') as any).links(links);
      sim.alpha(0.55).restart();

      paint();
    };

    // Recursive scheduler — fast at first, slows as graph fills, stops at HARD_CAP
    const schedule = () => {
      if (nodes.length >= HARD_CAP) return;
      const n = nodes.length;
      const delay = Math.min(1600, 200 + Math.pow(Math.max(0, n - 3), 1.5) * 5);
      timer = setTimeout(() => {
        addNode();
        schedule();
      }, delay);
    };
    schedule();

    return () => {
      if (timer) clearTimeout(timer);
      sim.stop();
    };
  }, []);

  return (
    <svg
      ref={svgRef}
      viewBox="0 0 920 920"
      style={{ width: '100%', height: '100%', overflow: 'visible' }}
    />
  );
}

export default function Home() {
  const { token } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (token) router.push('/learn');
  }, [token, router]);

  return (
    <div className="sl">
        <section className="sl-hero">
          <div>
            <h1 className="sl-h1">
              SAGE<span className="period">.</span>
            </h1>
            <p className="sl-desc">
              Six AI agents question, challenge, and guide you toward genuine
              understanding — not rote answers.
            </p>
            <div className="sl-ctas">
              <Link href="/register" className="sl-cta-p">Begin Learning →</Link>
              <Link href="/login" className="sl-cta-s">Sign In</Link>
            </div>
          </div>

          <div className="sl-orbital">
            <KnowledgeGraph />
          </div>
        </section>

        <div className="sl-sep">
          <div className="sl-sep-inner">
            <span className="sl-sep-label">01 — 06 · Capabilities</span>
          </div>
        </div>

        <div className="sl-features">
          {FEATURES.map((f) => (
            <div key={f.num} className="sl-feat">
              <div className="sl-feat-num">{f.num}</div>
              <div className="sl-feat-lbl">{f.label}</div>
              <div className="sl-feat-desc">{f.desc}</div>
            </div>
          ))}
        </div>

        <footer className="sl-footer">
          <span className="sl-footer-t">Fetch.ai Powered · Multi-Agent Architecture</span>
          <span className="sl-footer-t">LA Hacks 2026</span>
        </footer>
    </div>
  );
}
