# 04 - Frontend Technical Reference

## 1. Stack and Runtime

- Framework: Next.js 14 App Router
- Language: TypeScript + React 18
- State: Zustand (`auth` persisted + tutor session state)
- Styling: Tailwind CSS + global CSS
- Visualization: D3 (custom force simulation)
- Markdown/Math rendering: `react-markdown`, `remark-math`, `rehype-katex`

Default runtime URL assumptions:

- Frontend runs at `http://localhost:3000`
- Backend base URL uses `NEXT_PUBLIC_API_URL` (defaults to `http://localhost:8000`)

## 2. Route Map

- `/`
  - Marketing landing page + auth entry points
- `/login`
  - Login form (pre-filled demo credentials)
- `/register`
  - Registration form
- `/learn`
  - Course list and expandable lesson list
- `/learn/[courseId]/[lessonId]`
  - Main tutor workspace (3-column app shell)
- `/dashboard`
  - User analytics and cognition metrics summary

## 3. Shared Data Layer (`frontend/lib`)

## 3.1 API Client (`lib/api.ts`)

Covers all backend domains:

- Auth: `login`, `register`, `getMe`
- Courses: `getCourses`, `getCourse`, `getLessons`, `getLesson`
- Tutor: `createSession`, `streamChat`
- Concept map: `getConceptMap`, `updateMastery`
- Network: `requestPeerMatch`, `getNetworkStatus`
- Replay: `getSessions`, `getSessionReplay`
- Dashboard: `getDashboard`, `getCourseDashboard`
- Accessibility: `getAccessibilityProfiles`, `getMyAccessibility`, `saveAccessibility`
- Notes: `reviseNotes`, `generateLessonPlan`

## 3.2 Streaming Parser (`streamChat`)

Implementation detail:

- Uses `fetch` streaming reader.
- Splits incoming bytes by newline.
- Tracks current SSE event from `event:` lines.
- Parses `data:` JSON and dispatches callback `(event, data)`.
- Returns abort function to cancel stream.

## 3.3 Store (`lib/store.ts`)

`useAuthStore`:

- `token`, `user`, `setAuth`, `clearAuth`
- persisted under key `sage-auth`

`useTutorStore`:

- `messages`, `sessionId`, `teachingMode`, `isStreaming`, `agentEvents`
- append and verification update helpers
- stores only most recent 50 agent events

## 4. Main Lesson Workspace

Location: `app/learn/[courseId]/[lessonId]/page.tsx`

Layout composition:

- Left: `AgentPanel`
- Center tabs:
  - `TutorChat`
  - `ConceptMap`
  - `NetworkPanel`
  - `NotesPanel`
  - replay placeholder
- Right:
  - `VoiceAgent`
  - key concepts list
  - `ZeticAgent`
  - lesson summary

Topbar controls:

- Teaching mode selector
- Dashboard navigation
- Accessibility modal open button

## 5. Component Responsibilities

## 5.1 Tutor Components

`TutorChat`:

- Renders chat transcript from store
- Handles input box, enter-to-send behavior, starter chips
- Shows typing indicator while stream active

`MessageBubble`:

- User and assistant bubble variants
- Markdown + KaTeX rendering for assistant
- Parses optional `<quiz>` JSON block and renders interactive choices
- Displays verification pass/fail status and flags

## 5.2 Agent Panel

`AgentPanel`:

- Displays six logical agent slots and latest events by event type
- Uses `agentEvents` from store
- Current live backend emits only `content_retrieved` and `pedagogy_applied`, so other agent cards remain mostly idle/placeholder

## 5.3 Concept Map

`ConceptMap`:

- Draws force-directed graph in SVG
- Custom in-component simulation (repulsion + spring + centering)
- Clicking a node triggers mastery update (`+0.15`, capped at 1.0)
- Shows detail side panel for selected node

## 5.4 Network Panel

`NetworkPanel`:

- Polls `/network/status` every 10 seconds
- Allows peer-match requests per hot concept
- Displays waiting or matched token response
- Does not currently open peer WebSocket room for chat messages

## 5.5 Notes Panel

`NotesPanel`:

- Write/revise/analyze tab workflow
- Calls `/notes/revise` for AI feedback
- Calls `/notes/generate-plan` and triggers markdown download
- Saves local notes snapshot to `localStorage`

## 5.6 Accessibility Modal

`AccessibilityModal`:

- Fetches profile catalog and current user profile
- Allows selection of disability and learning-strength tags
- Persists settings via `/accessibility/me`
- Includes custom free-text note merged into backend prompt modifier

## 5.7 Voice Agent

`VoiceAgent`:

- Uses Web Speech API (`SpeechRecognition`/`webkitSpeechRecognition`)
- Captures transcript and sends to tutor callback
- Browser support gated; non-support displays fallback message

## 5.8 ZETIC Agent

`ZeticAgent`:

- Browser-only on-device LLM panel
- Attempts to load WebLLM from CDN and initialize Phi-3.5 model
- Requires WebGPU-capable environment
- Can inject on-device response back into tutor transcript

## 6. Frontend Request/Response Flow

Tutor send flow:

1. User submits prompt in `TutorChat`.
2. Page adds user message + blank assistant message to store.
3. `streamChat(...)` starts SSE request with history and session metadata.
4. Event handler updates store:
  - `token` -> append text to last assistant message
  - `agent_event` -> prepend to agentEvents list
  - `verification` -> annotate last assistant message
  - `done`/`error` -> stop streaming state

## 7. Frontend Extension Playbooks

## 7.1 Add New Panel Tab

1. Create component under `components/...`.
2. Add tab id + label in lesson page tab list.
3. Add conditional render branch in center panel area.
4. Wire API function in `lib/api.ts` if backend call needed.
5. Update this document and operations checklist.

## 7.2 Add New SSE Event Type

1. Update backend stream emitter event name.
2. Extend event handler in lesson page callback.
3. Add rendering logic in `AgentPanel` or relevant component.
4. Add fallback behavior for unknown event shapes.

## 7.3 Add Auth-Protected Page

1. Create route in `app/.../page.tsx`.
2. Guard with `useAuthStore().token` and redirect to `/login` if missing.
3. Include sign-out and navigation path.
4. Ensure API calls include bearer token.

## 8. Frontend Reliability Notes

- `streamChat` does not currently check `res.ok` before reading body; add explicit guard to surface HTTP failures cleanly.
- Lesson page currently creates an initial session with lesson id `0` before creating the real session.
- Concept map fetch in lesson page is hardcoded to course id `1` for demo behavior.

These are tracked as known issues in `06-operations-deployment-and-handoff.md`.
