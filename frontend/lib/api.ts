const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

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

// ── Replay ────────────────────────────────────────────────────────
export async function getSessions(token: string) {
  const res = await fetch(`${BASE}/replay/sessions`, { headers: { Authorization: `Bearer ${token}` } });
  return res.json();
}

export async function getSessionReplay(token: string, sessionId: number) {
  const res = await fetch(`${BASE}/replay/sessions/${sessionId}`, { headers: { Authorization: `Bearer ${token}` } });
  return res.json();
}
