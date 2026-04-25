#!/usr/bin/env python3
"""
Job: rebuild-wiki

Triggered by: wiki/.needs-rebuild sentinel file

Steps:
  1. Run update_wiki.py (classify new topics via LLM if needed, regenerate content)
  2. Build the Quartz static site
  3. Delete the sentinel file on success

Exit codes:
  0 — success
  1 — failure (sentinel is NOT deleted, job will retry next cycle)
"""

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
_WIKI_OUT = Path(os.environ.get("WIKI_OUTPUT_DIR", str(REPO_ROOT / "wiki" / "content"))).resolve().parent
SENTINEL = _WIKI_OUT / ".needs-rebuild"


def main() -> int:
    print("Starting rebuild-wiki job")

    if not SENTINEL.exists():
        print("Sentinel not found — nothing to do")
        return 0

    # Run the full update pipeline (classify + transform + build)
    print("Running update_wiki.py...")
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "update_wiki.py")],
        cwd=REPO_ROOT,
    )

    if result.returncode != 0:
        print("ERROR: update_wiki.py failed — sentinel retained for retry", file=sys.stderr)
        return 1

    # Clear sentinel only after a clean run
    SENTINEL.unlink(missing_ok=True)
    print("Sentinel cleared — rebuild complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
