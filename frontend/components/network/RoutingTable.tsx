'use client';

interface RouteRow {
  user_id: number;
  display: string;
  score: number;
  components: {
    mastery_delta: number;
    recency: number;
    style_compat: number;
    novelty: number;
  };
  role: string;
  last_seen_seconds: number;
}

interface Props {
  rows: RouteRow[];
  weights: Record<string, number>;
  selectedUserId?: number;
}

const COMPONENTS: { key: keyof RouteRow['components']; label: string }[] = [
  { key: 'mastery_delta', label: 'Δm' },
  { key: 'recency',       label: 'rec' },
  { key: 'style_compat',  label: 'style' },
  { key: 'novelty',       label: 'novel' },
];

export default function RoutingTable({ rows, weights, selectedUserId }: Props) {
  if (rows.length === 0) {
    return (
      <div className="text-[10px] text-t3 italic p-3 bg-bg2 border border-white/5 rounded-xl">
        Routing table is empty — no peers in scope.
      </div>
    );
  }

  return (
    <div className="bg-bg2 border border-ora/15 rounded-xl overflow-hidden">
      <div className="px-3 py-2 border-b border-ora/15 flex items-center gap-2">
        <span className="text-[10px] font-bold uppercase tracking-widest text-ora">
          Routing Table · SRP
        </span>
        <span className="ml-auto text-[9px] text-t3 font-mono">
          {COMPONENTS.map(c => `${c.label}=${(weights[c.key] * 100).toFixed(0)}%`).join(' · ')}
        </span>
      </div>
      <div className="text-[10px] font-mono">
        <div className="grid grid-cols-[24px_1fr_60px_repeat(4,_44px)_50px] gap-1 px-3 py-1.5 border-b border-white/5 text-t3 uppercase">
          <span>#</span>
          <span>peer</span>
          <span className="text-right">score</span>
          {COMPONENTS.map(c => (
            <span key={c.key} className="text-right">{c.label}</span>
          ))}
          <span className="text-right">role</span>
        </div>
        {rows.map((r, i) => {
          const isSelected = r.user_id === selectedUserId || i === 0;
          return (
            <div
              key={r.user_id}
              className={`grid grid-cols-[24px_1fr_60px_repeat(4,_44px)_50px] gap-1 px-3 py-1.5 border-b border-white/5 last:border-0 ${
                isSelected ? 'bg-ora/8 text-t0' : 'text-t1'
              }`}
            >
              <span className={isSelected ? 'text-ora font-bold' : 'text-t3'}>
                {isSelected ? '►' : i + 1}
              </span>
              <span className="truncate">{r.display}</span>
              <span className={`text-right font-bold ${isSelected ? 'text-ora' : ''}`}>
                {r.score.toFixed(3)}
              </span>
              {COMPONENTS.map(c => (
                <span key={c.key} className="text-right text-t2">
                  {r.components[c.key].toFixed(2)}
                </span>
              ))}
              <span className={`text-right text-[9px] ${
                r.role === 'tutor' ? 'text-ora' : 'text-acc'
              }`}>
                {r.role === 'tutor' ? 'TUT' : 'CO'}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
