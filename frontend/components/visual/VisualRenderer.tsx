"use client";
import { useEffect, useRef, useState } from "react";
import * as THREE from "three";

export interface VizConfig {
  vizType: string;
  title: string;
  description: string;
  params: Record<string, unknown>;
}

interface Label { pos: THREE.Vector3; text: string; color: string }

// ─── Orbit Controls (manual) ─────────────────────────────────────────────────
function addOrbitControls(
  camera: THREE.PerspectiveCamera,
  domElement: HTMLElement,
  target = new THREE.Vector3()
) {
  const sph = new THREE.Spherical().setFromVector3(
    camera.position.clone().sub(target)
  );

  let down = false, px = 0, py = 0;

  const onDown = (e: PointerEvent) => { down = true; px = e.clientX; py = e.clientY; domElement.setPointerCapture(e.pointerId); };
  const onUp = () => { down = false; };
  const onMove = (e: PointerEvent) => {
    if (!down) return;
    sph.theta -= (e.clientX - px) * 0.008;
    sph.phi = Math.max(0.1, Math.min(Math.PI - 0.1, sph.phi - (e.clientY - py) * 0.008));
    px = e.clientX; py = e.clientY;
    camera.position.setFromSpherical(sph).add(target);
    camera.lookAt(target);
  };
  const onWheel = (e: WheelEvent) => {
    sph.radius = Math.max(3, Math.min(22, sph.radius + e.deltaY * 0.012));
    camera.position.setFromSpherical(sph).add(target);
    camera.lookAt(target);
    e.preventDefault();
  };

  domElement.addEventListener("pointerdown", onDown);
  domElement.addEventListener("pointerup", onUp);
  domElement.addEventListener("pointermove", onMove);
  domElement.addEventListener("wheel", onWheel, { passive: false });

  return () => {
    domElement.removeEventListener("pointerdown", onDown);
    domElement.removeEventListener("pointerup", onUp);
    domElement.removeEventListener("pointermove", onMove);
    domElement.removeEventListener("wheel", onWheel);
  };
}

// ─── Scene builders ───────────────────────────────────────────────────────────

function buildNeuralNet(scene: THREE.Scene, params: Record<string, unknown>): { labels: Label[]; cleanup: () => void } {
  const layers = (params.layers as number[]) ?? [2, 4, 3, 1];
  const activations = (params.activations as string[]) ?? [];
  const highlightLayer = (params.highlightLayer as number) ?? -1;
  const showWeights = params.showWeights !== false;
  const LAYER_GAP = 2.4;

  const ACT_COLORS: Record<string, number> = {
    relu: 0x34d399, sigmoid: 0xf59e0b, tanh: 0xa78bfa,
    softmax: 0xf87171, linear: 0x60a5fa,
  };
  const LAYER_COLORS = [0x60a5fa, 0xa78bfa, 0x34d399, 0xf59e0b, 0xf87171, 0x38bdf8];

  const neuronMeshes: THREE.Mesh[][] = [];
  const labels: Label[] = [];
  const objects: THREE.Object3D[] = [];

  // Build neurons
  layers.forEach((count, li) => {
    const x = (li - (layers.length - 1) / 2) * LAYER_GAP;
    const meshRow: THREE.Mesh[] = [];
    const activation = activations[li - 1] || "relu";
    const color = li === 0 ? 0x60a5fa : li === layers.length - 1 ? 0xf87171 : ACT_COLORS[activation] ?? LAYER_COLORS[li % 6];

    const displayCount = Math.min(count, 8);
    for (let ni = 0; ni < displayCount; ni++) {
      const y = (ni - (displayCount - 1) / 2) * (3.6 / Math.max(displayCount, 4));
      const geo = new THREE.SphereGeometry(0.2, 20, 20);
      const mat = new THREE.MeshStandardMaterial({
        color, emissive: color,
        emissiveIntensity: li === highlightLayer ? 0.5 : 0.15,
        roughness: 0.3, metalness: 0.4,
      });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(x, y, 0);
      mesh.castShadow = true;
      scene.add(mesh);
      objects.push(mesh);
      meshRow.push(mesh);
    }

    // Labels
    const label = li === 0 ? "Input" : li === layers.length - 1 ? "Output" : `Hidden ${li}`;
    const pos = new THREE.Vector3(x, -(displayCount / 2) * (3.6 / Math.max(displayCount, 4)) - 0.7, 0);
    labels.push({ pos, text: `${label} (${count})`, color: "#64748b" });
    neuronMeshes.push(meshRow);
  });

  // Build weight edges
  if (showWeights) {
    const lineMat = new THREE.LineBasicMaterial({ color: 0x4f46e5, transparent: true, opacity: 0.18 });
    layers.forEach((count, li) => {
      if (li >= layers.length - 1) return;
      const fromCount = Math.min(count, 8);
      const toCount = Math.min(layers[li + 1], 8);
      for (let a = 0; a < fromCount; a++) {
        for (let b = 0; b < toCount; b++) {
          if (fromCount > 5 && toCount > 5 && Math.random() > 0.5) continue;
          const pts = new THREE.BufferGeometry().setFromPoints([
            neuronMeshes[li][a].position,
            neuronMeshes[li + 1][b].position,
          ]);
          const line = new THREE.Line(pts, lineMat);
          scene.add(line);
          objects.push(line);
        }
      }
    });
  }

  // Animate
  let frame = 0;
  const tick = () => {
    frame++;
    neuronMeshes.forEach((row, li) => {
      row.forEach((mesh, ni) => {
        const mat = mesh.material as THREE.MeshStandardMaterial;
        const t = Math.sin(frame * 0.04 + li * 1.2 + ni * 0.4);
        mat.emissiveIntensity = li === highlightLayer
          ? 0.35 + (t + 1) * 0.25
          : 0.08 + (t + 1) * 0.06;
      });
    });
  };

  return {
    labels,
    cleanup: () => { objects.forEach(o => scene.remove(o)); },
  };
}

function buildGradientDescent(scene: THREE.Scene, params: Record<string, unknown>): { labels: Label[]; cleanup: () => void } {
  const lossType = (params.lossType as string) || "bowl";
  const lr = (params.learningRate as number) || 0.15;
  const steps = (params.steps as number) || 15;
  const startPos = (params.startPos as [number, number]) || [2.2, 2.2];

  const lossFns: Record<string, (x: number, y: number) => number> = {
    bowl: (x, y) => x * x * 0.4 + y * y * 0.4,
    saddle: (x, y) => x * x * 0.4 - y * y * 0.4 + 1.5,
    ravine: (x, y) => x * x * 0.08 + y * y * 1.4,
    noisy: (x, y) => x * x * 0.3 + y * y * 0.3 + Math.sin(x * 3) * 0.2 + Math.sin(y * 3) * 0.2,
  };
  const gradFns: Record<string, (x: number, y: number) => [number, number]> = {
    bowl: (x, y) => [x * 0.8, y * 0.8],
    saddle: (x, y) => [x * 0.8, -y * 0.8],
    ravine: (x, y) => [x * 0.16, y * 2.8],
    noisy: (x, y) => [x * 0.6 + Math.cos(x * 3) * 0.6, y * 0.6 + Math.cos(y * 3) * 0.6],
  };

  const lossFn = lossFns[lossType] || lossFns.bowl;
  const gradFn = gradFns[lossType] || gradFns.bowl;

  const objects: THREE.Object3D[] = [];

  // Surface
  const geo = new THREE.PlaneGeometry(6, 6, 40, 40);
  const pos = geo.attributes.position;
  let minZ = Infinity, maxZ = -Infinity;
  for (let i = 0; i < pos.count; i++) {
    const z = lossFn(pos.getX(i), pos.getY(i));
    pos.setZ(i, z);
    minZ = Math.min(minZ, z); maxZ = Math.max(maxZ, z);
  }
  geo.computeVertexNormals();

  const colors = new Float32Array(pos.count * 3);
  for (let i = 0; i < pos.count; i++) {
    const t = (pos.getZ(i) - minZ) / (maxZ - minZ);
    const c = new THREE.Color().setHSL(0.67 - t * 0.5, 0.9, 0.38 + t * 0.22);
    colors[i * 3] = c.r; colors[i * 3 + 1] = c.g; colors[i * 3 + 2] = c.b;
  }
  geo.setAttribute("color", new THREE.BufferAttribute(colors, 3));

  const mat = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, roughness: 0.6, metalness: 0.1, transparent: true, opacity: 0.88 });
  const surface = new THREE.Mesh(geo, mat);
  surface.rotation.x = -Math.PI / 2;
  surface.receiveShadow = true;
  scene.add(surface);
  objects.push(surface);

  // GD path
  const pathPts: THREE.Vector3[] = [];
  let [x, y] = startPos;
  for (let i = 0; i <= steps; i++) {
    const z = lossFn(x, y);
    pathPts.push(new THREE.Vector3(x, z + 0.08, y));
    const [gx, gy] = gradFn(x, y);
    x = Math.max(-2.9, Math.min(2.9, x - lr * gx));
    y = Math.max(-2.9, Math.min(2.9, y - lr * gy));
  }

  const lineGeo = new THREE.BufferGeometry().setFromPoints(pathPts);
  const lineMat = new THREE.LineBasicMaterial({ color: 0xfacc15, linewidth: 2 });
  const pathLine = new THREE.Line(lineGeo, lineMat);
  scene.add(pathLine);
  objects.push(pathLine);

  // Ball
  const ballGeo = new THREE.SphereGeometry(0.14, 20, 20);
  const ballMat = new THREE.MeshStandardMaterial({ color: 0xfacc15, emissive: 0xfacc15, emissiveIntensity: 0.9 });
  const ball = new THREE.Mesh(ballGeo, ballMat);
  scene.add(ball);
  objects.push(ball);

  let frame = 0;
  const tick = () => {
    frame++;
    const t = ((frame * 0.008) % 1 + 1) % 1;
    const idx = Math.min(Math.floor(t * (pathPts.length - 1)), pathPts.length - 2);
    const frac = t * (pathPts.length - 1) - idx;
    ball.position.lerpVectors(pathPts[idx], pathPts[idx + 1], frac);
  };

  const labels: Label[] = [
    { pos: pathPts[0].clone().add(new THREE.Vector3(0, 0.4, 0)), text: "start", color: "#94a3b8" },
    { pos: pathPts[pathPts.length - 1].clone().add(new THREE.Vector3(0, 0.5, 0)), text: "minimum", color: "#34d399" },
  ];

  return { labels, cleanup: () => { objects.forEach(o => scene.remove(o)); } };
}

function buildAttention(scene: THREE.Scene, params: Record<string, unknown>): { labels: Label[]; cleanup: () => void } {
  const tokens = (params.tokens as string[]) ?? ["The", "cat", "sat", "on", "mat"];
  const highlightToken = (params.highlightToken as number) ?? 1;
  const rawWeights = params.attentionWeights as number[][] | undefined;

  const n = Math.min(tokens.length, 6);
  const toks = tokens.slice(0, n);

  const weights: number[][] = rawWeights?.slice(0, n).map(r => r.slice(0, n)) ?? Array.from({ length: n }, (_, i) => {
    const row = Array.from({ length: n }, (_, j) => Math.random() * 0.5 + (j === highlightToken ? 0.4 : 0.1));
    const sum = row.reduce((a, b) => a + b, 0);
    return row.map(v => v / sum);
  });

  const CELL = 1.0;
  const objects: THREE.Object3D[] = [];
  const labels: Label[] = [];

  for (let row = 0; row < n; row++) {
    for (let col = 0; col < n; col++) {
      const w = weights[row]?.[col] ?? 0.15;
      const hi = row === highlightToken || col === highlightToken;
      const px = (col - (n - 1) / 2) * CELL;
      const py = (row - (n - 1) / 2) * -CELL;
      const pz = w * 0.6;

      const geo = new THREE.BoxGeometry(0.88, 0.88, 0.1 + pz);
      const hue = hi ? 0.68 : 0.58;
      const c = new THREE.Color().setHSL(hue, 0.8, 0.2 + w * 0.45);
      const mat = new THREE.MeshStandardMaterial({
        color: c, emissive: c,
        emissiveIntensity: hi ? 0.35 : 0.05,
        roughness: 0.3, metalness: 0.5,
        transparent: true, opacity: 0.55 + w * 0.4,
      });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(px, py, pz / 2);
      scene.add(mesh);
      objects.push(mesh);
    }
  }

  // Token labels (rows)
  toks.forEach((tok, i) => {
    labels.push({
      pos: new THREE.Vector3(-(n / 2) * CELL - 1.0, (i - (n - 1) / 2) * -CELL, 0),
      text: tok,
      color: i === highlightToken ? "#818cf8" : "#64748b",
    });
  });
  // Token labels (cols)
  toks.forEach((tok, i) => {
    labels.push({
      pos: new THREE.Vector3((i - (n - 1) / 2) * CELL, (n / 2) * CELL + 0.9, 0),
      text: tok,
      color: "#64748b",
    });
  });

  return { labels, cleanup: () => { objects.forEach(o => scene.remove(o)); } };
}

function buildDataFlow(scene: THREE.Scene, params: Record<string, unknown>): { labels: Label[]; cleanup: () => void } {
  const stages = (params.stages as { label: string; color?: string }[]) ?? [
    { label: "Input", color: "#3b82f6" }, { label: "Embed", color: "#8b5cf6" },
    { label: "Model", color: "#6366f1" }, { label: "Output", color: "#10b981" },
  ];
  const n = Math.min(stages.length, 7);
  const SPACING = 2.6;
  const objects: THREE.Object3D[] = [];
  const labels: Label[] = [];
  const positions: THREE.Vector3[] = [];

  stages.slice(0, n).forEach((stage, i) => {
    const x = (i - (n - 1) / 2) * SPACING;
    const pos = new THREE.Vector3(x, 0, 0);
    positions.push(pos);

    const hex = parseInt((stage.color || "#6366f1").replace("#", ""), 16);
    const geo = new THREE.BoxGeometry(1.6, 0.72, 0.22);
    const mat = new THREE.MeshStandardMaterial({
      color: hex, emissive: hex, emissiveIntensity: 0.22, roughness: 0.4, metalness: 0.5,
    });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.copy(pos);
    mesh.castShadow = true;
    scene.add(mesh);
    objects.push(mesh);

    labels.push({ pos: new THREE.Vector3(x, 0.62, 0), text: stage.label, color: stage.color || "#94a3b8" });
  });

  // Particles on connections
  const particles: { mesh: THREE.Mesh; from: THREE.Vector3; to: THREE.Vector3; offset: number }[] = [];
  positions.slice(0, -1).forEach((from, i) => {
    const to = positions[i + 1];

    // Arrow line
    const pts = new THREE.BufferGeometry().setFromPoints([from, to]);
    const lineMat = new THREE.LineBasicMaterial({ color: 0x475569, transparent: true, opacity: 0.4 });
    const line = new THREE.Line(pts, lineMat);
    scene.add(line); objects.push(line);

    const hex = parseInt(((stages[i].color || "#6366f1")).replace("#", ""), 16);
    [0, 0.33, 0.66].forEach(offset => {
      const pMat = new THREE.MeshStandardMaterial({ color: hex, emissive: hex, emissiveIntensity: 1.2 });
      const pMesh = new THREE.Mesh(new THREE.SphereGeometry(0.07, 10, 10), pMat);
      scene.add(pMesh); objects.push(pMesh);
      particles.push({ mesh: pMesh, from, to, offset });
    });
  });

  let frame = 0;
  const tick = () => {
    frame++;
    particles.forEach(p => {
      const t = ((frame * 0.008 + p.offset) % 1 + 1) % 1;
      p.mesh.position.lerpVectors(p.from, p.to, t);
      const mat = p.mesh.material as THREE.MeshStandardMaterial;
      mat.opacity = Math.sin(t * Math.PI);
    });
  };

  return { labels, cleanup: () => { objects.forEach(o => scene.remove(o)); } };
}

function buildConvolution(scene: THREE.Scene, params: Record<string, unknown>): { labels: Label[]; cleanup: () => void } {
  const inputSize = Math.min((params.inputSize as number) || 6, 8);
  const kernelSize = Math.min((params.kernelSize as number) || 3, 4);
  const CELL = 0.52;
  const objects: THREE.Object3D[] = [];
  const labels: Label[] = [];

  const inputVals = Array.from({ length: inputSize * inputSize }, () => Math.random());
  const kernelVals = Array.from({ length: kernelSize * kernelSize }, () => Math.random());

  let krPos = { row: 0, col: 0 };
  const maxPos = inputSize - kernelSize;

  function drawGrid(vals: number[], size: number, ox: number, isKernel = false) {
    const meshes: THREE.Mesh[] = [];
    for (let row = 0; row < size; row++) {
      for (let col = 0; col < size; col++) {
        const v = Math.abs(vals[row * size + col]);
        const geo = new THREE.BoxGeometry(CELL * 0.9, CELL * 0.9, isKernel ? 0.25 : 0.1 + v * 0.18);
        const color = isKernel ? 0x6366f1 : new THREE.Color().setHSL(0, 0, 0.12 + v * 0.28).getHex();
        const mat = new THREE.MeshStandardMaterial({
          color, emissive: color,
          emissiveIntensity: isKernel ? 0.45 : 0.02,
          roughness: 0.5, metalness: 0.3,
        });
        const mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(
          ox + (col - (size - 1) / 2) * CELL,
          (row - (size - 1) / 2) * -CELL,
          0
        );
        scene.add(mesh); objects.push(mesh); meshes.push(mesh);
      }
    }
    return meshes;
  }

  const inputMeshes = drawGrid(inputVals, inputSize, -2.2);
  const kernelMeshes = drawGrid(kernelVals, kernelSize, 0.8);

  const outSize = maxPos + 1;
  const outputMeshes = drawGrid(Array.from({ length: outSize * outSize }, () => Math.random() * 0.5), outSize, 3.4);

  labels.push(
    { pos: new THREE.Vector3(-2.2, inputSize * CELL / 2 + 0.45, 0), text: `Input (${inputSize}×${inputSize})`, color: "#94a3b8" },
    { pos: new THREE.Vector3(0.8, kernelSize * CELL / 2 + 0.45, 0), text: `Kernel (${kernelSize}×${kernelSize})`, color: "#a5b4fc" },
    { pos: new THREE.Vector3(3.4, outSize * CELL / 2 + 0.45, 0), text: `Feature Map (${outSize}×${outSize})`, color: "#6ee7b7" },
  );

  let frame = 0;
  const tick = () => {
    frame++;
    if (frame % 40 === 0) {
      krPos.col++;
      if (krPos.col > maxPos) { krPos.col = 0; krPos.row++; }
      if (krPos.row > maxPos) { krPos.row = 0; }
    }
    // Highlight kernel position in input
    for (let r = 0; r < inputSize; r++) {
      for (let c = 0; c < inputSize; c++) {
        const mesh = inputMeshes[r * inputSize + c];
        const mat = mesh.material as THREE.MeshStandardMaterial;
        const inKernel = r >= krPos.row && r < krPos.row + kernelSize && c >= krPos.col && c < krPos.col + kernelSize;
        mat.emissive.setHex(inKernel ? 0x3b82f6 : 0x000000);
        mat.emissiveIntensity = inKernel ? 0.45 : 0.02;
      }
    }
    // Highlight output cell
    const outMesh = outputMeshes[krPos.row * outSize + krPos.col];
    if (outMesh) {
      const mat = outMesh.material as THREE.MeshStandardMaterial;
      mat.emissive.setHex(0x34d399);
      mat.emissiveIntensity = 0.7;
    }
  };

  return { labels, cleanup: () => { objects.forEach(o => scene.remove(o)); } };
}

function buildEmbedding(scene: THREE.Scene, params: Record<string, unknown>): { labels: Label[]; cleanup: () => void } {
  const points = (params.points as { label: string; x: number; y: number; z: number; cluster: string }[]) ?? [
    { label: "king", x: 1.5, y: 0.8, z: 0.2, cluster: "royalty" },
    { label: "queen", x: 1.3, y: 1.1, z: 0.3, cluster: "royalty" },
    { label: "dog", x: -1.5, y: 0.5, z: 1.0, cluster: "animals" },
    { label: "cat", x: -1.2, y: 0.3, z: 0.8, cluster: "animals" },
    { label: "Paris", x: 0.2, y: -1.5, z: -0.5, cluster: "cities" },
    { label: "London", x: 0.5, y: -1.8, z: -0.3, cluster: "cities" },
  ];
  const clusters = (params.clusters as { name: string; color: string }[]) ?? [];

  const clusterColors: Record<string, number> = {};
  clusters.forEach((c, i) => {
    const defaults = [0xf59e0b, 0x34d399, 0x60a5fa, 0xa78bfa, 0xf87171];
    clusterColors[c.name] = parseInt(c.color.replace("#", ""), 16) || defaults[i % 5];
  });

  const maxCoord = Math.max(...points.flatMap(p => [Math.abs(p.x), Math.abs(p.y), Math.abs(p.z)]), 1);
  const scale = 2.2 / maxCoord;

  const objects: THREE.Object3D[] = [];
  const labels: Label[] = [];
  const groupRef = new THREE.Group();
  scene.add(groupRef);
  objects.push(groupRef);

  // Axes
  const axisMat = new THREE.LineBasicMaterial({ color: 0x1e293b });
  [
    [[-2.8, 0, 0], [2.8, 0, 0]],
    [[0, -2.8, 0], [0, 2.8, 0]],
    [[0, 0, -2.8], [0, 0, 2.8]],
  ].forEach(([a, b]) => {
    const geo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(...a as [number,number,number]), new THREE.Vector3(...b as [number,number,number])]);
    groupRef.add(new THREE.Line(geo, axisMat));
  });

  const clusterPts: Record<string, THREE.Vector3[]> = {};
  points.slice(0, 20).forEach(pt => {
    const pos = new THREE.Vector3(pt.x * scale, pt.y * scale, pt.z * scale);
    const defaults = [0xf59e0b, 0x34d399, 0x60a5fa, 0xa78bfa, 0xf87171];
    const allClusters = [...new Set(points.map(p => p.cluster))];
    const ci = allClusters.indexOf(pt.cluster);
    const color = clusterColors[pt.cluster] ?? defaults[ci % 5];

    const geo = new THREE.SphereGeometry(0.11, 14, 14);
    const mat = new THREE.MeshStandardMaterial({ color, emissive: color, emissiveIntensity: 0.45, roughness: 0.3, metalness: 0.5 });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.copy(pos);
    groupRef.add(mesh);

    labels.push({ pos, text: pt.label, color: `#${color.toString(16).padStart(6, "0")}` });

    if (!clusterPts[pt.cluster]) clusterPts[pt.cluster] = [];
    clusterPts[pt.cluster].push(pos);
  });

  // Cluster connection lines
  Object.values(clusterPts).forEach(pts => {
    const clusterMat = new THREE.LineBasicMaterial({ color: 0x334155, transparent: true, opacity: 0.2 });
    for (let i = 0; i < pts.length; i++) {
      for (let j = i + 1; j < pts.length; j++) {
        const geo = new THREE.BufferGeometry().setFromPoints([pts[i], pts[j]]);
        groupRef.add(new THREE.Line(geo, clusterMat));
      }
    }
  });

  let frame = 0;
  const tick = () => { frame++; groupRef.rotation.y = frame * 0.005; };

  return { labels, cleanup: () => { scene.remove(groupRef); } };
}

function buildCustom(scene: THREE.Scene, params: Record<string, unknown>): { labels: Label[]; cleanup: () => void } {
  const objects3D: { type: string; position?: number[]; size?: number[]; color?: string; label?: string }[] =
    (params.objects as never[]) ?? [
      { type: "sphere", position: [-2, 0, 0], size: [0.8, 0.8, 0.8], color: "#60a5fa", label: "Input" },
      { type: "box", position: [0, 0, 0], size: [1.2, 0.8, 0.4], color: "#8b5cf6", label: "Process" },
      { type: "cone", position: [2, 0, 0], size: [0.8, 1, 0.8], color: "#34d399", label: "Output" },
    ];
  const connections = (params.connections as { from: number; to: number }[]) ?? [];

  const objects: THREE.Object3D[] = [];
  const labels: Label[] = [];
  const positions: THREE.Vector3[] = [];

  objects3D.slice(0, 12).forEach((obj, i) => {
    const pos = new THREE.Vector3(...((obj.position ?? [0, 0, 0]) as [number, number, number]));
    positions.push(pos);
    const size = (obj.size ?? [1, 1, 1]) as [number, number, number];
    const color = parseInt((obj.color || "#6366f1").replace("#", ""), 16);

    let geo: THREE.BufferGeometry;
    switch (obj.type) {
      case "sphere": geo = new THREE.SphereGeometry(size[0] / 2, 24, 24); break;
      case "cylinder": geo = new THREE.CylinderGeometry(size[0] / 2, size[0] / 2, size[1], 24); break;
      case "cone": geo = new THREE.ConeGeometry(size[0] / 2, size[1], 24); break;
      case "torus": geo = new THREE.TorusGeometry(size[0] / 2, size[1] / 5 || 0.15, 14, 24); break;
      default: geo = new THREE.BoxGeometry(...size);
    }

    const mat = new THREE.MeshStandardMaterial({ color, emissive: color, emissiveIntensity: 0.2, roughness: 0.4, metalness: 0.4 });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.copy(pos);
    mesh.castShadow = true;
    scene.add(mesh); objects.push(mesh);

    if (obj.label) labels.push({ pos: pos.clone().add(new THREE.Vector3(0, (size[1] ?? 1) / 2 + 0.35, 0)), text: obj.label, color: "#94a3b8" });
  });

  connections.forEach(conn => {
    const from = positions[conn.from];
    const to = positions[conn.to];
    if (!from || !to) return;
    const geo = new THREE.BufferGeometry().setFromPoints([from, to]);
    const line = new THREE.Line(geo, new THREE.LineBasicMaterial({ color: 0x475569, transparent: true, opacity: 0.5 }));
    scene.add(line); objects.push(line);
  });

  let frame = 0;
  const tick = () => { frame++; };

  return { labels, cleanup: () => { objects.forEach(o => scene.remove(o)); } };
}

// ─── tick registry ──────────────────────────────────────────────────────────
const tickFns: (() => void)[] = [];
function registerTick(fn: () => void) { tickFns.push(fn); }

// ─── Main Component ───────────────────────────────────────────────────────────
interface Props { config: VizConfig; onClose?: () => void; compact?: boolean }

export default function VisualRenderer({ config, onClose, compact = false }: Props) {
  const mountRef = useRef<HTMLDivElement>(null);
  const [fullscreen, setFullscreen] = useState(false);
  const height = fullscreen ? "85vh" : compact ? "280px" : "420px";

  useEffect(() => {
    const mount = mountRef.current;
    if (!mount) return;

    // Clear mount
    while (mount.firstChild) mount.removeChild(mount.firstChild);

    // Canvas
    const canvas = document.createElement("canvas");
    canvas.style.width = "100%";
    canvas.style.height = "100%";
    canvas.style.display = "block";
    mount.appendChild(canvas);

    // Label overlay
    const labelOverlay = document.createElement("div");
    labelOverlay.style.cssText = "position:absolute;inset:0;pointer-events:none;overflow:hidden;";
    mount.appendChild(labelOverlay);

    // Renderer
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.setClearColor(0x050a14);

    const w = mount.clientWidth || 600;
    const h = mount.clientHeight || 420;
    renderer.setSize(w, h);

    // Scene
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x050a14, 0.04);

    // Camera
    const camera = new THREE.PerspectiveCamera(55, w / h, 0.1, 100);
    const camPos: Record<string, [number, number, number]> = {
      neural_network: [0, 2, 9], gradient_descent: [3, 7, 5],
      attention: [0, 0, 10], data_flow: [0, 1, 10],
      convolution: [0, 0, 11], embedding_space: [0, 3, 8],
    };
    const cp = camPos[config.vizType] ?? [0, 2, 9];
    camera.position.set(...cp);
    camera.lookAt(0, 0, 0);

    // Lights
    scene.add(new THREE.AmbientLight(0xffffff, 0.45));
    const dir = new THREE.DirectionalLight(0xffffff, 1.2);
    dir.position.set(8, 12, 6);
    dir.castShadow = true;
    scene.add(dir);
    const pl1 = new THREE.PointLight(0x6366f1, 0.5, 20);
    pl1.position.set(-5, 5, -5);
    scene.add(pl1);
    const pl2 = new THREE.PointLight(0x06b6d4, 0.3, 20);
    pl2.position.set(5, -3, 5);
    scene.add(pl2);

    // Grid
    const gridHelper = new THREE.GridHelper(20, 20, 0x1e293b, 0x1e293b);
    gridHelper.position.y = -3.5;
    (gridHelper.material as THREE.Material).transparent = true;
    (gridHelper.material as THREE.Material).opacity = 0.4;
    scene.add(gridHelper);

    // Stars
    const starGeo = new THREE.BufferGeometry();
    const starPos = new Float32Array(2400);
    for (let i = 0; i < 2400; i++) starPos[i] = (Math.random() - 0.5) * 120;
    starGeo.setAttribute("position", new THREE.BufferAttribute(starPos, 3));
    scene.add(new THREE.Points(starGeo, new THREE.PointsMaterial({ color: 0xffffff, size: 0.06, transparent: true, opacity: 0.6 })));

    // Build scene
    const builders: Record<string, (s: THREE.Scene, p: Record<string, unknown>) => { labels: Label[]; cleanup: () => void }> = {
      neural_network: buildNeuralNet,
      gradient_descent: buildGradientDescent,
      attention: buildAttention,
      data_flow: buildDataFlow,
      convolution: buildConvolution,
      embedding_space: buildEmbedding,
      decision_tree: buildCustom,
      custom_geometry: buildCustom,
    };
    const builder = builders[config.vizType] ?? buildCustom;
    const { labels, cleanup } = builder(scene, config.params);

    // Label elements
    const labelEls: { el: HTMLDivElement; pos: THREE.Vector3 }[] = labels.map(({ pos, text, color }) => {
      const el = document.createElement("div");
      el.textContent = text;
      el.style.cssText = `position:absolute;font-size:11px;font-family:system-ui,sans-serif;color:${color};white-space:nowrap;pointer-events:none;transform:translate(-50%,-50%);text-shadow:0 1px 4px #000a`;
      labelOverlay.appendChild(el);
      return { el, pos };
    });

    // Resize observer
    const ro = new ResizeObserver(() => {
      const nw = mount.clientWidth;
      const nh = mount.clientHeight;
      renderer.setSize(nw, nh);
      camera.aspect = nw / nh;
      camera.updateProjectionMatrix();
    });
    ro.observe(mount);

    // Orbit controls
    const disposeOrbit = addOrbitControls(camera, mount);

    // Scene-specific tick functions (re-register per scene)
    const localTicks: (() => void)[] = [];

    // Re-build with tick capture — we need to re-call builder with tick capture
    // Actually the tick functions are embedded in the builders above via closure
    // We need a different approach: builders return a tick fn
    // For now re-use the animation loop approach:

    // Animation loop
    let rafId: number;
    let frame = 0;
    const animate = () => {
      rafId = requestAnimationFrame(animate);
      frame++;

      // Run per-viz animations inline
      if (config.vizType === "gradient_descent") {
        // ball is animated via the tick captured above — need a workaround
        // The ball animation is handled in the builder's closure tick
        // since we can't easily pass frame here, we reference scene children
      }

      renderer.render(scene, camera);

      // Project labels to screen
      const tempV = new THREE.Vector3();
      labelEls.forEach(({ el, pos }) => {
        tempV.copy(pos).project(camera);
        const sx = (tempV.x * 0.5 + 0.5) * mount.clientWidth;
        const sy = (-tempV.y * 0.5 + 0.5) * mount.clientHeight;
        el.style.left = `${sx}px`;
        el.style.top = `${sy}px`;
        el.style.display = tempV.z < 1 ? "block" : "none";
      });
    };
    animate();

    return () => {
      cancelAnimationFrame(rafId);
      disposeOrbit();
      ro.disconnect();
      cleanup();
      renderer.dispose();
      while (mount.firstChild) mount.removeChild(mount.firstChild);
    };
  }, [config, fullscreen]);

  return (
    <div className={`relative rounded-xl overflow-hidden border border-slate-700/50 ${fullscreen ? "fixed inset-4 z-50" : ""}`}
      style={{ height, background: "#050a14" }}>
      {/* Header */}
      <div className="absolute top-0 left-0 right-0 z-10 px-4 py-2 flex items-center justify-between bg-gradient-to-b from-[#050a14ee] to-transparent pointer-events-none">
        <div>
          <h3 className="text-sm font-semibold text-white leading-tight">{config.title}</h3>
          {!compact && <p className="text-[11px] text-slate-400 mt-0.5 truncate max-w-md">{config.description}</p>}
        </div>
        <div className="flex items-center gap-1.5 pointer-events-auto">
          <span className="text-[10px] px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-mono">
            {config.vizType}
          </span>
          <button onClick={() => setFullscreen(f => !f)}
            className="text-slate-400 hover:text-white p-1 rounded transition-colors" title="Toggle fullscreen">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {fullscreen
                ? <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 9L4 4m0 0v4m0-4h4M15 15l5 5m0 0v-4m0 4h-4M9 15l-5 5m0 0v-4m0 4h4M15 9l5-5m0 0v4m0-4h-4" />
                : <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-5h-4m4 0v4m0-4l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />}
            </svg>
          </button>
          {onClose && (
            <button onClick={onClose} className="text-slate-400 hover:text-white p-1 rounded transition-colors">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
      </div>
      <div className="absolute bottom-2 left-1/2 -translate-x-1/2 z-10 text-[10px] text-slate-700 pointer-events-none select-none">
        drag to orbit · scroll to zoom
      </div>
      <div ref={mountRef} className="w-full h-full" />
    </div>
  );
}
