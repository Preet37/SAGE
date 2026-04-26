export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function request<T>(
  path: string,
  options: RequestInit = {},
  token?: string | null,
  multipart = false,
): Promise<T> {
  const headers: Record<string, string> = multipart
    ? {}
    : { "Content-Type": "application/json", ...(options.headers as Record<string, string>) };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (!res.ok) {
    if (res.status === 401 && typeof window !== "undefined") {
      localStorage.removeItem("tutor_token");
      const returnTo = window.location.pathname;
      window.location.href = returnTo && returnTo !== "/" ? `/login?returnTo=${returnTo}` : "/login";
      return new Promise<T>(() => {});
    }
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Request failed");
  }
  return res.json();
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface UserResponse {
  id: string;
  email: string;
  username: string;
}

export interface LessonImageMeta {
  file: string;
  topic: string;
  source_page?: string;
  caption?: string;
  when_to_show?: string;
  concepts?: string[];
  description?: string;
}

export interface CourseOut {
  id: number;
  slug: string;
  title: string;
  description: string;
  level: string;
  tags: string[];
  thumbnail_url: string | null;
}

export interface LessonOut {
  id: string;
  slug: string;
  title: string;
  order: number;
  summary: string;
  key_concepts: string[];
  estimated_minutes: number;
  video_url: string | null;
}

export interface LessonResponse {
  id: string;
  title: string;
  slug: string;
  content: string;
  summary: string;
  concepts: string[];
  order_index: number;
  youtube_id: string | null;
  video_title: string | null;
  vimeo_url: string | null;
  module_id: string;
  image_metadata: LessonImageMeta[];
  sources_used: string[];
  reference_kb: string | null;
}

export interface ModuleResponse {
  id: string;
  title: string;
  order_index: number;
  lessons: LessonResponse[];
}

export interface LearningPathResponse {
  id: string;
  slug: string;
  title: string;
  description: string;
  level: string;
  modules: ModuleResponse[];
}

export interface LearningPathSummary {
  id: string;
  slug: string;
  title: string;
  description: string;
  level: string;
  visibility: string;
  is_mine: boolean;
}

export interface ShareEntry {
  user_id: string;
  email: string;
  username: string;
}

export interface ProgressResponse {
  lesson_id: string;
  completed: boolean;
  completed_at: string | null;
}

export interface ChatMessageResponse {
  id: string;
  role: string;
  content: string;
  created_at: string;
  message_meta?: string | null;
}

export interface TutorSessionResponse {
  id: string;
  lesson_id: string;
  created_at: string;
  updated_at: string;
}

export interface ExplorationSessionResponse {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface ExplorationMessageResponse {
  id: string;
  role: string;
  content: string;
  created_at: string;
}

export interface QuizTopicResponse {
  lesson_id: string;
  lesson_title: string;
  module_title: string;
  path_title: string;
  level: string;
  concepts: string[];
}

export interface QuizOptionResponse {
  id: string;
  text: string;
}

export interface QuizQuestionResponse {
  id: string;
  order_index: number;
  difficulty: string;
  question_type: string;
  question_text: string;
  options: QuizOptionResponse[];
  hint: string;
}

export interface QuizSessionResponse {
  id: string;
  topic: string;
  difficulty: string;
  total_questions: number;
  correct_count: number;
  completed: boolean;
  created_at: string;
  questions: QuizQuestionResponse[];
}

export interface QuizSessionSummary {
  id: string;
  topic: string;
  difficulty: string;
  total_questions: number;
  correct_count: number;
  completed: boolean;
  created_at: string;
}

export interface QuizAnswerResponse {
  is_correct: boolean;
  correct_option_id: string;
  explanation: string;
  correct_count: number;
  completed: boolean;
}

export interface ConceptMisconception {
  text: string;
  is_correct: boolean;
}

export interface KeyEquation {
  label: string;
  latex: string;
  description: string;
}

export interface ConceptPaper {
  title: string;
  authors: string;
  year: string;
  description: string;
}

export interface ConceptVideo {
  title: string;
  channel: string;
  search_query: string;
}

export interface ConceptPageResponse {
  id: string;
  topic: string;
  level: string;
  simple_definition: string;
  why_it_matters: string;
  detailed_explanation: string;
  analogy: string;
  real_world_example: string;
  misconceptions: ConceptMisconception[];
  key_takeaways: string[];
  related_concepts: string[];
  further_reading: string[];
  prerequisites: string[];
  key_equations: KeyEquation[];
  papers: ConceptPaper[];
  videos: ConceptVideo[];
  lesson_id: string | null;
  created_at: string;
}

export interface ConceptSuggestion {
  label: string;
  lesson_id: string | null;
}

export interface SkillDimensionResponse {
  name: string;
  level: string;
  score: number;
  max_score: number;
  description: string;
}

export interface AssessmentResponse {
  id: string;
  overall_level: string;
  overall_summary: string;
  skill_dimensions: SkillDimensionResponse[];
  strengths: string[];
  gaps: string[];
  recommended_module_id: string | null;
  recommendation_text: string;
  background_text: string;
  created_at: string;
}

export interface AssessmentSummaryResponse {
  id: string;
  overall_level: string;
  created_at: string;
}

export interface CurriculumLessonRef {
  id: string;
  title: string;
  summary: string;
  course_title: string;
  path_slug: string;
  completed: boolean;
}

export interface CurriculumPhaseResponse {
  order: number;
  title: string;
  level: string;
  estimated_hours: number;
  description: string;
  lessons: CurriculumLessonRef[];
  milestone_title: string;
  milestone_skills: string[];
}

export interface CurriculumGapResponse {
  topic: string;
  description: string;
  explore_query: string;
}

export interface CurriculumResponse {
  id: string;
  title: string;
  level_range: string;
  estimated_hours: number;
  personalization_note: string;
  phases: CurriculumPhaseResponse[];
  gaps: CurriculumGapResponse[];
  learning_goals: string;
  created_at: string;
}

export interface CurriculumSummaryResponse {
  id: string;
  title: string;
  level_range: string;
  created_at: string;
}

export interface ProjectSummaryResponse {
  id: string;
  slug: string;
  title: string;
  subtitle: string;
  course_slug: string;
  status: string;
  difficulty: string;
  hero_emoji: string;
  concepts: string[];
  order_index: number;
}

export interface ProjectDetailResponse {
  id: string;
  slug: string;
  title: string;
  subtitle: string;
  course_slug: string;
  status: string;
  difficulty: string;
  hero_emoji: string;
  vision: string;
  learning_outcomes: string[];
  concepts: string[];
  architecture_mermaid: string;
  demo_url: string;
  demo_embed: boolean;
  repo_url: string;
  setup_instructions: string;
  challenges: string[];
  related_lesson_slugs: string[];
  order_index: number;
}

export interface DraftSummaryResponse {
  id: string;
  title: string;
  slug: string;
  source_type: string;
  phase: string;
  stage: string;
  created_at: string;
  updated_at: string;
}

export interface DraftDetailResponse {
  id: string;
  title: string;
  slug: string;
  source_type: string;
  phase: string;
  stage: string;
  data: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export const api = {
  auth: {
    register: (email: string, username: string, password: string) =>
      request<TokenResponse>("/auth/register", {
        method: "POST",
        body: JSON.stringify({ email, username, password }),
      }),
    login: (email: string, password: string) =>
      request<TokenResponse>("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      }),
  },
  courses: {
    list: (token: string) =>
      request<CourseOut[]>("/courses/", {}, token),
    lessons: (slug: string, token: string) =>
      request<LessonOut[]>(`/courses/${slug}/lessons`, {}, token),
    lesson: (slug: string, lessonSlug: string, token: string) =>
      request<LessonOut>(`/courses/${slug}/lessons/${lessonSlug}`, {}, token),
  },
  learningPaths: {
    list: (token: string) =>
      request<LearningPathSummary[]>("/learning-paths", {}, token),
    get: (slug: string, token: string) =>
      request<LearningPathResponse>(`/learning-paths/${slug}`, {}, token),
    getLesson: (lessonId: string, token: string) =>
      request<LessonResponse>(`/learning-paths/lessons/${lessonId}`, {}, token),
    share: (slug: string, email: string, token: string) =>
      request<{ status: string }>(`/learning-paths/${slug}/share`, {
        method: "POST",
        body: JSON.stringify({ email }),
      }, token),
    unshare: (slug: string, userId: string, token: string) =>
      request<{ status: string }>(`/learning-paths/${slug}/share/${userId}`, {
        method: "DELETE",
      }, token),
    getShares: (slug: string, token: string) =>
      request<ShareEntry[]>(`/learning-paths/${slug}/shares`, {}, token),
    getShareLink: (slug: string, token: string) =>
      request<{ share_token: string; slug: string }>(`/learning-paths/${slug}/share-link`, {
        method: "POST",
      }, token),
    joinViaLink: (shareToken: string, token: string) =>
      request<{ status: string; slug: string }>(`/learning-paths/join/${shareToken}`, {
        method: "POST",
      }, token),
  },
  progress: {
    getAll: (token: string) =>
      request<ProgressResponse[]>("/progress", {}, token),
    markComplete: (lessonId: string, token: string) =>
      request<ProgressResponse>("/progress", {
        method: "POST",
        body: JSON.stringify({ lesson_id: lessonId }),
      }, token),
    getChatHistory: (lessonId: string, token: string) =>
      request<ChatMessageResponse[]>(`/progress/chat-history/${lessonId}`, {}, token),
    getSessions: (lessonId: string, token: string) =>
      request<TutorSessionResponse[]>(`/progress/sessions/${lessonId}`, {}, token),
    getSessionHistory: (lessonId: string, sessionId: string, token: string) =>
      request<ChatMessageResponse[]>(`/progress/sessions/${lessonId}/${sessionId}/history`, {}, token),
    deleteSession: (lessonId: string, sessionId: string, token: string) =>
      request<{ ok: boolean }>(`/progress/sessions/${lessonId}/${sessionId}`, { method: "DELETE" }, token),
  },
  explore: {
    getSessions: (token: string) =>
      request<ExplorationSessionResponse[]>("/explore/sessions", {}, token),
    getSessionHistory: (sessionId: string, token: string) =>
      request<ExplorationMessageResponse[]>(`/explore/sessions/${sessionId}/history`, {}, token),
    deleteSession: (sessionId: string, token: string) =>
      request<{ ok: boolean }>(`/explore/sessions/${sessionId}`, { method: "DELETE" }, token),
  },
  quiz: {
    getTopics: (token: string) =>
      request<QuizTopicResponse[]>("/quiz/topics", {}, token),
    generate: (lessonId: string, difficulty: string, numQuestions: number, token: string) =>
      request<QuizSessionResponse>("/quiz/generate", {
        method: "POST",
        body: JSON.stringify({ lesson_id: lessonId, difficulty, num_questions: numQuestions }),
      }, token),
    getSessions: (token: string) =>
      request<QuizSessionSummary[]>("/quiz/sessions", {}, token),
    getSession: (sessionId: string, token: string) =>
      request<QuizSessionResponse>(`/quiz/sessions/${sessionId}`, {}, token),
    submitAnswer: (sessionId: string, questionId: string, selectedOptionId: string, token: string) =>
      request<QuizAnswerResponse>(`/quiz/sessions/${sessionId}/answer`, {
        method: "POST",
        body: JSON.stringify({ question_id: questionId, selected_option_id: selectedOptionId }),
      }, token),
    deleteSession: (sessionId: string, token: string) =>
      request<{ ok: boolean }>(`/quiz/sessions/${sessionId}`, { method: "DELETE" }, token),
  },
  concepts: {
    search: (topic: string, token: string) =>
      request<ConceptPageResponse>("/concepts/search", {
        method: "POST",
        body: JSON.stringify({ topic }),
      }, token),
    getSuggestions: (token: string) =>
      request<ConceptSuggestion[]>("/concepts/suggestions", {}, token),
  },
  assessment: {
    assess: (backgroundText: string, token: string) =>
      request<AssessmentResponse>("/assess", {
        method: "POST",
        body: JSON.stringify({ background_text: backgroundText }),
      }, token),
    getLatest: (token: string) =>
      request<AssessmentResponse>("/assess/latest", {}, token),
    getHistory: (token: string) =>
      request<AssessmentSummaryResponse[]>("/assess/history", {}, token),
  },
  curriculum: {
    generate: (learningGoals: string, token: string) =>
      request<CurriculumResponse>("/curriculum/generate", {
        method: "POST",
        body: JSON.stringify({ learning_goals: learningGoals }),
      }, token),
    getLatest: (token: string) =>
      request<CurriculumResponse>("/curriculum/latest", {}, token),
    getHistory: (token: string) =>
      request<CurriculumSummaryResponse[]>("/curriculum/history", {}, token),
  },
  projects: {
    list: (token: string) =>
      request<ProjectSummaryResponse[]>("/projects", {}, token),
    get: (slug: string, token: string) =>
      request<ProjectDetailResponse>(`/projects/${slug}`, {}, token),
  },
  courseCreator: {
    createDraft: (title: string, sourceText: string, token: string) =>
      request<DraftDetailResponse>("/course-creator/drafts", {
        method: "POST",
        body: JSON.stringify({ title, source_type: "prompt", source_text: sourceText }),
      }, token),
    listDrafts: (token: string) =>
      request<DraftSummaryResponse[]>("/course-creator/drafts", {}, token),
    getDraft: (draftId: string, token: string) =>
      request<DraftDetailResponse>(`/course-creator/drafts/${draftId}`, {}, token),
    deleteDraft: (draftId: string, token: string) =>
      request<{ ok: boolean }>(`/course-creator/drafts/${draftId}`, { method: "DELETE" }, token),
    patchDraft: (draftId: string, patch: Record<string, unknown>, token: string) =>
      request<{ ok: boolean }>(`/course-creator/drafts/${draftId}/patch`, {
        method: "PATCH",
        body: JSON.stringify(patch),
      }, token),
    applyChatAction: (draftId: string, action: Record<string, unknown>, token: string) =>
      request<{ status: string; summary: string }>(`/course-creator/drafts/${draftId}/apply-chat-action`, {
        method: "POST",
        body: JSON.stringify(action),
      }, token),
    getWikiCoverage: (draftId: string, token: string) =>
      request<Record<string, unknown>>(`/course-creator/drafts/${draftId}/wiki-coverage`, {}, token),
    getQualityGate: (draftId: string, token: string) =>
      request<Record<string, unknown>>(`/course-creator/drafts/${draftId}/quality-gate`, {}, token),
    getFinalDashboard: (draftId: string, token: string) =>
      request<Record<string, unknown>>(`/course-creator/drafts/${draftId}/final-dashboard`, {}, token),
    publish: (draftId: string, token: string) =>
      request<Record<string, unknown>>(`/course-creator/drafts/${draftId}/publish`, {
        method: "POST",
      }, token),
    exportDraft: (draftId: string, token: string) =>
      request<Record<string, unknown>>(`/course-creator/drafts/${draftId}/export`, {}, token),
    promoteSource: (draftId: string, topicSlug: string, url: string, title: string, token: string) =>
      request<{ success: boolean; saved_path: string; word_count: number }>(
        `/course-creator/drafts/${draftId}/promote-source`,
        {
          method: "POST",
          body: JSON.stringify({ topic_slug: topicSlug, url, title }),
        },
        token,
      ),
  },
  network: {
    heartbeat: (
      payload: {
        lesson_id?: string | null;
        status?: string;
        note?: string;
        looking_for_pair?: boolean;
        display_name?: string;
      },
      token: string,
    ) =>
      request<PresenceResponse>("/network/presence", {
        method: "POST",
        body: JSON.stringify(payload),
      }, token),
    leave: (token: string) =>
      request<{ ok: boolean }>("/network/presence", { method: "DELETE" }, token),
    routeResources: (
      params: { query?: string; lessonId?: string; sources?: string },
      token: string,
    ) => {
      const qs = new URLSearchParams();
      if (params.query) qs.set("query", params.query);
      if (params.lessonId) qs.set("lesson_id", params.lessonId);
      if (params.sources) qs.set("sources", params.sources);
      return request<ResourceRouterResponseT>(
        `/network/resources?${qs.toString()}`, {}, token,
      );
    },
  },
  media: {
    sign: (
      payload: {
        folder?: string;
        public_id?: string;
        upload_preset?: string;
        tags?: string[];
        eager?: string;
      },
      token: string,
    ) =>
      request<MediaSignResponse>("/media/sign", {
        method: "POST",
        body: JSON.stringify(payload),
      }, token),
    recordAsset: (asset: MediaAssetCreate, token: string) =>
      request<MediaAssetResponse>("/media/assets", {
        method: "POST",
        body: JSON.stringify(asset),
      }, token),
    listAssets: (token: string, lessonId?: string, kind?: string) => {
      const qs = new URLSearchParams();
      if (lessonId) qs.set("lesson_id", lessonId);
      if (kind) qs.set("kind", kind);
      const tail = qs.toString() ? `?${qs.toString()}` : "";
      return request<MediaAssetResponse[]>(`/media/assets${tail}`, {}, token);
    },
    deleteAsset: (id: string, token: string) =>
      request<{ ok: boolean }>(`/media/assets/${id}`, { method: "DELETE" }, token),
    transform: (
      payload: { public_id: string; transformations: string[]; resource_type?: string },
      token: string,
    ) =>
      request<{ url: string }>("/media/transform", {
        method: "POST",
        body: JSON.stringify(payload),
      }, token),
    sketchExplain: (
      payload: { asset_id: string; note?: string; lesson_id?: string },
      token: string,
    ) =>
      request<SketchExplainResponseT>("/media/sketch-explain", {
        method: "POST",
        body: JSON.stringify(payload),
      }, token),
  },
  cognition: {
    listMemory: (token: string, lessonId?: string, limit = 50) => {
      const qs = new URLSearchParams();
      if (lessonId) qs.set("lesson_id", lessonId);
      qs.set("limit", String(limit));
      return request<{ items: MemoryItemResponse[]; enabled: boolean }>(
        `/cognition/memory?${qs.toString()}`, {}, token,
      );
    },
    recall: (query: string, token: string, opts?: { lessonId?: string; k?: number; sameLessonOnly?: boolean }) =>
      request<{ hits: MemoryHitResponse[] }>("/cognition/memory/recall", {
        method: "POST",
        body: JSON.stringify({
          query,
          k: opts?.k ?? 5,
          lesson_id: opts?.lessonId,
          same_lesson_only: !!opts?.sameLessonOnly,
        }),
      }, token),
    deleteMemory: (id: string, token: string) =>
      request<{ ok: boolean }>(`/cognition/memory/${id}`, { method: "DELETE" }, token),
    clearMemory: (token: string, lessonId?: string) => {
      const qs = lessonId ? `?lesson_id=${encodeURIComponent(lessonId)}` : "";
      return request<{ ok: boolean; deleted: number }>(`/cognition/memory${qs}`, { method: "DELETE" }, token);
    },
    verify: (claim: string, lessonId: string, token: string) =>
      request<{
        score: number; label: string;
        grounded_claims: string[]; unsupported_claims: string[]; rationale: string;
      }>("/cognition/verify", {
        method: "POST",
        body: JSON.stringify({ claim, lesson_id: lessonId }),
      }, token),
  },
  visual: {
    generatePlot: (topic: string, context: string, token: string) =>
      request<{ html?: string; topic?: string; error?: string }>("/visual/plot", {
        method: "POST",
        body: JSON.stringify({ topic, context }),
      }, token),
    generate3D: (topic: string, context: string, token: string) =>
      request<{ html: string; topic: string; error?: string }>("/visual/3d", {
        method: "POST",
        body: JSON.stringify({ topic, context }),
      }, token),
    generateGenesis: (topic: string, context: string, token: string) =>
      request<{ video_b64?: string; script?: string; topic: string; error?: string; fallback?: boolean }>("/visual/genesis", {
        method: "POST",
        body: JSON.stringify({ topic, context }),
      }, token),
  },
  documents: {
    upload: (file: File, token: string) => {
      const form = new FormData();
      form.append("file", file);
      return request<DocumentOut>("/documents/upload", {
        method: "POST",
        body: form,
      }, token, true);
    },
    list: (token: string) =>
      request<DocumentOut[]>("/documents", {}, token),
    get: (id: string, token: string) =>
      request<DocumentDetail>(`/documents/${id}`, {}, token),
    delete: (id: string, token: string) =>
      request<{ ok: boolean; deleted: number }>(`/documents/${id}`, { method: "DELETE" }, token),
  },
};

export interface DocumentOut {
  id: string;
  filename: string;
  mime: string;
  size_bytes: number;
  chunk_count: number;
  preview: string;
  created_at: string;
  cld_public_id: string;
  cld_secure_url: string;
  doc_type: string;
  subject: string;
  summary: string;
  key_topics: string[];
  is_image: boolean;
  thumbnail_url: string | null;
  enhanced_url: string | null;
  nobg_url: string | null;
}

export interface DocumentDetail extends DocumentOut {
  chunks: string[];
}

export interface MemoryItemResponse {
  id: string;
  role: string;
  content: string;
  lesson_id: string | null;
  session_id: string | null;
  importance: number;
  created_at: string;
}

export interface PeerOut {
  user_id: string;
  display_name: string;
  lesson_id: string | null;
  status: string;
  note: string;
  looking_for_pair: boolean;
  last_seen: string;
}

export interface PresenceResponse {
  me: PeerOut;
  peers_on_lesson: PeerOut[];
  other_peers_online: PeerOut[];
}

export interface ResourceItem {
  source: string;
  title: string;
  url: string;
  snippet?: string;
  authors?: string[];
  published?: string;
  stars?: number;
  language?: string;
  channel?: string;
}

export interface MediaSignResponse {
  cloud_name: string;
  api_key: string;
  timestamp: number;
  folder: string;
  upload_preset: string;
  signature: string;
  tags: string;
  eager: string | null;
}

export interface MediaAssetCreate {
  public_id: string;
  secure_url: string;
  resource_type?: string;
  format?: string;
  width?: number;
  height?: number;
  bytes?: number;
  folder?: string;
  tags?: string[];
  lesson_id?: string;
  kind?: string;
  asset_meta?: Record<string, unknown>;
}

export interface MediaAssetResponse {
  id: string;
  public_id: string;
  secure_url: string;
  resource_type: string;
  format: string;
  width: number;
  height: number;
  bytes: number;
  folder: string;
  kind: string;
  lesson_id: string | null;
  asset_meta: Record<string, unknown> | null;
  created_at: string;
}

export interface SketchExplainResponseT {
  explanation: string;
  detected_concepts: string[];
  suggested_prompt: string;
}

export interface ResourceRouterResponseT {
  query: string;
  items: ResourceItem[];
  by_source: Record<string, number>;
  elapsed_ms: number;
}

export interface MemoryHitResponse {
  id: string;
  role: string;
  content: string;
  lesson_id: string | null;
  session_id: string | null;
  score: number;
  created_at: string | null;
}

// ── Diagnostic ──────────────────────────────────────────────────────────────

export interface DiagnosticQuestion {
  id: string;
  text: string;
  options: string[];
  subject: string;
}

export interface DiagnosticResult {
  knowledge_profile: string;
  gaps: string[];
  recommended_start: string;
  grade_estimate: string;
  encouragement: string;
}

export function getDiagnosticQuestions(): Promise<DiagnosticQuestion[]> {
  return request<DiagnosticQuestion[]>("/diagnostic/questions");
}

export function submitDiagnostic(
  answers: Record<string, string>,
  name?: string,
): Promise<DiagnosticResult> {
  return request<DiagnosticResult>("/diagnostic/submit", {
    method: "POST",
    body: JSON.stringify({ answers, name }),
  });
}

// ── Broadcast ────────────────────────────────────────────────────────────────

export interface BroadcastRoom {
  code: string;
  join_url: string;
  qr_url: string;
}

export function createBroadcastRoom(teacherId: string, lessonId?: number | string): Promise<BroadcastRoom> {
  return request<BroadcastRoom>("/broadcast/room", {
    method: "POST",
    body: JSON.stringify({ teacher_id: teacherId, lesson_id: lessonId }),
  });
}

export function pushBroadcastContent(
  token: string,
  code: string,
  payload: { lesson_id: number | string; title: string; content_md: string; key_concepts: string[] },
): Promise<{ students_reached: number }> {
  return request<{ students_reached: number }>(`/broadcast/room/${code}/push`, {
    method: "POST",
    body: JSON.stringify(payload),
  }, token);
}

export function getBroadcastStreamUrl(code: string): string {
  const base = (API_URL || "http://localhost:8000").replace(/^http/, "ws");
  return `${base}/broadcast/room/${code}/stream`;
}

export function getBroadcastQrUrl(code: string): string {
  return `${API_URL}/broadcast/room/${code}/qr`;
}

// ── PDF Export ───────────────────────────────────────────────────────────────

export async function exportSessionPDF(
  messages: { role: string; content: string }[],
  lessonTitle?: string,
  courseTitle?: string,
  token?: string,
): Promise<Blob> {
  const res = await fetch(`${API_URL}/export/pdf`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify({ messages, lesson_title: lessonTitle, course_title: courseTitle }),
  });
  if (!res.ok) throw new Error("PDF export failed");
  return res.blob();
}

// ── SMS status ───────────────────────────────────────────────────────────────

export function getSmsStatus(): Promise<{ connected: boolean; active_sessions: number; mock_mode: boolean }> {
  return request("/sms/status");
}

// ── Course / Lesson helpers (for broadcast page) ─────────────────────────────

export interface CourseStub { id: number; slug: string; title: string; }
export interface LessonStub { id: number; slug: string; title: string; content_md: string; key_concepts: string[]; }

export function getCourses(token?: string): Promise<CourseStub[]> {
  return request<CourseStub[]>("/learning-paths", {}, token);
}

export function getLessons(courseSlug: string, token?: string): Promise<LessonStub[]> {
  return request<LessonStub[]>(`/learning-paths/${courseSlug}/lessons`, {}, token);
}

// ── Diagnostic (user-scoped submit) ──────────────────────────────────────────

export function submitDiagnosticForUser(
  token: string,
  answers: Record<string, string>,
  name?: string,
): Promise<DiagnosticResult> {
  return request<DiagnosticResult>("/diagnostic/submit", {
    method: "POST",
    body: JSON.stringify({ answers, name }),
  }, token);
}
