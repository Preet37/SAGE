"use client";
import { useState } from "react";
import { Maximize2, Minimize2, X } from "lucide-react";

interface VisualPlotRendererProps {
  html: string;
  topic: string;
}

export function VisualPlotRenderer({ html, topic }: VisualPlotRendererProps) {
  const [fullscreen, setFullscreen] = useState(false);

  const iframe = (
    <iframe
      srcDoc={html}
      sandbox="allow-scripts allow-same-origin"
      className="w-full h-full border-0"
      title={`Interactive simulation: ${topic}`}
    />
  );

  if (fullscreen) {
    return (
      <div className="fixed inset-0 z-50 bg-[#0f1117] flex flex-col">
        <div className="flex items-center justify-between px-4 py-2 bg-[#161b22] border-b border-[#30363d] shrink-0">
          <span className="text-sm font-medium text-gray-200">⚡ {topic}</span>
          <button
            onClick={() => setFullscreen(false)}
            className="p-1.5 rounded-md hover:bg-[#21262d] text-gray-400 hover:text-gray-200 transition-colors"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
        <div className="flex-1 overflow-hidden">{iframe}</div>
      </div>
    );
  }

  return (
    <div className="rounded-xl overflow-hidden border border-border my-3 bg-[#0f1117]" style={{ height: 520 }}>
      <div className="flex items-center justify-between px-3 py-2 bg-[#161b22] border-b border-[#30363d] shrink-0">
        <div className="flex items-center gap-2">
          <span className="text-xs font-medium text-gray-300">⚡ Interactive Simulation</span>
          <span className="text-xs text-gray-500 truncate max-w-48">{topic}</span>
        </div>
        <button
          onClick={() => setFullscreen(true)}
          className="p-1 rounded hover:bg-[#21262d] text-gray-500 hover:text-gray-300 transition-colors"
          title="Fullscreen"
        >
          <Maximize2 className="h-3.5 w-3.5" />
        </button>
      </div>
      <div className="h-[calc(100%-37px)]">{iframe}</div>
    </div>
  );
}
