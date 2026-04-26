"use client";
import { useEffect, useRef } from "react";

interface GNode {
  id: number;
  x: number;
  y: number;
  vx: number;
  vy: number;
  r: number;
  primary: boolean;
  born: number;
}
interface GEdge {
  a: number;
  b: number;
}

const MAX_NODES = 56;

export function KnowledgeGraph() {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const container = containerRef.current!;
    const canvas = canvasRef.current!;
    if (!container || !canvas) return;

    const ctx = canvas.getContext("2d")!;
    if (!ctx) return;

    const nodes: GNode[] = [];
    const edges: GEdge[] = [];
    const nodeMap = new Map<number, GNode>();
    let nextId = 0;
    let raf: number;
    let spawnTimeout: ReturnType<typeof setTimeout>;

    function resize() {
      const dpr = window.devicePixelRatio || 1;
      const w = container.offsetWidth;
      const h = container.offsetHeight;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      canvas.style.width = w + "px";
      canvas.style.height = h + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    const ro = new ResizeObserver(resize);
    ro.observe(container);
    resize();

    function addNode() {
      if (nodes.length >= MAX_NODES) return;
      const w = container.offsetWidth;
      const h = container.offsetHeight;
      const cx = w * 0.48;
      const cy = h * 0.5;
      const spread = Math.min(w, h) * 0.38;
      const isPrimary = Math.random() < 0.28;
      const node: GNode = {
        id: nextId++,
        x: cx + (Math.random() - 0.5) * spread * 2,
        y: cy + (Math.random() - 0.5) * spread * 1.7,
        vx: (Math.random() - 0.5) * 1.2,
        vy: (Math.random() - 0.5) * 1.2,
        r: isPrimary ? 7 + Math.random() * 8 : 2.5 + Math.random() * 4.5,
        primary: isPrimary,
        born: performance.now(),
      };
      if (nodes.length > 0) {
        const numLinks = Math.min(nodes.length, 1 + Math.floor(Math.random() * 2));
        const shuffled = [...nodes].sort(() => Math.random() - 0.5).slice(0, numLinks);
        for (const n of shuffled) edges.push({ a: node.id, b: n.id });
      }
      nodes.push(node);
      nodeMap.set(node.id, node);
    }

    function scheduleSpawn() {
      if (nodes.length >= MAX_NODES) return;
      // Exponential backoff: starts at ~500ms, grows to ~6s near limit
      const delay = Math.min(500 * Math.pow(1.09, nodes.length), 6000);
      spawnTimeout = setTimeout(() => {
        addNode();
        scheduleSpawn();
      }, delay);
    }

    // Seed initial cluster
    for (let i = 0; i < 8; i++) addNode();
    scheduleSpawn();

    function physics() {
      const w = container.offsetWidth;
      const h = container.offsetHeight;
      const n = nodes.length;

      // Repulsion between all node pairs
      for (let i = 0; i < n; i++) {
        for (let j = i + 1; j < n; j++) {
          const a = nodes[i];
          const b = nodes[j];
          const dx = b.x - a.x;
          const dy = b.y - a.y;
          const d2 = dx * dx + dy * dy + 1;
          const d = Math.sqrt(d2);
          const f = Math.min(2000 / d2, 2.5);
          const fx = (dx / d) * f;
          const fy = (dy / d) * f;
          a.vx -= fx;
          a.vy -= fy;
          b.vx += fx;
          b.vy += fy;
        }
      }

      // Spring attraction along edges
      for (const e of edges) {
        const a = nodeMap.get(e.a);
        const b = nodeMap.get(e.b);
        if (!a || !b) continue;
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const d = Math.sqrt(dx * dx + dy * dy) || 1;
        const rest = 88;
        const f = (d - rest) * 0.005;
        const fx = (dx / d) * f;
        const fy = (dy / d) * f;
        a.vx += fx;
        a.vy += fy;
        b.vx -= fx;
        b.vy -= fy;
      }

      // Weak center gravity
      const cx = w * 0.48;
      const cy = h * 0.5;
      for (const node of nodes) {
        node.vx += (cx - node.x) * 0.00006;
        node.vy += (cy - node.y) * 0.00006;
        // Damping — floaty feel
        node.vx *= 0.91;
        node.vy *= 0.91;
        // Clamp to boundary
        node.x = Math.max(node.r, Math.min(w - node.r, node.x + node.vx));
        node.y = Math.max(node.r, Math.min(h - node.r, node.y + node.vy));
      }
    }

    function draw() {
      const w = container.offsetWidth;
      const h = container.offsetHeight;
      const now = performance.now();
      ctx.clearRect(0, 0, w, h);

      // Edges
      for (const e of edges) {
        const a = nodeMap.get(e.a);
        const b = nodeMap.get(e.b);
        if (!a || !b) continue;
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const d = Math.sqrt(dx * dx + dy * dy);
        if (d > 260) continue;
        const edgeAge = Math.min((now - Math.max(a.born, b.born)) / 900, 1);
        const opacity = 0.2 * (1 - d / 260) * edgeAge;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.strokeStyle = `rgba(196,152,90,${opacity})`;
        ctx.lineWidth = 0.55;
        ctx.stroke();
      }

      // Nodes
      for (const node of nodes) {
        const age = Math.min((now - node.born) / 700, 1);
        if (age <= 0) continue;

        if (node.primary) {
          // Soft glow
          const grd = ctx.createRadialGradient(node.x, node.y, 0, node.x, node.y, node.r * 3.2);
          grd.addColorStop(0, `rgba(196,152,90,${0.18 * age})`);
          grd.addColorStop(1, `rgba(196,152,90,0)`);
          ctx.beginPath();
          ctx.arc(node.x, node.y, node.r * 3.2, 0, Math.PI * 2);
          ctx.fillStyle = grd;
          ctx.fill();
        }

        // Node body — scales in on birth
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.r * age, 0, Math.PI * 2);
        ctx.fillStyle = node.primary
          ? `rgba(196,152,90,${age})`
          : `rgba(123,158,130,${age})`;
        ctx.fill();
      }
    }

    function loop() {
      physics();
      draw();
      raf = requestAnimationFrame(loop);
    }

    loop();

    return () => {
      cancelAnimationFrame(raf);
      clearTimeout(spawnTimeout);
      ro.disconnect();
    };
  }, []);

  return (
    <div ref={containerRef} className="absolute inset-0">
      <canvas ref={canvasRef} style={{ display: "block" }} />
    </div>
  );
}
