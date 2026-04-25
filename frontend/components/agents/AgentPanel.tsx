'use client';
import { useTutorStore } from '@/lib/store';

const AGENTS = [
  { id: 'pedagogy_applied',    name: 'Pedagogy',   icon: '◎', color: '#5b9fff', desc: 'Teaching strategy' },
  { id: 'content_retrieved',   name: 'Content',    icon: '◈', color: '#2dd4a4', desc: 'KB retrieval' },
  { id: 'concept_map_updated', name: 'Concept Map',icon: '⬡', color: '#9d78f5', desc: 'Graph builder' },
  { id: 'assessment_check',    name: 'Assessment', icon: '✓', color: '#f5c842', desc: 'Quiz generator' },
  { id: 'peer_match_check',    name: 'Peer Match', icon: '◉', color: '#f5834a', desc: 'Peer routing' },
  { id: 'progress_updated',    name: 'Progress',   icon: '↗', color: '#e8689a', desc: 'Mastery tracker' },
];

export default function AgentPanel() {
  const { agentEvents, isStreaming, fetchAiBadge } = useTutorStore();

  const latestByType = new Map<string, { type: string; data: unknown; ts: number }>();
  agentEvents.forEach(ev => { latestByType.set(ev.type, ev); });

  return (
    <div className="flex flex-col p-4 gap-3">
      <div className="flex items-center gap-2 mb-1">
        <div className="text-[9.5px] font-bold uppercase tracking-widest text-t3">Fetch.ai Bureau</div>
        {isStreaming && (
          <div className="ml-auto flex items-center gap-1">
            <div className="w-1.5 h-1.5 rounded-full bg-acc animate-pulse" />
            <span className="text-[9px] text-acc font-semibold">LIVE</span>
          </div>
        )}
      </div>

      {/* Director badge — shown after first turn so it's not noise on load */}
      {fetchAiBadge && (
        <div className="rounded-xl border border-acc/30 bg-acc/5 p-3">
          <div className="flex items-center gap-2 mb-1.5">
            <div className="w-6 h-6 rounded-lg bg-acc/20 flex items-center justify-center text-xs text-acc font-bold">
              ★
            </div>
            <span className="text-xs font-bold text-t0">Director</span>
            <a
              href={fetchAiBadge.agentverse_url}
              target="_blank"
              rel="noopener noreferrer"
              className="ml-auto text-[9px] font-bold text-acc hover:underline"
            >
              Agentverse ↗
            </a>
          </div>
          <div className="text-[9px] font-mono text-t3 break-all leading-relaxed">
            {fetchAiBadge.director_address || 'agent1q…'}
          </div>
          {fetchAiBadge.payment && (
            <div className="mt-2 pt-2 border-t border-acc/15 flex items-center justify-between">
              <span className="text-[9px] text-t3 uppercase tracking-wider">Deep Dive paid</span>
              <span className="text-[10px] font-bold text-acc">
                {fetchAiBadge.payment.amount_micro_asi} μASI
              </span>
            </div>
          )}
        </div>
      )}

      {AGENTS.map(agent => {
        const event = latestByType.get(agent.id);
        const isActive = isStreaming && !!event;
        const wasActive = !!event;

        return (
          <div
            key={agent.id}
            className={`rounded-xl border p-3 transition-all ${
              isActive ? 'border-opacity-40 bg-bg2' : wasActive ? 'border-opacity-20 bg-bg2' : 'border-white/5 bg-bg2 opacity-40'
            }`}
            style={{ borderColor: wasActive ? agent.color + (isActive ? '60' : '30') : undefined }}
          >
            <div className="flex items-center gap-2 mb-1.5">
              <div className="w-6 h-6 rounded-lg flex items-center justify-center text-sm flex-shrink-0"
                style={{ background: agent.color + '18', color: agent.color }}>
                {agent.icon}
              </div>
              <span className="text-xs font-semibold text-t0 flex-1">{agent.name}</span>
              <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded-full ${
                isActive
                  ? 'text-acc bg-acc/15'
                  : wasActive
                  ? 'text-grn bg-grn/15'
                  : 'text-t3 bg-bg3'
              }`}>
                {isActive ? 'RUN' : wasActive ? 'DONE' : 'IDLE'}
              </span>
            </div>

            <div className="text-[10px] text-t2 font-mono leading-tight">
              {event ? formatEventLog(agent.id, event.data) : agent.desc}
            </div>

            {isActive && (
              <div className="mt-2 h-0.5 bg-bg3 rounded-full overflow-hidden">
                <div className="h-full rounded-full animate-pulse" style={{ background: agent.color, width: '60%' }} />
              </div>
            )}
          </div>
        );
      })}

      {/* Agent ports — proves they're real uAgents on chain */}
      <div className="mt-2 p-3 bg-bg2 border border-pur/15 rounded-xl">
        <div className="flex items-center justify-between mb-2">
          <div className="text-[9px] font-bold uppercase tracking-widest text-pur">Bureau Ports</div>
          <a
            href="https://agentverse.ai/"
            target="_blank"
            rel="noopener noreferrer"
            className="text-[9px] font-semibold text-pur hover:underline"
          >
            agentverse.ai
          </a>
        </div>
        <div className="space-y-1">
          {(fetchAiBadge?.agents ?? [
            { name: 'Director', port: 8007, role: 'coordinator' },
            { name: 'Pedagogy', port: 8001, role: 'teaching strategy' },
            { name: 'Content', port: 8002, role: 'KB retrieval' },
            { name: 'ConceptMap', port: 8003, role: 'graph' },
            { name: 'Assessment', port: 8004, role: 'quiz' },
            { name: 'PeerMatch', port: 8005, role: 'peers' },
            { name: 'Progress', port: 8006, role: 'mastery' },
          ]).map(a => (
            <div key={a.port} className="flex items-center gap-2 text-[9px]">
              <div className="w-1.5 h-1.5 rounded-full bg-pur/60 flex-shrink-0" />
              <span className="text-t3 font-mono flex-1">sage_{a.name.toLowerCase()}</span>
              <span className="text-t2 font-mono">:{a.port}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function formatEventLog(agentId: string, data: unknown): string {
  const d = data as Record<string, unknown>;
  switch (agentId) {
    case 'pedagogy_applied':
      return `Mode: ${d.mode ?? 'default'}`;
    case 'content_retrieved':
      return `${d.chunks ?? 0} chunks retrieved`;
    case 'concept_map_updated':
      return `Graph nodes updated`;
    case 'assessment_check':
      return `Quiz: ${d.quiz ?? d.should_quiz ?? 'pending'}`;
    case 'peer_match_check':
      return `Matching peers...`;
    case 'progress_updated':
      return `Progress tracked`;
    default:
      return JSON.stringify(d).slice(0, 40);
  }
}
