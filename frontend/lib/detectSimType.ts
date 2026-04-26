/**
 * Keyword-based physics simulation detector.
 * Maps natural-language text to a simType string consumed by PhysicsScene.
 */

export type SimType =
  | "pendulum"
  | "newton_cradle"
  | "inverted_pendulum"
  | "orbit"
  | "spring_mass"
  | "projectile"
  | "rocket"
  | "wind_turbine"
  | "bridge"
  | "water_bottle"
  | "helicopter"
  | "mechanical_gears"
  | "bicycle"
  | "submarine"
  | "breadboard"
  | "f1_car"
  | "steam_engine"
  | "robot_arm";

interface SimEntry {
  simType: SimType;
  /** Lower-cased keyword fragments — ALL need not match, first hit wins */
  keywords: string[];
  /** Weight: higher = checked first */
  priority: number;
}

const SIM_ENTRIES: SimEntry[] = [
  // ── Compound / specific terms (highest priority, checked first) ──────────
  {
    simType: "newton_cradle",
    keywords: ["newton's cradle", "newtons cradle", "newton cradle", "elastic collision", "collision chain", "momentum transfer ball"],
    priority: 100,
  },
  {
    simType: "inverted_pendulum",
    keywords: ["inverted pendulum", "cart-pole", "cartpole", "pole balancing", "control system pendulum"],
    priority: 100,
  },

  // ── Single-word / short triggers that must beat broader matches ──────────
  {
    simType: "wind_turbine",
    keywords: ["wind turbine", "turbine", "wind energy", "turbine blade", "betz limit", "wind farm", "rotor blade", "windmill"],
    priority: 90,
  },
  {
    simType: "steam_engine",
    keywords: ["steam engine", "steam", "carnot", "piston", "flywheel", "boiler", "rankine"],
    priority: 90,
  },
  {
    simType: "f1_car",
    keywords: ["f1 car", "formula 1", "formula one", "f1", "racing car", "downforce", "drs", "formula car"],
    priority: 90,
  },
  {
    simType: "mechanical_gears",
    keywords: ["gear train", "gear ratio", "spur gear", "mechanical gear", "gear mesh", "gears", "gear", "gearbox", "transmission"],
    priority: 90,
  },
  {
    simType: "helicopter",
    keywords: ["helicopter", "chopper", "rotorcraft", "rotor lift", "collective pitch", "autorotation", "tail rotor"],
    priority: 85,
  },
  {
    simType: "submarine",
    keywords: ["submarine", "sub", "submersible", "ballast tank", "neutral buoyancy", "pressure hull"],
    priority: 85,
  },
  {
    simType: "bicycle",
    keywords: ["bicycle", "bike", "cycling", "pedal", "wheel gear", "cycling kinematics"],
    priority: 85,
  },
  {
    simType: "robot_arm",
    keywords: ["robot arm", "robotic arm", "robot", "robotic manipulator", "inverse kinematics", "end effector", "gripper"],
    priority: 85,
  },
  {
    simType: "rocket",
    keywords: ["rocket", "tsiolkovsky", "rocket propulsion", "exhaust velocity", "specific impulse", "spacecraft", "launch vehicle"],
    priority: 80,
  },
  {
    simType: "bridge",
    keywords: ["bridge", "suspension bridge", "beam bending", "structural load", "truss bridge", "truss"],
    priority: 80,
  },
  {
    simType: "breadboard",
    keywords: ["breadboard", "circuit board", "solderless", "electronics prototype", "circuit prototype"],
    priority: 80,
  },
  {
    simType: "water_bottle",
    keywords: ["water bottle", "bottle", "plastic bottle", "pressure vessel", "fluid pressure", "hoop stress"],
    priority: 80,
  },
  {
    simType: "orbit",
    keywords: ["orbit", "orbital", "kepler", "satellite", "planetary motion", "solar system", "planet", "moon orbit", "celestial"],
    priority: 75,
  },
  {
    simType: "projectile",
    keywords: ["projectile", "trajectory", "ballistic", "launch angle", "parabolic", "cannon", "thrown object"],
    priority: 70,
  },
  {
    simType: "spring_mass",
    keywords: ["spring mass", "mass-spring", "spring", "hooke", "hooke's law", "spring constant", "damped oscillation"],
    priority: 65,
  },
  // pendulum: very common single-word physics topic — priority above bridge/orbit/projectile
  // so that "pendulum" in any text always wins over broad metaphorical matches
  {
    simType: "pendulum",
    keywords: ["pendulum", "simple pendulum", "swinging bob", "simple harmonic motion"],
    priority: 82,
  },
];

// Sort by priority descending once at load time
SIM_ENTRIES.sort((a, b) => b.priority - a.priority);

/**
 * How much of the assistant reply to scan when userQuery / lessonTitle are empty.
 * Keeps false positives (e.g. "bridge" used metaphorically many paragraphs in) low
 * while still matching topic words in the opening paragraph.
 */
export const SIM_ASSISTANT_PREFIX_LEN = 360;

/**
 * Preferred order: what the user typed, then lesson topic, then the start of the reply.
 * Use this for MessageBubble so Explore (no lesson title) and streaming still work.
 */
export function detectSimFromSources(
  userQuery: string | undefined,
  lessonTitle: string | undefined,
  assistantContent: string,
): SimType | null {
  return (
    detectSimType((userQuery ?? "").trim()) ??
    detectSimType((lessonTitle ?? "").trim()) ??
    detectSimType(assistantContent.slice(0, SIM_ASSISTANT_PREFIX_LEN))
  );
}

/**
 * Returns the best matching simType for a block of text, or null if no match.
 * Uses the first keyword hit across all entries (sorted by priority).
 */
export function detectSimType(text: string): SimType | null {
  const lower = text.toLowerCase();
  for (const entry of SIM_ENTRIES) {
    for (const kw of entry.keywords) {
      if (lower.includes(kw)) {
        return entry.simType;
      }
    }
  }
  return null;
}

/** Camera / target config for each simType */
export const SCENE_CONFIGS: Record<SimType | "custom", { camera: [number, number, number]; target: [number, number, number]; fov: number }> = {
  wind_turbine:       { camera: [10, 8, 16],         target: [0, 6, 0],     fov: 35 },
  pendulum:           { camera: [0, 1, 8],            target: [0, 0, 0],     fov: 45 },
  newton_cradle:      { camera: [0, 1, 8],            target: [0, 0, 0],     fov: 45 },
  inverted_pendulum:  { camera: [2.2, 1.4, 4.2],      target: [0, 0.55, 0],  fov: 42 },
  projectile:         { camera: [0, 3, 12],           target: [0, 1, 0],     fov: 50 },
  rocket:             { camera: [0, 4, 14],           target: [0, 2, 0],     fov: 50 },
  spring_mass:        { camera: [4, 2.5, 8],          target: [0, 2, 0],     fov: 40 },
  orbit:              { camera: [0, 10, 10],          target: [0, 0, 0],     fov: 45 },
  robot_arm:          { camera: [2.2, 1.8, 2.8],      target: [0, 1.0, 0],   fov: 48 },
  bridge:             { camera: [0, 4, 14],           target: [0, 0, 0],     fov: 40 },
  water_bottle:       { camera: [3.5, 3, 4.5],        target: [0, 1.2, 0],   fov: 38 },
  helicopter:         { camera: [5, 3.5, 7],          target: [0, 1.2, 0],   fov: 44 },
  mechanical_gears:   { camera: [2.8, 2.2, 3.5],      target: [0, 0.65, 0],  fov: 42 },
  bicycle:            { camera: [3.5, 2.0, -0.5],     target: [0, 0.6, 0.5], fov: 44 },
  submarine:          { camera: [4.2, 2.2, 5.5],      target: [0, 0.5, 0],   fov: 42 },
  breadboard:         { camera: [2.4, 1.9, 2.8],      target: [0, 0.08, 0],  fov: 40 },
  f1_car:             { camera: [4.5, 2.8, 7],        target: [0, 0.5, 0],   fov: 42 },
  steam_engine:       { camera: [0, 3.5, 11],         target: [0, 1.2, 0],   fov: 48 },
  custom:             { camera: [1.8, 1.5, 2.5],      target: [0, 0.9, 0],   fov: 35 },
};
