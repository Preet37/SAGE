# Deploying SocraticTutor (DigitalOcean Droplet + Docker)

This guide runs the **Next.js frontend**, **FastAPI backend**, SQLite database, and **pedagogy wiki content** (including image files) on a single VM. The public **Quartz wiki** can stay on Vercel as a separate site; link to it from the app as you do today.

## What you need

- A domain (optional but recommended for HTTPS) with DNS you can edit
- API keys in `backend/.env` (`LLM_API_KEY`, `JWT_SECRET`, etc. — see `backend/.env.example`)
- Docker and Docker Compose on the server

## 1. Create a droplet

- **Ubuntu 24.04**, 2–4 GB RAM is enough for a demo ($12–24/mo on DigitalOcean)
- Add your SSH key
- Optionally enable **Automated backups** (~$2.40/mo on DO) for the droplet disk

## 2. Install Docker

On the droplet:

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker "$USER"
# log out and back in
```

## 3. Clone and configure

```bash
git clone <your-repo-url> SocraticTutor
cd SocraticTutor
cp backend/.env.example backend/.env
nano backend/.env   # LLM_API_KEY, JWT_SECRET, FRONTEND_URL, ...
```

Copy compose env if you use it:

```bash
cp .env.example .env
```

Set **`FRONTEND_URL`** in `backend/.env` to your public site origin (e.g. `https://learn.example.com`). CORS uses this value.

Set **`NEXT_PUBLIC_API_URL`** for the **Next.js build** to the URL the browser will use to reach the API:

- **Same host as the app (Caddy routes `/auth`, `/tutor`, … to the API):** use that origin, e.g. `https://learn.example.com`
- **API on a subdomain:** e.g. `https://api.example.com` (then point Caddy or another proxy accordingly)

Rebuild the frontend after changing `NEXT_PUBLIC_API_URL` (it is baked in at build time).

## 4. Caddy and TLS

```bash
cp Caddyfile.example Caddyfile
nano Caddyfile   # replace YOURDOMAIN with learn.example.com
```

Ensure DNS **A record** points to the droplet’s public IP. Caddy obtains Let’s Encrypt certificates automatically when ports **80** and **443** are open.

## 5. Build and run

From the repo root:

```bash
chmod +x scripts/setup-production.sh
./scripts/setup-production.sh
```

Or manually:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec backend uv run alembic upgrade head
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec backend uv run python scripts/batch_extract_images.py --rehydrate
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec backend uv run python seed.py
```

## 6. Firewall

- Allow **22** (SSH), **80**, **443**
- Optionally **deny** public access to **3000** and **8000** if you only use Caddy (use `ufw` or cloud firewall rules)

## 7. Updates

```bash
cd SocraticTutor
git pull
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec backend uv run alembic upgrade head
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec backend uv run python seed.py
```

## 8. Wiki enrichment in production

The `content/` volume is mounted **read-write** so the enrichment pipeline can download new sources into the wiki at runtime. These writes are **local to the server** — they are not committed back to git automatically.

To preserve enrichment data across deploys:
- Before running `git pull`, back up `content/` (or use a named Docker volume)
- After pulling, merge any new wiki content from git with the server's enriched data
- Alternatively, periodically commit enrichment data from the server back to git

## 9. Backups

- **`backend/tutor.db`** — copy off-box periodically or rely on droplet snapshots
- **`content/`** — versioned in git; large binary images may be gitignored and rehydrated with `batch_extract_images.py --rehydrate`. Runtime enrichment data lives only on the server until committed.

## 9. Wiki (Quartz) on Vercel

Keep deploying `wiki/` to Vercel as today. Update any in-app “Wiki” links to the Vercel URL if needed.

## Troubleshooting

- **502 from Caddy:** ensure `backend` and `frontend` containers are healthy (`docker compose ps`, `docker compose logs backend`).
- **CORS errors:** `FRONTEND_URL` in `backend/.env` must match the browser origin exactly (scheme + host + port).
- **Images 404:** confirm `./content` is mounted (`docker-compose.yml`) and run image rehydration on the server.

For migration workflows, see [backend/MIGRATIONS.md](backend/MIGRATIONS.md).
