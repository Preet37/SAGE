'use client';

interface CognitionPayload {
  confidence_score: number;
  grounded: boolean;
  socratic: boolean;
  no_fabrications: boolean;
  on_topic: boolean;
  flags: string[];
  retrieved_chunks: number;
  hyde_improvement_pct: number;
}

interface Props {
  data: CognitionPayload;
}

function Check({ pass, label }: { pass: boolean; label: string }) {
  return (
    <span className={`text-[10px] ${pass ? 'text-grn' : 'text-amber-400'}`}>
      {pass ? '✓' : '✗'} {label}
    </span>
  );
}

export default function CognitionScoreCard({ data }: Props) {
  const {
    confidence_score,
    grounded,
    socratic,
    no_fabrications,
    on_topic,
    flags,
    retrieved_chunks,
    hyde_improvement_pct,
  } = data;

  const isLow = confidence_score < 60;
  const isAmber = confidence_score < 85 && confidence_score >= 60;

  const borderColor = isLow
    ? 'border-amber-500/40 bg-amber-500/5'
    : isAmber
    ? 'border-amber-400/20 bg-amber-400/5'
    : 'border-purple-500/20 bg-purple-500/5';

  return (
    <div className={`mt-2 rounded-xl border px-3 py-2.5 ${borderColor}`}>
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-1.5">
          <span className="text-[10px] font-bold text-purple-400 tracking-wide">◈ Cognition Score</span>
          <span
            className={`text-xs font-bold ${
              isLow ? 'text-amber-400' : isAmber ? 'text-amber-300' : 'text-grn'
            }`}
          >
            {confidence_score}/100
          </span>
        </div>
        <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-purple-500/15 text-purple-400 border border-purple-500/20">
          cognition
        </span>
      </div>

      <div className="flex flex-wrap gap-x-3 gap-y-0.5 mb-2">
        <Check pass={grounded} label="Grounded in KB" />
        <Check pass={socratic} label="Socratic" />
        <Check pass={no_fabrications} label="No fabrications" />
        <Check pass={on_topic} label="On-topic" />
      </div>

      <div className="flex gap-3 text-[10px] text-t3">
        <span>Retrieved {retrieved_chunks} chunks</span>
        {hyde_improvement_pct > 0 && (
          <span className="text-purple-400">
            · HyDE improved relevance +{hyde_improvement_pct.toFixed(0)}%
          </span>
        )}
      </div>

      {flags.length > 0 && (
        <div className="mt-1.5 text-[10px] text-amber-400">
          {flags.map((f, i) => (
            <div key={i}>⚠ {f}</div>
          ))}
        </div>
      )}
    </div>
  );
}
