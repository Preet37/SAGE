# SAGE API Contracts (v0.1)

> Shared between backend + frontend swarms. Source of truth for fetch shapes.

## Auth (`/auth`)
- `POST /auth/register` — body `{email, name?, password}` → `UserOut` (201)
- `POST /auth/login` — `application/x-www-form-urlencoded` `{username=email, password}` → `{access_token, token_type:"bearer"}`
- `GET /auth/me` — Bearer → `UserOut`

All routes below require `Authorization: Bearer <token>` unless noted.

## Courses (`/courses`)
- `GET /courses` → `LessonOut[]`
- `POST /courses` → `LessonOut` (201). Body: `{title, subject?, objective?}`
- `GET /courses/{id}` → `LessonOut`
- `DELETE /courses/{id}` → 204

## Tutor (`/tutor`)
- `POST /tutor/sessions` body `{lesson_id?}` → `SessionOut` (201)
- `GET /tutor/sessions` → `SessionOut[]`
- `POST /tutor/turn` body `{session_id, message}` → `{agent, reply}`

## Concept Map (`/concept-map`)
- `GET /concept-map/{session_id}` → `ConceptOut[]`

## Network (`/network`)
- `GET /network/peers` → `{peers: []}`

## Replay (`/replay`)
- `GET /replay/{session_id}` → `{session_id, transcript, started_at}`

## Accessibility (`/accessibility`)
- `GET /accessibility` → `A11yPrefs`
- `PUT /accessibility` body `A11yPrefs` → `A11yPrefs`
- `A11yPrefs = {dyslexia_font, high_contrast, reduce_motion, tts_voice}`

## Dashboard (`/dashboard`)
- `GET /dashboard` → `{user, courses, sessions}`

## Notes (`/notes`)
- `GET /notes/{session_id}` → `{session_id, markdown}`

## Health
- `GET /health` → `{status:"ok"}`

## Schema shapes
```ts
type UserOut       = { id:number; email:string; name:string; created_at:string }
type LessonOut     = { id:number; owner_id:number; title:string; subject:string; objective:string; created_at:string }
type SessionOut    = { id:number; user_id:number; lesson_id:number|null; status:string; started_at:string; ended_at:string|null }
type ConceptOut    = { id:number; session_id:number; label:string; summary:string; mastery:number; parent_id:number|null }
type Token         = { access_token:string; token_type:"bearer" }
```
