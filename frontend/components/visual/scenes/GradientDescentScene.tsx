"use client";
import { useRef, useMemo, useState } from "react";
import { useFrame } from "@react-three/fiber";
import { Text, Sphere } from "@react-three/drei";
import * as THREE from "three";

interface GradientDescentParams {
  lossType?: "bowl" | "saddle" | "ravine" | "noisy";
  learningRate?: number;
  steps?: number;
  startPos?: [number, number];
  title?: string;
  description?: string;
}

// Loss functions
const lossFunctions: Record<string, (x: number, y: number) => number> = {
  bowl: (x, y) => x * x * 0.4 + y * y * 0.4,
  saddle: (x, y) => x * x * 0.4 - y * y * 0.4 + 1.5,
  ravine: (x, y) => x * x * 0.1 + y * y * 1.5,
  noisy: (x, y) =>
    x * x * 0.3 +
    y * y * 0.3 +
    Math.sin(x * 3) * 0.2 +
    Math.sin(y * 3) * 0.2,
};

const gradients: Record<string, (x: number, y: number) => [number, number]> = {
  bowl: (x, y) => [x * 0.8, y * 0.8],
  saddle: (x, y) => [x * 0.8, -y * 0.8],
  ravine: (x, y) => [x * 0.2, y * 3.0],
  noisy: (x, y) => [
    x * 0.6 + Math.cos(x * 3) * 0.6,
    y * 0.6 + Math.cos(y * 3) * 0.6,
  ],
};

function LossSurface({ lossType }: { lossType: string }) {
  const geometry = useMemo(() => {
    const geo = new THREE.PlaneGeometry(6, 6, 40, 40);
    const positions = geo.attributes.position;
    const lossFunc = lossFunctions[lossType] || lossFunctions.bowl;

    for (let i = 0; i < positions.count; i++) {
      const x = positions.getX(i);
      const y = positions.getY(i);
      const z = lossFunc(x, y);
      positions.setZ(i, z);
    }
    geo.computeVertexNormals();
    return geo;
  }, [lossType]);

  const colors = useMemo(() => {
    const positions = geometry.attributes.position;
    const colorArray = new Float32Array(positions.count * 3);
    let minZ = Infinity, maxZ = -Infinity;
    for (let i = 0; i < positions.count; i++) {
      const z = positions.getZ(i);
      minZ = Math.min(minZ, z);
      maxZ = Math.max(maxZ, z);
    }
    for (let i = 0; i < positions.count; i++) {
      const z = positions.getZ(i);
      const t = (z - minZ) / (maxZ - minZ);
      const color = new THREE.Color().setHSL(0.67 - t * 0.5, 0.9, 0.4 + t * 0.2);
      colorArray[i * 3] = color.r;
      colorArray[i * 3 + 1] = color.g;
      colorArray[i * 3 + 2] = color.b;
    }
    geometry.setAttribute("color", new THREE.BufferAttribute(colorArray, 3));
    return colorArray;
  }, [geometry]);

  return (
    <mesh geometry={geometry} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
      <meshStandardMaterial
        vertexColors
        side={THREE.DoubleSide}
        roughness={0.6}
        metalness={0.1}
        transparent
        opacity={0.88}
        wireframe={false}
      />
    </mesh>
  );
}

function GDPath({
  lossType,
  learningRate,
  steps,
  startPos,
}: {
  lossType: string;
  learningRate: number;
  steps: number;
  startPos: [number, number];
}) {
  const pathRef = useRef<THREE.Line>(null!);
  const ballRef = useRef<THREE.Mesh>(null!);
  const stepRef = useRef(0);

  const path = useMemo(() => {
    const lossFunc = lossFunctions[lossType] || lossFunctions.bowl;
    const gradFunc = gradients[lossType] || gradients.bowl;
    const points: THREE.Vector3[] = [];
    let [x, y] = startPos;
    for (let i = 0; i <= steps; i++) {
      const z = lossFunc(x, y);
      points.push(new THREE.Vector3(x, z + 0.05, y));
      const [gx, gy] = gradFunc(x, y);
      x -= learningRate * gx;
      y -= learningRate * gy;
      x = Math.max(-3, Math.min(3, x));
      y = Math.max(-3, Math.min(3, y));
    }
    return points;
  }, [lossType, learningRate, steps, startPos]);

  useFrame(({ clock }) => {
    if (!ballRef.current || path.length < 2) return;
    const t = (clock.getElapsedTime() * 0.5) % 1;
    const idx = Math.floor(t * (path.length - 1));
    const frac = t * (path.length - 1) - idx;
    const from = path[Math.min(idx, path.length - 1)];
    const to = path[Math.min(idx + 1, path.length - 1)];
    ballRef.current.position.lerpVectors(from, to, frac);
  });

  const lineGeometry = useMemo(() => {
    const geo = new THREE.BufferGeometry().setFromPoints(path);
    return geo;
  }, [path]);

  return (
    <group>
      <primitive object={new THREE.Line(
        lineGeometry,
        new THREE.LineBasicMaterial({ color: "#facc15", linewidth: 2 })
      )} />
      <mesh ref={ballRef} position={path[0]?.toArray() as [number, number, number] ?? [0, 0, 0]} castShadow>
        <sphereGeometry args={[0.12, 24, 24]} />
        <meshStandardMaterial color="#facc15" emissive="#facc15" emissiveIntensity={0.8} />
      </mesh>
      {/* Start and end markers */}
      <Text position={[path[0]?.x ?? 0, (path[0]?.y ?? 0) + 0.3, path[0]?.z ?? 0]} fontSize={0.18} color="#94a3b8" anchorX="center">
        start
      </Text>
      <Text
        position={[path[path.length - 1]?.x ?? 0, (path[path.length - 1]?.y ?? 0) + 0.3, path[path.length - 1]?.z ?? 0]}
        fontSize={0.18}
        color="#34d399"
        anchorX="center"
      >
        minimum
      </Text>
    </group>
  );
}

export default function GradientDescentScene({ params }: { params: GradientDescentParams }) {
  const {
    lossType = "bowl",
    learningRate = 0.15,
    steps = 15,
    startPos = [2.2, 2.2],
  } = params;

  return (
    <group>
      <LossSurface lossType={lossType} />
      <GDPath
        lossType={lossType}
        learningRate={learningRate}
        steps={steps}
        startPos={startPos}
      />
      <Text position={[0, -0.3, 3.5]} fontSize={0.22} color="#94a3b8" anchorX="center">
        Loss Surface · lr={learningRate}
      </Text>
    </group>
  );
}
