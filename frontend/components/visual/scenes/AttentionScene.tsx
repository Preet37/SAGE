"use client";
import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import { Text, RoundedBox } from "@react-three/drei";
import * as THREE from "three";

interface AttentionParams {
  tokens?: string[];
  highlightToken?: number;
  attentionWeights?: number[][];
  title?: string;
  description?: string;
}

function AttentionCell({
  position,
  weight,
  isHighlighted,
  rowLabel,
  colLabel,
  showLabels,
}: {
  position: [number, number, number];
  weight: number;
  isHighlighted: boolean;
  rowLabel?: string;
  colLabel?: string;
  showLabels: boolean;
}) {
  const meshRef = useRef<THREE.Mesh>(null!);

  useFrame(({ clock }) => {
    if (!meshRef.current || !isHighlighted) return;
    const t = clock.getElapsedTime();
    const mat = meshRef.current.material as THREE.MeshStandardMaterial;
    mat.emissiveIntensity = 0.3 + Math.sin(t * 2) * 0.15;
  });

  const color = new THREE.Color().setHSL(
    isHighlighted ? 0.62 : 0.55,
    0.85,
    0.2 + weight * 0.45
  );

  return (
    <mesh ref={meshRef} position={position} castShadow>
      <boxGeometry args={[0.85, 0.85, 0.1 + weight * 0.5]} />
      <meshStandardMaterial
        color={color}
        emissive={color}
        emissiveIntensity={isHighlighted ? 0.4 : 0.05}
        roughness={0.3}
        metalness={0.5}
        transparent
        opacity={0.6 + weight * 0.35}
      />
    </mesh>
  );
}

function TokenLabel({
  position,
  label,
  isQuery,
}: {
  position: [number, number, number];
  label: string;
  isQuery: boolean;
}) {
  return (
    <group>
      <RoundedBox position={position} args={[1.1, 0.35, 0.06]} radius={0.06} smoothness={4}>
        <meshStandardMaterial
          color={isQuery ? "#6366f1" : "#1e293b"}
          emissive={isQuery ? "#6366f1" : "#0f172a"}
          emissiveIntensity={isQuery ? 0.5 : 0.1}
        />
      </RoundedBox>
      <Text position={position} fontSize={0.16} color={isQuery ? "#e0e7ff" : "#94a3b8"} anchorX="center" anchorY="middle" renderOrder={1}>
        {label}
      </Text>
    </group>
  );
}

export default function AttentionScene({ params }: { params: AttentionParams }) {
  const {
    tokens = ["The", "cat", "sat", "on", "mat"],
    highlightToken = 1,
    attentionWeights,
  } = params;

  const n = Math.min(tokens.length, 6);
  const displayTokens = tokens.slice(0, n);

  // Default uniform attention if not provided, then highlight pattern
  const weights = useMemo<number[][]>(() => {
    if (attentionWeights && attentionWeights.length >= n) {
      return attentionWeights.slice(0, n).map(row => row.slice(0, n));
    }
    // Synthesize plausible attention weights
    return Array.from({ length: n }, (_, i) => {
      const row = Array.from({ length: n }, (_, j) => {
        if (i === highlightToken) return Math.random() * 0.4 + (j === i ? 0.5 : 0.1);
        return Math.random() * 0.3 + 0.1;
      });
      const sum = row.reduce((a, b) => a + b, 0);
      return row.map(v => v / sum);
    });
  }, [attentionWeights, n, highlightToken]);

  const CELL_SIZE = 0.95;
  const offset = ((n - 1) * CELL_SIZE) / 2;

  return (
    <group position={[0, 0.5, 0]}>
      {/* Attention matrix cells */}
      {Array.from({ length: n }, (_, row) =>
        Array.from({ length: n }, (_, col) => {
          const w = weights[row]?.[col] ?? 0.1;
          return (
            <AttentionCell
              key={`${row}-${col}`}
              position={[
                (col - (n - 1) / 2) * CELL_SIZE,
                (row - (n - 1) / 2) * -CELL_SIZE,
                0,
              ]}
              weight={w}
              isHighlighted={row === highlightToken || col === highlightToken}
              rowLabel={displayTokens[row]}
              colLabel={displayTokens[col]}
              showLabels={false}
            />
          );
        })
      )}

      {/* Row labels (Query) */}
      {displayTokens.map((token, i) => (
        <TokenLabel
          key={`row-${i}`}
          position={[-(n / 2) * CELL_SIZE - 0.8, (i - (n - 1) / 2) * -CELL_SIZE, 0]}
          label={token}
          isQuery={i === highlightToken}
        />
      ))}

      {/* Col labels (Key) */}
      {displayTokens.map((token, i) => (
        <TokenLabel
          key={`col-${i}`}
          position={[(i - (n - 1) / 2) * CELL_SIZE, (n / 2) * CELL_SIZE + 0.5, 0]}
          label={token}
          isQuery={false}
        />
      ))}

      {/* Axis labels */}
      <Text position={[-(n / 2) * CELL_SIZE - 0.8, (n / 2) * CELL_SIZE + 0.5, 0]} fontSize={0.16} color="#64748b" anchorX="center">
        Query →
      </Text>
      <Text position={[-(n / 2) * CELL_SIZE - 1.8, 0, 0]} fontSize={0.16} color="#64748b" anchorX="center" rotation={[0, 0, Math.PI / 2]}>
        ← Key
      </Text>

      {/* Highlight row/col bars */}
      <mesh position={[0, (highlightToken - (n - 1) / 2) * -CELL_SIZE, -0.08]} receiveShadow>
        <planeGeometry args={[n * CELL_SIZE, 0.85]} />
        <meshStandardMaterial color="#6366f1" transparent opacity={0.07} />
      </mesh>
      <mesh position={[(highlightToken - (n - 1) / 2) * CELL_SIZE, 0, -0.08]} receiveShadow>
        <planeGeometry args={[0.85, n * CELL_SIZE]} />
        <meshStandardMaterial color="#6366f1" transparent opacity={0.07} />
      </mesh>
    </group>
  );
}
