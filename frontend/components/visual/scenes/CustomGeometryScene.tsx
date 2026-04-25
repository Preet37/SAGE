"use client";
import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import { Text, Line } from "@react-three/drei";
import * as THREE from "three";

interface SceneObject {
  type: "box" | "sphere" | "cylinder" | "cone" | "torus";
  position?: [number, number, number];
  size?: [number, number, number];
  color?: string;
  label?: string;
  opacity?: number;
}

interface Connection {
  from: number;
  to: number;
  color?: string;
}

interface CustomParams {
  objects?: SceneObject[];
  connections?: Connection[];
  animated?: boolean;
  title?: string;
}

function SceneObj({ obj, index, animated }: { obj: SceneObject; index: number; animated: boolean }) {
  const ref = useRef<THREE.Mesh>(null!);

  useFrame(({ clock }) => {
    if (!animated || !ref.current) return;
    ref.current.rotation.y = clock.getElapsedTime() * 0.3 + index * 0.5;
  });

  const pos = obj.position ?? [0, 0, 0];
  const size = obj.size ?? [1, 1, 1];
  const color = obj.color ?? "#6366f1";
  const opacity = obj.opacity ?? 1;

  const geometry = useMemo(() => {
    switch (obj.type) {
      case "sphere":
        return <sphereGeometry args={[size[0] / 2, 32, 32]} />;
      case "cylinder":
        return <cylinderGeometry args={[size[0] / 2, size[0] / 2, size[1], 32]} />;
      case "cone":
        return <coneGeometry args={[size[0] / 2, size[1], 32]} />;
      case "torus":
        return <torusGeometry args={[size[0] / 2, size[1] / 5, 16, 32]} />;
      default:
        return <boxGeometry args={size} />;
    }
  }, [obj.type, size]);

  return (
    <group position={pos}>
      <mesh ref={ref} castShadow>
        {geometry}
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={0.2}
          roughness={0.4}
          metalness={0.4}
          transparent={opacity < 1}
          opacity={opacity}
        />
      </mesh>
      {obj.label && (
        <Text position={[0, (size[1] ?? 1) / 2 + 0.3, 0]} fontSize={0.18} color="#94a3b8" anchorX="center">
          {obj.label}
        </Text>
      )}
    </group>
  );
}

export default function CustomGeometryScene({ params }: { params: CustomParams }) {
  const {
    objects = [
      { type: "sphere", position: [-2, 0, 0], size: [0.8, 0.8, 0.8], color: "#60a5fa", label: "Input" },
      { type: "box", position: [0, 0, 0], size: [1.2, 0.8, 0.4], color: "#8b5cf6", label: "Process" },
      { type: "cone", position: [2, 0, 0], size: [0.8, 1, 0.8], color: "#34d399", label: "Output" },
    ],
    connections = [{ from: 0, to: 1 }, { from: 1, to: 2 }],
    animated = true,
  } = params;

  const safeObjects = objects.slice(0, 12);

  return (
    <group>
      {/* Connection lines */}
      {connections.map((conn, i) => {
        const from = safeObjects[conn.from];
        const to = safeObjects[conn.to];
        if (!from || !to) return null;
        const fp = from.position ?? [0, 0, 0];
        const tp = to.position ?? [0, 0, 0];
        return (
          <Line
            key={i}
            points={[fp, tp]}
            color={conn.color ?? "#475569"}
            lineWidth={1.5}
            transparent
            opacity={0.5}
          />
        );
      })}

      {/* Objects */}
      {safeObjects.map((obj, i) => (
        <SceneObj key={i} obj={obj} index={i} animated={animated} />
      ))}
    </group>
  );
}
