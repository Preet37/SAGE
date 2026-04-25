"use client";
import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import { Text } from "@react-three/drei";
import * as THREE from "three";

interface ConvParams {
  inputSize?: number;
  kernelSize?: number;
  stride?: number;
  featureMaps?: number;
  animated?: boolean;
  title?: string;
}

function GridCell({ position, value, highlighted, isKernel }: {
  position: [number, number, number];
  value: number;
  highlighted: boolean;
  isKernel: boolean;
}) {
  const ref = useRef<THREE.Mesh>(null!);

  useFrame(({ clock }) => {
    if (!ref.current) return;
    if (highlighted && !isKernel) {
      const mat = ref.current.material as THREE.MeshStandardMaterial;
      mat.emissiveIntensity = 0.3 + Math.sin(clock.getElapsedTime() * 3) * 0.2;
    }
  });

  const color = isKernel
    ? "#6366f1"
    : highlighted
    ? "#3b82f6"
    : new THREE.Color().setHSL(0, 0, 0.15 + value * 0.25).getHexString();

  return (
    <mesh ref={ref} position={position} castShadow>
      <boxGeometry args={[0.44, 0.44, isKernel ? 0.3 : 0.12 + value * 0.15]} />
      <meshStandardMaterial
        color={isKernel ? "#6366f1" : highlighted ? "#3b82f6" : `#${color}`}
        emissive={isKernel ? "#6366f1" : highlighted ? "#3b82f6" : "#000000"}
        emissiveIntensity={isKernel ? 0.5 : highlighted ? 0.3 : 0}
        roughness={0.5}
        metalness={0.3}
        transparent
        opacity={isKernel ? 0.85 : 0.9}
      />
    </mesh>
  );
}

export default function ConvolutionScene({ params }: { params: ConvParams }) {
  const {
    inputSize = 6,
    kernelSize = 3,
    stride = 1,
    featureMaps = 2,
    animated = true,
  } = params;

  const n = Math.min(inputSize, 8);
  const k = Math.min(kernelSize, 4);
  const CELL = 0.5;

  // Random "image" values
  const inputValues = useMemo(
    () => Array.from({ length: n * n }, () => Math.random()),
    [n]
  );

  // Random kernel weights
  const kernelValues = useMemo(
    () => Array.from({ length: k * k }, () => Math.random() * 2 - 1),
    [k]
  );

  const animState = useRef({ row: 0, col: 0 });

  useFrame(({ clock }) => {
    if (!animated) return;
    const speed = 0.8;
    const maxPos = n - k;
    const totalSteps = (maxPos + 1) * (maxPos + 1);
    const step = Math.floor(clock.getElapsedTime() * speed) % totalSteps;
    animState.current.row = Math.floor(step / (maxPos + 1));
    animState.current.col = step % (maxPos + 1);
  });

  const offsetX = -(n * CELL) / 2;
  const offsetY = (n * CELL) / 2;

  // Output size
  const outSize = Math.floor((n - k) / stride) + 1;

  return (
    <group>
      {/* Input grid */}
      <group position={[-1.5, 0, 0]}>
        <Text position={[offsetX + (n * CELL) / 2, offsetY + 0.5, 0]} fontSize={0.2} color="#94a3b8" anchorX="center">
          Input ({n}×{n})
        </Text>
        {Array.from({ length: n }, (_, row) =>
          Array.from({ length: n }, (_, col) => {
            const val = inputValues[row * n + col];
            const kr = animState.current.row;
            const kc = animState.current.col;
            const highlighted =
              row >= kr && row < kr + k && col >= kc && col < kc + k;
            return (
              <GridCell
                key={`${row}-${col}`}
                position={[offsetX + col * CELL + CELL / 2, offsetY - row * CELL - CELL / 2, 0]}
                value={val}
                highlighted={highlighted}
                isKernel={false}
              />
            );
          })
        )}
      </group>

      {/* Kernel */}
      <group position={[0.6, 0.8, 0]}>
        <Text position={[0, (k * CELL) / 2 + 0.3, 0]} fontSize={0.18} color="#a5b4fc" anchorX="center">
          Kernel ({k}×{k})
        </Text>
        {Array.from({ length: k }, (_, row) =>
          Array.from({ length: k }, (_, col) => (
            <GridCell
              key={`k-${row}-${col}`}
              position={[
                -(k * CELL) / 2 + col * CELL + CELL / 2,
                (k * CELL) / 2 - row * CELL - CELL / 2,
                0,
              ]}
              value={Math.abs(kernelValues[row * k + col])}
              highlighted={false}
              isKernel={true}
            />
          ))
        )}
      </group>

      {/* Arrow */}
      <Text position={[2.4, 0, 0]} fontSize={0.5} color="#6366f1" anchorX="center">→</Text>

      {/* Output */}
      <group position={[3.8, 0, 0]}>
        <Text
          position={[-(outSize * CELL) / 2 + (outSize * CELL) / 2, (outSize * CELL) / 2 + 0.5, 0]}
          fontSize={0.2}
          color="#34d399"
          anchorX="center"
        >
          Feature Map ({outSize}×{outSize})
        </Text>
        {Array.from({ length: outSize }, (_, row) =>
          Array.from({ length: outSize }, (_, col) => {
            const active = row === animState.current.row && col === animState.current.col;
            return (
              <GridCell
                key={`o-${row}-${col}`}
                position={[
                  -(outSize * CELL) / 2 + col * CELL + CELL / 2,
                  (outSize * CELL) / 2 - row * CELL - CELL / 2,
                  0,
                ]}
                value={active ? 0.9 : Math.random() * 0.5}
                highlighted={active}
                isKernel={false}
              />
            );
          })
        )}
      </group>
    </group>
  );
}
