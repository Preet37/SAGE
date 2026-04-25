#!/usr/bin/env python3
"""
Job: curate-wiki

Runs the wiki curator in fix mode to auto-repair source quality issues
(missing URLs, placeholder youtube_ids, casing inconsistencies).

If any fixes are applied, touches wiki/.needs-rebuild so the rebuild-wiki
job picks up the changes on its next cycle.

Exit codes:
  0 — success (fixes applied or nothing to fix)
  1 — curator script failed
"""

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
_WIKI_OUT = Path(os.environ.get("WIKI_OUTPUT_DIR", str(REPO_ROOT / "wiki" / "content"))).resolve().parent
SENTINEL = _WIKI_OUT / ".needs-rebuild"


def main() -> int:
    print("Starting curate-wiki job")

    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "wiki_curator.py"), "--fix"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )

    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    if result.returncode != 0:
        print("ERROR: wiki_curator.py failed", file=sys.stderr)
        return 1

    if "fixed=0" not in result.stdout and "fixed=" in result.stdout:
        SENTINEL.touch()
        print("Fixes applied — sentinel touched for rebuild")
    else:
        print("No fixes needed")

    return 0


if __name__ == "__main__":
    sys.exit(main())
