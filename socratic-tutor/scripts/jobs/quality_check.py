#!/usr/bin/env python3
"""Background job: Production quality monitoring with alerting.

Runs periodically to analyze recent sessions and alert on quality degradation.

Thresholds:
- Dead-end rate > 20% → ALERT
- No-tool rate > 50% → WARNING
- Avg response length < 200 chars → WARNING
- Zero sessions in period → INFO (no data)

Outputs:
- Log file: logs/quality_check.log
- Alert file: logs/quality_alerts.json (when thresholds breached)
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add backend to path
REPO_ROOT = Path(__file__).parent.parent.parent
BACKEND_DIR = REPO_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from scripts.eval_sessions import analyze_all_sessions, AggregateAnalysis

LOG_DIR = BACKEND_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "quality_check.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


# Alert thresholds
THRESHOLDS = {
    "dead_end_rate_alert": 0.20,        # >20% dead-ends → ALERT
    "dead_end_rate_warning": 0.10,      # >10% dead-ends → WARNING
    "no_tool_rate_warning": 0.50,       # >50% sessions with no tools → WARNING
    "min_avg_response_length": 200,     # <200 chars avg → WARNING
    "min_sessions_for_analysis": 5,     # Need at least 5 sessions to analyze
}


def check_quality(days: int = 1) -> dict:
    """Run quality checks and return results with alert status."""
    logger.info(f"Running quality check for last {days} day(s)")
    
    agg = analyze_all_sessions(days=days)
    
    alerts: list[dict] = []
    warnings: list[dict] = []
    
    if agg.total_sessions == 0:
        logger.info("No sessions found in the analysis period")
        return {
            "status": "no_data",
            "timestamp": datetime.utcnow().isoformat(),
            "days_analyzed": days,
            "alerts": [],
            "warnings": [],
            "metrics": agg.as_dict(),
        }
    
    if agg.total_sessions < THRESHOLDS["min_sessions_for_analysis"]:
        logger.info(f"Only {agg.total_sessions} sessions — not enough for reliable analysis")
        return {
            "status": "insufficient_data",
            "timestamp": datetime.utcnow().isoformat(),
            "days_analyzed": days,
            "session_count": agg.total_sessions,
            "alerts": [],
            "warnings": [],
            "metrics": agg.as_dict(),
        }
    
    # Check dead-end rate
    if agg.dead_end_rate > THRESHOLDS["dead_end_rate_alert"]:
        alert = {
            "type": "dead_end_rate",
            "severity": "ALERT",
            "message": f"Dead-end rate is {agg.dead_end_rate:.1%} (threshold: {THRESHOLDS['dead_end_rate_alert']:.0%})",
            "value": agg.dead_end_rate,
            "threshold": THRESHOLDS["dead_end_rate_alert"],
            "sample_sessions": [s.session_id for s in agg.dead_end_sessions[:5]],
        }
        alerts.append(alert)
        logger.error(f"ALERT: {alert['message']}")
    elif agg.dead_end_rate > THRESHOLDS["dead_end_rate_warning"]:
        warning = {
            "type": "dead_end_rate",
            "severity": "WARNING",
            "message": f"Dead-end rate is {agg.dead_end_rate:.1%} (threshold: {THRESHOLDS['dead_end_rate_warning']:.0%})",
            "value": agg.dead_end_rate,
            "threshold": THRESHOLDS["dead_end_rate_warning"],
        }
        warnings.append(warning)
        logger.warning(f"WARNING: {warning['message']}")
    
    # Check no-tool rate
    if agg.no_tool_rate > THRESHOLDS["no_tool_rate_warning"]:
        warning = {
            "type": "no_tool_rate",
            "severity": "WARNING",
            "message": f"Sessions with no tool usage: {agg.no_tool_rate:.1%} (threshold: {THRESHOLDS['no_tool_rate_warning']:.0%})",
            "value": agg.no_tool_rate,
            "threshold": THRESHOLDS["no_tool_rate_warning"],
        }
        warnings.append(warning)
        logger.warning(f"WARNING: {warning['message']}")
    
    # Check avg response length
    if agg.avg_response_length < THRESHOLDS["min_avg_response_length"]:
        warning = {
            "type": "short_responses",
            "severity": "WARNING",
            "message": f"Avg response length is {agg.avg_response_length:.0f} chars (min: {THRESHOLDS['min_avg_response_length']})",
            "value": agg.avg_response_length,
            "threshold": THRESHOLDS["min_avg_response_length"],
        }
        warnings.append(warning)
        logger.warning(f"WARNING: {warning['message']}")
    
    # Determine overall status
    if alerts:
        status = "alert"
    elif warnings:
        status = "warning"
    else:
        status = "healthy"
    
    result = {
        "status": status,
        "timestamp": datetime.utcnow().isoformat(),
        "days_analyzed": days,
        "session_count": agg.total_sessions,
        "alerts": alerts,
        "warnings": warnings,
        "metrics": {
            "dead_end_rate": agg.dead_end_rate,
            "no_tool_rate": agg.no_tool_rate,
            "avg_response_length": agg.avg_response_length,
            "avg_messages_per_session": agg.avg_messages_per_session,
            "tool_usage": dict(agg.tool_usage.most_common(10)),
            "modality_usage": dict(agg.modality_usage.most_common(10)),
        },
    }
    
    # Write alerts to file if any
    if alerts or warnings:
        alert_file = LOG_DIR / "quality_alerts.json"
        with open(alert_file, "w") as f:
            json.dump(result, f, indent=2)
        logger.info(f"Alerts written to {alert_file}")
    
    return result


def main():
    """Entry point for job runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run production quality check")
    parser.add_argument("--days", type=int, default=1, help="Days to analyze (default: 1)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    result = check_quality(days=args.days)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        logger.info(f"Quality check complete: status={result['status']}")
        logger.info(f"  Sessions analyzed: {result.get('session_count', 0)}")
        logger.info(f"  Alerts: {len(result['alerts'])}")
        logger.info(f"  Warnings: {len(result['warnings'])}")
        
        if result['status'] == 'healthy':
            logger.info("  All metrics within healthy thresholds")
    
    # Exit with non-zero if alerts
    if result['status'] == 'alert':
        sys.exit(1)


if __name__ == "__main__":
    main()
