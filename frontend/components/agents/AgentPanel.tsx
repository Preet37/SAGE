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
  const { agentEvents, isStreaming } = useTutorStore();

  const latestByType = new Map<string, { type: string; data: unknown; ts: number }>();
  agentEvents.forEach(ev => { latestByType.set(ev.type, ev); });

  const fetchaiBadge = latestByType.get('fetchai_badge');
  const fetchaiData = fetchaiBadge?.data as Record<string, unknown> | undefined;

  return (
    <div className="flex flex-col p-4 gap-3">
      <div className="flex items-center gap-2 mb-1">
        <div className="text-[9.5px] font-bold uppercase tracking-widest text-t3">Fetch.ai Agent Network</div>
        {isStreaming && (
          <div className="ml-auto flex items-center gap-1">
            <div className="w-1.5 h-1.5 rounded-full bg-acc animate-pulse" />
            <span className="text-[9px] text-acc font-semibold">LIVE</span>
          </div>
        )}
      </div>

      {fetchaiData && (
        <div className="rounded-xl border border-teal-500/25 bg-teal-500/5 p-3">
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-[10px] font-bold text-teal-400">◎ Fetch.ai Bureau Active</span>
            <a
              href="https://agentverse.ai"
              target="_blank"
              rel="noopener noreferrer"
              className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-teal-500/15 text-teal-400 border border-teal-500/20 hover:bg-teal-500/25 transition-all"
            >
              fetch.ai ↗
            </a>
          </div>
          <div className="text-[10px] text-t3 font-mono">
            Director: {(fetchaiData.director_address as string)?.slice(0, 20) ?? 'sage-director'}…
          </div>
          {fetchaiData.teaching_mode && (
            <div className="text-[10px] text-teal-400 mt-0.5">
              Mode: {fetchaiData.teaching_mode as string}
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

      {/* Agent addresses (Fetch.ai) */}
      <div className="mt-2 p-3 bg-bg2 border border-pur/15 rounded-xl">
        <div className="text-[9px] font-bold uppercase tracking-widest text-pur mb-2">Agentverse</div>
        <div className="space-y-1">
          {['pedagogy', 'content', 'concept_map', 'assessment', 'peer_match', 'progress'].map(a => (
            <div key={a} className="flex items-center gap-2 text-[9px]">
              <div className="w-1.5 h-1.5 rounded-full bg-pur/60 flex-shrink-0" />
              <span className="text-t3 font-mono">sage_{a}_agent</span>
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
      return `Quiz: ${d.quiz ?? 'pending'}`;
    case 'peer_match_check':
      return `Matching peers...`;
    case 'progress_updated':
      return `Progress tracked`;
    default:
      return JSON.stringify(d).slice(0, 40);
  }
}
