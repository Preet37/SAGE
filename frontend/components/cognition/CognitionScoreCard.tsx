'use client';
import { useState } from 'react';
import type { CognitionData } from '@/lib/store';

interface Props {
  data: CognitionData;
}

export default function CognitionScoreCard({ data }: Props) {
  const [expanded, setExpanded] = useState(false);
  const judge = data.judge;
  const scorePct = Math.round((judge?.score ?? 0) * 100);

  const scoreColor =
    scorePct >= 80 ? 'text-grn'
    : scorePct >= 60 ? 'text-yel'
    : 'text-pnk';
  const scoreBg =
    scorePct >= 80 ? 'border-grn/30 bg-grn/5'
    : scorePct >= 60 ? 'border-yel/30 bg-yel/5'
    : 'border-pnk/30 bg-pnk/5';

  return (
    <div className={`mt-2 rounded-xl border ${scoreBg}`}>
      {/* Header — always visible */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center gap-3 px-3 py-2 hover:bg-white/[0.02] transition-colors"
      >
        <div className="w-8 h-8 rounded-lg bg-bg3 flex items-center justify-center flex-shrink-0">
          <svg className="w-4 h-4 text-pur" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M9 5h6m-6 4h6m-6 4h6m-6 4h6M5 5a1 1 0 11-2 0 1 1 0 012 0zm0 4a1 1 0 11-2 0 1 1 0 012 0zm0 4a1 1 0 11-2 0 1 1 0 012 0zm0 4a1 1 0 11-2 0 1 1 0 012 0z" />
          </svg>
        </div>
        <div className="flex-1 text-left min-w-0">
          <div className="text-[10px] font-bold uppercase tracking-widest text-pur">
            Cognition Score Card
          </div>
          <div className="text-[10px] text-t3 truncate">
            {data.retrieved.length} sources · {data.rerank_used ? 'reranked' : 'cosine'} · {data.latency_ms}ms
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className={`text-2xl font-black ${scoreColor}`}>{scorePct}</span>
          <span className="text-[9px] text-t3 font-bold">/100</span>
          {judge?.grounded && (
            <span className="text-[9px] font-bold text-grn bg-grn/10 px-1.5 py-0.5 rounded-full">
              GROUNDED
            </span>
          )}
        </div>
        <svg
          className={`w-4 h-4 text-t3 transition-transform ${expanded ? 'rotate-180' : ''}`}
          fill="none" viewBox="0 0 24 24" stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Expanded body */}
      {expanded && (
        <div className="px-3 pb-3 space-y-3 border-t border-white/5">
          {/* Judge reasoning */}
          {judge && (
            <div className="pt-3">
              <div className="text-[9px] font-bold uppercase tracking-widest text-pur mb-1.5">
                LLM Judge
              </div>
              <p className="text-[11px] text-t1 leading-relaxed italic">
                "{judge.reasoning}"
              </p>
              {judge.citations.length > 0 && (
                <div className="mt-1.5 flex items-center gap-1.5 flex-wrap">
                  <span className="text-[9px] text-t3">cites:</span>
                  {judge.citations.map(i => (
                    <span key={i} className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-pur/15 text-pur">
                      [{i}]
                    </span>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* HyDE query */}
          {data.hyde_query && data.hyde_query.length > 80 && (
            <div>
              <div className="text-[9px] font-bold uppercase tracking-widest text-pur mb-1.5">
                HyDE Expansion
              </div>
              <p className="text-[10px] text-t2 font-mono leading-relaxed line-clamp-3">
                {data.hyde_query.slice(0, 240)}…
              </p>
            </div>
          )}

          {/* Retrieved sources */}
          <div>
            <div className="text-[9px] font-bold uppercase tracking-widest text-pur mb-1.5">
              Retrieved Sources ({data.retrieved.length})
            </div>
            <div className="space-y-1.5">
              {data.retrieved.map((c, i) => {
                const isCited = judge?.citations.includes(i);
                return (
                  <div
                    key={c.id}
                    className={`flex items-start gap-2 p-2 rounded-lg ${
                      isCited
                        ? 'bg-pur/10 border border-pur/20'
                        : 'bg-bg3 border border-white/5'
                    }`}
                  >
                    <span className={`text-[9px] font-mono font-bold mt-0.5 flex-shrink-0 ${
                      isCited ? 'text-pur' : 'text-t3'
                    }`}>
                      [{i}]
                    </span>
                    <div className="flex-1 min-w-0">
                      <p className="text-[10px] text-t1 leading-tight line-clamp-2">
                        {c.preview}
                      </p>
                      <div className="mt-1 flex items-center gap-2 text-[9px] text-t3">
                        <span>cos {c.cosine.toFixed(3)}</span>
                        {c.rerank !== null && c.rerank !== undefined && (
                          <span className="text-pur">rrk {c.rerank.toFixed(3)}</span>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="pt-2 border-t border-white/5 flex items-center justify-between text-[9px] text-t3">
            <span>powered by</span>
            <span className="font-bold text-pur">cognition.ai pipeline</span>
          </div>
        </div>
      )}
    </div>
  );
}
