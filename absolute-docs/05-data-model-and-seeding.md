# 05 - Data Model and Seeding

## 1. Database Technology

- SQLAlchemy async ORM
- Default URL: `sqlite+aiosqlite:///./sage.db`
- Tables created automatically at backend startup (`create_tables()`)

## 2. Table Inventory

## 2.1 `users`

Purpose: auth identity + learning preferences.

Key fields:

- `id` (PK)
- `email` (unique, indexed)
- `username` (unique, indexed)
- `hashed_password`
- `display_name`
- `is_active`
- `preferred_language`
- `teaching_mode`
- `accessibility_profile` (JSON, nullable)
- `subscription_tier`
- `created_at`

## 2.2 `courses`

Purpose: top-level course metadata.

Key fields:

- `id` (PK)
- `slug` (unique, indexed)
- `title`
- `description`
- `level`
- `tags` (JSON list)
- `thumbnail_url` (nullable)
- `created_at`

## 2.3 `lessons`

Purpose: lesson payload and navigation metadata within a course.

Key fields:

- `id` (PK)
- `course_id` (FK -> `courses.id`)
- `slug` (indexed)
- `title`
- `order`
- `summary`
- `content_md` (full lesson markdown)
- `key_concepts` (JSON list)
- `prerequisites` (JSON list)
- `video_url` (nullable)
- `estimated_minutes`
- `created_at`

## 2.4 `lesson_chunks`

Purpose: retrieval units for semantic context.

Key fields:

- `id` (PK)
- `lesson_id` (FK -> `lessons.id`)
- `chunk_index`
- `text`
- `embedding` (JSON-encoded vector string, nullable)

## 2.5 `tutor_sessions`

Purpose: chat-session container for replay and analytics.

Key fields:

- `id` (PK)
- `user_id` (FK -> `users.id`)
- `lesson_id` (FK -> `lessons.id`)
- `teaching_mode`
- `started_at`
- `ended_at` (nullable)
- `agent_decisions` (JSON list)

## 2.6 `tutor_messages`

Purpose: per-turn transcript and verification telemetry.

Key fields:

- `id` (PK)
- `session_id` (FK -> `tutor_sessions.id`)
- `role` (`user|assistant`)
- `content`
- `retrieved_chunks` (JSON list)
- `verification_passed` (bool)
- `verification_flags` (JSON list)
- `agent_trace` (JSON dict)
- `created_at`

## 2.7 `concept_nodes`

Purpose: course concept graph nodes.

Key fields:

- `id` (PK)
- `course_id` (FK -> `courses.id`)
- `lesson_id` (FK -> `lessons.id`, nullable)
- `label` (indexed)
- `description`
- `node_type` (`concept|skill|prereq`)
- `x_pos`, `y_pos`

## 2.8 `concept_edges`

Purpose: directed edges in concept graph.

Key fields:

- `id` (PK)
- `source_id` (FK -> `concept_nodes.id`)
- `target_id` (FK -> `concept_nodes.id`)
- `edge_type` (`requires|extends|relates`)
- `weight`

## 2.9 `student_mastery`

Purpose: user-specific mastery tracking per concept.

Key fields:

- `id` (PK)
- `user_id` (FK -> `users.id`)
- `concept_id` (FK -> `concept_nodes.id`)
- `score` (`0.0..1.0`)
- `attempts`
- `last_seen`
- `is_mastered`

## 2.10 `peer_sessions`

Purpose: peer matching records and room token linkage.

Key fields:

- `id` (PK)
- `concept_id` (FK -> `concept_nodes.id`, nullable)
- `initiator_id` (FK -> `users.id`)
- `partner_id` (FK -> `users.id`, nullable)
- `room_token` (unique)
- `status` (`waiting|active|ended`)
- `created_at`

## 3. Relationship Summary

- One `course` has many `lessons`.
- One `lesson` has many `lesson_chunks`.
- One `user` has many `tutor_sessions`.
- One `tutor_session` has many `tutor_messages`.
- One `course` has many `concept_nodes` and concept edges among those nodes.
- One `user` has many `student_mastery` rows (one per concept touched).
- One peer match creates one `peer_sessions` row and optional partner linkage.

## 4. Seed Script Behavior (`backend/seed.py`)

## 4.1 Entry Sequence

1. Ensure tables exist (`create_tables()`).
2. Seed courses and lessons if not already present by slug checks.
3. Seed demo user if email missing.

## 4.2 Seeded User

- Email: `demo@sage.ai`
- Password: `demo1234`
- Username: `demo`
- Display name: `Demo Student`

## 4.3 Seeded Courses

Course 1: `ml-ai-foundations`

- 3 lessons:
  - `neural-networks-basics`
  - `attention-transformers`
  - `fine-tuning-lora`
- Lesson markdown is chunked into retrieval chunks.
- Concept graph seeded with 10 nodes and directed edges.

Course 2: `agentic-ai`

- 1 lesson:
  - `agent-fundamentals`

## 4.4 Idempotency Characteristics

- Course seeding checks by course slug.
- Demo user seeding checks by email.
- Re-running seed script is designed to avoid duplicating these entities.

## 5. Important Data Caveats

- `lesson_chunks.embedding` is not populated by seed script.
  - Retrieval still works, but semantic scoring defaults to non-informative ranking unless embeddings are later generated.
- No migration discipline is enforced yet (tables auto-created from models).
- SQLite is suitable for local/dev but not recommended for production multi-node use.

## 6. Adding New Content Safely

## 6.1 Add New Course and Lessons

1. Insert new `Course` and `Lesson` rows in seed path or admin flow.
2. Generate lesson chunks using `chunk_text(...)`.
3. Optionally populate embeddings for improved retrieval.
4. Add concept nodes and edges for dashboard/map continuity.
5. Validate `/courses`, `/learn`, `/concept-map`, and `/dashboard` flows.

## 6.2 Add New Concept Type

1. Extend node_type conventions in backend model and frontend color mapping.
2. Ensure `ConceptMap` component handles visual semantics.
3. Update docs and acceptance tests.

## 7. Migration Recommendation

For production-hardening:

1. Introduce strict migration workflow using Alembic (already in dependencies).
2. Disable implicit table creation in production boot path.
3. Add schema migration CI gate before deploy.
4. Move from SQLite to Postgres with async driver.

## 8. Data Validation Checklist

Before merge of schema/content changes:

1. Fresh DB build succeeds.
2. Seed script runs cleanly.
3. Login with seeded user works.
4. Tutor session persists user and assistant turns.
5. Dashboard reflects mastery/session stats.
6. Concept map returns valid node/edge arrays.
