'use client';
import { useState } from 'react';
import { SUPPORTED_LANGUAGES, type LangCode } from '@/lib/i18n';

interface Props {
  value: LangCode;
  onChange: (lang: LangCode) => void;
}

export default function LanguagePicker({ value, onChange }: Props) {
  const [open, setOpen] = useState(false);
  const current = SUPPORTED_LANGUAGES.find((l) => l.code === value) ?? SUPPORTED_LANGUAGES[0];

  return (
    <div className="relative">
      <button
        onClick={() => setOpen((o) => !o)}
        title="Change language / تغيير اللغة"
        className="flex items-center gap-1.5 text-[11px] font-semibold text-t2 hover:text-t0 px-2 py-1 rounded-lg hover:bg-white/5 transition-all"
        aria-haspopup="listbox"
        aria-expanded={open}
      >
        <svg className="w-3 h-3 opacity-70" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
            d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
        </svg>
        <span className={current.rtl ? 'font-arabic' : ''}>{current.nativeLabel}</span>
        <svg className={`w-2.5 h-2.5 opacity-50 transition-transform ${open ? 'rotate-180' : ''}`}
          fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {open && (
        <>
          <div className="fixed inset-0 z-40" onClick={() => setOpen(false)} />
          <div
            role="listbox"
            aria-label="Select language"
            className="absolute right-0 top-full mt-1 z-50 w-52 bg-bg2 border border-white/10 rounded-xl shadow-2xl overflow-hidden"
          >
            <div className="py-1 max-h-72 overflow-y-auto">
              {SUPPORTED_LANGUAGES.map((lang) => (
                <button
                  key={lang.code}
                  role="option"
                  aria-selected={lang.code === value}
                  onClick={() => { onChange(lang.code); setOpen(false); }}
                  className={`w-full flex items-center justify-between px-3 py-2 text-xs transition-colors ${
                    lang.code === value
                      ? 'bg-acc/20 text-acc'
                      : 'text-t1 hover:bg-white/5 hover:text-t0'
                  }`}
                >
                  <span className="font-medium">{lang.label}</span>
                  <span className={`text-t2 ${lang.rtl ? 'font-arabic' : ''}`}>{lang.nativeLabel}</span>
                </button>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
