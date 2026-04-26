import React from "react";

interface SageLogoProps {
  /** em-relative size of the SAGE text. Default: 1.1rem */
  fontSize?: string;
}

/** Brand logo: mini constellation + SAGE + gold circle period */
export function SageLogo({ fontSize = "1.1rem" }: SageLogoProps) {
  return (
    <div style={{ display: "inline-flex", alignItems: "center", gap: "0.55em", lineHeight: 1 }}>
      {/* Mini knowledge-graph icon */}
      <svg
        viewBox="0 0 44 64"
        fill="none"
        style={{ height: "1.15em", width: "auto", flexShrink: 0 }}
        aria-hidden="true"
      >
        {/* Edges */}
        <line x1="14" y1="10" x2="28" y2="18" stroke="#A89880" strokeWidth="0.9" strokeOpacity="0.45" />
        <line x1="14" y1="10" x2="6"  y2="26" stroke="#A89880" strokeWidth="0.9" strokeOpacity="0.45" />
        <line x1="6"  y1="26" x2="20" y2="32" stroke="#A89880" strokeWidth="0.9" strokeOpacity="0.45" />
        <line x1="20" y1="32" x2="28" y2="18" stroke="#A89880" strokeWidth="0.9" strokeOpacity="0.45" />
        <line x1="6"  y1="26" x2="12" y2="44" stroke="#A89880" strokeWidth="0.9" strokeOpacity="0.45" />
        <line x1="12" y1="44" x2="26" y2="52" stroke="#A89880" strokeWidth="0.9" strokeOpacity="0.45" />
        <line x1="20" y1="32" x2="12" y2="44" stroke="#A89880" strokeWidth="0.9" strokeOpacity="0.45" />
        <line x1="28" y1="18" x2="38" y2="28" stroke="#A89880" strokeWidth="0.9" strokeOpacity="0.45" />
        <line x1="26" y1="52" x2="36" y2="58" stroke="#A89880" strokeWidth="0.9" strokeOpacity="0.45" />

        {/* Cream / white large nodes */}
        <circle cx="14" cy="10" r="4.5" fill="#F0E9D6" />
        <circle cx="20" cy="32" r="6"   fill="#F0E9D6" />
        <circle cx="26" cy="52" r="4"   fill="#F0E9D6" />

        {/* Gold medium nodes */}
        <circle cx="6"  cy="26" r="4.2" fill="#C4985A" />
        <circle cx="36" cy="58" r="3.5" fill="#C4985A" />

        {/* Sage-green small nodes */}
        <circle cx="28" cy="18" r="2.8" fill="#7B9E82" />
        <circle cx="12" cy="44" r="2.8" fill="#7B9E82" />
        <circle cx="38" cy="28" r="2.2" fill="#7B9E82" />
      </svg>

      {/* SAGE text */}
      <span
        style={{
          fontFamily: "var(--font-cormorant)",
          fontWeight: 700,
          fontStyle: "normal",
          fontSize,
          color: "var(--cream-0)",
          letterSpacing: "-0.01em",
          lineHeight: 1,
        }}
      >
        SAGE
      </span>

      {/* Gold circle period */}
      <span
        style={{
          display: "inline-block",
          width: "0.22em",
          height: "0.22em",
          borderRadius: "50%",
          background: "var(--gold)",
          flexShrink: 0,
          alignSelf: "flex-end",
          marginBottom: "0.08em",
        }}
      />
    </div>
  );
}
