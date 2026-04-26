"use client";
import { useEffect, useState, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import { AppHeader } from "@/components/AppHeader";
import { getToken } from "@/lib/auth";
import { API_URL } from "@/lib/api";
import { Trophy, Flame, Star, Zap, BookOpen } from "lucide-react";

interface GalaxyNode {
  id: string;
  label: string;
  module_id: string;
  module_name: string;
  path_id: string;
  path_name: string;
  completed: boolean;
  order_index: number;
}
interface GalaxyEdge { source: string; target: string; }
interface GalaxyRank { rank: number; total_users: number; score: number; percentile: number; }
interface GalaxyData {
  nodes: GalaxyNode[];
  edges: GalaxyEdge[];
  rank: GalaxyRank;
  total_lessons: number;
  completed_count: number;
  streak_days: number;
}

// Deterministic position from a stable hash
function hashPos(id: string, w: number, h: number): [number, number] {
  let h1 = 5381, h2 = 52711;
  for (let i = 0; i < id.length; i++) {
    const c = id.charCodeAt(i);
    h1 = ((h1 << 5) + h1) ^ c;
    h2 = ((h2 << 5) + h2) ^ c;
  }
  const u = Math.abs(h1) / 2147483647;
  const v = Math.abs(h2) / 2147483647;
  const r = 0.1 + u * 0.85;
  const angle = v * Math.PI * 2;
  return [w / 2 + r * (w / 2 - 60) * Math.cos(angle), h / 2 + r * (h / 2 - 60) * Math.sin(angle)];
}

// Color per path
const PATH_COLORS: Record<string, string> = {};
const PALETTE = ["#58a6ff", "#f78166", "#56d364", "#f0883e", "#bc8cff", "#79c0ff", "#ffa657", "#d2a8ff"];
let colorIdx = 0;
function pathColor(pathId: string) {
  if (!PATH_COLORS[pathId]) PATH_COLORS[pathId] = PALETTE[colorIdx++ % PALETTE.length];
  return PATH_COLORS[pathId];
}

export default function GalaxyPage() {
  const router = useRouter();
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [data, setData] = useState<GalaxyData | null>(null);
  const [hovered, setHovered] = useState<GalaxyNode | null>(null);
  const [tooltip, setTooltip] = useState<{ x: number; y: number } | null>(null);
  const animRef = useRef<number>(0);
  const timeRef = useRef(0);
  const posCache = useRef<Map<string, [number, number]>>(new Map());

  useEffect(() => {
    const token = getToken();
    if (!token) { router.push("/login"); return; }
    fetch(`${API_URL}/progress/galaxy`, { headers: { Authorization: `Bearer ${token}` } })
      .then((r) => r.json())
      .then(setData)
      .catch(console.error);
  }, [router]);

  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas || !data) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    const W = canvas.width, H = canvas.height;
    timeRef.current += 0.005;
    const t = timeRef.current;

    // Background
    ctx.fillStyle = "#090d14";
    ctx.fillRect(0, 0, W, H);

    // Nebula glow
    const grad = ctx.createRadialGradient(W / 2, H / 2, 0, W / 2, H / 2, W * 0.6);
    grad.addColorStop(0, "rgba(31,111,235,0.05)");
    grad.addColorStop(0.5, "rgba(188,140,255,0.03)");
    grad.addColorStop(1, "transparent");
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, W, H);

    // Pre-compute positions
    if (posCache.current.size !== data.nodes.length) {
      posCache.current.clear();
      for (const node of data.nodes) {
        posCache.current.set(node.id, hashPos(node.id, W, H));
      }
    }
    const pos = (id: string) => posCache.current.get(id) ?? [W / 2, H / 2];

    // Draw edges
    for (const edge of data.edges) {
      const [x1, y1] = pos(edge.source);
      const [x2, y2] = pos(edge.target);
      const srcNode = data.nodes.find((n) => n.id === edge.source);
      const completed = srcNode?.completed ?? false;
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.strokeStyle = completed ? "rgba(88,166,255,0.25)" : "rgba(255,255,255,0.04)";
      ctx.lineWidth = completed ? 1 : 0.5;
      ctx.stroke();
    }

    // Draw nodes
    for (const node of data.nodes) {
      const [x, y] = pos(node.id);
      const color = pathColor(node.path_id);
      const isHov = hovered?.id === node.id;
      const pulse = node.completed ? 1 + 0.15 * Math.sin(t * 2 + x * 0.01) : 1;
      const r = (node.completed ? 6 : 3.5) * pulse + (isHov ? 3 : 0);

      if (node.completed) {
        // Glow ring
        const glow = ctx.createRadialGradient(x, y, 0, x, y, r * 3.5);
        glow.addColorStop(0, color + "55");
        glow.addColorStop(1, "transparent");
        ctx.fillStyle = glow;
        ctx.beginPath(); ctx.arc(x, y, r * 3.5, 0, Math.PI * 2); ctx.fill();
      }

      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fillStyle = node.completed ? color : "rgba(255,255,255,0.18)";
      ctx.fill();

      if (isHov) {
        ctx.strokeStyle = "#fff";
        ctx.lineWidth = 1.5;
        ctx.stroke();
      }
    }

    // Labels for hovered node
    if (hovered && tooltip) {
      const [x, y] = pos(hovered.id);
      const text = hovered.label;
      ctx.font = "bold 12px -apple-system, sans-serif";
      const tw = ctx.measureText(text).width;
      const px = 8, py = 5;
      const bx = x + 14, by = y - 20;
      ctx.fillStyle = "rgba(15,17,23,0.92)";
      ctx.beginPath();
      ctx.roundRect(bx - px, by - py - 12, tw + px * 2, 22, 6);
      ctx.fill();
      ctx.fillStyle = hovered.completed ? "#79c0ff" : "#8b949e";
      ctx.fillText(text, bx, by);
    }

    animRef.current = requestAnimationFrame(draw);
  }, [data, hovered, tooltip]);

  useEffect(() => {
    animRef.current = requestAnimationFrame(draw);
    return () => cancelAnimationFrame(animRef.current);
  }, [draw]);

  // Handle canvas resize
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const resize = () => {
      const rect = canvas.getBoundingClientRect();
      canvas.width = rect.width * devicePixelRatio;
      canvas.height = rect.height * devicePixelRatio;
      const ctx = canvas.getContext("2d");
      if (ctx) ctx.scale(devicePixelRatio, devicePixelRatio);
      posCache.current.clear();
    };
    resize();
    const ro = new ResizeObserver(resize);
    ro.observe(canvas);
    return () => ro.disconnect();
  }, []);

  // Mouse interaction
  const onMouseMove = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!data || !canvasRef.current) return;
    const rect = canvasRef.current.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    const W = rect.width, H = rect.height;
    let closest: GalaxyNode | null = null;
    let minDist = 20;
    for (const node of data.nodes) {
      const [x, y] = hashPos(node.id, W, H);
      const d = Math.hypot(mx - x, my - y);
      if (d < minDist) { minDist = d; closest = node; }
    }
    setHovered(closest);
    setTooltip(closest ? { x: mx, y: my } : null);
  }, [data]);

  const onClick = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!hovered) return;
    router.push(`/learn/${hovered.path_id}/${hovered.id}`);
  }, [hovered, router]);

  const completedPct = data ? Math.round((data.completed_count / Math.max(data.total_lessons, 1)) * 100) : 0;
  const tier =
    completedPct >= 80 ? { label: "Master", color: "#f0883e", icon: "👑" } :
    completedPct >= 50 ? { label: "Scholar", color: "#bc8cff", icon: "🌟" } :
    completedPct >= 25 ? { label: "Explorer", color: "#58a6ff", icon: "🚀" } :
    completedPct >= 5  ? { label: "Learner", color: "#56d364", icon: "🌱" } :
    { label: "Beginner", color: "#8b949e", icon: "✨" };

  return (
    <div className="flex flex-col h-screen bg-[#090d14] text-white overflow-hidden">
      <AppHeader />
      <div className="flex flex-1 min-h-0 gap-0">
        {/* Sidebar */}
        <div className="w-72 flex-shrink-0 bg-[#0d1117] border-r border-[#21262d] flex flex-col p-5 gap-5 overflow-y-auto">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-2xl">{tier.icon}</span>
              <span className="text-lg font-bold" style={{ color: tier.color }}>{tier.label}</span>
            </div>
            <p className="text-xs text-zinc-500">Knowledge tier based on completed lessons</p>
          </div>

          {/* Progress ring */}
          <div className="flex items-center gap-4">
            <svg width="72" height="72" className="flex-shrink-0">
              <circle cx="36" cy="36" r="30" fill="none" stroke="#21262d" strokeWidth="6" />
              <circle cx="36" cy="36" r="30" fill="none"
                stroke={tier.color} strokeWidth="6"
                strokeDasharray={`${2 * Math.PI * 30 * completedPct / 100} 999`}
                strokeLinecap="round"
                transform="rotate(-90 36 36)"
                style={{ transition: "stroke-dasharray 1s ease" }} />
              <text x="36" y="40" textAnchor="middle" fontSize="14" fontWeight="bold" fill="white">
                {completedPct}%
              </text>
            </svg>
            <div>
              <div className="text-2xl font-bold">{data?.completed_count ?? 0}</div>
              <div className="text-xs text-zinc-400">of {data?.total_lessons ?? 0} lessons</div>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 gap-2">
            <Stat icon={<Trophy className="h-4 w-4 text-amber-400" />}
              value={`#${data?.rank.rank ?? "—"}`} label="Global Rank" />
            <Stat icon={<Flame className="h-4 w-4 text-orange-400" />}
              value={`${data?.streak_days ?? 0}d`} label="Streak" />
            <Stat icon={<Star className="h-4 w-4 text-yellow-400" />}
              value={`${data?.rank.score ?? 0}`} label="Score" />
            <Stat icon={<Zap className="h-4 w-4 text-purple-400" />}
              value={`${data?.rank.percentile ?? 0}%`} label="Percentile" />
          </div>

          {/* Legend */}
          <div className="pt-2 border-t border-[#21262d]">
            <p className="text-[11px] font-semibold text-zinc-500 uppercase tracking-wider mb-2">Paths</p>
            {data && Array.from(new Set(data.nodes.map((n) => n.path_id))).map((pid) => {
              const pname = data.nodes.find((n) => n.path_id === pid)?.path_name ?? pid;
              const total = data.nodes.filter((n) => n.path_id === pid).length;
              const done = data.nodes.filter((n) => n.path_id === pid && n.completed).length;
              return (
                <div key={pid} className="flex items-center gap-2 mb-1.5">
                  <span className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ background: pathColor(pid) }} />
                  <span className="text-xs text-zinc-300 truncate flex-1">{pname}</span>
                  <span className="text-[10px] text-zinc-500">{done}/{total}</span>
                </div>
              );
            })}
          </div>

          <div className="text-[10px] text-zinc-600 mt-auto">
            <BookOpen className="h-3 w-3 inline mr-1" />
            Click any star to open its lesson
          </div>
        </div>

        {/* Canvas */}
        <div className="flex-1 relative min-w-0">
          <canvas
            ref={canvasRef}
            className="w-full h-full"
            style={{ cursor: hovered ? "pointer" : "default" }}
            onMouseMove={onMouseMove}
            onClick={onClick}
          />
          {!data && (
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-zinc-500 text-sm">Loading your galaxy…</div>
            </div>
          )}
          {/* Title overlay */}
          <div className="absolute top-4 left-1/2 -translate-x-1/2 text-center pointer-events-none">
            <h1 className="text-xl font-bold text-white/80">Knowledge Galaxy</h1>
            <p className="text-xs text-zinc-600 mt-0.5">Hover stars to explore · Click to open lesson</p>
          </div>
        </div>
      </div>
    </div>
  );
}

function Stat({ icon, value, label }: { icon: React.ReactNode; value: string; label: string }) {
  return (
    <div className="bg-[#161b22] rounded-lg p-3 flex flex-col gap-1 border border-[#21262d]">
      <div className="flex items-center gap-1.5">{icon}<span className="text-xs text-zinc-500">{label}</span></div>
      <div className="text-lg font-bold text-white">{value}</div>
    </div>
  );
}
