import asyncio
import sys
import httpx
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/sandbox", tags=["sandbox"])

BLOCKED_IMPORTS = {"os", "subprocess", "sys", "shutil", "socket", "importlib", "ctypes", "multiprocessing"}
MAX_CODE_LEN = 8_000
TIMEOUT_SECS = 10


class SandboxRequest(BaseModel):
    language: str
    code: str


class SandboxResponse(BaseModel):
    stdout: str
    stderr: str
    error: str | None = None


@router.post("/run", response_model=SandboxResponse)
async def run_code(req: SandboxRequest):
    if req.language not in {"python", "py", "python3"}:
        return SandboxResponse(stdout="", stderr="", error="Only Python execution is supported via the backend.")

    code = req.code
    if len(code) > MAX_CODE_LEN:
        return SandboxResponse(stdout="", stderr="", error="Code too long (max 8 000 chars).")

    # Lightweight block of obviously dangerous imports
    for blocked in BLOCKED_IMPORTS:
        if f"import {blocked}" in code or f"from {blocked}" in code:
            return SandboxResponse(
                stdout="",
                stderr=f"Import '{blocked}' is not allowed in the sandbox.",
                error=f"Blocked import: {blocked}",
            )

    try:
        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            "-c",
            code,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                proc.communicate(), timeout=TIMEOUT_SECS
            )
        except asyncio.TimeoutError:
            try:
                proc.kill()
            except ProcessLookupError:
                pass
            return SandboxResponse(stdout="", stderr="", error=f"Execution timed out after {TIMEOUT_SECS}s.")

        return SandboxResponse(
            stdout=stdout_bytes.decode("utf-8", errors="replace").strip(),
            stderr=stderr_bytes.decode("utf-8", errors="replace").strip(),
        )
    except Exception as e:
        return SandboxResponse(stdout="", stderr="", error=str(e))


# ── Judge0 CE proxy — free public instance, no auth needed ───────────────────
JUDGE0_URL = "https://ce.judge0.com"

# Map language slug → Judge0 language_id (latest stable versions)
JUDGE0_LANG_IDS: dict[str, int] = {
    "python":     100,  # Python 3.12.5
    "py":         100,
    "python3":    100,
    "c":          103,  # C GCC 14
    "c++":        105,  # C++ GCC 14
    "cpp":        105,
    "java":        91,  # Java JDK 17
    "go":         106,  # Go 1.22
    "rust":       108,  # Rust 1.85
    "ruby":        72,  # Ruby 2.7
    "bash":        46,  # Bash 5
    "sh":          46,
    "typescript":  94,  # TS 5
    "swift":       83,
    "kotlin":     111,
    "csharp":      51,
    "c#":          51,
    "php":         98,
    "r":           99,
    "lua":         64,
    "javascript": 102,  # Node 22
    "js":         102,
}


class PistonFile(BaseModel):
    name: str
    content: str

class PistonRequest(BaseModel):
    language: str
    version: str = "*"
    files: list[PistonFile]
    stdin: str = ""
    args: list[str] = []


@router.post("/piston")
async def piston_proxy(req: PistonRequest):
    """Execute code — Python via subprocess (numpy/scipy available), others via Judge0 CE."""
    import base64

    lang = req.language.lower()
    source = req.files[0].content if req.files else ""

    # Python: use our own subprocess which has all scientific packages installed
    if lang in {"python", "py", "python3"}:
        if len(source) > MAX_CODE_LEN:
            return {"run": {"stdout": "", "stderr": "Code too long.", "output": ""}}
        try:
            proc = await asyncio.create_subprocess_exec(
                sys.executable, "-c", source,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            try:
                out, err = await asyncio.wait_for(proc.communicate(), timeout=TIMEOUT_SECS)
            except asyncio.TimeoutError:
                try: proc.kill()
                except ProcessLookupError: pass
                return {"run": {"stdout": "", "stderr": f"Timed out after {TIMEOUT_SECS}s", "output": ""}}
            stdout = out.decode("utf-8", errors="replace").strip()
            stderr = err.decode("utf-8", errors="replace").strip()
            return {"run": {"stdout": stdout, "stderr": stderr, "output": stdout or stderr}}
        except Exception as e:
            return {"run": {"stdout": "", "stderr": str(e), "output": ""}}

    lang_id = JUDGE0_LANG_IDS.get(lang)
    if lang_id is None:
        return {"run": {"stdout": "", "stderr": f"Unsupported language: {lang}", "output": ""}}

    # All other languages: Judge0 CE
    source = req.files[0].content if req.files else ""
    payload = {
        "source_code": base64.b64encode(source.encode()).decode(),
        "language_id": lang_id,
        "stdin": base64.b64encode(req.stdin.encode()).decode() if req.stdin else "",
        "base64_encoded": True,
        "wait": True,
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Submit + wait in one call
            r = await client.post(
                f"{JUDGE0_URL}/submissions?base64_encoded=true&wait=true",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            r.raise_for_status()
            data = r.json()

        def decode(s: str | None) -> str:
            if not s:
                return ""
            try:
                return base64.b64decode(s).decode("utf-8", errors="replace").strip()
            except Exception:
                return s

        stdout = decode(data.get("stdout"))
        stderr = decode(data.get("stderr")) or decode(data.get("compile_output"))
        return {"run": {"stdout": stdout, "stderr": stderr, "output": stdout or stderr}}

    except httpx.HTTPStatusError as e:
        return {"run": {"stdout": "", "stderr": f"Judge0 error: {e.response.status_code}", "output": ""}}
    except Exception as e:
        return {"run": {"stdout": "", "stderr": str(e), "output": ""}}
