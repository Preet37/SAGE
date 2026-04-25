/**
 * SAGE API client.
 *
 * Calls go through the Next.js rewrite to the FastAPI backend
 * (`/api/*` -> `http://localhost:8000/*`). All authed routes require a bearer
 * token; pass it explicitly so this module stays free of React/Next state.
 */

export const API_BASE = "/api";

// ----- Domain types -------------------------------------------------------

export type TeachingMode =
  | "default"
  | "eli5"
  | "analogy"
  | "code"
  | "deep_dive";

export const TEACHING_MODES: { id: TeachingMode; label: string; description: string }[] = [
  { id: "default", label: "Socratic", description: "Balanced guiding questions." },
  { id: "eli5", label: "ELI5", description: "Explain like I'm five." },
  { id: "analogy", label: "Analogy", description: "Lead with everyday analogies." },
  { id: "code", label: "Code", description: "Show small code snippets." },
  { id: "deep_dive", label: "Deep dive", description: "Go several levels deep." },
];

export interface User {
  id: number;
  email: string;
  name: string;
  teaching_mode: TeachingMode;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: "bearer";
}

export interface Lesson {
  id: number;
  owner_id: number;
  title: string;
  subject: string;
  objective: string;
  created_at: string;
}

export interface TutorSession {
  id: number;
  user_id: number;
  lesson_id: number | null;
  status: string;
  started_at: string;
  ended_at: string | null;
}

export interface Concept {
  id: number;
  session_id: number;
  label: string;
  summary: string;
  mastery: number;
  parent_id: number | null;
}

export interface AgentTrace {
  plan?: Record<string, unknown>;
  concept_map_delta?: { label: string; summary?: string; mastery?: number }[];
  assessment?: { question?: string | null; concept?: string; skip?: boolean };
  peers?: { peer_id: string; complements: string[]; score: number }[];
  progress_delta?: { bump?: number; by_concept?: Record<string, number> };
  teaching_mode?: TeachingMode;
}

export interface TutorMessageRow {
  id: number;
  session_id: number;
  role: "user" | "assistant";
  content: string;
  verification_passed: boolean;
  verification_score: number;
  verification_flags: string[];
  agent_trace: AgentTrace;
  retrieved_chunks: { id: string; score: number }[];
  created_at: string;
}

export interface ReplaySession {
  session_id: number;
  lesson_id: number | null;
  status: string;
  started_at: string;
  ended_at: string | null;
  transcript: string;
  concepts: Concept[];
  messages: TutorMessageRow[];
}

export interface Notes {
  session_id: number;
  markdown: string;
  summary: string;
  gaps: string[];
  suggestions: string[];
}

export interface NetworkStatus {
  waiting: number;
  active_rooms: number;
  hot_concepts: string[];
}

export interface PeerMatch {
  state: "waiting" | "matched";
  room_token: string;
  peer: string | null;
}

export interface Dashboard {
  user: User;
  catalog_size: number;
  my_courses: number;
  sessions: number;
  messages: number;
  concepts_total: number;
  concepts_mastered: number;
  grounded_rate: number;
  recent_sessions: TutorSession[];
}

export interface AccessibilityPrefs {
  dyslexia_font: boolean;
  high_contrast: boolean;
  reduce_motion: boolean;
  tts_voice: string;
}

// ----- SSE types ----------------------------------------------------------

export type AgentName =
  | "orchestrator"
  | "retriever"
  | "socratic"
  | "pedagogy"
  | "content"
  | "concept_map"
  | "assessment"
  | "peer_match"
  | "progress"
  | "verifier";

export interface AgentEvent {
  agent: AgentName;
  phase: "start" | "retrieved" | "generating" | "verifying" | "done";
  k?: number;
  scores?: number[];
  system_prompt_chars?: number;
  chars?: number;
  plan?: Record<string, unknown>;
  delta?: unknown;
  data?: unknown;
  peers?: unknown;
  trace_id?: string;
  session_id?: number;
}

export interface TokenEvent {
  agent: "socratic";
  text: string;
}

export interface ClaimVerdict {
  claim: string;
  score: number;
  grounded: boolean;
  source_index: number | null;
}

export interface VerificationEvent {
  score: number;
  grounded: boolean;
  claims: ClaimVerdict[];
}

export interface DoneEvent {
  session_id: number;
  ok: boolean;
  grounded: boolean;
}

export interface AudioEvent {
  mime: string;
  base64: string;
}

export interface SSEHandlers {
  onAgent?: (e: AgentEvent) => void;
  onToken?: (e: TokenEvent) => void;
  onVerification?: (e: VerificationEvent) => void;
  onAudio?: (e: AudioEvent) => void;
  onDone?: (e: DoneEvent) => void;
  onError?: (err: unknown) => void;
}

// ----- Internal helpers ---------------------------------------------------

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

async function request<T>(
  path: string,
  init: RequestInit = {},
  token?: string,
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(init.headers as Record<string, string> | undefined),
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, { ...init, headers });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new ApiError(res.status, text || res.statusText);
  }
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

// ----- Auth ---------------------------------------------------------------

export async function register(
  email: string,
  password: string,
  name: string,
): Promise<User> {
  return request<User>("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password, name }),
  });
}

export async function login(
  email: string,
  password: string,
): Promise<AuthResponse> {
  const form = new URLSearchParams();
  form.set("username", email);
  form.set("password", password);

  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: form.toString(),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new ApiError(res.status, text || "Invalid credentials");
  }
  return (await res.json()) as AuthResponse;
}

export const getMe = (token: string): Promise<User> =>
  request<User>("/auth/me", {}, token);

export const updateTeachingMode = (
  mode: TeachingMode,
  token: string,
): Promise<User> =>
  request<User>(
    "/auth/me/mode",
    { method: "PATCH", body: JSON.stringify({ mode }) },
    token,
  );

// ----- Courses / Lessons --------------------------------------------------

export const getCourses = (token: string): Promise<Lesson[]> =>
  request<Lesson[]>("/courses", {}, token);

export const getCourse = (id: number, token: string): Promise<Lesson> =>
  request<Lesson>(`/courses/${id}`, {}, token);

export const createCourse = (
  token: string,
  body: { title: string; subject?: string; objective?: string },
): Promise<Lesson> =>
  request<Lesson>("/courses", { method: "POST", body: JSON.stringify(body) }, token);

// ----- Sessions -----------------------------------------------------------

export const createSession = (
  lessonId: number | null,
  token: string,
): Promise<TutorSession> =>
  request<TutorSession>(
    "/tutor/sessions",
    { method: "POST", body: JSON.stringify({ lesson_id: lessonId }) },
    token,
  );

export const listSessions = (token: string): Promise<TutorSession[]> =>
  request<TutorSession[]>("/tutor/sessions", {}, token);

// ----- Concept map --------------------------------------------------------

export const getConceptMap = (
  sessionId: number,
  token: string,
): Promise<Concept[]> => request<Concept[]>(`/concept-map/${sessionId}`, {}, token);

export const bumpMastery = (
  sessionId: number,
  conceptId: number,
  delta: number,
  token: string,
): Promise<Concept> =>
  request<Concept>(
    `/concept-map/${sessionId}/concepts/${conceptId}/mastery`,
    { method: "PATCH", body: JSON.stringify({ delta }) },
    token,
  );

export const getNextConcepts = (
  sessionId: number,
  token: string,
): Promise<Concept[]> =>
  request<Concept[]>(`/concept-map/${sessionId}/next`, {}, token);

// ----- Replay -------------------------------------------------------------

export const listReplays = (token: string): Promise<TutorSession[]> =>
  request<TutorSession[]>("/replay", {}, token);

export const getReplay = (
  sessionId: number,
  token: string,
): Promise<ReplaySession> =>
  request<ReplaySession>(`/replay/${sessionId}`, {}, token);

// ----- Dashboard ----------------------------------------------------------

export const getDashboard = (token: string): Promise<Dashboard> =>
  request<Dashboard>("/dashboard", {}, token);

export interface CourseDashboard {
  course: Lesson;
  sessions: number;
  messages: number;
  concepts_total: number;
  concepts_mastered: number;
  weakest: Concept[];
  next_concepts: Concept[];
}

export const getCourseDashboard = (
  courseId: number,
  token: string,
): Promise<CourseDashboard> =>
  request<CourseDashboard>(`/dashboard/course/${courseId}`, {}, token);

// ----- Notes --------------------------------------------------------------

export const getNotes = (sessionId: number, token: string): Promise<Notes> =>
  request<Notes>(`/notes/${sessionId}`, {}, token);

export const reviseNotes = (
  sessionId: number,
  text: string,
  token: string,
): Promise<Notes> =>
  request<Notes>(
    `/notes/${sessionId}/revise`,
    { method: "POST", body: JSON.stringify({ text }) },
    token,
  );

export interface StudyPlan {
  session_id: number;
  filename: string;
  markdown: string;
}

export const generateStudyPlan = (
  sessionId: number,
  token: string,
): Promise<StudyPlan> =>
  request<StudyPlan>(
    `/notes/${sessionId}/study-plan`,
    { method: "POST" },
    token,
  );

// ----- Network ------------------------------------------------------------

export const networkStatus = (token: string): Promise<NetworkStatus> =>
  request<NetworkStatus>("/network/status", {}, token);

export const requestPeerMatch = (
  token: string,
  body: { concept?: string | null; lesson_id?: number | null },
): Promise<PeerMatch> =>
  request<PeerMatch>(
    "/network/peer-match",
    { method: "POST", body: JSON.stringify(body) },
    token,
  );

export function openPeerSocket(roomToken: string, token: string): WebSocket {
  // Browser WebSocket protocol must match the page protocol.
  const proto = typeof window !== "undefined" && window.location.protocol === "https:" ? "wss" : "ws";
  // Bypass Next.js rewrites; talk to backend directly.
  const apiOrigin = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
  const url =
    apiOrigin.replace(/^http/, proto) +
    `/network/peer-session/${encodeURIComponent(roomToken)}` +
    `?token=${encodeURIComponent(token)}`;
  return new WebSocket(url);
}

// ----- Accessibility ------------------------------------------------------

export const getAccessibility = (token: string): Promise<AccessibilityPrefs> =>
  request<AccessibilityPrefs>("/accessibility", {}, token);

export const saveAccessibility = (
  prefs: AccessibilityPrefs,
  token: string,
): Promise<AccessibilityPrefs> =>
  request<AccessibilityPrefs>(
    "/accessibility",
    { method: "PUT", body: JSON.stringify(prefs) },
    token,
  );

// ----- Tutor SSE stream ---------------------------------------------------

export interface StreamOptions {
  voice?: boolean;
}

export function streamTutorChat(
  sessionId: number,
  message: string,
  token: string,
  handlers: SSEHandlers,
  options: StreamOptions = {},
): () => void {
  const ctl = new AbortController();
  const voiceParam = options.voice ? "&voice=true" : "";
  const url =
    `${API_BASE}/tutor/chat?session_id=${sessionId}` +
    `&message=${encodeURIComponent(message)}${voiceParam}`;

  (async () => {
    try {
      const res = await fetch(url, {
        headers: { Authorization: `Bearer ${token}`, Accept: "text/event-stream" },
        signal: ctl.signal,
      });
      if (!res.ok || !res.body) {
        throw new ApiError(res.status, `SSE failed (${res.status})`);
      }

      const reader = res.body.getReader();
      const dec = new TextDecoder();
      let buf = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });

        let idx: number;
        while ((idx = indexOfDoubleNewline(buf)) !== -1) {
          const block = buf.slice(0, idx);
          buf = buf.slice(idx + 2);
          dispatchSSEBlock(block, handlers);
        }
      }
    } catch (err) {
      if (!ctl.signal.aborted) handlers.onError?.(err);
    }
  })();

  return () => ctl.abort();
}

function indexOfDoubleNewline(buf: string): number {
  // SSE separator is "\n\n" but tolerant of "\r\n\r\n".
  const lf = buf.indexOf("\n\n");
  const crlf = buf.indexOf("\r\n\r\n");
  if (lf === -1) return crlf === -1 ? -1 : crlf + 2;
  if (crlf === -1) return lf;
  return Math.min(lf, crlf + 2);
}

function dispatchSSEBlock(block: string, h: SSEHandlers): void {
  let event = "message";
  const dataLines: string[] = [];
  for (const raw of block.split("\n")) {
    const line = raw.replace(/\r$/, "");
    if (line.startsWith("event:")) event = line.slice(6).trim();
    else if (line.startsWith("data:")) dataLines.push(line.slice(5).trim());
  }
  if (!dataLines.length) return;
  let data: unknown;
  try {
    data = JSON.parse(dataLines.join("\n"));
  } catch {
    return;
  }

  switch (event) {
    case "agent_event":
      h.onAgent?.(data as AgentEvent);
      break;
    case "token":
      h.onToken?.(data as TokenEvent);
      break;
    case "verification":
      h.onVerification?.(data as VerificationEvent);
      break;
    case "audio":
      h.onAudio?.(data as AudioEvent);
      break;
    case "done":
      h.onDone?.(data as DoneEvent);
      break;
    case "error":
      h.onError?.(data);
      break;
  }
}
