'use client';
import { useState, useEffect, useRef } from 'react';
import { useAuthStore } from '@/lib/store';
import ReactMarkdown from 'react-markdown';

interface Props { lessonId: number }

interface RevisionResult {
  original: string;
  revised: string;
  gaps_identified: string[];
  concept_connections: { from: string; to: string; relationship: string }[];
  misconceptions: string[];
  strength_score: number;
  suggestions: string[];
}

const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function NotesPanel({ lessonId }: Props) {
  const { token } = useAuthStore();
  const STORAGE_KEY = `sage-notes-${lessonId}`;
  const [notes, setNotes] = useState('');
  const [result, setResult] = useState<RevisionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'write' | 'revised' | 'analysis'>('write');
  const [planLoading, setPlanLoading] = useState(false);
  const [planContent, setPlanContent] = useState('');
  const [savedAt, setSavedAt] = useState<string | null>(null);
  const saveTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Load from localStorage on mount
  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const data = JSON.parse(raw);
        if (data.notes) setNotes(data.notes);
        if (data.result) setResult(data.result);
        if (data.saved_at) setSavedAt(data.saved_at);
      }
    } catch {}
  }, [lessonId]);

  // Auto-save notes to localStorage with 1s debounce
  useEffect(() => {
    if (!notes.trim()) return;
    if (saveTimerRef.current) clearTimeout(saveTimerRef.current);
    saveTimerRef.current = setTimeout(() => {
      const ts = new Date().toISOString();
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ notes, result, saved_at: ts }));
      setSavedAt(ts);
    }, 1000);
    return () => { if (saveTimerRef.current) clearTimeout(saveTimerRef.current); };
  }, [notes]);

  async function handleRevise() {
    if (!notes.trim() || !token) return;
    setLoading(true);
    try {
      const res = await fetch(`${BASE}/notes/revise`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ lesson_id: lessonId, content: notes }),
      });
      const data = await res.json();
      setResult(data);
      setActiveTab('revised');
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  async function downloadPlan() {
    if (!token) return;
    setPlanLoading(true);
    try {
      const res = await fetch(`${BASE}/notes/generate-plan?lesson_id=${lessonId}`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      setPlanContent(data.plan_markdown);

      // Trigger download
      const blob = new Blob([data.plan_markdown], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = data.download_filename;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error(e);
    } finally {
      setPlanLoading(false);
    }
  }

  function saveOffline() {
    if (!notes.trim()) return;
    const ts = new Date().toISOString();
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ notes, result, saved_at: ts }));
    setSavedAt(ts);
  }

  return (
    <div className="h-full flex flex-col p-4">
      <div className="flex items-center gap-2 mb-4 flex-shrink-0">
        <div>
          <div className="text-[9.5px] font-bold uppercase tracking-widest text-t3">Notes & AI Revision</div>
          {savedAt && (
            <div className="text-[9px] text-t3 mt-0.5">
              ✓ auto-saved {new Date(savedAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          )}
        </div>
        <div className="ml-auto flex gap-2">
          <button
            onClick={saveOffline}
            className="text-[10px] text-t2 hover:text-grn border border-white/5 hover:border-grn/30 px-3 py-1 rounded-lg transition-all"
          >
            ↓ Save Offline
          </button>
          <button
            onClick={downloadPlan}
            disabled={planLoading}
            className="text-[10px] text-acc border border-acc/20 hover:border-acc/40 px-3 py-1 rounded-lg transition-all disabled:opacity-50"
          >
            {planLoading ? '…' : '↓ Lesson Plan'}
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-0 border-b border-white/5 mb-4 flex-shrink-0">
        {(['write', 'revised', 'analysis'] as const).map(t => (
          <button key={t} onClick={() => setActiveTab(t)}
            className={`px-4 py-2 text-[10px] font-semibold uppercase tracking-wider border-b-2 transition-all ${
              activeTab === t ? 'text-acc border-acc' : 'text-t3 border-transparent hover:text-t1'
            }`}>
            {t === 'write' ? '✎ Write' : t === 'revised' ? '◎ AI Revised' : '◈ Analysis'}
          </button>
        ))}
      </div>

      <div className="flex-1 overflow-hidden flex flex-col">
        {activeTab === 'write' && (
          <div className="flex-1 flex flex-col gap-3">
            <textarea
              value={notes}
              onChange={e => setNotes(e.target.value)}
              placeholder={`Write your notes here...\n\nTip: Explain concepts in your own words. The AI will review them, find gaps, and suggest improvements.\n\nExample:\n- Neural networks are like... \n- Backprop works by...\n- I'm confused about...`}
              className="flex-1 bg-bg2 border border-white/5 rounded-2xl p-4 text-sm text-t0 outline-none focus:border-acc/30 resize-none font-sans placeholder-t3 transition-colors min-h-[200px]"
            />
            <button
              onClick={handleRevise}
              disabled={loading || !notes.trim()}
              className="w-full py-3 text-sm font-bold bg-acc/15 text-acc border border-acc/25 rounded-xl hover:bg-acc/25 transition-all disabled:opacity-40"
            >
              {loading ? 'AI is reviewing your notes…' : '◎ Get AI Revision →'}
            </button>
          </div>
        )}

        {activeTab === 'revised' && (
          <div className="flex-1 overflow-y-auto">
            {result ? (
              <div className="space-y-3">
                {/* Score */}
                <div className="flex items-center gap-3 p-3 bg-bg2 border border-white/5 rounded-xl">
                  <div className="text-2xl font-black" style={{
                    color: result.strength_score >= 0.7 ? '#2dd4a4' : result.strength_score >= 0.4 ? '#f5c842' : '#e8689a'
                  }}>
                    {Math.round(result.strength_score * 100)}%
                  </div>
                  <div>
                    <div className="text-xs font-semibold text-t0">Note Strength</div>
                    <div className="text-[10px] text-t2">
                      {result.strength_score >= 0.7 ? 'Strong understanding' : result.strength_score >= 0.4 ? 'Developing' : 'Needs work'}
                    </div>
                  </div>
                </div>

                {/* Revised notes */}
                <div className="bg-bg2 border border-grn/20 rounded-xl p-4">
                  <div className="text-[9px] font-bold uppercase tracking-widest text-grn mb-2">AI Revised Version</div>
                  <div className="prose-sage text-xs">
                    <ReactMarkdown>{result.revised}</ReactMarkdown>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-t2 text-sm text-center py-8">Write notes and click "Get AI Revision" first</div>
            )}
          </div>
        )}

        {activeTab === 'analysis' && (
          <div className="flex-1 overflow-y-auto space-y-3">
            {result ? (
              <>
                {result.misconceptions.length > 0 && (
                  <div className="bg-pnk/5 border border-pnk/20 rounded-xl p-3">
                    <div className="text-[9px] font-bold uppercase tracking-widest text-pnk mb-2">Misconceptions Detected</div>
                    {result.misconceptions.map((m, i) => (
                      <div key={i} className="text-xs text-t1 flex gap-2 mb-1.5">
                        <span className="text-pnk mt-0.5">✗</span> {m}
                      </div>
                    ))}
                  </div>
                )}

                {result.gaps_identified.length > 0 && (
                  <div className="bg-yel/5 border border-yel/20 rounded-xl p-3">
                    <div className="text-[9px] font-bold uppercase tracking-widest text-yel mb-2">Knowledge Gaps</div>
                    {result.gaps_identified.map((g, i) => (
                      <div key={i} className="text-xs text-t1 flex gap-2 mb-1.5">
                        <span className="text-yel mt-0.5">○</span> {g}
                      </div>
                    ))}
                  </div>
                )}

                {result.concept_connections.length > 0 && (
                  <div className="bg-acc/5 border border-acc/20 rounded-xl p-3">
                    <div className="text-[9px] font-bold uppercase tracking-widest text-acc mb-2">Concept Connections</div>
                    {result.concept_connections.map((c, i) => (
                      <div key={i} className="text-xs text-t1 mb-1.5">
                        <span className="text-acc font-mono">{c.from}</span>
                        <span className="text-t3 mx-2">→</span>
                        <span className="text-grn font-mono">{c.to}</span>
                        <div className="text-[9px] text-t3 ml-4">{c.relationship}</div>
                      </div>
                    ))}
                  </div>
                )}

                {result.suggestions.length > 0 && (
                  <div className="bg-pur/5 border border-pur/20 rounded-xl p-3">
                    <div className="text-[9px] font-bold uppercase tracking-widest text-pur mb-2">Suggestions</div>
                    {result.suggestions.map((s, i) => (
                      <div key={i} className="text-xs text-t1 flex gap-2 mb-1.5">
                        <span className="text-pur mt-0.5">→</span> {s}
                      </div>
                    ))}
                  </div>
                )}
              </>
            ) : (
              <div className="text-t2 text-sm text-center py-8">Write notes and get AI revision to see analysis</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
