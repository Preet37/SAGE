"use client";
import { Suspense, useRef, useState } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Environment, Stars, Grid } from "@react-three/drei";
import dynamic from "next/dynamic";

// Lazy-load scenes to avoid SSR issues
const NeuralNetScene = dynamic(() => import("./scenes/NeuralNetScene"), { ssr: false });
const GradientDescentScene = dynamic(() => import("./scenes/GradientDescentScene"), { ssr: false });
const AttentionScene = dynamic(() => import("./scenes/AttentionScene"), { ssr: false });
const DataFlowScene = dynamic(() => import("./scenes/DataFlowScene"), { ssr: false });
const ConvolutionScene = dynamic(() => import("./scenes/ConvolutionScene"), { ssr: false });
const EmbeddingScene = dynamic(() => import("./scenes/EmbeddingScene"), { ssr: false });
const CustomGeometryScene = dynamic(() => import("./scenes/CustomGeometryScene"), { ssr: false });

export interface VizConfig {
  vizType: string;
  title: string;
  description: string;
  params: Record<string, unknown>;
}

interface VisualRendererProps {
  config: VizConfig;
  onClose?: () => void;
  compact?: boolean;
}

function SceneRouter({ vizType, params }: { vizType: string; params: Record<string, unknown> }) {
  switch (vizType) {
    case "neural_network":
      return <NeuralNetScene params={params as never} />;
    case "gradient_descent":
      return <GradientDescentScene params={params as never} />;
    case "attention":
      return <AttentionScene params={params as never} />;
    case "data_flow":
      return <DataFlowScene params={params as never} />;
    case "convolution":
      return <ConvolutionScene params={params as never} />;
    case "embedding_space":
      return <EmbeddingScene params={params as never} />;
    case "decision_tree":
    case "custom_geometry":
    default:
      return <CustomGeometryScene params={params as never} />;
  }
}

function CameraPreset({ vizType }: { vizType: string }) {
  const presets: Record<string, [number, number, number]> = {
    neural_network: [0, 2, 8],
    gradient_descent: [3, 6, 5],
    attention: [0, 0, 9],
    data_flow: [0, 1, 9],
    convolution: [0, 0, 10],
    embedding_space: [0, 2, 7],
    custom_geometry: [0, 2, 8],
  };
  const pos = presets[vizType] ?? [0, 2, 8];

  return (
    <OrbitControls
      enablePan={false}
      enableZoom={true}
      autoRotate={vizType === "embedding_space"}
      autoRotateSpeed={0.8}
      minDistance={3}
      maxDistance={20}
      target={[0, 0, 0]}
    />
  );
}

export default function VisualRenderer({ config, onClose, compact = false }: VisualRendererProps) {
  const [fullscreen, setFullscreen] = useState(false);

  const height = fullscreen ? "85vh" : compact ? "280px" : "420px";

  return (
    <div
      className={`relative rounded-xl overflow-hidden border border-slate-700/50 bg-[#050a14] ${fullscreen ? "fixed inset-4 z-50" : ""}`}
      style={{ height }}
    >
      {/* Header */}
      <div className="absolute top-0 left-0 right-0 z-10 px-4 py-2 flex items-center justify-between bg-gradient-to-b from-[#050a14] to-transparent pointer-events-none">
        <div>
          <h3 className="text-sm font-semibold text-white">{config.title}</h3>
          {!compact && (
            <p className="text-xs text-slate-400 mt-0.5">{config.description}</p>
          )}
        </div>
        <div className="flex items-center gap-1.5 pointer-events-auto">
          {/* Viz type badge */}
          <span className="text-[10px] px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-mono">
            {config.vizType}
          </span>
          <button
            onClick={() => setFullscreen(f => !f)}
            className="text-slate-400 hover:text-white p-1 rounded transition-colors"
            title={fullscreen ? "Exit fullscreen" : "Fullscreen"}
          >
            {fullscreen ? (
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 9L4 4m0 0v4m0-4h4M15 15l5 5m0 0v-4m0 4h-4M9 15l-5 5m0 0v-4m0 4h4M15 9l5-5m0 0v4m0-4h-4" />
              </svg>
            ) : (
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-5h-4m4 0v4m0-4l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
              </svg>
            )}
          </button>
          {onClose && (
            <button
              onClick={onClose}
              className="text-slate-400 hover:text-white p-1 rounded transition-colors"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
      </div>

      {/* Orbit hint */}
      <div className="absolute bottom-2 left-1/2 -translate-x-1/2 z-10 text-[10px] text-slate-600 pointer-events-none">
        drag to orbit · scroll to zoom
      </div>

      {/* Three.js Canvas */}
      <Canvas
        camera={{ position: [0, 2, 8], fov: 55 }}
        gl={{ antialias: true, alpha: false }}
        shadows
        dpr={[1, 2]}
      >
        {/* Lighting */}
        <ambientLight intensity={0.4} />
        <directionalLight
          position={[8, 12, 6]}
          intensity={1.2}
          castShadow
          shadow-mapSize={[2048, 2048]}
        />
        <pointLight position={[-5, 5, -5]} intensity={0.4} color="#6366f1" />
        <pointLight position={[5, -3, 5]} intensity={0.2} color="#06b6d4" />

        {/* Background stars */}
        <Stars radius={60} depth={40} count={800} factor={2} saturation={0} fade speed={0.5} />

        {/* Grid floor */}
        <Grid
          args={[20, 20]}
          cellSize={1}
          cellThickness={0.3}
          cellColor="#1e293b"
          sectionSize={5}
          sectionThickness={0.6}
          sectionColor="#1e3a5f"
          fadeDistance={18}
          fadeStrength={1}
          position={[0, -3.5, 0]}
        />

        {/* Camera controls */}
        <CameraPreset vizType={config.vizType} />

        {/* Scene */}
        <Suspense fallback={null}>
          <SceneRouter vizType={config.vizType} params={config.params} />
        </Suspense>
      </Canvas>
    </div>
  );
}
