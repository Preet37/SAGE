# Contributing to SocraticTutor

Thanks for your interest in contributing! This guide covers everything you need
to get started.

## Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (fast Python package manager)
- Node.js 20+
- An API key for an OpenAI-compatible LLM provider ([OpenAI](https://platform.openai.com/api-keys), [NVIDIA](https://build.nvidia.com/), etc.)

### Development Setup

1. **Clone the repo:**
   ```bash
   git clone https://github.com/pratik008/SocraticTutor.git
   cd SocraticTutor
   ```

2. **Backend:**
   ```bash
   cd backend
   uv sync
   cp .env.example .env   # then edit with your LLM_API_KEY and JWT_SECRET
   uv run python seed.py
   uv run uvicorn app.main:app --reload --port 8000
   ```

3. **Frontend:**
   ```bash
   cd frontend
   cp .env.local.example .env.local
   npm install
   npm run dev
   ```

The app runs at [http://localhost:3000](http://localhost:3000) with API docs at
[http://localhost:8000/docs](http://localhost:8000/docs).

## How to Contribute

### Reporting Bugs

Open a GitHub issue with:
- Steps to reproduce
- Expected vs. actual behavior
- Browser/OS/Python/Node versions

### Suggesting Features

Open a GitHub issue describing the feature, the problem it solves, and any
alternatives you've considered.

### Submitting Code

1. Fork the repo and create a branch from `main`:
   ```bash
   git checkout -b feature/my-change
   ```
2. Make your changes. Follow the existing code style.
3. Test your changes locally (backend + frontend).
4. Commit with a clear message describing *what* and *why*.
5. Open a pull request against `main`.

### Pull Request Guidelines

- Keep PRs focused — one logical change per PR.
- Update documentation if your change affects user-facing behavior.
- Add or update tests when possible.
- Ensure `npm run lint` passes for frontend changes.
- Describe what you changed and why in the PR description.

## Adding Course Content

SocraticTutor's content lives in the `content/` directory. Each course is a folder
containing a `course.json` manifest and optional enrichment reference knowledge. See
`content/README.md` for the format specification.

To create a course interactively, use the **Course Creator** wizard
(`course-creator/`). To add content manually, create a `course.json` and run
`python seed.py` from `backend/`.

## Code Style

- **Python:** Follow PEP 8. Use type hints.
- **TypeScript/React:** Follow the existing patterns. The project uses Next.js
  App Router with shadcn/ui components.
- **Commits:** Write clear, concise commit messages. Prefer present tense
  ("Add feature" not "Added feature").

## License

By contributing, you agree that your contributions will be licensed under the
[Apache License 2.0](LICENSE).
