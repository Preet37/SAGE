'use client';
import { useEffect, useState } from 'react';
import { useAuthStore } from '@/lib/store';

interface RouteEntry {
  concept_id: number;
  concept: string;
  peers_available: number;
  students_waiting: number;
  sessions_completed: number;
}

interface Analytics {
  routing_table: RouteEntry[];
  network_health: { active_peers: number; total_waiting: number; active_sessions: number };
}

export default function RoutingTable() {
  const { token } = useAuthStore();
  const [analytics, setAnalytics] = useState<Analytics | null>(null);

  useEffect(() => {
    if (!token) return;
    const load = () =>
      fetch('/api/network/analytics', {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((r) => r.json())
        .then(setAnalytics)
        .catch(() => {});

    load();
    const id = setInterval(load, 10000);
    return () => clearInterval(id);
  }, [token]);

  if (!analytics) {
    return (
      <div className="rounded-xl border border-green-500/20 bg-green-500/5 p-4 text-t3 text-xs">
        Loading routing table…
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-green-500/20 bg-green-500/5 p-3">
      <div className="flex items-center justify-between mb-3">
        <span className="text-[10px] font-bold uppercase tracking-widest text-green-400">
          SRP Routing Table
        </span>
        <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-green-500/15 text-green-400 border border-green-500/20">
          arista
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-[10px]">
          <thead>
            <tr className="text-t3 uppercase tracking-wide border-b border-white/5">
              <th className="text-left pb-2 pr-3">Concept</th>
              <th className="text-right pb-2 pr-3">Peers</th>
              <th className="text-right pb-2 pr-3">Waiting</th>
              <th className="text-right pb-2">Sessions</th>
            </tr>
          </thead>
          <tbody>
            {analytics.routing_table.slice(0, 10).map((row) => (
              <tr key={row.concept_id} className="border-b border-white/3">
                <td className="py-1.5 pr-3 text-t0 font-medium">{row.concept}</td>
                <td className="text-right pr-3">
                  <span
                    className={`font-semibold ${
                      row.peers_available > 2
                        ? 'text-green-400'
                        : row.peers_available > 0
                        ? 'text-yellow-400'
                        : 'text-t3'
                    }`}
                  >
                    {row.peers_available}
                  </span>
                </td>
                <td className="text-right pr-3 text-t2">{row.students_waiting}</td>
                <td className="text-right text-t2">{row.sessions_completed}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-3 pt-3 border-t border-white/5">
        <div className="text-[9px] text-t3 uppercase tracking-wide mb-1.5">Network Health</div>
        <div className="flex gap-4 text-[10px]">
          <span>
            Active peers:{' '}
            <span className="text-green-400 font-semibold">
              {analytics.network_health.active_peers}
            </span>
          </span>
          <span>
            Queue:{' '}
            <span className="text-yellow-400 font-semibold">
              {analytics.network_health.total_waiting}
            </span>
          </span>
          <span>
            Sessions:{' '}
            <span className="text-blue-400 font-semibold">
              {analytics.network_health.active_sessions}
            </span>
          </span>
        </div>
      </div>
    </div>
  );
}
