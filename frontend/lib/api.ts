const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

function websocketBase() {
  return BASE.replace(/^http:/, 'ws:').replace(/^https:/, 'wss:');
}

// ── Auth ──────────────────────────────────────────────────────────
export async function login(email: string, password: string) {
  const form = new URLSearchParams({ username: email, password });
  const res = await fetch(`${BASE}/auth/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: form.toString(),
  });
  if (!res.ok) throw new Error((await res.json()).detail || 'Login failed');
  return res.json();
}

export async function register(email: string, username: string, password: string, displayName?: string) {
  const res = await fetch(`${BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, username, password, display_name: displayName || username }),
  });
  if (!res.ok) throw new Error((await res.json()).detail || 'Registration failed');
  return res.json();
}

export async function getMe(token: string) {
  const res = await fetch(`${BASE}/auth/me`, { headers: { Authorization: `Bearer ${token}` } });
  if (!res.ok) throw new Error('Unauthorized');
  return res.json();
}

export async function updateTeachingMode(token: string, mode: string) {
  const res = await fetch(`${BASE}/auth/me/mode`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({ mode }),
  });
  if (!res.ok) throw new Error('Teaching mode update failed');
  return res.json();
}

// ── Courses ────────────────────────────────────────────────────────
export async function getCourses() {
  const res = await fetch(`${BASE}/courses/`);
  return res.json();
}

export async function getCourse(slug: string) {
  const res = await fetch(`${BASE}/courses/${slug}`);
  return res.json();
}

export async function getLessons(courseSlug: string) {
  const res = await fetch(`${BASE}/courses/${courseSlug}/lessons`);
  return res.json();
}

export async function getLesson(courseSlug: string, lessonSlug: string) {
  const res = await fetch(`${BASE}/courses/${courseSlug}/lessons/${lessonSlug}`);
  return res.json();
}

// ── Tutor ─────────────────────────────────────────────────────────
export async function createSession(token: string, lessonId: number, teachingMode = 'default') {
  const res = await fetch(`${BASE}/tutor/session`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({ lesson_id: lessonId, teaching_mode: teachingMode }),
  });
  return res.json();
}

export function streamChat(
  token: string,
  payload: {
    lesson_id: number;
    message: string;
    history: { role: string; content: string }[];
    session_id?: number;
    teaching_mode?: string;
    voice_enabled?: boolean;
    image_url?: string;
    extracted_text?: string;
  },
  onEvent: (event: string, data: unknown) => void,
): () => void {
  let aborted = false;
  const controller = new AbortController();

  (async () => {
    try {
      const res = await fetch(`${BASE}/tutor/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });
      if (!res.ok || !res.body) {
        let message = `Tutor request failed (${res.status})`;
        try {
          message = ((await res.json()).detail as string) || message;
        } catch {}
        onEvent('error', { message });
        return;
      }

      const reader = res.body!.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (!aborted) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        let currentEvent = '';
        for (const line of lines) {
          if (line.startsWith('event: ')) {
            currentEvent = line.slice(7).trim();
          } else if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              onEvent(currentEvent, data);
            } catch {}
          }
        }
      }
    } catch (e: unknown) {
      if ((e as Error).name !== 'AbortError') {
        onEvent('error', { message: String(e) });
      }
    }
  })();

  return () => {
    aborted = true;
    controller.abort();
  };
}

// ── Concept Map ────────────────────────────────────────────────────
export async function getConceptMap(token: string, courseId: number) {
  const res = await fetch(`${BASE}/concept-map/${courseId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}

export async function updateMastery(token: string, conceptId: number, score: number) {
  const res = await fetch(`${BASE}/concept-map/mastery`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({ concept_id: conceptId, score }),
  });
  return res.json();
}

// ── Network ────────────────────────────────────────────────────────
export async function requestPeerMatch(token: string, conceptId: number, lessonId: number) {
  const res = await fetch(`${BASE}/network/peer-match`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({ concept_id: conceptId, lesson_id: lessonId }),
  });
  return res.json();
}

export async function getNetworkStatus() {
  const res = await fetch(`${BASE}/network/status`);
  return res.json();
}

export function getPeerSocketUrl(roomToken: string) {
  return `${websocketBase()}/network/peer-session/${encodeURIComponent(roomToken)}`;
}

export async function getTopology(token: string, conceptId: number) {
  const res = await fetch(`${BASE}/network/topology/${conceptId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Could not fetch topology');
  return res.json() as Promise<{
    nodes: { id: string; label: string; kind: 'self' | 'tutor' | 'co_learner'; score?: number }[];
    edges: { source: string; target: string; weight: number }[];
    weights: Record<string, number>;
    routing_table: {
      user_id: number;
      display: string;
      score: number;
      components: { mastery_delta: number; recency: number; style_compat: number; novelty: number };
      role: string;
      last_seen_seconds: number;
    }[];
  }>;
}

// ── Replay ────────────────────────────────────────────────────────
export async function getSessions(token: string) {
  const res = await fetch(`${BASE}/replay/sessions`, { headers: { Authorization: `Bearer ${token}` } });
  return res.json();
}

export async function getSessionReplay(token: string, sessionId: number) {
  const res = await fetch(`${BASE}/replay/sessions/${sessionId}`, { headers: { Authorization: `Bearer ${token}` } });
  return res.json();
}

// ── Dashboard ────────────────────────────────────────────────────
export async function getDashboard(token: string) {
  const res = await fetch(`${BASE}/dashboard/overview`, { headers: { Authorization: `Bearer ${token}` } });
  return res.json();
}

export async function getCourseDashboard(token: string, courseId: number) {
  const res = await fetch(`${BASE}/dashboard/course/${courseId}`, { headers: { Authorization: `Bearer ${token}` } });
  return res.json();
}

// ── Accessibility ────────────────────────────────────────────────
export async function getAccessibilityProfiles() {
  const res = await fetch(`${BASE}/accessibility/profiles`);
  return res.json();
}

export async function getMyAccessibility(token: string) {
  const res = await fetch(`${BASE}/accessibility/me`, { headers: { Authorization: `Bearer ${token}` } });
  return res.json();
}

export async function saveAccessibility(
  token: string,
  profile: { disabilities: string[]; strengths: string[]; custom_note?: string }
) {
  const res = await fetch(`${BASE}/accessibility/me`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify(profile),
  });
  return res.json();
}

// ── Notes ────────────────────────────────────────────────────────
export async function reviseNotes(token: string, lessonId: number, content: string) {
  const res = await fetch(`${BASE}/notes/revise`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({ lesson_id: lessonId, content }),
  });
  return res.json();
}

export async function generateLessonPlan(token: string, lessonId: number) {
  const res = await fetch(`${BASE}/notes/generate-plan?lesson_id=${lessonId}`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}

// ── Visual Generation ─────────────────────────────────────────────
export async function generateVisual(
  token: string,
  concept: string,
  context: string,
  lessonId?: number
) {
  const res = await fetch(`${BASE}/visual/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ concept, context, lesson_id: lessonId }),
  });
  if (!res.ok) throw new Error('Visual generation failed');
  return res.json();
}

export async function generateVisualPlot(
  token: string,
  concept: string,
  context: string,
  lessonId?: number
) {
  const res = await fetch(`${BASE}/visual/plot`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ concept, context, lesson_id: lessonId }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error((err as { detail?: string }).detail || 'Plot generation failed');
  }
  return res.json() as Promise<{ html: string; title: string; concept: string; chars: number }>;
}

export async function generateVisualCode(
  token: string,
  concept: string,
  context: string,
  lessonId?: number
) {
  const res = await fetch(`${BASE}/visual/code`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ concept, context, lesson_id: lessonId }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error((err as { detail?: string }).detail || 'Code generation failed');
  }
  return res.json() as Promise<{ code: string; title: string; concept: string; lines: number }>;
}

// ── Media (Cloudinary) ────────────────────────────────────────────
export interface SignedUploadParams {
  cloud_name: string;
  api_key: string;
  timestamp: number;
  signature: string;
  folder: string;
  upload_url: string;
  public_id?: string;
  use_ocr: boolean;
}

export async function getSignedUpload(token: string, lessonId: number = 0): Promise<SignedUploadParams> {
  const res = await fetch(`${BASE}/media/upload-signed`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({ folder: 'sage_uploads', lesson_id: lessonId, use_ocr: true }),
  });
  if (!res.ok) throw new Error('Could not get upload signature');
  return res.json();
}

export async function ingestOcr(
  token: string,
  payload: { image_url: string; public_id?: string; lesson_id?: number; width?: number; height?: number; bytes?: number },
): Promise<{ extracted_text: string; image_url: string; mock: boolean; annotations: number }> {
  const res = await fetch(`${BASE}/media/ingest-ocr`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('OCR ingestion failed');
  return res.json();
}

export async function getDiagramLibrary(courseId: number, lessonId: number, conceptSlug: string) {
  const res = await fetch(`${BASE}/media/diagram/${courseId}/${lessonId}/${encodeURIComponent(conceptSlug)}`);
  if (!res.ok) return { items: [], mock: true };
  return res.json() as Promise<{ items: { label: string; url: string; thumb_url: string }[]; mock: boolean }>;
}

export async function getMaterials(token: string, lessonId: number) {
  const res = await fetch(`${BASE}/media/materials/${lessonId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) return { items: [], mock: true };
  return res.json() as Promise<{
    items: { public_id: string; url: string; thumb_url: string; width: number; height: number; bytes: number; format: string }[];
    mock: boolean;
  }>;
}
