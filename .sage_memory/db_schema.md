# SAGE Database Schema (SQLite via SQLAlchemy 2.x)

DB URL: `sqlite:///./sage.db` (configurable via `DATABASE_URL`).

## `users`
| col | type | notes |
|---|---|---|
| id | INTEGER PK | |
| email | VARCHAR(255) UNIQUE INDEX | login id |
| name | VARCHAR(120) | |
| hashed_password | VARCHAR(255) | bcrypt via passlib |
| created_at | DATETIME | utcnow default |

## `lessons`
| col | type | notes |
|---|---|---|
| id | INTEGER PK | |
| owner_id | FK→users.id INDEX | cascade delete |
| title | VARCHAR(200) | |
| subject | VARCHAR(80) | |
| objective | TEXT | learning goal |
| created_at | DATETIME | |

## `tutor_sessions`
| col | type | notes |
|---|---|---|
| id | INTEGER PK | |
| user_id | FK→users.id INDEX | |
| lesson_id | FK→lessons.id NULLABLE INDEX | |
| status | VARCHAR(32) | active/ended |
| transcript | TEXT | append-only log |
| started_at | DATETIME | |
| ended_at | DATETIME NULLABLE | |

## `concepts`
| col | type | notes |
|---|---|---|
| id | INTEGER PK | |
| session_id | FK→tutor_sessions.id INDEX | cascade |
| label | VARCHAR(200) | concept name |
| summary | TEXT | |
| mastery | FLOAT | 0.0–1.0 |
| parent_id | FK→concepts.id NULLABLE | tree edge |

## Relationships
```
User 1─* Lesson
User 1─* Session
Lesson 1─* Session
Session 1─* Concept (self-referential parent_id forms the map tree)
```

## Bootstrap
`init_db()` runs on FastAPI lifespan startup → `Base.metadata.create_all`.
