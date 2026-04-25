"use client";
import { useState } from "react";

export interface VisualPlot {
  html: string;
  title: string;
  concept: string;
  chars?: number;
  user_code_lines?: number;
}

interface Props {
  data: VisualPlot;
  onClose?: () => void;
}

export default function VisualPlotRenderer({ data, onClose }: Props) {
  const [fullscreen, setFullscreen] = useState(true);

  return (
    <div
      className={`relative rounded-xl overflow-hidden border border-slate-700/30 bg-[#07111f] ${
        fullscreen
          ? "fixed inset-2 z-50 shadow-2xl shadow-black/80"
          : "mt-1"
      }`}
      style={{ height: fullscreen ? "calc(100vh - 16px)" : "600px" }}
    >
      {/* Slim top bar */}
      <div className="absolute top-0 left-0 right-0 z-10 h-8 flex items-center justify-between px-3 bg-[#07111fee] border-b border-slate-800/60 backdrop-blur-sm">
        <div className="flex items-center gap-2 min-w-0">
          <div className="w-1.5 h-1.5 rounded-full bg-indigo-500 flex-shrink-0" />
          <span className="text-[11px] font-semibold text-slate-300 truncate">{data.title}</span>
          {data.user_code_lines && (
            <span className="text-[10px] text-slate-600 hidden sm:inline">· {data.user_code_lines} lines</span>
          )}
        </div>
        <div className="flex items-center gap-0.5 flex-shrink-0">
          <button
            onClick={() => setFullscreen((f) => !f)}
            className="p-1.5 rounded-lg text-slate-500 hover:text-slate-300 hover:bg-slate-800/50 transition-colors"
            title={fullscreen ? "Exit fullscreen" : "Fullscreen (recommended)"}
          >
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {fullscreen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M9 9L4 4m0 0v4m0-4h4M15 15l5 5m0 0v-4m0 4h-4M9 15l-5 5m0 0v-4m0 4h4M15 9l5-5m0 0v4m0-4h-4" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M4 8V4m0 0h4M4 4l5 5m11-5h-4m4 0v4m0-4l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
              )}
            </svg>
          </button>
          {onClose && (
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-500 hover:text-slate-300 hover:bg-slate-800/50 transition-colors"
            >
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
      </div>

      {/* The interactive Plotly page — full height minus the slim top bar */}
      <div className="absolute inset-0 top-8">
        <iframe
          srcDoc={data.html}
          className="w-full h-full border-0"
          sandbox="allow-scripts"
          title={`Interactive plot: ${data.title}`}
        />
      </div>
    </div>
  );
}
