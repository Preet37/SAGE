'use client';
import { useState, useEffect } from 'react';
import { useAuthStore } from '@/lib/store';

const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface DisabilityOption { id: string; label: string; description: string }
interface StrengthOption { id: string; label: string; description: string }

const DISABILITY_ICONS: Record<string, string> = {
  dyslexia: '📖',
  adhd: '⚡',
  visual_impairment: '◉',
  hearing_impairment: '◎',
  dyscalculia: '∑',
  autism: '◈',
  esl: '◐',
  cognitive_load: '◑',
};

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export default function AccessibilityModal({ isOpen, onClose }: Props) {
  const { token } = useAuthStore();
  const [disabilities, setDisabilities] = useState<DisabilityOption[]>([]);
  const [strengths, setStrengths] = useState<StrengthOption[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [selectedStrengths, setSelectedStrengths] = useState<string[]>([]);
  const [customNote, setCustomNote] = useState('');
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (!isOpen || !token) return;
    fetch(`${BASE}/accessibility/profiles`).then(r => r.json()).then(d => {
      setDisabilities(d.disabilities || []);
      setStrengths(d.strengths || []);
    });
    fetch(`${BASE}/accessibility/me`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.json())
      .then(d => {
        setSelected(d.disabilities || []);
        setSelectedStrengths(d.strengths || []);
        setCustomNote(d.custom_note || '');
      });
  }, [isOpen, token]);

  function toggle(id: string, list: string[], setList: (l: string[]) => void) {
    setList(list.includes(id) ? list.filter(x => x !== id) : [...list, id]);
  }

  async function save() {
    if (!token) return;
    setSaving(true);
    const res = await fetch(`${BASE}/accessibility/me`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ disabilities: selected, strengths: selectedStrengths, custom_note: customNote }),
    });
    await res.json();
    setSaving(false);
    setSaved(true);
    setTimeout(() => { setSaved(false); onClose(); }, 1200);
  }

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <div className="relative bg-bg1 border border-white/10 rounded-2xl w-full max-w-lg max-h-[85vh] flex flex-col z-10">
        {/* Header */}
        <div className="p-5 border-b border-white/5">
          <div className="flex items-center gap-2 mb-1">
            <div className="text-xl">◈</div>
            <h2 className="text-base font-bold">Accessibility Settings</h2>
            <button onClick={onClose} className="ml-auto text-t2 hover:text-t0 transition-colors">✕</button>
          </div>
          <p className="text-xs text-t2">Tell SAGE how you learn best. Every setting adjusts the AI tutor's language, pacing, and format instantly.</p>
        </div>

        <div className="flex-1 overflow-y-auto p-5 space-y-5">
          {/* Disabilities */}
          <div>
            <div className="text-[10px] font-bold uppercase tracking-widest text-t3 mb-3">Learning Differences</div>
            <div className="grid grid-cols-2 gap-2">
              {disabilities.map(d => (
                <button
                  key={d.id}
                  onClick={() => toggle(d.id, selected, setSelected)}
                  className={`flex items-start gap-2 p-3 rounded-xl border text-left transition-all ${
                    selected.includes(d.id)
                      ? 'border-acc/50 bg-acc/10'
                      : 'border-white/5 bg-bg2 hover:border-white/10'
                  }`}
                >
                  <span className="text-base flex-shrink-0">{DISABILITY_ICONS[d.id] || '○'}</span>
                  <div>
                    <div className="text-xs font-semibold text-t0 leading-tight">{d.label}</div>
                    <div className="text-[9px] text-t2 mt-0.5 leading-tight line-clamp-2">{d.description}</div>
                  </div>
                  {selected.includes(d.id) && (
                    <span className="ml-auto text-acc text-xs flex-shrink-0">✓</span>
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* Learning strengths */}
          <div>
            <div className="text-[10px] font-bold uppercase tracking-widest text-t3 mb-3">Learning Style</div>
            <div className="grid grid-cols-2 gap-2">
              {strengths.map(s => (
                <button
                  key={s.id}
                  onClick={() => toggle(s.id, selectedStrengths, setSelectedStrengths)}
                  className={`flex items-start gap-2 p-3 rounded-xl border text-left transition-all ${
                    selectedStrengths.includes(s.id)
                      ? 'border-grn/40 bg-grn/8'
                      : 'border-white/5 bg-bg2 hover:border-white/10'
                  }`}
                >
                  <div>
                    <div className="text-xs font-semibold text-t0">{s.label}</div>
                    <div className="text-[9px] text-t2 mt-0.5 line-clamp-2">{s.description}</div>
                  </div>
                  {selectedStrengths.includes(s.id) && (
                    <span className="ml-auto text-grn text-xs flex-shrink-0">✓</span>
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* Custom note */}
          <div>
            <div className="text-[10px] font-bold uppercase tracking-widest text-t3 mb-2">Anything else?</div>
            <textarea
              value={customNote}
              onChange={e => setCustomNote(e.target.value)}
              placeholder="Tell SAGE anything about how you learn best, challenges you face, or what helps you understand…"
              rows={3}
              className="w-full bg-bg2 border border-white/5 rounded-xl px-3 py-2.5 text-xs text-t0 outline-none focus:border-acc/30 resize-none placeholder-t3 transition-colors"
            />
          </div>

          {/* Active summary */}
          {(selected.length > 0 || selectedStrengths.length > 0) && (
            <div className="bg-acc/5 border border-acc/15 rounded-xl p-3">
              <div className="text-[9px] font-bold uppercase tracking-widest text-acc mb-2">Active Adaptations</div>
              <div className="text-[10px] text-t1 leading-relaxed">
                SAGE will adapt for: {[...selected, ...selectedStrengths].join(', ')}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-white/5">
          <button
            onClick={save}
            disabled={saving}
            className={`w-full py-3 text-sm font-bold rounded-xl transition-all ${
              saved
                ? 'bg-grn/20 text-grn border border-grn/30'
                : 'bg-acc text-white hover:bg-blue-400'
            } disabled:opacity-50`}
          >
            {saved ? '✓ Saved! Tutor updated.' : saving ? 'Saving…' : 'Save Accessibility Profile →'}
          </button>
          <p className="text-[9px] text-t3 text-center mt-2">Changes apply to all future tutor responses immediately</p>
        </div>
      </div>
    </div>
  );
}
