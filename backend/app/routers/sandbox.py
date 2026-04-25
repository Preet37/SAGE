import asyncio
import sys
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
