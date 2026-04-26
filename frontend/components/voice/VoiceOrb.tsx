"use client";

import { useCallback, useRef, useState } from "react";
import { Mic, MicOff, X, Volume2, Loader2, MessageSquare, ChevronDown, ChevronUp } from "lucide-react";
import { useVoiceConversation, VoiceMessage } from "@/lib/useVoiceConversation";

interface VoiceOrbProps {
  contextOverride?: string;
}

export function VoiceOrb({ contextOverride }: VoiceOrbProps) {
  const [expanded, setExpanded] = useState(false);
  const [showTranscript, setShowTranscript] = useState(false);
  const transcriptRef = useRef<HTMLDivElement>(null);

  const {
    status,
    mode,
    messages,
    error,
    isMuted,
    isActive,
    startConversation,
    stopConversation,
    toggleMute,
  } = useVoiceConversation({ contextOverride });

  const handleToggle = useCallback(async () => {
    if (isActive) {
      await stopConversation();
      setExpanded(false);
      setShowTranscript(false);
    } else {
      setExpanded(true);
      await startConversation();
    }
  }, [isActive, startConversation, stopConversation]);

  const orbBg = {
    idle:       "linear-gradient(135deg, #C4985A 0%, #9A7840 100%)",
    connecting: "linear-gradient(135deg, #C4985A 0%, #D4A870 100%)",
    connected:
      mode === "speaking"
        ? "linear-gradient(135deg, #7B9E82 0%, #4E7A5A 100%)"
        : mode === "listening"
        ? "linear-gradient(135deg, #C4985A 0%, #7B9E82 100%)"
        : "linear-gradient(135deg, #C4985A 0%, #9A7840 100%)",
    error: "linear-gradient(135deg, #C97C68 0%, #A05040 100%)",
  }[status];

  const pulseClass =
    mode === "listening"
      ? "animate-pulse"
      : mode === "speaking"
      ? "animate-bounce"
      : "";

  const statusLabel = {
    idle: "Start Voice Learning",
    connecting: "Connecting...",
    connected:
      mode === "speaking" ? "SAGE is speaking..." : mode === "listening" ? "Listening..." : "Connected",
    error: "Error — tap to retry",
  }[status];

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3">
      {/* Expanded panel */}
      {expanded && (
        <div className="w-80 rounded-2xl border border-border bg-background/95 backdrop-blur-md shadow-2xl overflow-hidden">
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 text-white" style={{ background: orbBg }}>
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full bg-white ${pulseClass}`} />
              <span className="text-sm font-semibold">{statusLabel}</span>
            </div>
            <div className="flex items-center gap-1">
              {isActive && (
                <button
                  onClick={() => setShowTranscript((p) => !p)}
                  className="p-1.5 rounded-lg hover:bg-white/20 transition-colors"
                  title="Toggle transcript"
                >
                  <MessageSquare className="h-3.5 w-3.5" />
                </button>
              )}
              <button
                onClick={() => setExpanded(false)}
                className="p-1.5 rounded-lg hover:bg-white/20 transition-colors"
              >
                <ChevronDown className="h-3.5 w-3.5" />
              </button>
            </div>
          </div>

          {/* Error message */}
          {error && (
            <div className="mx-3 mt-3 px-3 py-2 rounded-lg bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 text-xs">
              {error}
            </div>
          )}

          {/* Visualizer / idle state */}
          {isActive && (
            <div className="px-4 py-4 flex flex-col items-center gap-4">
              {/* Audio wave visualizer */}
              <div className="flex items-end gap-1 h-10">
                {Array.from({ length: 12 }).map((_, i) => (
                  <div
                    key={i}
                    className="w-1.5 rounded-full transition-all"
                    style={{ background: orbBg }}
                    style={{
                      height: mode !== "idle" ? `${8 + (i % 4) * 8}px` : "4px",
                      animation: mode !== "idle" ? `voice-bar ${0.6 + (i % 4) * 0.1}s ease-in-out infinite alternate` : "none",
                      animationDelay: `${i * 60}ms`,
                    }}
                  />
                ))}
              </div>

              {/* Controls */}
              <div className="flex items-center gap-3">
                <button
                  onClick={toggleMute}
                  className={`p-2.5 rounded-full border transition-all ${
                    isMuted
                      ? "bg-red-100 dark:bg-red-950 border-red-300 dark:border-red-700 text-red-600 dark:text-red-400"
                      : "border-border hover:bg-muted"
                  }`}
                  title={isMuted ? "Unmute" : "Mute"}
                >
                  {isMuted ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
                </button>

                <button
                  onClick={handleToggle}
                  className="p-3 rounded-full bg-red-600 hover:bg-red-700 text-white transition-colors"
                  title="End conversation"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
            </div>
          )}

          {/* Transcript */}
          {showTranscript && messages.length > 0 && (
            <div
              ref={transcriptRef}
              className="max-h-56 overflow-y-auto px-3 pb-3 flex flex-col gap-2 border-t border-border"
            >
              <p className="text-[10px] font-medium text-muted-foreground uppercase tracking-widest pt-2 pb-1">
                Transcript
              </p>
              {messages.map((msg: VoiceMessage) => (
                <div
                  key={msg.id}
                  className={`text-xs px-3 py-2 rounded-xl max-w-[90%] ${
                    msg.role === "user"
                      ? "self-end bg-primary text-primary-foreground"
                      : "self-start bg-muted text-foreground"
                  }`}
                >
                  {msg.text}
                </div>
              ))}
            </div>
          )}

          {/* Start button when not yet connected */}
          {!isActive && (
            <div className="px-4 pb-4 pt-3">
              <button
                onClick={handleToggle}
                disabled={status === "connecting"}
                className="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-medium text-white transition-all hover:opacity-90 disabled:opacity-60"
                style={{ background: orbBg }}
              >
                {status === "connecting" ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Connecting...
                  </>
                ) : (
                  <>
                    <Mic className="h-4 w-4" />
                    Start Voice Session
                  </>
                )}
              </button>
            </div>
          )}
        </div>
      )}

      {/* Floating orb button */}
      <button
        onClick={expanded ? () => setExpanded(false) : handleToggle}
        className={`
          relative w-14 h-14 rounded-full shadow-2xl flex items-center justify-center
          text-white transition-all duration-300
          hover:scale-110 active:scale-95 focus:outline-none focus:ring-4 focus:ring-[#C4985A]/40
          ${isActive && mode !== "idle" ? "ring-4 ring-white/30" : ""}
        `}
        title={isActive ? statusLabel : "Start SAGE Voice Tutor"}
        aria-label="SAGE Voice Tutor"
        style={{ background: orbBg }}
      >
        {/* Ripple ring when active */}
        {isActive && (
          <span className="absolute inset-0 rounded-full animate-ping bg-white/20 pointer-events-none" />
        )}

        {status === "connecting" ? (
          <Loader2 className="h-6 w-6 animate-spin" />
        ) : isActive ? (
          mode === "speaking" ? (
            <Volume2 className="h-6 w-6" />
          ) : mode === "listening" ? (
            <Mic className="h-6 w-6 animate-pulse" />
          ) : expanded ? (
            <ChevronDown className="h-6 w-6" />
          ) : (
            <Mic className="h-6 w-6" />
          )
        ) : expanded ? (
          <ChevronDown className="h-6 w-6" />
        ) : (
          <Mic className="h-6 w-6" />
        )}
      </button>
    </div>
  );
}
