"use client";
import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import { Text, Line } from "@react-three/drei";
import * as THREE from "three";

interface NeuralNetParams {
  layers: number[];
  activations?: string[];
  highlightLayer?: number;
  showWeights?: boolean;
  animated?: boolean;
  title?: string;
  description?: string;
}

const LAYER_COLORS = ["#60a5fa", "#a78bfa", "#34d399", "#f59e0b", "#f87171", "#38bdf8"];
const ACTIVATION_COLORS: Record<string, string> = {
  relu: "#34d399",
  sigmoid: "#f59e0b",
  tanh: "#a78bfa",
  softmax: "#f87171",
  linear: "#60a5fa",
};

function Neuron({
  position,
  color,
  layerIndex,
  highlightLayer,
  pulseOffset,
  animated,
}: {
  position: [number, number, number];
  color: string;
  layerIndex: number;
  highlightLayer?: number;
  pulseOffset: number;
  animated: boolean;
}) {
  const meshRef = useRef<THREE.Mesh>(null!);
  const isHighlighted = highlightLayer === layerIndex;

  useFrame(({ clock }) => {
    if (!animated || !meshRef.current) return;
    const t = clock.getElapsedTime();
    const wave = (Math.sin(t * 1.5 + pulseOffset) + 1) / 2;
    const mat = meshRef.current.material as THREE.MeshStandardMaterial;
    mat.emissiveIntensity = isHighlighted ? 0.4 + wave * 0.6 : 0.1 + wave * 0.15;
    meshRef.current.scale.setScalar(isHighlighted ? 1 + wave * 0.08 : 1);
  });

  return (
    <mesh ref={meshRef} position={position} castShadow>
      <sphereGeometry args={[0.18, 32, 32]} />
      <meshStandardMaterial
        color={color}
        emissive={color}
        emissiveIntensity={isHighlighted ? 0.6 : 0.15}
        roughness={0.3}
        metalness={0.4}
      />
    </mesh>
  );
}

export default function NeuralNetScene({ params }: { params: NeuralNetParams }) {
  const {
    layers = [2, 4, 4, 1],
    activations = [],
    highlightLayer,
    showWeights = true,
    animated = true,
  } = params;

  const LAYER_SPACING = 2.2;
  const MAX_NEURONS = Math.max(...layers);

  // Build neuron positions
  const neuronPositions = useMemo(() => {
    return layers.map((count, li) => {
      const x = (li - (layers.length - 1) / 2) * LAYER_SPACING;
      return Array.from({ length: count }, (_, ni) => {
        const y = (ni - (count - 1) / 2) * (4 / Math.max(count, 4));
        return [x, y, 0] as [number, number, number];
      });
    });
  }, [layers]);

  // Build connection lines (weight edges)
  const connections = useMemo(() => {
    if (!showWeights) return [];
    const lines: { start: [number, number, number]; end: [number, number, number]; opacity: number }[] = [];
    for (let li = 0; li < layers.length - 1; li++) {
      for (let ni = 0; ni < layers[li]; ni++) {
        for (let nj = 0; nj < layers[li + 1]; nj++) {
          // limit edges for large layers
          if (layers[li] > 5 && layers[li + 1] > 5 && Math.random() > 0.4) continue;
          lines.push({
            start: neuronPositions[li][ni],
            end: neuronPositions[li + 1][nj],
            opacity: 0.12 + Math.random() * 0.12,
          });
        }
      }
    }
    return lines;
  }, [neuronPositions, layers, showWeights]);

  return (
    <group>
      {/* Connections */}
      {connections.map((c, i) => (
        <Line
          key={i}
          points={[c.start, c.end]}
          color="#6366f1"
          lineWidth={0.5}
          transparent
          opacity={c.opacity}
        />
      ))}

      {/* Neurons */}
      {neuronPositions.map((layerNeurons, li) =>
        layerNeurons.map((pos, ni) => {
          const activation = activations[li] || "relu";
          const color =
            li === 0
              ? "#60a5fa"
              : li === layers.length - 1
              ? "#f87171"
              : ACTIVATION_COLORS[activation] || LAYER_COLORS[li % LAYER_COLORS.length];
          return (
            <Neuron
              key={`${li}-${ni}`}
              position={pos}
              color={color}
              layerIndex={li}
              highlightLayer={highlightLayer}
              pulseOffset={li * 0.8 + ni * 0.3}
              animated={animated}
            />
          );
        })
      )}

      {/* Layer labels */}
      {layers.map((count, li) => {
        const x = (li - (layers.length - 1) / 2) * LAYER_SPACING;
        const label =
          li === 0 ? "Input" : li === layers.length - 1 ? "Output" : `Hidden ${li}`;
        const activation = activations[li - 1];
        return (
          <group key={li}>
            <Text
              position={[x, -2.6, 0]}
              fontSize={0.18}
              color="#94a3b8"
              anchorX="center"
              anchorY="middle"
            >
              {label}
            </Text>
            <Text
              position={[x, -3.0, 0]}
              fontSize={0.13}
              color="#64748b"
              anchorX="center"
              anchorY="middle"
            >
              {count} neurons{activation ? ` · ${activation}` : ""}
            </Text>
          </group>
        );
      })}
    </group>
  );
}

