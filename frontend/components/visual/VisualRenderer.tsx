"use client";
import { useEffect, useRef, useState } from "react";
import * as THREE from "three";

export interface VizConfig {
  vizType: string;
  title: string;
  description: string;
  params: Record<string, unknown>;
}

interface Label { pos: THREE.Vector3; text: string; color: string; size?: number }

// ─── PBR Material factory ─────────────────────────────────────────────────────
function pbr(color: number | string, opts: {
  metalness?: number; roughness?: number; emissive?: number;
  emissiveIntensity?: number; transparent?: boolean; opacity?: number;
  transmission?: number; wireframe?: boolean;
} = {}): THREE.MeshStandardMaterial {
  const hex = typeof color === "string" ? parseInt(color.replace("#", ""), 16) : color;
  return new THREE.MeshStandardMaterial({
    color: hex,
    metalness: opts.metalness ?? 0.1,
    roughness: opts.roughness ?? 0.5,
    emissive: opts.emissive ? new THREE.Color(opts.emissive) : new THREE.Color(0x000000),
    emissiveIntensity: opts.emissiveIntensity ?? 0,
    transparent: opts.transparent ?? false,
    opacity: opts.opacity ?? 1,
    wireframe: opts.wireframe ?? false,
  });
}

// ─── Orbit Controls ───────────────────────────────────────────────────────────
function addOrbitControls(camera: THREE.PerspectiveCamera, el: HTMLElement, target = new THREE.Vector3()) {
  const sph = new THREE.Spherical().setFromVector3(camera.position.clone().sub(target));
  let down = false, px = 0, py = 0;
  const onDown = (e: PointerEvent) => { down = true; px = e.clientX; py = e.clientY; el.setPointerCapture(e.pointerId); };
  const onUp = () => { down = false; };
  const onMove = (e: PointerEvent) => {
    if (!down) return;
    sph.theta -= (e.clientX - px) * 0.007;
    sph.phi = Math.max(0.08, Math.min(Math.PI - 0.08, sph.phi - (e.clientY - py) * 0.007));
    px = e.clientX; py = e.clientY;
    camera.position.setFromSpherical(sph).add(target);
    camera.lookAt(target);
  };
  const onWheel = (e: WheelEvent) => {
    sph.radius = Math.max(2, Math.min(28, sph.radius + e.deltaY * 0.01));
    camera.position.setFromSpherical(sph).add(target);
    camera.lookAt(target); e.preventDefault();
  };
  el.addEventListener("pointerdown", onDown);
  el.addEventListener("pointerup", onUp);
  el.addEventListener("pointermove", onMove);
  el.addEventListener("wheel", onWheel, { passive: false });
  return () => {
    el.removeEventListener("pointerdown", onDown);
    el.removeEventListener("pointerup", onUp);
    el.removeEventListener("pointermove", onMove);
    el.removeEventListener("wheel", onWheel);
  };
}

// ─── MECHANICAL SCENES ────────────────────────────────────────────────────────

function buildWindTurbine(scene: THREE.Scene, params: Record<string, unknown>) {
  const rpm = (params.rpm as number) || 14;
  const objects: THREE.Object3D[] = [];
  const labels: Label[] = [];

  // Ground base disc
  const baseGeo = new THREE.CylinderGeometry(1.8, 2.2, 0.25, 48);
  const baseMesh = new THREE.Mesh(baseGeo, pbr(0x2a3a4a, { metalness: 0.4, roughness: 0.7 }));
  baseMesh.position.y = -3.8;
  baseMesh.receiveShadow = true;
  scene.add(baseMesh); objects.push(baseMesh);

  // Tower: LatheGeometry — tapered tube
  const towerPts = [
    new THREE.Vector2(0.38, 0),
    new THREE.Vector2(0.35, 0.3),
    new THREE.Vector2(0.28, 1.5),
    new THREE.Vector2(0.22, 3.0),
    new THREE.Vector2(0.18, 4.5),
    new THREE.Vector2(0.16, 6.0),
    new THREE.Vector2(0.155, 6.8),
  ];
  const towerGeo = new THREE.LatheGeometry(towerPts, 48);
  const towerMat = pbr(0xd6d6d6, { metalness: 0.55, roughness: 0.38 });
  const tower = new THREE.Mesh(towerGeo, towerMat);
  tower.position.y = -3.65;
  tower.castShadow = true; tower.receiveShadow = true;
  scene.add(tower); objects.push(tower);

  // Nacelle (housing at top)
  const nacelleGeo = new THREE.BoxGeometry(1.1, 0.55, 0.65);
  // Round the nacelle top — use CylinderGeometry cap
  const nacelleMat = pbr(0xe8e8e8, { metalness: 0.45, roughness: 0.3 });
  const nacelle = new THREE.Mesh(nacelleGeo, nacelleMat);
  nacelle.position.set(0.15, 3.35, 0);
  nacelle.castShadow = true;
  scene.add(nacelle); objects.push(nacelle);

  // Hub sphere
  const hubGeo = new THREE.SphereGeometry(0.28, 32, 32);
  const hubMat = pbr(0x888899, { metalness: 0.8, roughness: 0.2 });
  const hub = new THREE.Mesh(hubGeo, hubMat);
  hub.position.set(-0.55, 3.35, 0);
  hub.castShadow = true;
  scene.add(hub); objects.push(hub);

  // Rotor group (rotates)
  const rotor = new THREE.Group();
  rotor.position.copy(hub.position);
  scene.add(rotor); objects.push(rotor);

  // Blade shape — realistic aerofoil profile
  function makeBlade() {
    const shape = new THREE.Shape();
    // Chord profile (NACA-ish)
    shape.moveTo(0, 0);
    shape.bezierCurveTo(0.14, 0.06, 0.11, 0.4, 0.07, 0.9);
    shape.bezierCurveTo(0.04, 1.4, 0.015, 2.0, 0, 2.55);
    shape.bezierCurveTo(-0.01, 2.0, -0.04, 1.4, -0.055, 0.9);
    shape.bezierCurveTo(-0.08, 0.4, -0.07, 0.06, 0, 0);

    const settings: THREE.ExtrudeGeometryOptions = {
      depth: 0.035,
      bevelEnabled: true,
      bevelThickness: 0.012,
      bevelSize: 0.009,
      bevelSegments: 3,
    };
    return new THREE.ExtrudeGeometry(shape, settings);
  }

  const bladeMat = pbr(0xf0f0f0, { metalness: 0.25, roughness: 0.22 });
  for (let i = 0; i < 3; i++) {
    const blade = new THREE.Mesh(makeBlade(), bladeMat);
    blade.rotation.z = (i / 3) * Math.PI * 2;
    blade.castShadow = true;
    rotor.add(blade);
  }

  // Blade root attachment rings
  for (let i = 0; i < 3; i++) {
    const ringGeo = new THREE.TorusGeometry(0.09, 0.025, 12, 24);
    const ring = new THREE.Mesh(ringGeo, pbr(0x778899, { metalness: 0.9, roughness: 0.15 }));
    ring.rotation.z = (i / 3) * Math.PI * 2;
    ring.position.set(0, 0.15, 0.018);
    ring.rotation.x = Math.PI / 2;
    rotor.add(ring);
  }

  labels.push({ pos: new THREE.Vector3(-0.55, 4.0, 0), text: "Rotor Hub", color: "#94a3b8" });
  labels.push({ pos: new THREE.Vector3(1.4, 3.35, 0), text: "Nacelle", color: "#94a3b8" });
  labels.push({ pos: new THREE.Vector3(0, -3.4, 0), text: "Tower", color: "#94a3b8" });
  labels.push({ pos: new THREE.Vector3(-1.8, 5.5, 0), text: "Blade", color: "#c7d2fe" });

  const speed = (rpm * 2 * Math.PI) / (60 * 60);
  let frame = 0;
  const tick = () => { frame++; rotor.rotation.z = frame * speed * 0.8; };
  return { labels, tick, cleanup: () => { objects.forEach(o => scene.remove(o)); } };
}

function buildPendulum(scene: THREE.Scene, params: Record<string, unknown>) {
  const length = (params.length as number) || 3;
  const angle = ((params.angle as number) || 40) * (Math.PI / 180);
  const damping = (params.damping as number) || 0.999;
  const objects: THREE.Object3D[] = [];
  const labels: Label[] = [];

  // Pivot
  const pivotGeo = new THREE.SphereGeometry(0.12, 24, 24);
  const pivot = new THREE.Mesh(pivotGeo, pbr(0x555566, { metalness: 0.9, roughness: 0.15 }));
  pivot.position.set(0, 2, 0);
  scene.add(pivot); objects.push(pivot);

  // Support frame
  const frameGeo = new THREE.BoxGeometry(0.08, 0.8, 0.08);
  const frameMat = pbr(0x333344, { metalness: 0.8, roughness: 0.2 });
  const frameL = new THREE.Mesh(frameGeo, frameMat);
  frameL.position.set(-1.2, 2.4, 0); frameL.castShadow = true;
  const frameR = new THREE.Mesh(frameGeo, frameMat);
  frameR.position.set(1.2, 2.4, 0); frameR.castShadow = true;
  const crossBar = new THREE.Mesh(new THREE.BoxGeometry(2.5, 0.08, 0.08), frameMat);
  crossBar.position.set(0, 2.82, 0);
  scene.add(frameL, frameR, crossBar);
  objects.push(frameL, frameR, crossBar);

  // Arm group
  const armGroup = new THREE.Group();
  armGroup.position.copy(pivot.position);
  scene.add(armGroup); objects.push(armGroup);

  // Rod
  const rodGeo = new THREE.CylinderGeometry(0.025, 0.025, length, 16);
  const rod = new THREE.Mesh(rodGeo, pbr(0x888899, { metalness: 0.8, roughness: 0.2 }));
  rod.position.y = -length / 2;
  armGroup.add(rod);

  // Bob
  const bobGeo = new THREE.SphereGeometry(0.28, 32, 32);
  const bobMat = pbr(0xe8b84b, { metalness: 0.85, roughness: 0.12, emissive: 0xb87020, emissiveIntensity: 0.08 });
  const bob = new THREE.Mesh(bobGeo, bobMat);
  bob.position.y = -length;
  bob.castShadow = true;
  armGroup.add(bob);

  // Shadow catcher arc
  const arcPath = new THREE.EllipseCurve(-0, 0, length, length * 0.12, -Math.PI / 2 - 0.8, -Math.PI / 2 + 0.8, false, 0);
  const arcGeo = new THREE.BufferGeometry().setFromPoints(arcPath.getPoints(40));
  const arcLine = new THREE.Line(arcGeo, new THREE.LineBasicMaterial({ color: 0x334455, transparent: true, opacity: 0.35 }));
  arcLine.position.copy(pivot.position);
  scene.add(arcLine); objects.push(arcLine);

  labels.push({ pos: new THREE.Vector3(0.35, 2, 0), text: "Pivot", color: "#94a3b8" });
  labels.push({ pos: new THREE.Vector3(0.45, 2 - length, 0), text: "Bob (mass)", color: "#fbbf24" });
  labels.push({ pos: new THREE.Vector3(-0.5, 2 - length / 2, 0), text: `L = ${length}m`, color: "#64748b" });

  let phi = angle, omega = 0, frame = 0;
  const g = 9.81, dt = 1 / 60;
  const tick = () => {
    frame++;
    omega += (-g / length) * Math.sin(phi) * dt;
    omega *= damping;
    phi += omega * dt;
    armGroup.rotation.z = phi;
    // update bob world position for label
  };
  return { labels, tick, cleanup: () => { objects.forEach(o => scene.remove(o)); } };
}

function buildAtom(scene: THREE.Scene, params: Record<string, unknown>) {
  const element = (params.element as string) || "Carbon";
  const protons = (params.protons as number) || 6;
  const electrons = (params.electrons as number) || 6;
  const shells = (params.shells as number[]) || [2, 4];
  const objects: THREE.Object3D[] = [];
  const labels: Label[] = [];

  // Nucleus
  const nucleusGroup = new THREE.Group();
  scene.add(nucleusGroup); objects.push(nucleusGroup);
  for (let i = 0; i < Math.min(protons + Math.floor(protons * 1.2), 16); i++) {
    const isProton = i < protons;
    const geo = new THREE.SphereGeometry(0.2, 16, 16);
    const mat = pbr(isProton ? 0xe8484a : 0x5588cc, { metalness: 0.6, roughness: 0.3, emissive: isProton ? 0x880000 : 0x003366, emissiveIntensity: 0.12 });
    const mesh = new THREE.Mesh(geo, mat);
    const theta = Math.random() * Math.PI * 2, phi = Math.random() * Math.PI;
    const r = 0.38 * Math.cbrt(i + 1);
    mesh.position.set(r * Math.sin(phi) * Math.cos(theta), r * Math.sin(phi) * Math.sin(theta), r * Math.cos(phi));
    mesh.castShadow = true;
    nucleusGroup.add(mesh);
  }

  // Electron shells
  const electronMeshes: { mesh: THREE.Mesh; shell: number; angle: number; speed: number }[] = [];
  let eIdx = 0;
  shells.forEach((count, si) => {
    const radius = 1.4 + si * 1.1;
    // Orbit ring
    const ring = new THREE.Mesh(
      new THREE.TorusGeometry(radius, 0.015, 8, 64),
      pbr(0x334455, { metalness: 0.3, roughness: 0.8, transparent: true, opacity: 0.35 })
    );
    ring.rotation.x = Math.PI / 2 + si * 0.3;
    ring.rotation.y = si * 0.8;
    scene.add(ring); objects.push(ring);

    for (let e = 0; e < count && eIdx < electrons; e++, eIdx++) {
      const eMat = pbr(0x44aaff, { metalness: 0, roughness: 0.4, emissive: 0x0066cc, emissiveIntensity: 0.6 });
      const eMesh = new THREE.Mesh(new THREE.SphereGeometry(0.1, 12, 12), eMat);
      scene.add(eMesh); objects.push(eMesh);
      electronMeshes.push({ mesh: eMesh, shell: si, angle: (e / count) * Math.PI * 2, speed: 0.6 / (si + 1) });
    }
  });

  labels.push({ pos: new THREE.Vector3(0, 0.7, 0), text: element, color: "#f8fafc", size: 16 });
  labels.push({ pos: new THREE.Vector3(0, -0.55, 0), text: `${protons}p · ${Math.floor(protons * 1.2)}n`, color: "#64748b" });

  let frame = 0;
  const tick = () => {
    frame++;
    nucleusGroup.rotation.y = frame * 0.008;
    electronMeshes.forEach(e => {
      e.angle += e.speed * 0.022;
      const radius = 1.4 + e.shell * 1.1;
      const tiltX = Math.PI / 2 + e.shell * 0.3;
      const tiltY = e.shell * 0.8;
      const x = radius * Math.cos(e.angle);
      const z = radius * Math.sin(e.angle);
      const y = 0;
      // Apply tilt manually
      e.mesh.position.set(
        x * Math.cos(tiltY) - z * Math.sin(tiltX) * Math.sin(tiltY),
        z * Math.cos(tiltX),
        x * Math.sin(tiltY) + z * Math.sin(tiltX) * Math.cos(tiltY)
      );
    });
  };
  return { labels, tick, cleanup: () => { objects.forEach(o => scene.remove(o)); } };
}

function buildOrbit(scene: THREE.Scene, params: Record<string, unknown>) {
  const bodyCount = (params.bodies as number) || 2;
  const labels: Label[] = [];
  const objects: THREE.Object3D[] = [];
  const bodies: { mesh: THREE.Mesh; radius: number; speed: number; angle: number; color: number; name: string; size: number }[] = [];

  // Sun
  const sunGeo = new THREE.SphereGeometry(0.65, 32, 32);
  const sunMat = pbr(0xffcc44, { metalness: 0, roughness: 0.4, emissive: 0xff9900, emissiveIntensity: 0.6 });
  const sun = new THREE.Mesh(sunGeo, sunMat);
  sun.castShadow = false;
  scene.add(sun); objects.push(sun);
  const sunGlow = new THREE.PointLight(0xffbb44, 2.0, 20);
  scene.add(sunGlow); objects.push(sunGlow);
  labels.push({ pos: new THREE.Vector3(0, 0.9, 0), text: "Star", color: "#fbbf24" });

  const planetDefs = [
    { r: 2.2, speed: 0.9, color: 0x6688cc, name: "Planet 1", size: 0.22 },
    { r: 3.5, speed: 0.55, color: 0x88cc66, name: "Planet 2", size: 0.3 },
    { r: 5.0, speed: 0.33, color: 0xcc8844, name: "Planet 3", size: 0.38 },
  ];

  planetDefs.slice(0, Math.min(bodyCount, 3)).forEach((def, i) => {
    // Orbit ring
    const ring = new THREE.Mesh(
      new THREE.TorusGeometry(def.r, 0.012, 8, 80),
      pbr(0x1e293b, { metalness: 0, roughness: 1, transparent: true, opacity: 0.5 })
    );
    ring.rotation.x = Math.PI / 2;
    scene.add(ring); objects.push(ring);

    const planet = new THREE.Mesh(
      new THREE.SphereGeometry(def.size, 24, 24),
      pbr(def.color, { metalness: 0.2, roughness: 0.6 })
    );
    planet.castShadow = true;
    scene.add(planet); objects.push(planet);
    bodies.push({ mesh: planet, radius: def.r, speed: def.speed, angle: i * 2.1, color: def.color, name: def.name, size: def.size });
    labels.push({ pos: planet.position.clone(), text: def.name, color: `#${def.color.toString(16).padStart(6, "0")}` });
  });

  let frame = 0;
  const tick = () => {
    frame++;
    bodies.forEach((b, i) => {
      b.angle += b.speed * 0.008;
      b.mesh.position.set(b.radius * Math.cos(b.angle), 0, b.radius * Math.sin(b.angle));
      b.mesh.rotation.y += 0.01;
      // update label pos
      if (labels[i + 1]) labels[i + 1].pos.copy(b.mesh.position).add(new THREE.Vector3(0, b.size + 0.25, 0));
    });
  };
  return { labels, tick, cleanup: () => { objects.forEach(o => scene.remove(o)); } };
}

function buildSpringMass(scene: THREE.Scene, params: Record<string, unknown>) {
  const k = (params.springConstant as number) || 8;
  const mass = (params.mass as number) || 1;
  const amplitude = (params.amplitude as number) || 1.2;
  const objects: THREE.Object3D[] = [];
  const labels: Label[] = [];

  // Ceiling
  const ceilGeo = new THREE.BoxGeometry(2.5, 0.15, 0.8);
  const ceil = new THREE.Mesh(ceilGeo, pbr(0x334455, { metalness: 0.5, roughness: 0.5 }));
  ceil.position.y = 3;
  scene.add(ceil); objects.push(ceil);

  // Spring (will be updated each frame)
  const COILS = 14;
  const springGroup = new THREE.Group();
  scene.add(springGroup); objects.push(springGroup);

  const coilMat = pbr(0x8899aa, { metalness: 0.85, roughness: 0.15 });
  const coilMeshes: THREE.Mesh[] = [];
  for (let i = 0; i < COILS; i++) {
    const geo = new THREE.TorusGeometry(0.22, 0.028, 10, 24);
    const coil = new THREE.Mesh(geo, coilMat);
    coil.castShadow = true;
    springGroup.add(coil);
    coilMeshes.push(coil);
  }

  // Mass block
  const blockGeo = new THREE.BoxGeometry(0.7, 0.7, 0.7);
  const blockMat = pbr(0x4466ff, { metalness: 0.6, roughness: 0.3, emissive: 0x001188, emissiveIntensity: 0.08 });
  const block = new THREE.Mesh(blockGeo, blockMat);
  block.castShadow = true;
  scene.add(block); objects.push(block);

  // Equilibrium line
  const eqLine = new THREE.Line(
    new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(-1, 0, 0), new THREE.Vector3(1, 0, 0)]),
    new THREE.LineDashedMaterial({ color: 0x334455, dashSize: 0.1, gapSize: 0.08 })
  );
  eqLine.computeLineDistances();
  scene.add(eqLine); objects.push(eqLine);

  labels.push({ pos: new THREE.Vector3(1.4, 3, 0), text: "Fixed point", color: "#64748b" });
  labels.push({ pos: new THREE.Vector3(1.0, 0, 0), text: "Equilibrium", color: "#475569" });
  labels.push({ pos: new THREE.Vector3(0, 0, 0), text: `m = ${mass}kg  k = ${k}N/m`, color: "#818cf8" });

  const omega = Math.sqrt(k / mass);
  let frame = 0;
  const restY = 0;
  const springTop = 2.92;

  const tick = () => {
    frame++;
    const t = frame * (1 / 60);
    const y = restY + amplitude * Math.cos(omega * t);
    block.position.y = y - 0.35;
    const springLen = springTop - y;
    coilMeshes.forEach((coil, i) => {
      const frac = i / COILS;
      coil.position.y = springTop - springLen * frac;
      coil.scale.y = springLen / COILS / 0.4;
    });
    if (labels[2]) labels[2].pos.set(1.0, y, 0);
  };
  return { labels, tick, cleanup: () => { objects.forEach(o => scene.remove(o)); } };
}

function buildGearSystem(scene: THREE.Scene, params: Record<string, unknown>) {
  const gearCount = (params.gears as number) || 3;
  const objects: THREE.Object3D[] = [];
  const labels: Label[] = [];

  function makeGear(teeth: number, r: number, thick: number) {
    const shape = new THREE.Shape();
    const toothH = r * 0.22;
    for (let i = 0; i < teeth; i++) {
      const a0 = (i / teeth) * Math.PI * 2;
      const a1 = ((i + 0.35) / teeth) * Math.PI * 2;
      const a2 = ((i + 0.65) / teeth) * Math.PI * 2;
      const a3 = ((i + 1) / teeth) * Math.PI * 2;
      if (i === 0) shape.moveTo(r * Math.cos(a0), r * Math.sin(a0));
      else shape.lineTo(r * Math.cos(a0), r * Math.sin(a0));
      shape.lineTo((r + toothH) * Math.cos(a1), (r + toothH) * Math.sin(a1));
      shape.lineTo((r + toothH) * Math.cos(a2), (r + toothH) * Math.sin(a2));
      shape.lineTo(r * Math.cos(a3), r * Math.sin(a3));
    }
    shape.closePath();
    return new THREE.ExtrudeGeometry(shape, { depth: thick, bevelEnabled: false });
  }

  const gearDefs = [
    { teeth: 24, r: 1.1, pos: [-2.4, 0], color: 0x5577ee, name: "Driver (24T)" },
    { teeth: 12, r: 0.58, pos: [-0.95, 0], color: 0xee7755, name: "Idler (12T)" },
    { teeth: 20, r: 0.95, pos: [0.72, 0], color: 0x55cc88, name: "Output (20T)" },
  ];

  const gearMeshes: THREE.Mesh[] = [];
  gearDefs.slice(0, Math.min(gearCount, 3)).forEach((def, i) => {
    const geo = makeGear(def.teeth, def.r, 0.22);
    const mat = pbr(def.color, { metalness: 0.75, roughness: 0.22 });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(def.pos[0], def.pos[1], 0);
    mesh.castShadow = true; mesh.receiveShadow = true;
    // Hub
    const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.35, 24), pbr(0x222233, { metalness: 0.9, roughness: 0.1 }));
    hub.rotation.x = Math.PI / 2; hub.position.z = 0.11;
    mesh.add(hub);
    scene.add(mesh); objects.push(mesh); gearMeshes.push(mesh);
    labels.push({ pos: new THREE.Vector3(def.pos[0], def.r + 0.5, 0), text: def.name, color: `#${def.color.toString(16).padStart(6, "0")}` });
  });

  // Backing plate
  const plate = new THREE.Mesh(new THREE.BoxGeometry(5, 3, 0.06), pbr(0x1a2030, { metalness: 0.3, roughness: 0.9 }));
  plate.position.z = -0.18; plate.receiveShadow = true;
  scene.add(plate); objects.push(plate);

  const ratios = [1, -gearDefs[0].teeth / gearDefs[1].teeth, gearDefs[0].teeth / gearDefs[2].teeth * (gearDefs[1].teeth / gearDefs[1].teeth)];
  let frame = 0;
  const tick = () => {
    frame++;
    gearMeshes.forEach((g, i) => { g.rotation.z += 0.012 * (i % 2 === 0 ? 1 : -1) / (gearDefs[i]?.teeth ?? 20) * 12; });
  };
  return { labels, tick, cleanup: () => { objects.forEach(o => scene.remove(o)); } };
}

function buildMechanical(scene: THREE.Scene, params: Record<string, unknown>) {
  const subtype = (params.subtype as string) || "custom";
  switch (subtype) {
    case "wind_turbine": return buildWindTurbine(scene, params);
    case "pendulum": return buildPendulum(scene, params);
    case "atom": return buildAtom(scene, params);
    case "orbital": case "orbit": return buildOrbit(scene, params);
    case "spring": case "spring_mass": return buildSpringMass(scene, params);
    case "gears": case "gear_system": return buildGearSystem(scene, params);
    default: return buildWindTurbine(scene, params); // fallback
  }
}

// ─── EXISTING SCENES (improved materials) ────────────────────────────────────

function buildNeuralNet(scene: THREE.Scene, params: Record<string, unknown>) {
  const layers = (params.layers as number[]) ?? [2, 4, 4, 1];
  const activations = (params.activations as string[]) ?? [];
  const highlightLayer = (params.highlightLayer as number) ?? -1;
  const showWeights = params.showWeights !== false;
  const LAYER_GAP = 2.4;
  const ACT_COLORS: Record<string, number> = { relu: 0x34d399, sigmoid: 0xf59e0b, tanh: 0xa78bfa, softmax: 0xf87171, linear: 0x60a5fa };
  const LAYER_COLORS = [0x60a5fa, 0xa78bfa, 0x34d399, 0xf59e0b, 0xf87171, 0x38bdf8];
  const neuronMeshes: THREE.Mesh[][] = [];
  const labels: Label[] = [];
  const objects: THREE.Object3D[] = [];

  layers.forEach((count, li) => {
    const x = (li - (layers.length - 1) / 2) * LAYER_GAP;
    const row: THREE.Mesh[] = [];
    const act = activations[li - 1] || "relu";
    const col = li === 0 ? 0x60a5fa : li === layers.length - 1 ? 0xf87171 : ACT_COLORS[act] ?? LAYER_COLORS[li % 6];
    const n = Math.min(count, 8);
    for (let ni = 0; ni < n; ni++) {
      const y = (ni - (n - 1) / 2) * (3.4 / Math.max(n, 4));
      const mesh = new THREE.Mesh(new THREE.SphereGeometry(0.22, 24, 24), pbr(col, { metalness: 0.45, roughness: 0.3, emissive: col, emissiveIntensity: li === highlightLayer ? 0.5 : 0.12 }));
      mesh.position.set(x, y, 0); mesh.castShadow = true;
      scene.add(mesh); objects.push(mesh); row.push(mesh);
    }
    const lbl = li === 0 ? "Input" : li === layers.length - 1 ? "Output" : `Hidden ${li}`;
    labels.push({ pos: new THREE.Vector3(x, -2.4, 0), text: `${lbl} (${count})`, color: "#64748b" });
    neuronMeshes.push(row);
  });

  if (showWeights) {
    const lineMat = new THREE.LineBasicMaterial({ color: 0x4338ca, transparent: true, opacity: 0.14 });
    layers.forEach((c, li) => {
      if (li >= layers.length - 1) return;
      const fromN = Math.min(c, 8), toN = Math.min(layers[li + 1], 8);
      for (let a = 0; a < fromN; a++) for (let b = 0; b < toN; b++) {
        if (fromN > 5 && toN > 5 && Math.random() > 0.45) continue;
        const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints([neuronMeshes[li][a].position, neuronMeshes[li + 1][b].position]), lineMat);
        scene.add(line); objects.push(line);
      }
    });
  }

  let frame = 0;
  const tick = () => {
    frame++;
    neuronMeshes.forEach((row, li) => row.forEach((m, ni) => {
      const mat = m.material as THREE.MeshStandardMaterial;
      const t = Math.sin(frame * 0.04 + li * 1.2 + ni * 0.35);
      mat.emissiveIntensity = li === highlightLayer ? 0.35 + (t + 1) * 0.28 : 0.07 + (t + 1) * 0.05;
    }));
  };
  return { labels, tick, cleanup: () => { objects.forEach(o => scene.remove(o)); } };
}

function buildGradientDescent(scene: THREE.Scene, params: Record<string, unknown>) {
  const lossType = (params.lossType as string) || "bowl";
  const lr = (params.learningRate as number) || 0.15;
  const steps = (params.steps as number) || 18;
  const startPos = (params.startPos as [number, number]) || [2.2, 2.2];
  const lossFns: Record<string, (x: number, y: number) => number> = {
    bowl: (x, y) => x * x * 0.4 + y * y * 0.4,
    saddle: (x, y) => x * x * 0.4 - y * y * 0.4 + 1.5,
    ravine: (x, y) => x * x * 0.08 + y * y * 1.4,
    noisy: (x, y) => x * x * 0.3 + y * y * 0.3 + Math.sin(x * 3) * 0.2 + Math.sin(y * 3) * 0.2,
  };
  const gradFns: Record<string, (x: number, y: number) => [number, number]> = {
    bowl: (x, y) => [x * 0.8, y * 0.8], saddle: (x, y) => [x * 0.8, -y * 0.8],
    ravine: (x, y) => [x * 0.16, y * 2.8], noisy: (x, y) => [x * 0.6 + Math.cos(x * 3) * 0.6, y * 0.6 + Math.cos(y * 3) * 0.6],
  };
  const lossFn = lossFns[lossType] || lossFns.bowl;
  const gradFn = gradFns[lossType] || gradFns.bowl;
  const objects: THREE.Object3D[] = [];

  const geo = new THREE.PlaneGeometry(6, 6, 44, 44);
  const pos = geo.attributes.position;
  let minZ = Infinity, maxZ = -Infinity;
  for (let i = 0; i < pos.count; i++) { const z = lossFn(pos.getX(i), pos.getY(i)); pos.setZ(i, z); minZ = Math.min(minZ, z); maxZ = Math.max(maxZ, z); }
  geo.computeVertexNormals();
  const colors = new Float32Array(pos.count * 3);
  for (let i = 0; i < pos.count; i++) { const t = (pos.getZ(i) - minZ) / (maxZ - minZ); const c = new THREE.Color().setHSL(0.67 - t * 0.5, 0.88, 0.35 + t * 0.25); colors[i * 3] = c.r; colors[i * 3 + 1] = c.g; colors[i * 3 + 2] = c.b; }
  geo.setAttribute("color", new THREE.BufferAttribute(colors, 3));
  const surface = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, roughness: 0.55, metalness: 0.1, transparent: true, opacity: 0.9 }));
  surface.rotation.x = -Math.PI / 2; surface.receiveShadow = true;
  scene.add(surface); objects.push(surface);

  const pathPts: THREE.Vector3[] = [];
  let [x, y] = startPos;
  for (let i = 0; i <= steps; i++) {
    pathPts.push(new THREE.Vector3(x, lossFn(x, y) + 0.08, y));
    const [gx, gy] = gradFn(x, y);
    x = Math.max(-2.9, Math.min(2.9, x - lr * gx)); y = Math.max(-2.9, Math.min(2.9, y - lr * gy));
  }
  const pathLine = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pathPts), new THREE.LineBasicMaterial({ color: 0xfacc15, linewidth: 2 }));
  scene.add(pathLine); objects.push(pathLine);

  const ball = new THREE.Mesh(new THREE.SphereGeometry(0.15, 24, 24), pbr(0xfacc15, { metalness: 0.2, roughness: 0.2, emissive: 0xfacc15, emissiveIntensity: 0.9 }));
  scene.add(ball); objects.push(ball);

  const labels: Label[] = [
    { pos: pathPts[0].clone().add(new THREE.Vector3(0, 0.35, 0)), text: "start", color: "#94a3b8" },
    { pos: pathPts[pathPts.length - 1].clone().add(new THREE.Vector3(0, 0.45, 0)), text: "minimum", color: "#34d399" },
  ];
  let frame = 0;
  const tick = () => {
    frame++;
    const t = ((frame * 0.007) % 1);
    const idx = Math.min(Math.floor(t * (pathPts.length - 1)), pathPts.length - 2);
    ball.position.lerpVectors(pathPts[idx], pathPts[idx + 1], t * (pathPts.length - 1) - idx);
  };
  return { labels, tick, cleanup: () => { objects.forEach(o => scene.remove(o)); } };
}

function buildAttention(scene: THREE.Scene, params: Record<string, unknown>) {
  const tokens = (params.tokens as string[]) ?? ["The", "cat", "sat", "on", "mat"];
  const highlightToken = (params.highlightToken as number) ?? 1;
  const rawWeights = params.attentionWeights as number[][] | undefined;
  const n = Math.min(tokens.length, 6);
  const weights = rawWeights?.slice(0, n).map(r => r.slice(0, n)) ?? Array.from({ length: n }, (_, i) => { const row = Array.from({ length: n }, (_, j) => Math.random() * 0.5 + (j === highlightToken ? 0.4 : 0.1)); const s = row.reduce((a, b) => a + b, 0); return row.map(v => v / s); });
  const CELL = 1.0;
  const objects: THREE.Object3D[] = [];
  const labels: Label[] = [];
  for (let row = 0; row < n; row++) for (let col = 0; col < n; col++) {
    const w = weights[row]?.[col] ?? 0.15;
    const hi = row === highlightToken || col === highlightToken;
    const c = new THREE.Color().setHSL(hi ? 0.68 : 0.58, 0.82, 0.2 + w * 0.45);
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(0.88, 0.88, 0.1 + w * 0.65), pbr(c.getHex(), { metalness: 0.4, roughness: 0.3, emissive: c.getHex(), emissiveIntensity: hi ? 0.32 : 0.04, transparent: true, opacity: 0.6 + w * 0.38 }));
    mesh.position.set((col - (n - 1) / 2) * CELL, (row - (n - 1) / 2) * -CELL, w * 0.32);
    scene.add(mesh); objects.push(mesh);
  }
  tokens.slice(0, n).forEach((tok, i) => { labels.push({ pos: new THREE.Vector3(-(n / 2) * CELL - 1.0, (i - (n - 1) / 2) * -CELL, 0), text: tok, color: i === highlightToken ? "#818cf8" : "#64748b" }); labels.push({ pos: new THREE.Vector3((i - (n - 1) / 2) * CELL, (n / 2) * CELL + 0.85, 0), text: tok, color: "#64748b" }); });
  let frame = 0;
  const tick = () => { frame++; };
  return { labels, tick, cleanup: () => { objects.forEach(o => scene.remove(o)); } };
}

function buildDataFlow(scene: THREE.Scene, params: Record<string, unknown>) {
  const stages = (params.stages as { label: string; color?: string }[]) ?? [{ label: "Input", color: "#3b82f6" }, { label: "Embed", color: "#8b5cf6" }, { label: "Model", color: "#6366f1" }, { label: "Output", color: "#10b981" }];
  const n = Math.min(stages.length, 7);
  const SPACING = 2.6;
  const objects: THREE.Object3D[] = [];
  const labels: Label[] = [];
  const positions: THREE.Vector3[] = [];
  stages.slice(0, n).forEach((s, i) => {
    const x = (i - (n - 1) / 2) * SPACING;
    const pos = new THREE.Vector3(x, 0, 0); positions.push(pos);
    const hex = parseInt((s.color || "#6366f1").replace("#", ""), 16);
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.72, 0.22), pbr(hex, { metalness: 0.5, roughness: 0.35, emissive: hex, emissiveIntensity: 0.18 }));
    mesh.position.copy(pos); mesh.castShadow = true;
    scene.add(mesh); objects.push(mesh);
    labels.push({ pos: new THREE.Vector3(x, 0.62, 0), text: s.label, color: s.color || "#94a3b8" });
  });
  const particles: { mesh: THREE.Mesh; from: THREE.Vector3; to: THREE.Vector3; offset: number }[] = [];
  positions.slice(0, -1).forEach((from, i) => {
    const to = positions[i + 1];
    scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([from, to]), new THREE.LineBasicMaterial({ color: 0x475569, transparent: true, opacity: 0.4 })));
    const hex = parseInt((stages[i].color || "#6366f1").replace("#", ""), 16);
    [0, 0.33, 0.66].forEach(offset => { const pm = new THREE.Mesh(new THREE.SphereGeometry(0.07, 10, 10), pbr(hex, { emissive: hex, emissiveIntensity: 1.3 })); scene.add(pm); objects.push(pm); particles.push({ mesh: pm, from, to, offset }); });
  });
  let frame = 0;
  const tick = () => { frame++; particles.forEach(p => { const t = ((frame * 0.008 + p.offset) % 1 + 1) % 1; p.mesh.position.lerpVectors(p.from, p.to, t); (p.mesh.material as THREE.MeshStandardMaterial).opacity = Math.sin(t * Math.PI); }); };
  return { labels, tick, cleanup: () => { objects.forEach(o => scene.remove(o)); } };
}

function buildEmbedding(scene: THREE.Scene, params: Record<string, unknown>) {
  const points = (params.points as { label: string; x: number; y: number; z: number; cluster: string }[]) ?? [{ label: "king", x: 1.5, y: 0.8, z: 0.2, cluster: "royalty" }, { label: "queen", x: 1.3, y: 1.1, z: 0.3, cluster: "royalty" }, { label: "dog", x: -1.5, y: 0.5, z: 1.0, cluster: "animals" }, { label: "cat", x: -1.2, y: 0.3, z: 0.8, cluster: "animals" }, { label: "Paris", x: 0.2, y: -1.5, z: -0.5, cluster: "cities" }];
  const clusters = (params.clusters as { name: string; color: string }[]) ?? [];
  const clusterColorMap: Record<string, number> = {};
  const defaults = [0xf59e0b, 0x34d399, 0x60a5fa, 0xa78bfa, 0xf87171];
  clusters.forEach((c, i) => { clusterColorMap[c.name] = parseInt(c.color.replace("#", ""), 16) || defaults[i % 5]; });
  const allClusters = [...new Set(points.map(p => p.cluster))];
  const maxC = Math.max(...points.flatMap(p => [Math.abs(p.x), Math.abs(p.y), Math.abs(p.z)]), 1);
  const scale = 2.2 / maxC;
  const groupRef = new THREE.Group(); scene.add(groupRef);
  [[-2.8, 0, 0], [2.8, 0, 0]].forEach(([ax, ay, az]) => { const geo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(ax, ay, az), new THREE.Vector3(-ax, -ay, -az)]); groupRef.add(new THREE.Line(geo, new THREE.LineBasicMaterial({ color: 0x1e293b }))); });
  const labels: Label[] = [];
  const clusterPts: Record<string, THREE.Vector3[]> = {};
  points.slice(0, 20).forEach(pt => {
    const pos = new THREE.Vector3(pt.x * scale, pt.y * scale, pt.z * scale);
    const ci = allClusters.indexOf(pt.cluster);
    const color = clusterColorMap[pt.cluster] ?? defaults[ci % 5];
    const mesh = new THREE.Mesh(new THREE.SphereGeometry(0.12, 16, 16), pbr(color, { metalness: 0.5, roughness: 0.3, emissive: color, emissiveIntensity: 0.45 }));
    mesh.position.copy(pos); groupRef.add(mesh);
    labels.push({ pos, text: pt.label, color: `#${color.toString(16).padStart(6, "0")}` });
    if (!clusterPts[pt.cluster]) clusterPts[pt.cluster] = [];
    clusterPts[pt.cluster].push(pos);
  });
  Object.values(clusterPts).forEach(pts => { for (let i = 0; i < pts.length; i++) for (let j = i + 1; j < pts.length; j++) groupRef.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([pts[i], pts[j]]), new THREE.LineBasicMaterial({ color: 0x334155, transparent: true, opacity: 0.18 }))); });
  let frame = 0;
  const tick = () => { frame++; groupRef.rotation.y = frame * 0.006; };
  return { labels, tick, cleanup: () => { scene.remove(groupRef); } };
}

function buildCustomAdvanced(scene: THREE.Scene, params: Record<string, unknown>) {
  const rawObjects = (params.objects as Record<string, unknown>[]) ?? [
    { type: "sphere", position: [-2, 0, 0], size: [0.8], color: "#60a5fa", metalness: 0.5, roughness: 0.3, label: "Input" },
    { type: "box", position: [0, 0, 0], size: [1.2, 0.8, 0.4], color: "#8b5cf6", metalness: 0.4, roughness: 0.35, label: "Process" },
    { type: "cone", position: [2, 0, 0], size: [0.8, 1.2], color: "#34d399", metalness: 0.4, roughness: 0.3, label: "Output" },
  ];
  const connections = (params.connections as { from: number; to: number; color?: string }[]) ?? [];
  const objects: THREE.Object3D[] = [];
  const labels: Label[] = [];
  const positions: THREE.Vector3[] = [];

  rawObjects.slice(0, 14).forEach((obj, i) => {
    const pos = new THREE.Vector3(...((obj.position as number[] ?? [0, 0, 0]) as [number, number, number]));
    positions.push(pos);
    const size = (obj.size as number[]) ?? [1, 1, 1];
    const color = parseInt(((obj.color as string) || "#6366f1").replace("#", ""), 16);
    const mat = pbr(color, {
      metalness: (obj.metalness as number) ?? 0.4,
      roughness: (obj.roughness as number) ?? 0.4,
      emissive: color,
      emissiveIntensity: (obj.emissiveIntensity as number) ?? 0.08,
      transparent: (obj.opacity as number) < 1,
      opacity: (obj.opacity as number) ?? 1,
    });

    let geo: THREE.BufferGeometry;
    switch (obj.type) {
      case "sphere": geo = new THREE.SphereGeometry(size[0] / 2, 32, 32); break;
      case "cylinder": geo = new THREE.CylinderGeometry(size[0] / 2, size[0] / 2, size[1] ?? 1, 32); break;
      case "cone": geo = new THREE.ConeGeometry(size[0] / 2, size[1] ?? 1, 32); break;
      case "torus": geo = new THREE.TorusGeometry(size[0] / 2, (size[1] ?? 0.25) / 2, 16, 48); break;
      case "octahedron": geo = new THREE.OctahedronGeometry(size[0] / 2); break;
      case "lathe": {
        const pts2D = ((obj.radiusPoints as number[][]) ?? [[0.3, 0], [0.25, 0.5], [0.15, 1.5], [0.1, 2.5]]).map(([r, y]) => new THREE.Vector2(r, y));
        geo = new THREE.LatheGeometry(pts2D, 32); break;
      }
      default: geo = new THREE.BoxGeometry(...(size as [number, number, number]));
    }

    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.copy(pos); mesh.castShadow = true; mesh.receiveShadow = true;

    // Animation
    const anim = obj.animate as { type?: string; axis?: string; speed?: number } | undefined;
    if (anim?.type === "rotate") {
      (mesh as THREE.Mesh & { _animSpeed?: number; _animAxis?: string })._animSpeed = anim.speed ?? 0.01;
      (mesh as THREE.Mesh & { _animAxis?: string })._animAxis = anim.axis ?? "y";
    }

    scene.add(mesh); objects.push(mesh);
    if (obj.label) labels.push({ pos: pos.clone().add(new THREE.Vector3(0, (size[1] ?? size[0] ?? 1) / 2 + 0.4, 0)), text: obj.label as string, color: "#94a3b8" });
  });

  // Tube connections (much nicer than lines)
  connections.forEach(conn => {
    const from = positions[conn.from]; const to = positions[conn.to];
    if (!from || !to) return;
    const color = parseInt((conn.color || "#475569").replace("#", ""), 16);
    // Create a smooth tube path
    const mid = from.clone().add(to).multiplyScalar(0.5).add(new THREE.Vector3(0, 0.6, 0));
    const curve = new THREE.QuadraticBezierCurve3(from, mid, to);
    const tubeGeo = new THREE.TubeGeometry(curve, 20, 0.035, 8, false);
    const tube = new THREE.Mesh(tubeGeo, pbr(color, { metalness: 0.5, roughness: 0.4, transparent: true, opacity: 0.6 }));
    scene.add(tube); objects.push(tube);
  });

  let frame = 0;
  const tick = () => {
    frame++;
    objects.forEach(o => {
      const m = o as THREE.Mesh & { _animSpeed?: number; _animAxis?: string };
      if (m._animSpeed) {
        if (m._animAxis === "x") m.rotation.x += m._animSpeed;
        else if (m._animAxis === "z") m.rotation.z += m._animSpeed;
        else m.rotation.y += m._animSpeed;
      }
    });
  };
  return { labels, tick, cleanup: () => { objects.forEach(o => scene.remove(o)); } };
}

// ─── Main Component ───────────────────────────────────────────────────────────
interface Props { config: VizConfig; onClose?: () => void; compact?: boolean }

export default function VisualRenderer({ config, onClose, compact = false }: Props) {
  const mountRef = useRef<HTMLDivElement>(null);
  const [fullscreen, setFullscreen] = useState(false);
  const height = fullscreen ? "90vh" : compact ? "280px" : "480px";

  useEffect(() => {
    const mount = mountRef.current;
    if (!mount) return;
    while (mount.firstChild) mount.removeChild(mount.firstChild);

    const canvas = document.createElement("canvas");
    canvas.style.cssText = "width:100%;height:100%;display:block;";
    mount.appendChild(canvas);

    const labelOverlay = document.createElement("div");
    labelOverlay.style.cssText = "position:absolute;inset:0;pointer-events:none;overflow:hidden;";
    mount.appendChild(labelOverlay);

    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.setClearColor(0x060c18);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.15;

    const w = mount.clientWidth || 700, h = mount.clientHeight || 480;
    renderer.setSize(w, h);

    const scene = new THREE.Scene();

    // Lighting — studio quality
    const hemi = new THREE.HemisphereLight(0x223366, 0x110822, 0.55);
    scene.add(hemi);
    const sun = new THREE.DirectionalLight(0xffffff, 1.4);
    sun.position.set(7, 14, 6); sun.castShadow = true;
    sun.shadow.mapSize.set(2048, 2048);
    sun.shadow.camera.near = 0.1; sun.shadow.camera.far = 40;
    sun.shadow.camera.left = -10; sun.shadow.camera.right = 10;
    sun.shadow.camera.top = 10; sun.shadow.camera.bottom = -10;
    sun.shadow.bias = -0.001;
    scene.add(sun);
    const fill = new THREE.DirectionalLight(0x8899ff, 0.4);
    fill.position.set(-6, 4, -4); scene.add(fill);
    const rim = new THREE.PointLight(0x6366f1, 0.6, 18);
    rim.position.set(-5, 6, -5); scene.add(rim);
    const rimB = new THREE.PointLight(0x06b6d4, 0.35, 14);
    rimB.position.set(5, -2, 6); scene.add(rimB);

    // Camera
    const camera = new THREE.PerspectiveCamera(50, w / h, 0.05, 120);
    const camPresets: Record<string, [number, number, number]> = {
      mechanical: [5, 4, 8], neural_network: [0, 2, 9], gradient_descent: [3, 7, 5],
      attention: [0, 1, 10], data_flow: [0, 1, 10], convolution: [0, 1, 12],
      embedding_space: [0, 3, 8], custom_geometry: [4, 3, 8],
    };
    const cp = camPresets[config.vizType] ?? [5, 4, 8];
    camera.position.set(...cp); camera.lookAt(0, 0, 0);

    // Grid floor
    const grid = new THREE.GridHelper(22, 22, 0x1e293b, 0x0f172a);
    grid.position.y = -4.2;
    (grid.material as THREE.Material).transparent = true; (grid.material as THREE.Material).opacity = 0.45;
    scene.add(grid);

    // Stars
    const starGeo = new THREE.BufferGeometry();
    const sp = new Float32Array(3600);
    for (let i = 0; i < 3600; i++) sp[i] = (Math.random() - 0.5) * 140;
    starGeo.setAttribute("position", new THREE.BufferAttribute(sp, 3));
    scene.add(new THREE.Points(starGeo, new THREE.PointsMaterial({ color: 0xffffff, size: 0.055, transparent: true, opacity: 0.55 })));

    // Build scene
    const builders: Record<string, (s: THREE.Scene, p: Record<string, unknown>) => { labels: Label[]; tick: () => void; cleanup: () => void }> = {
      mechanical: buildMechanical,
      neural_network: buildNeuralNet,
      gradient_descent: buildGradientDescent,
      attention: buildAttention,
      data_flow: buildDataFlow,
      embedding_space: buildEmbedding,
      custom_geometry: buildCustomAdvanced,
      decision_tree: buildCustomAdvanced,
      convolution: buildCustomAdvanced,
    };
    const builder = builders[config.vizType] ?? buildCustomAdvanced;
    const { labels, tick, cleanup } = builder(scene, config.params);

    // Label DOM elements
    const labelEls = labels.map(({ pos, text, color, size }) => {
      const el = document.createElement("div");
      el.textContent = text;
      el.style.cssText = `position:absolute;font-size:${size ?? 11}px;font-family:system-ui,sans-serif;font-weight:500;color:${color};white-space:nowrap;pointer-events:none;transform:translate(-50%,-50%);text-shadow:0 1px 5px #000c;letter-spacing:0.01em;`;
      labelOverlay.appendChild(el);
      return { el, pos };
    });

    const ro = new ResizeObserver(() => {
      const nw = mount.clientWidth, nh = mount.clientHeight;
      renderer.setSize(nw, nh); camera.aspect = nw / nh; camera.updateProjectionMatrix();
    });
    ro.observe(mount);

    const disposeOrbit = addOrbitControls(camera, mount);

    const tmpV = new THREE.Vector3();
    let rafId: number, frame = 0;
    const animate = () => {
      rafId = requestAnimationFrame(animate);
      frame++;
      tick();
      renderer.render(scene, camera);
      labelEls.forEach(({ el, pos }) => {
        tmpV.copy(pos).project(camera);
        const sx = (tmpV.x * 0.5 + 0.5) * mount.clientWidth;
        const sy = (-tmpV.y * 0.5 + 0.5) * mount.clientHeight;
        el.style.left = `${sx}px`; el.style.top = `${sy}px`;
        el.style.display = tmpV.z < 1 ? "block" : "none";
      });
    };
    animate();

    return () => {
      cancelAnimationFrame(rafId); disposeOrbit(); ro.disconnect(); cleanup();
      renderer.dispose(); while (mount.firstChild) mount.removeChild(mount.firstChild);
    };
  }, [config, fullscreen]);

  return (
    <div className={`relative rounded-xl overflow-hidden border border-slate-700/40 ${fullscreen ? "fixed inset-4 z-50" : ""}`}
      style={{ height, background: "#060c18" }}>
      <div className="absolute top-0 left-0 right-0 z-10 px-4 py-2.5 flex items-center justify-between bg-gradient-to-b from-[#060c18ee] via-[#060c18aa] to-transparent pointer-events-none">
        <div>
          <h3 className="text-sm font-semibold text-white leading-snug">{config.title}</h3>
          {!compact && <p className="text-[11px] text-slate-400 mt-0.5 max-w-lg">{config.description}</p>}
        </div>
        <div className="flex items-center gap-1.5 pointer-events-auto">
          <span className="text-[10px] px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/25 font-mono">{config.vizType}</span>
          <button onClick={() => setFullscreen(f => !f)} className="text-slate-400 hover:text-white p-1.5 rounded-lg hover:bg-white/5 transition-colors" title="Toggle fullscreen">
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {fullscreen ? <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 9L4 4m0 0v4m0-4h4M15 15l5 5m0 0v-4m0 4h-4M9 15l-5 5m0 0v-4m0 4h4M15 9l5-5m0 0v4m0-4h-4" /> : <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-5h-4m4 0v4m0-4l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />}
            </svg>
          </button>
          {onClose && <button onClick={onClose} className="text-slate-400 hover:text-white p-1.5 rounded-lg hover:bg-white/5 transition-colors"><svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg></button>}
        </div>
      </div>
      <div className="absolute bottom-2 left-1/2 -translate-x-1/2 z-10 text-[9px] text-slate-700 pointer-events-none select-none tracking-wide uppercase">drag · zoom · orbit</div>
      <div ref={mountRef} className="w-full h-full" />
    </div>
  );
}
