"use client";

/**
 * PhysicsRobotArm — standalone 6-DOF industrial robot arm.
 * No external store dependency. Animates through a continuous pick-and-place cycle.
 * Joints: base yaw → shoulder pitch → elbow pitch → wrist pitch → wrist roll → gripper
 */

import { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

// ── Helpers ────────────────────────────────────────────────────────────────
function lerp(a: number, b: number, t: number) { return a + (b - a) * t; }
function easeInOut(t: number) { return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t; }

// ── Cylindrical link between two joint positions ───────────────────────────
function Link({
  from, to, radius = 0.055, color = "#e2e8f0",
}: {
  from: [number, number, number];
  to: [number, number, number];
  radius?: number;
  color?: string;
}) {
  const [fx, fy, fz] = from;
  const [tx, ty, tz] = to;
  const dx = tx - fx, dy = ty - fy, dz = tz - fz;
  const len = Math.sqrt(dx * dx + dy * dy + dz * dz);
  const mid: [number, number, number] = [(fx + tx) / 2, (fy + ty) / 2, (fz + tz) / 2];
  const dir = new THREE.Vector3(dx, dy, dz).normalize();
  const quat = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);
  const euler = new THREE.Euler().setFromQuaternion(quat);
  return (
    <mesh position={mid} rotation={euler} castShadow>
      <cylinderGeometry args={[radius, radius, len, 20]} />
      <meshStandardMaterial color={color} metalness={0.55} roughness={0.3} />
    </mesh>
  );
}

// ── Joint sphere ────────────────────────────────────────────────────────────
function Joint({ pos, r = 0.08, color = "#334155" }: { pos: [number, number, number]; r?: number; color?: string }) {
  return (
    <mesh position={pos} castShadow>
      <sphereGeometry args={[r, 20, 16]} />
      <meshStandardMaterial color={color} metalness={0.7} roughness={0.2} />
    </mesh>
  );
}

export default function PhysicsRobotArm({ params = {} }: { params?: Record<string, number> }) {
  // Joint angle refs (radians) — mutated every frame, no React re-renders
  const baseYaw    = useRef(0);
  const shoulder   = useRef(0.4);
  const elbow      = useRef(-0.9);
  const wristP     = useRef(0.5);
  const wristR     = useRef(0);
  const gripOpen   = useRef(0.06);

  // Group refs for transform hierarchy
  const baseRef    = useRef<THREE.Group>(null);
  const shoulderRef= useRef<THREE.Group>(null);
  const elbowRef   = useRef<THREE.Group>(null);
  const wristRef   = useRef<THREE.Group>(null);
  const gripLRef   = useRef<THREE.Mesh>(null);
  const gripRRef   = useRef<THREE.Mesh>(null);

  const clock = useRef(0);

  // Robot arm dimensions
  const L1 = 0.75; // upper arm
  const L2 = 0.65; // forearm
  const L3 = 0.35; // wrist

  useFrame((_, delta) => {
    clock.current += delta * 0.4;
    const t = clock.current % 1; // 0→1 cycle

    // Keyframed pick-and-place motion
    let tBaseYaw: number, tShoulder: number, tElbow: number, tWristP: number, tWristR: number, tGrip: number;

    if (t < 0.25) {
      // Phase 1: reach down to pick position
      const p = easeInOut(t / 0.25);
      tBaseYaw  = lerp(0,    0.6,  p);
      tShoulder = lerp(0.4,  0.85, p);
      tElbow    = lerp(-0.9, -1.3, p);
      tWristP   = lerp(0.5,  0.8,  p);
      tWristR   = lerp(0,    0,    p);
      tGrip     = lerp(0.06, 0.02, p); // close gripper
    } else if (t < 0.5) {
      // Phase 2: lift
      const p = easeInOut((t - 0.25) / 0.25);
      tBaseYaw  = lerp(0.6,  0.6,   p);
      tShoulder = lerp(0.85, 0.3,   p);
      tElbow    = lerp(-1.3, -0.7,  p);
      tWristP   = lerp(0.8,  0.4,   p);
      tWristR   = lerp(0,    1.2,   p);
      tGrip     = 0.02;
    } else if (t < 0.75) {
      // Phase 3: swing to place position
      const p = easeInOut((t - 0.5) / 0.25);
      tBaseYaw  = lerp(0.6,  -0.6,  p);
      tShoulder = lerp(0.3,  0.75,  p);
      tElbow    = lerp(-0.7, -1.1,  p);
      tWristP   = lerp(0.4,  0.7,   p);
      tWristR   = lerp(1.2,  -1.2,  p);
      tGrip     = 0.02;
    } else {
      // Phase 4: place + open + return
      const p = easeInOut((t - 0.75) / 0.25);
      tBaseYaw  = lerp(-0.6, 0,    p);
      tShoulder = lerp(0.75, 0.4,  p);
      tElbow    = lerp(-1.1, -0.9, p);
      tWristP   = lerp(0.7,  0.5,  p);
      tWristR   = lerp(-1.2, 0,    p);
      tGrip     = lerp(0.02, 0.06, p); // open gripper
    }

    baseYaw.current  = tBaseYaw;
    shoulder.current = tShoulder;
    elbow.current    = tElbow;
    wristP.current   = tWristP;
    wristR.current   = tWristR;
    gripOpen.current = tGrip;

    if (baseRef.current)     baseRef.current.rotation.y     = tBaseYaw;
    if (shoulderRef.current) shoulderRef.current.rotation.x = tShoulder;
    if (elbowRef.current)    elbowRef.current.rotation.x    = tElbow;
    if (wristRef.current) {
      wristRef.current.rotation.x = tWristP;
      wristRef.current.rotation.z = tWristR;
    }
    if (gripLRef.current) gripLRef.current.position.x =  tGrip;
    if (gripRRef.current) gripRRef.current.position.x = -tGrip;
  });

  return (
    <group>
      {/* Ground disc */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <circleGeometry args={[3, 64]} />
        <meshStandardMaterial color="#0b1220" roughness={0.9} />
      </mesh>

      {/* Work surface */}
      <mesh position={[0.9, 0.04, 0.6]} receiveShadow>
        <boxGeometry args={[0.6, 0.04, 0.6]} />
        <meshStandardMaterial color="#1e293b" roughness={0.6} metalness={0.2} />
      </mesh>
      <mesh position={[-0.9, 0.04, 0.6]} receiveShadow>
        <boxGeometry args={[0.6, 0.04, 0.6]} />
        <meshStandardMaterial color="#1e293b" roughness={0.6} metalness={0.2} />
      </mesh>
      {/* Workpiece cubes */}
      <mesh position={[0.9, 0.1, 0.6]} castShadow>
        <boxGeometry args={[0.12, 0.12, 0.12]} />
        <meshStandardMaterial color="#6366f1" metalness={0.3} roughness={0.4} />
      </mesh>
      <mesh position={[-0.9, 0.1, 0.6]} castShadow>
        <boxGeometry args={[0.12, 0.12, 0.12]} />
        <meshStandardMaterial color="#10b981" metalness={0.3} roughness={0.4} emissive="#10b981" emissiveIntensity={0.08} />
      </mesh>

      {/* ── Robot base ── */}
      <mesh position={[0, 0.12, 0]} castShadow>
        <cylinderGeometry args={[0.28, 0.32, 0.24, 32]} />
        <meshStandardMaterial color="#1e293b" metalness={0.6} roughness={0.35} />
      </mesh>

      {/* ── Rotating turret + all joints above it ── */}
      <group ref={baseRef} position={[0, 0.24, 0]}>
        {/* Turret body */}
        <mesh castShadow>
          <cylinderGeometry args={[0.20, 0.22, 0.18, 28]} />
          <meshStandardMaterial color="#334155" metalness={0.55} roughness={0.3} />
        </mesh>
        <mesh position={[0, 0.18, 0]} castShadow>
          <boxGeometry args={[0.30, 0.22, 0.28]} />
          <meshStandardMaterial color="#e2e8f0" metalness={0.45} roughness={0.28} />
        </mesh>

        {/* ── Shoulder joint ── */}
        <group ref={shoulderRef} position={[0, 0.30, 0]}>
          <Joint pos={[0, 0, 0]} r={0.09} color="#475569" />

          {/* Upper arm */}
          <group>
            <mesh position={[0, L1 / 2, 0]} castShadow>
              <boxGeometry args={[0.14, L1, 0.12]} />
              <meshStandardMaterial color="#e2e8f0" metalness={0.45} roughness={0.28} />
            </mesh>

            {/* ── Elbow joint ── */}
            <group ref={elbowRef} position={[0, L1, 0]}>
              <Joint pos={[0, 0, 0]} r={0.08} color="#475569" />

              {/* Forearm */}
              <group>
                <mesh position={[0, L2 / 2, 0]} castShadow>
                  <boxGeometry args={[0.12, L2, 0.10]} />
                  <meshStandardMaterial color="#e2e8f0" metalness={0.45} roughness={0.28} />
                </mesh>

                {/* ── Wrist joint ── */}
                <group ref={wristRef} position={[0, L2, 0]}>
                  <Joint pos={[0, 0, 0]} r={0.065} color="#475569" />

                  {/* Wrist / tool flange */}
                  <mesh position={[0, L3 / 2, 0]} castShadow>
                    <cylinderGeometry args={[0.055, 0.065, L3, 16]} />
                    <meshStandardMaterial color="#94a3b8" metalness={0.7} roughness={0.2} />
                  </mesh>

                  {/* Tool mount */}
                  <mesh position={[0, L3, 0]} castShadow>
                    <cylinderGeometry args={[0.07, 0.07, 0.04, 16]} />
                    <meshStandardMaterial color="#334155" metalness={0.75} roughness={0.2} />
                  </mesh>

                  {/* ── Parallel gripper fingers ── */}
                  <mesh ref={gripLRef} position={[0.06, L3 + 0.1, 0]} castShadow>
                    <boxGeometry args={[0.025, 0.16, 0.04]} />
                    <meshStandardMaterial color="#0ea5e9" metalness={0.5} roughness={0.3} />
                  </mesh>
                  <mesh ref={gripRRef} position={[-0.06, L3 + 0.1, 0]} castShadow>
                    <boxGeometry args={[0.025, 0.16, 0.04]} />
                    <meshStandardMaterial color="#0ea5e9" metalness={0.5} roughness={0.3} />
                  </mesh>
                  {/* Finger tips */}
                  <mesh position={[0.06, L3 + 0.19, 0]} castShadow>
                    <boxGeometry args={[0.022, 0.03, 0.03]} />
                    <meshStandardMaterial color="#1e293b" roughness={0.8} />
                  </mesh>
                  <mesh position={[-0.06, L3 + 0.19, 0]} castShadow>
                    <boxGeometry args={[0.022, 0.03, 0.03]} />
                    <meshStandardMaterial color="#1e293b" roughness={0.8} />
                  </mesh>
                </group>
              </group>
            </group>
          </group>
        </group>
      </group>
    </group>
  );
}
