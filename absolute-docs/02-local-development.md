# 02 - Local Development

## 1. Prerequisites

Required:

- macOS/Linux/WSL compatible shell
- Python 3.11+
- Node.js 20+
- npm 10+

Optional but recommended:

- `uv` for faster Python package installation

## 2. One-Command Bootstrap

From repository root:

```bash
bash scripts/setup.sh
```

What this script does:

1. Installs backend dependencies (`uv pip install -r requirements.txt` or `python3 -m pip ...` fallback).
2. Creates `backend/.env` from `backend/.env.example` if missing.
3. Seeds database with courses, lessons, concepts, and demo user.
4. Installs frontend dependencies (`npm install`).
5. Creates `frontend/.env.local` from example if missing.

## 3. Manual Setup (if not using script)

## 3.1 Backend

```bash
cd backend
cp .env.example .env
pip install -r requirements.txt
python seed.py
```

Start API:

```bash
uvicorn app.main:app --reload --port 8000
```

## 3.2 Frontend

```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

## 4. Environment Configuration

## 4.1 Backend `.env`

Core variables:

- `LLM_API_KEY`: primary API key for Anthropic/OpenAI/Groq path.
- `LLM_PROVIDER`: provider selector used at runtime.
  - Supported by code path: `anthropic`, `openai`, `groq`, `asi1`
- `AGENTVERSE_API_KEY`: key for Fetch.ai agentverse registration.
- `ASI1_API_KEY`: key for ASI1 provider in OpenAI-compatible path.
- `JWT_SECRET`: signing key for bearer tokens.
- `DATABASE_URL`: async SQLAlchemy database URL.
- `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`: optional TTS.
- `FRONTEND_URL`: CORS allow-list seed value.

Notes:

- `settings.yaml` also contains model/provider defaults. Final model selection is influenced by both env and yaml entries.
- `.env.example` currently comments `nvidia` as provider option, but code does not implement that provider branch.

## 4.2 Frontend `.env.local`

- `NEXT_PUBLIC_API_URL=http://localhost:8000`

If omitted, frontend defaults to `http://localhost:8000`.

## 5. Runbook: Start and Verify

## 5.1 Start Services

Terminal A:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Terminal B:

```bash
cd frontend
npm run dev
```

## 5.2 Verify Backend Health

- `GET http://localhost:8000/health` -> `{"status":"ok"}`
- `GET http://localhost:8000/` -> service metadata and feature list
- Swagger docs: `http://localhost:8000/docs`

## 5.3 Verify Frontend

- Open `http://localhost:3000`
- Login using demo credentials:
  - Email: `demo@sage.ai`
  - Password: `demo1234`
- Navigate to course > lesson and send a tutor message.

## 6. Local Developer Workflows

## 6.1 Dependency Management

Backend:

```bash
cd backend
pip install <package>
pip freeze > requirements.txt
```

Frontend:

```bash
cd frontend
npm install <package>
```

## 6.2 DB Reset (Destructive)

```bash
cd backend
rm -f sage.db
python seed.py
```

## 6.3 LLM Provider Switching

Update `backend/.env`:

```dotenv
LLM_PROVIDER=groq
LLM_API_KEY=<your-key>
```

Restart backend after changes.

## 7. Common Local Failures and Fixes

- `401 Unauthorized` on protected endpoints:
  - Ensure frontend has valid bearer token in Zustand store; re-login if needed.
- Tutor stream fails immediately:
  - Check provider keys and `LLM_PROVIDER` value.
- Empty or weak retrieval results:
  - Seed created chunks without embeddings; retrieval falls back to zero-score ordering.
- Voice output missing:
  - Requires valid ElevenLabs key and `voice_enabled=true` in chat payload.
- WebGPU/ZETIC unavailable:
  - Requires browser + device with WebGPU support.

## 8. Daily Engineering Checklist

Before opening a PR:

1. Re-run backend and frontend locally from clean restart.
2. Validate at least one auth, one tutor, one dashboard, and one concept map flow.
3. Ensure any new env vars are added to examples and docs.
4. If DB schema changed, update seed logic and schema docs.

Continue with `03-backend-technical-reference.md` for full endpoint and protocol details.
