# SAGE Hardening Report — 2026-04-25

## Tools used
- **ecc-agentshield@1.5.0** — config-level secret/permission scan
- **Manual targeted pentest via FastAPI TestClient** — covers the surfaces
  Shannon would target (JWT auth, SSE, CORS, cross-tenant). Shannon
  (`@keygraph/shannon`) requires Docker workers + credential setup;
  not run in this session.

## Findings & fixes (all patched)

| # | Severity | Finding | Fix |
|---|---|---|---|
| 1 | **CRITICAL** | `ASI1_API_KEY` and Agentverse JWT auto-recorded into `.claude/settings.local.json` from a prior `curl` invocation | File rewritten with parameterized allow rules; recommend immediate key rotation |
| 2 | **HIGH** | `passlib[bcrypt]` incompatible with `bcrypt>=4.0` → every `/auth/register` returns 500 | Replaced with direct `bcrypt` lib, SHA-256 pre-hash to dodge 72-byte limit |
| 3 | **HIGH** | No password length validation → bcrypt could silently truncate at 72 bytes (auth confusion) | Schema-level `min_length=8, max_length=1024` + length guard in `hash_password` |
| 4 | MEDIUM | JWT had no `iss`/`iat`, no claim-presence enforcement → tokens missing `sub`/`iss` could pass | Added `iss="sage"`, required claims `["exp","iat","sub","iss"]` via `jose.decode(... options=...)` |
| 5 | MEDIUM | No rate limit on `/auth/login` → credential stuffing | Added slowapi: `5/min` register, `10/min` login |
| 6 | MEDIUM | `init_db()` only on lifespan startup → schema absent under non-lifespan deploys | Eager idempotent `init_db()` at module import |
| 7 | LOW | No 422 on bad UserCreate (raised ValueError → 500) | Pydantic `Field(min_length=8, max_length=1024)` |

## Pentest results (post-patch)

| Test | Expected | Actual |
|---|---|---|
| 9× protected GETs without token | 401 | ✅ all 401 |
| Register 7-char password | 422 | ✅ 422 `string_too_short` |
| Register duplicate email | 400 | ✅ 400 |
| `alg=none` token | 401 | ✅ |
| Tampered signature | 401 | ✅ |
| Expired `exp` | 401 | ✅ |
| Missing `sub`/`iss` claims | 401 | ✅ |
| Wrong `iss` value | 401 | ✅ |
| Cross-tenant read of another user's course | 404 | ✅ |
| Cross-tenant DELETE | 404 | ✅ |
| Unauth `/tutor/chat` | 401 | ✅ |
| `/tutor/chat` against another user's session | 404 | ✅ |
| CORS preflight from `evil.example` | no ACAO | ✅ 400, no ACAO header |
| CORS preflight from `localhost:3000` | ACAO set | ✅ |
| 200-byte password roundtrip | ok | ✅ register 201, login 200 |
| 201-byte password mismatch | 401 (proves no truncation) | ✅ |
| 1100-byte password | 422 | ✅ |

## AgentShield report
Project root scan — **0 findings in SAGE code**. All flags are in
`hackathon_tools/` (third-party submodules, not deployed).

## Test suite
`pytest tests/ -q` → **29 passed** post-hardening.

## Remaining recommendations (not blockers for hackathon submission)
- Run a real Shannon pentest in CI when Docker is available.
- Add CSRF protection if SSE is ever moved off Bearer auth (e.g. to cookies).
- Move `JWT_SECRET` out of `Settings()` default and require it via env.
- Add account-lockout after N failed logins (per-account, not just per-IP).
