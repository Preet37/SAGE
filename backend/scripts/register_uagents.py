"""Register the SAGE uAgent with Agentverse.

Usage:
    AGENTVERSE_API_KEY=<key> python scripts/register_uagents.py

The SAGE tutor uAgent must be running first (so it has booted and printed
its address). Run in another terminal:

    python -m app.agents.sage_uagent
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Allow running directly from backend/.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import get_settings


def main() -> None:
    settings = get_settings()
    address_file = Path("/tmp/sage_uagent_address")
    if not address_file.is_file():
        print("ERROR: /tmp/sage_uagent_address missing. Start the uAgent first.")
        sys.exit(1)
    address = address_file.read_text().strip()

    api_key = settings.agentverse_api_key
    if not api_key:
        print("ERROR: AGENTVERSE_API_KEY env var not set.")
        sys.exit(1)

    try:
        from agentverse_client import AgentverseClient
    except ImportError:
        print("ERROR: agentverse_client not installed. `pip install agentverse-client`")
        sys.exit(1)

    client = AgentverseClient(token=api_key, base_url=settings.fetchai_agentverse_url)
    print(f"Registering {settings.fetchai_agent_name} ({address}) on {settings.fetchai_agentverse_url}...")

    # The exact registration call differs across agentverse-client versions —
    # we try the most common shape and fall back to printing the manual URL.
    try:
        result = client.register_agent(  # type: ignore[attr-defined]
            address=address,
            name=settings.fetchai_agent_name,
            readme=(
                "SAGE: Socratic AI tutor. Implements the Chat Protocol so any ASI:One user "
                "can ask grounded questions about ML, agents, multimodal AI, LoRA, and more. "
                "Quiz requests are delegated to a sibling agent (multi-agent orchestration)."
            ),
        )
        print("OK:", result)
    except Exception as e:
        print("Programmatic registration failed (this is OK — register manually):", e)
        print()
        print("Manual registration:")
        print(f"  1. Visit {settings.fetchai_agentverse_url}/agents/register")
        print(f"  2. Provide agent address: {address}")
        print(f"  3. Set the protocol manifests automatically by clicking 'Sync from agent'.")


if __name__ == "__main__":
    main()
