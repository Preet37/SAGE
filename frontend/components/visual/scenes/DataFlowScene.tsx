"use client";
import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import { Text, RoundedBox } from "@react-three/drei";
import * as THREE from "three";

interface Stage {
  label: string;
  type?: string;
  color?: string;
}

interface DataFlowParams {
  stages?: Stage[];
  animated?: boolean;
  title?: string;
  description?: string;
}

const DEFAULT_COLORS: Record<string, string> = {
  input: "#3b82f6",
  transform: "#8b5cf6",
  output: "#10b981",
  process: "#f59e0b",
  model: "#ec4899",
  storage: "#64748b",
  default: "#6366f1",
};

function DataParticle({ from, to, offset, color }: {
  from: THREE.Vector3;
  to: THREE.Vector3;
  offset: number;
  color: string;
}) {
  const ref = useRef<THREE.Mesh>(null!);

  useFrame(({ clock }) => {
    if (!ref.current) return;
    const t = ((clock.getElapsedTime() * 0.5 + offset) % 1 + 1) % 1;
    ref.current.position.lerpVectors(from, to, t);
    ref.current.scale.setScalar(0.5 + Math.sin(t * Math.PI) * 0.5);
    const mat = ref.current.material as THREE.MeshStandardMaterial;
    mat.opacity = Math.sin(t * Math.PI);
  });

  return (
    <mesh ref={ref}>
      <sphereGeometry args={[0.06, 12, 12]} />
      <meshStandardMaterial color={color} emissive={color} emissiveIntensity={1.2} transparent opacity={1} />
    </mesh>
  );
}

function ConnectionArrow({ from, to, color }: {
  from: [number, number, number];
  to: [number, number, number];
  color: string;
}) {
  const dir = useMemo(() => {
    const d = new THREE.Vector3(to[0] - from[0], to[1] - from[1], to[2] - from[2]);
    return d.normalize();
  }, [from, to]);

  const mid: [number, number, number] = [
    (from[0] + to[0]) / 2,
    (from[1] + to[1]) / 2,
    (from[2] + to[2]) / 2,
  ];

  const len = Math.sqrt(
    (to[0] - from[0]) ** 2 + (to[1] - from[1]) ** 2 + (to[2] - from[2]) ** 2
  );

  return (
    <group>
      <mesh position={mid}>
        <cylinderGeometry args={[0.015, 0.015, len - 1.4, 6]} />
        <meshStandardMaterial color={color} transparent opacity={0.4} />
      </mesh>
    </group>
  );
}

export default function DataFlowScene({ params }: { params: DataFlowParams }) {
  const {
    stages = [
      { label: "Raw Data", type: "input", color: "#3b82f6" },
      { label: "Preprocess", type: "transform", color: "#8b5cf6" },
      { label: "Embedding", type: "model", color: "#ec4899" },
      { label: "Model", type: "model", color: "#6366f1" },
      { label: "Output", type: "output", color: "#10b981" },
    ],
    animated = true,
  } = params;

  const n = Math.min(stages.length, 7);
  const displayStages = stages.slice(0, n);
  const SPACING = 2.4;

  const positions = useMemo<THREE.Vector3[]>(() => {
    return displayStages.map((_, i) => {
      const x = (i - (n - 1) / 2) * SPACING;
      return new THREE.Vector3(x, 0, 0);
    });
  }, [displayStages, n, SPACING]);

  return (
    <group>
      {/* Stage nodes */}
      {displayStages.map((stage, i) => {
        const color = stage.color || DEFAULT_COLORS[stage.type || "default"] || DEFAULT_COLORS.default;
        const pos = positions[i];

        return (
          <group key={i} position={pos.toArray() as [number, number, number]}>
            <RoundedBox args={[1.5, 0.7, 0.2]} radius={0.1} smoothness={4} castShadow>
              <meshStandardMaterial
                color={color}
                emissive={color}
                emissiveIntensity={0.25}
                roughness={0.4}
                metalness={0.5}
              />
            </RoundedBox>
            <Text
              position={[0, 0, 0.15]}
              fontSize={0.18}
              color="#f8fafc"
              anchorX="center"
              anchorY="middle"
              maxWidth={1.3}
            >
              {stage.label}
            </Text>
            {/* Step number */}
            <Text
              position={[0, -0.55, 0]}
              fontSize={0.13}
              color="#64748b"
              anchorX="center"
            >
              step {i + 1}
            </Text>
          </group>
        );
      })}

      {/* Connections + particles */}
      {displayStages.slice(0, -1).map((stage, i) => {
        const from = positions[i];
        const to = positions[i + 1];
        const color = stage.color || "#6366f1";

        return (
          <group key={`conn-${i}`}>
            <ConnectionArrow
              from={from.toArray() as [number, number, number]}
              to={to.toArray() as [number, number, number]}
              color={color}
            />
            {animated && [0, 0.33, 0.66].map((offset, pi) => (
              <DataParticle
                key={pi}
                from={from}
                to={to}
                offset={offset}
                color={color}
              />
            ))}
          </group>
        );
      })}
    </group>
  );
}
