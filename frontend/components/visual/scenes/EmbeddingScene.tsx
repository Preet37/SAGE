"use client";
import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import { Text, Sphere, Line } from "@react-three/drei";
import * as THREE from "three";

interface EmbeddingPoint {
  label: string;
  x: number;
  y: number;
  z: number;
  cluster: string;
}

interface EmbeddingCluster {
  name: string;
  color: string;
}

interface EmbeddingParams {
  points?: EmbeddingPoint[];
  clusters?: EmbeddingCluster[];
  title?: string;
}

const CLUSTER_COLORS = ["#60a5fa", "#f87171", "#34d399", "#f59e0b", "#a78bfa", "#38bdf8", "#fb923c"];

export default function EmbeddingScene({ params }: { params: EmbeddingParams }) {
  const {
    points = [
      { label: "king", x: 1.5, y: 0.8, z: 0.2, cluster: "royalty" },
      { label: "queen", x: 1.3, y: 1.1, z: 0.3, cluster: "royalty" },
      { label: "prince", x: 1.8, y: 0.5, z: 0.4, cluster: "royalty" },
      { label: "dog", x: -1.5, y: 0.5, z: 1.0, cluster: "animals" },
      { label: "cat", x: -1.2, y: 0.3, z: 0.8, cluster: "animals" },
      { label: "wolf", x: -1.8, y: 0.7, z: 1.2, cluster: "animals" },
      { label: "Paris", x: 0.2, y: -1.5, z: -0.5, cluster: "cities" },
      { label: "London", x: 0.5, y: -1.8, z: -0.3, cluster: "cities" },
      { label: "Tokyo", x: -0.2, y: -1.3, z: -0.7, cluster: "cities" },
    ],
    clusters = [
      { name: "royalty", color: "#f59e0b" },
      { name: "animals", color: "#34d399" },
      { name: "cities", color: "#60a5fa" },
    ],
  } = params;

  const groupRef = useRef<THREE.Group>(null!);

  useFrame(({ clock }) => {
    if (!groupRef.current) return;
    groupRef.current.rotation.y = clock.getElapsedTime() * 0.12;
  });

  const clusterColorMap = useMemo(() => {
    const map: Record<string, string> = {};
    clusters.forEach((c, i) => {
      map[c.name] = c.color || CLUSTER_COLORS[i % CLUSTER_COLORS.length];
    });
    return map;
  }, [clusters]);

  // Scale points to fit [-2, 2] range
  const scaledPoints = useMemo(() => {
    if (!points.length) return [];
    const maxCoord = Math.max(
      ...points.flatMap(p => [Math.abs(p.x), Math.abs(p.y), Math.abs(p.z)])
    ) || 1;
    const scale = 2.0 / maxCoord;
    return points.map(p => ({
      ...p,
      x: p.x * scale,
      y: p.y * scale,
      z: p.z * scale,
    }));
  }, [points]);

  // Cluster centroid lines
  const clusterGroups = useMemo(() => {
    const groups: Record<string, EmbeddingPoint[]> = {};
    scaledPoints.forEach(p => {
      if (!groups[p.cluster]) groups[p.cluster] = [];
      groups[p.cluster].push(p);
    });
    return groups;
  }, [scaledPoints]);

  return (
    <group ref={groupRef}>
      {/* Axes */}
      <Line points={[[-2.5, 0, 0], [2.5, 0, 0]]} color="#1e293b" lineWidth={1} />
      <Line points={[[0, -2.5, 0], [0, 2.5, 0]]} color="#1e293b" lineWidth={1} />
      <Line points={[[0, 0, -2.5], [0, 0, 2.5]]} color="#1e293b" lineWidth={1} />

      {/* Cluster hulls (simplified as connecting lines) */}
      {Object.entries(clusterGroups).map(([cluster, pts]) => {
        const color = clusterColorMap[cluster] || "#6366f1";
        return pts.map((p, i) =>
          pts.slice(i + 1).map((p2, j) => (
            <Line
              key={`${cluster}-${i}-${j}`}
              points={[[p.x, p.y, p.z], [p2.x, p2.y, p2.z]]}
              color={color}
              lineWidth={0.5}
              transparent
              opacity={0.15}
            />
          ))
        );
      })}

      {/* Points */}
      {scaledPoints.map((point, i) => {
        const color = clusterColorMap[point.cluster] || CLUSTER_COLORS[i % CLUSTER_COLORS.length];
        return (
          <group key={i} position={[point.x, point.y, point.z]}>
            <mesh castShadow>
              <sphereGeometry args={[0.1, 20, 20]} />
              <meshStandardMaterial
                color={color}
                emissive={color}
                emissiveIntensity={0.5}
                roughness={0.3}
                metalness={0.5}
              />
            </mesh>
            <Text
              position={[0.15, 0.15, 0]}
              fontSize={0.16}
              color={color}
              anchorX="left"
              anchorY="middle"
            >
              {point.label}
            </Text>
          </group>
        );
      })}

      {/* Cluster legend */}
      {clusters.slice(0, 5).map((c, i) => (
        <group key={i} position={[2.8, 1.5 - i * 0.4, 0]}>
          <mesh>
            <sphereGeometry args={[0.08, 12, 12]} />
            <meshStandardMaterial color={c.color || CLUSTER_COLORS[i]} emissive={c.color || CLUSTER_COLORS[i]} emissiveIntensity={0.4} />
          </mesh>
          <Text position={[0.15, 0, 0]} fontSize={0.14} color="#94a3b8" anchorX="left" anchorY="middle">
            {c.name}
          </Text>
        </group>
      ))}
    </group>
  );
}
