"use client";

import { Suspense, lazy } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, ContactShadows, Html } from "@react-three/drei";
import * as THREE from "three";
import { type SimType, SCENE_CONFIGS } from "@/lib/detectSimType";

// ── Lazy-loaded physics components ────────────────────────────────────────────
const PhysicsPendulum        = lazy(() => import("./PhysicsPendulum"));
const PhysicsNewtonsCradle   = lazy(() => import("./PhysicsNewtonsCradle"));
const PhysicsInvertedPendulum= lazy(() => import("./PhysicsInvertedPendulum"));
const PhysicsOrbit           = lazy(() => import("./PhysicsOrbit"));
const PhysicsSpringMass      = lazy(() => import("./PhysicsSpringMass"));
const PhysicsProjectile      = lazy(() => import("./PhysicsProjectile"));
const PhysicsRocket          = lazy(() => import("./PhysicsRocket"));
const PhysicsWindTurbine     = lazy(() => import("./PhysicsWindTurbine"));
const PhysicsBridge          = lazy(() => import("./PhysicsBridge"));
const PhysicsHelicopter      = lazy(() => import("./PhysicsHelicopter"));
const PhysicsMechanicalGears = lazy(() => import("./PhysicsMechanicalGears"));
const PhysicsBicycle         = lazy(() => import("./PhysicsBicycle"));
const PhysicsSubmarine       = lazy(() => import("./PhysicsSubmarine"));
const PhysicsBreadboard      = lazy(() => import("./PhysicsBreadboard"));
const PhysicsF1Car           = lazy(() => import("./PhysicsF1Car"));
const PhysicsSteamEngine     = lazy(() => import("./PhysicsSteamEngine"));
const PhysicsWaterBottle     = lazy(() => import("./PhysicsWaterBottle"));
const PhysicsRobotArm        = lazy(() => import("./PhysicsRobotArm"));

// ── Loading fallback ──────────────────────────────────────────────────────────
function Loader() {
  return (
    <Html center>
      <div className="flex flex-col items-center gap-2">
        <div className="w-7 h-7 border-2 border-indigo-500/60 border-t-indigo-400 rounded-full animate-spin" />
        <span className="text-[11px] text-white/40 font-mono">Loading simulation…</span>
      </div>
    </Html>
  );
}

// ── Scene content ─────────────────────────────────────────────────────────────
function SceneContent({ simType, params }: { simType: SimType; params: Record<string, number> }) {
  const showGround = simType !== "orbit";

  return (
    <>
      <ambientLight intensity={0.55} />
      <directionalLight position={[10, 20, 10]} intensity={1.6} castShadow shadow-mapSize={[2048, 2048]} />
      <directionalLight position={[-5, 10, -5]} intensity={0.5} color="#b4c6ef" />
      <pointLight position={[-8, 5, -8]} intensity={0.35} color="#ffd4a3" />

      {simType === "pendulum"          && <PhysicsPendulum params={params} />}
      {simType === "newton_cradle"     && <PhysicsNewtonsCradle params={params} />}
      {simType === "inverted_pendulum" && <PhysicsInvertedPendulum params={params} />}
      {simType === "orbit"             && <PhysicsOrbit params={params} />}
      {simType === "spring_mass"       && <PhysicsSpringMass params={params} />}
      {simType === "projectile"        && <PhysicsProjectile params={params} />}
      {simType === "rocket"            && <PhysicsRocket params={params} />}
      {simType === "wind_turbine"      && <PhysicsWindTurbine params={params} />}
      {simType === "bridge"            && <PhysicsBridge params={params} />}
      {simType === "helicopter"        && <PhysicsHelicopter params={params} />}
      {simType === "mechanical_gears"  && <PhysicsMechanicalGears params={params} />}
      {simType === "bicycle"           && <PhysicsBicycle params={params} />}
      {simType === "submarine"         && <PhysicsSubmarine params={params} />}
      {simType === "breadboard"        && <PhysicsBreadboard params={params} />}
      {simType === "f1_car"            && <PhysicsF1Car params={params} />}
      {simType === "steam_engine"      && <PhysicsSteamEngine params={params} />}
      {simType === "water_bottle"      && <PhysicsWaterBottle params={params} />}
      {simType === "robot_arm"         && <PhysicsRobotArm params={params} />}

      {showGround && (
        <ContactShadows position={[0, 0, 0]} opacity={0.4} scale={18} blur={2} far={8} resolution={512} />
      )}
    </>
  );
}

// ── Public component ──────────────────────────────────────────────────────────

interface Props {
  simType: SimType;
  params?: Record<string, number>;
  height?: number;
}

export default function InlinePhysicsSim({ simType, params = {}, height = 320 }: Props) {
  const cfg = SCENE_CONFIGS[simType] ?? SCENE_CONFIGS.custom;

  return (
    <div
      className="rounded-2xl overflow-hidden border border-white/10 bg-[#070a0f]"
      style={{ height }}
    >
      <Canvas
        shadows
        dpr={[1, 2]}
        camera={{ fov: cfg.fov, position: cfg.camera }}
        gl={{
          antialias: true,
          toneMapping: THREE.ACESFilmicToneMapping,
          toneMappingExposure: 1.2,
        }}
      >
        <Suspense fallback={<Loader />}>
          <SceneContent simType={simType} params={params} />
          <OrbitControls
            makeDefault
            minDistance={0.5}
            maxDistance={30}
            target={cfg.target}
            enableDamping
            dampingFactor={0.05}
          />
        </Suspense>
      </Canvas>
    </div>
  );
}
