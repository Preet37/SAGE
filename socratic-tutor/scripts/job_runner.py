#!/usr/bin/env python3
"""
SocraticTutor Background Job Runner

Reads scripts/jobs_config.yaml and runs enabled jobs when their trigger
conditions are met.

Usage:
    # Run as a daemon (polls every 60 seconds)
    python3 scripts/job_runner.py

    # Run all pending jobs once then exit (good for cron)
    python3 scripts/job_runner.py --once

    # Run a specific job immediately regardless of trigger state
    python3 scripts/job_runner.py --job rebuild-wiki

    # Change the polling interval
    python3 scripts/job_runner.py --interval 120

    # List configured jobs and their status
    python3 scripts/job_runner.py --status

Trigger types (defined in jobs_config.yaml):
    sentinel: <path>       Run when the named file exists. File is managed
                           by the job itself (job deletes it on success).
    interval_hours: <n>    Run every N hours since the last successful run.
    manual                 Only run when explicitly requested via --job.

State is persisted in scripts/.job_state.json (last_run timestamps, etc.).
"""

import argparse
import json
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
CONFIG_PATH = REPO_ROOT / "scripts" / "jobs_config.yaml"
STATE_PATH = REPO_ROOT / "scripts" / ".job_state.json"

# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

def load_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except Exception:
            pass
    return {}


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2))


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        print(f"ERROR: {CONFIG_PATH} not found.", file=sys.stderr)
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)

# ---------------------------------------------------------------------------
# Trigger evaluation
# ---------------------------------------------------------------------------

def is_triggered(job_name: str, job_cfg: dict, state: dict) -> tuple[bool, str]:
    """Returns (should_run, reason_string)."""
    trigger = job_cfg.get("trigger", {})

    # Sentinel file trigger
    if "sentinel" in trigger:
        sentinel_path = REPO_ROOT / trigger["sentinel"]
        if sentinel_path.exists():
            return True, f"sentinel found: {trigger['sentinel']}"
        return False, f"waiting for sentinel: {trigger['sentinel']}"

    # Interval trigger
    if "interval_hours" in trigger:
        hours = trigger["interval_hours"]
        last_run_iso = state.get(job_name, {}).get("last_success")
        if not last_run_iso:
            return True, "never run before"
        last_run = datetime.fromisoformat(last_run_iso)
        elapsed_hours = (datetime.now(timezone.utc) - last_run).total_seconds() / 3600
        if elapsed_hours >= hours:
            return True, f"interval elapsed ({elapsed_hours:.1f}h >= {hours}h)"
        remaining = hours - elapsed_hours
        return False, f"next run in {remaining:.1f}h"

    # Manual trigger — never auto-fires
    if trigger == "manual" or "manual" in trigger:
        return False, "manual trigger only"

    return False, "no trigger configured"

# ---------------------------------------------------------------------------
# Job execution
# ---------------------------------------------------------------------------

def run_job(job_name: str, job_cfg: dict, state: dict) -> bool:
    """Run a job script. Returns True on success."""
    script = REPO_ROOT / job_cfg["script"]
    timeout = job_cfg.get("timeout_minutes", 30) * 60

    if not script.exists():
        print(f"  [ERROR] Script not found: {script}", file=sys.stderr)
        return False

    started = datetime.now(timezone.utc)
    print(f"\n{'='*60}")
    print(f"  JOB: {job_name}")
    print(f"  Started: {started.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"  Script: {job_cfg['script']}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=REPO_ROOT,
            timeout=timeout,
        )
        success = result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"  [ERROR] Job timed out after {job_cfg.get('timeout_minutes', 30)} minutes",
              file=sys.stderr)
        success = False
    except Exception as e:
        print(f"  [ERROR] {e}", file=sys.stderr)
        success = False

    finished = datetime.now(timezone.utc)
    elapsed = (finished - started).total_seconds()
    status = "SUCCESS" if success else "FAILED"
    print(f"\n  {status} in {elapsed:.1f}s")

    # Update state
    if job_name not in state:
        state[job_name] = {}
    state[job_name]["last_run"] = started.isoformat()
    state[job_name]["last_status"] = status
    if success:
        state[job_name]["last_success"] = started.isoformat()
    save_state(state)

    return success

# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_status(config: dict, state: dict) -> None:
    """Print current status of all configured jobs."""
    jobs = config.get("jobs", {})
    print(f"\n{'Job':<25} {'Enabled':<8} {'Last Run':<25} {'Status':<10} {'Trigger'}")
    print("-" * 85)
    for name, cfg in jobs.items():
        enabled = "yes" if cfg.get("enabled", True) else "no"
        job_state = state.get(name, {})
        last_run = job_state.get("last_run", "never")[:19] if job_state.get("last_run") else "never"
        last_status = job_state.get("last_status", "-")
        trigger = cfg.get("trigger", {})
        if "sentinel" in trigger:
            trigger_str = f"sentinel: {trigger['sentinel']}"
            sentinel_path = REPO_ROOT / trigger["sentinel"]
            if sentinel_path.exists():
                trigger_str += " [PENDING]"
        elif "interval_hours" in trigger:
            trigger_str = f"every {trigger['interval_hours']}h"
        else:
            trigger_str = "manual"
        print(f"{name:<25} {enabled:<8} {last_run:<25} {last_status:<10} {trigger_str}")
    print()


def cmd_run_once(config: dict, state: dict, specific_job: str = None) -> None:
    """Check all jobs and run any that are triggered. Exit when done."""
    jobs = config.get("jobs", {})
    ran = 0
    failed = 0

    for name, cfg in jobs.items():
        if specific_job and name != specific_job:
            continue

        if not cfg.get("enabled", True) and not specific_job:
            continue

        if specific_job == name:
            # Force run regardless of trigger
            triggered, reason = True, "manually requested"
        else:
            triggered, reason = is_triggered(name, cfg, state)

        if triggered:
            print(f"\n[{name}] Triggering: {reason}")
            success = run_job(name, cfg, state)
            ran += 1
            if not success:
                failed += 1
        else:
            print(f"[{name}] Skipping: {reason}")

    if specific_job and ran == 0:
        print(f"ERROR: Job '{specific_job}' not found in jobs_config.yaml", file=sys.stderr)
        sys.exit(1)

    print(f"\nRan {ran} job(s), {failed} failed.")
    if failed:
        sys.exit(1)


def cmd_daemon(config: dict, state: dict, interval_seconds: int) -> None:
    """Poll continuously, running triggered jobs."""
    running = True

    def handle_signal(signum, frame):
        nonlocal running
        print("\nShutdown signal received — finishing current cycle...")
        running = False

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    print(f"Job runner started (polling every {interval_seconds}s)")
    print(f"Config: {CONFIG_PATH}")
    print(f"State:  {STATE_PATH}")
    print(f"Jobs:   {', '.join(config.get('jobs', {}).keys())}")
    print("Press Ctrl+C to stop.\n")

    while running:
        # Reload config each cycle so changes take effect without restart
        try:
            config = load_config()
        except Exception as e:
            print(f"WARNING: Failed to reload config: {e}")

        state = load_state()
        jobs = config.get("jobs", {})

        for name, cfg in jobs.items():
            if not running:
                break
            if not cfg.get("enabled", True):
                continue

            triggered, reason = is_triggered(name, cfg, state)
            if triggered:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] [{name}] {reason}")
                run_job(name, cfg, state)
                state = load_state()  # reload after job updates it

        if running:
            try:
                time.sleep(interval_seconds)
            except KeyboardInterrupt:
                break

    print("Job runner stopped.")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="SocraticTutor background job runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run all triggered jobs once then exit (good for cron)",
    )
    parser.add_argument(
        "--job",
        metavar="NAME",
        help="Run a specific job immediately regardless of trigger state",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        metavar="SECONDS",
        help="Polling interval in daemon mode (default: 60)",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="List all jobs and their current status",
    )
    args = parser.parse_args()

    config = load_config()
    state = load_state()

    if args.status:
        cmd_status(config, state)
    elif args.once or args.job:
        cmd_run_once(config, state, specific_job=args.job)
    else:
        cmd_daemon(config, state, interval_seconds=args.interval)


if __name__ == "__main__":
    main()
