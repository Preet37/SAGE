#!/bin/bash
# run_all_evals.sh - Run eval scenarios across all lessons
#
# Usage:
#   ./run_all_evals.sh                    # Full eval (all scenarios, all lessons)
#   ./run_all_evals.sh --quick            # Quick: behavioral-focused scenarios only (~15 min)
#   ./run_all_evals.sh --lesson lora      # Run only lora scenarios
#   ./run_all_evals.sh --ablation         # Run ablation test after main eval
#   ./run_all_evals.sh --explore-only     # Run only explore mode scenarios
#
# Output:
#   Results are saved to backend/evals/results/
#   Summary log is saved to backend/evals/results/eval_run_<timestamp>.log

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"
cd "$BACKEND_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="evals/results/eval_run_${TIMESTAMP}.log"
mkdir -p evals/results

# Default settings
PROMPT_VERSION="v2"
MAX_TURNS=10
QUICK_MODE=false
EXPLORE_ONLY=false
RUN_ABLATION=false
LESSON_FILTER=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --quick)
            QUICK_MODE=true
            MAX_TURNS=6
            shift
            ;;
        --explore-only)
            EXPLORE_ONLY=true
            shift
            ;;
        --ablation)
            RUN_ABLATION=true
            shift
            ;;
        --lesson)
            LESSON_FILTER="$2"
            shift 2
            ;;
        --prompt-version)
            PROMPT_VERSION="$2"
            shift 2
            ;;
        --max-turns)
            MAX_TURNS="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --quick            Quick eval: behavioral-focused scenarios (faster)"
            echo "  --explore-only     Run only explore mode scenarios"
            echo "  --ablation         Run ablation test after main eval"
            echo "  --lesson SLUG      Run only scenarios for a specific lesson"
            echo "  --prompt-version   Prompt version: v1, v2, v2-explore (default: v2)"
            echo "  --max-turns N      Maximum turns per scenario (default: 10)"
            echo "  -h, --help         Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

log() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

run_eval() {
    local lesson=$1
    local scenario=$2
    local prompt=$3

    log "Running: lesson=$lesson scenario=$scenario prompt=$prompt"

    if [ -n "$scenario" ]; then
        uv run python -m evals.run_eval \
            --lesson "$lesson" \
            --scenario "$scenario" \
            --prompt-version "$prompt" \
            --max-turns "$MAX_TURNS" \
            2>&1 | tee -a "$LOG_FILE"
    else
        uv run python -m evals.run_eval \
            --lesson "$lesson" \
            --prompt-version "$prompt" \
            --max-turns "$MAX_TURNS" \
            2>&1 | tee -a "$LOG_FILE"
    fi

    log "Completed: lesson=$lesson scenario=$scenario"
    echo "" >> "$LOG_FILE"
}

log "=========================================="
log "SocraticTutor Eval Suite"
log "Timestamp: $TIMESTAMP"
log "Prompt Version: $PROMPT_VERSION"
log "Max Turns: $MAX_TURNS"
log "Mode: $([ "$QUICK_MODE" = true ] && echo 'QUICK' || echo 'FULL')"
log "=========================================="
echo ""

FAILED=0
PASSED=0

# ── Explore mode scenarios ────────────────────────────────────────────────
if [ "$EXPLORE_ONLY" = true ] || [ -z "$LESSON_FILTER" ]; then
    log "--- EXPLORE MODE SCENARIOS ---"

    for scenario in explore_format_probe_quiz explore_format_probe_sources explore_format_probe_visual; do
        if run_eval "self-attention" "$scenario" "v2-explore"; then
            ((PASSED++))
        else
            ((FAILED++))
            log "FAILED: explore/$scenario"
        fi
    done
fi

if [ "$EXPLORE_ONLY" = true ]; then
    log "=========================================="
    log "Explore-only mode complete"
    log "Passed: $PASSED, Failed: $FAILED"
    log "Results: $LOG_FILE"
    exit $FAILED
fi

# ── LoRA scenarios ────────────────────────────────────────────────────────
if [ -z "$LESSON_FILTER" ] || [ "$LESSON_FILTER" = "lora" ] || [ "$LESSON_FILTER" = "lora-parameter-efficient" ]; then
    log "=== LoRA Lesson ==="

    if [ "$QUICK_MODE" = true ]; then
        # Quick: behavioral-focused scenarios only
        scenarios=(
            "curious_beginner"
            "proactive_visuals"
            "compound_analogy"
            "confusion_recovery"
        )
    else
        # Full: all scenarios
        scenarios=(
            "curious_beginner"
            "visual_learner"
            "factual_probe"
            "sharp_intermediate"
            "cross_topic"
            "wrong_intuition"
            "demands_answer"
            "eli5_mode"
            "code_mode"
            "deep_dive_mode"
            "analogy_mode"
            "proactive_visuals"
            "compound_analogy"
            "tangent_follow"
            "structured_overview"
            "resource_timing"
            "confusion_recovery"
        )
    fi

    for scenario in "${scenarios[@]}"; do
        if run_eval "lora-parameter-efficient" "$scenario" "$PROMPT_VERSION"; then
            ((PASSED++))
        else
            ((FAILED++))
            log "FAILED: lora/$scenario"
        fi
    done
fi

# ── Self-attention scenarios ──────────────────────────────────────────────
if [ -z "$LESSON_FILTER" ] || [ "$LESSON_FILTER" = "self-attention" ]; then
    log "=== Self-Attention Lesson ==="

    if [ "$QUICK_MODE" = true ]; then
        scenarios=(
            "format_probe_quiz"
            "compound_analogy"
        )
    else
        scenarios=(
            "format_probe_quiz"
            "format_probe_sources"
            "format_probe_visual"
            "compound_analogy"
        )
    fi

    for scenario in "${scenarios[@]}"; do
        if run_eval "self-attention" "$scenario" "$PROMPT_VERSION"; then
            ((PASSED++))
        else
            ((FAILED++))
            log "FAILED: self-attention/$scenario"
        fi
    done
fi

# ── Attention breakthrough scenarios ──────────────────────────────────────
if [ -z "$LESSON_FILTER" ] || [ "$LESSON_FILTER" = "attention-breakthrough" ]; then
    if [ "$QUICK_MODE" = false ]; then
        log "=== Attention Breakthrough Lesson ==="

        scenarios=(
            "attention_curious_beginner"
            "attention_format_probe_visual"
        )

        for scenario in "${scenarios[@]}"; do
            if run_eval "attention-breakthrough" "$scenario" "$PROMPT_VERSION"; then
                ((PASSED++))
            else
                ((FAILED++))
                log "FAILED: attention-breakthrough/$scenario"
            fi
        done
    fi
fi

# ── Alignment RLHF scenarios ─────────────────────────────────────────────
if [ -z "$LESSON_FILTER" ] || [ "$LESSON_FILTER" = "alignment-rlhf" ]; then
    if [ "$QUICK_MODE" = false ]; then
        log "=== Alignment RLHF Lesson ==="

        scenarios=(
            "rlhf_curious_beginner"
            "rlhf_technical_deep_dive"
        )

        for scenario in "${scenarios[@]}"; do
            if run_eval "alignment-rlhf" "$scenario" "$PROMPT_VERSION"; then
                ((PASSED++))
            else
                ((FAILED++))
                log "FAILED: alignment-rlhf/$scenario"
            fi
        done
    fi
fi

# ── LangGraph (framework/tooling) ────────────────────────────────────────
if [ -z "$LESSON_FILTER" ] || [ "$LESSON_FILTER" = "building-first-langgraph-agent" ] || [ "$LESSON_FILTER" = "langgraph" ]; then
    log "=== LangGraph Agent Lesson ==="

    if [ "$QUICK_MODE" = true ]; then
        scenarios=(
            "langgraph_curious_beginner"
        )
    else
        scenarios=(
            "langgraph_curious_beginner"
            "langgraph_proactive_visuals"
            "langgraph_compound_analogy"
        )
    fi

    for scenario in "${scenarios[@]}"; do
        if run_eval "building-first-langgraph-agent" "$scenario" "$PROMPT_VERSION"; then
            ((PASSED++))
        else
            ((FAILED++))
            log "FAILED: langgraph/$scenario"
        fi
    done
fi

# ── Sim-to-Real (physical AI) ───────────────────────────────────────────
if [ -z "$LESSON_FILTER" ] || [ "$LESSON_FILTER" = "sim-to-real-transfer" ] || [ "$LESSON_FILTER" = "sim-to-real" ]; then
    log "=== Sim-to-Real Transfer Lesson ==="

    if [ "$QUICK_MODE" = true ]; then
        scenarios=(
            "simtoreal_curious_beginner"
        )
    else
        scenarios=(
            "simtoreal_curious_beginner"
            "simtoreal_proactive_visuals"
            "simtoreal_compound_analogy"
        )
    fi

    for scenario in "${scenarios[@]}"; do
        if run_eval "sim-to-real-transfer" "$scenario" "$PROMPT_VERSION"; then
            ((PASSED++))
        else
            ((FAILED++))
            log "FAILED: sim-to-real/$scenario"
        fi
    done
fi

# ── Chatbots to Agents (intro/conceptual) ────────────────────────────────
if [ -z "$LESSON_FILTER" ] || [ "$LESSON_FILTER" = "from-chatbots-to-agents" ] || [ "$LESSON_FILTER" = "chatbots" ]; then
    log "=== From Chatbots to Agents Lesson ==="

    if [ "$QUICK_MODE" = true ]; then
        scenarios=(
            "chatbots_curious_beginner"
        )
    else
        scenarios=(
            "chatbots_curious_beginner"
            "chatbots_proactive_visuals"
            "chatbots_compound_analogy"
        )
    fi

    for scenario in "${scenarios[@]}"; do
        if run_eval "from-chatbots-to-agents" "$scenario" "$PROMPT_VERSION"; then
            ((PASSED++))
        else
            ((FAILED++))
            log "FAILED: chatbots/$scenario"
        fi
    done
fi

# ── Code Execution & Retrieval (code-heavy) ──────────────────────────────
if [ -z "$LESSON_FILTER" ] || [ "$LESSON_FILTER" = "code-execution-retrieval" ] || [ "$LESSON_FILTER" = "code-exec" ]; then
    log "=== Code Execution & Retrieval Lesson ==="

    if [ "$QUICK_MODE" = true ]; then
        scenarios=(
            "codeexec_curious_beginner"
        )
    else
        scenarios=(
            "codeexec_curious_beginner"
            "codeexec_proactive_visuals"
            "codeexec_compound_analogy"
        )
    fi

    for scenario in "${scenarios[@]}"; do
        if run_eval "code-execution-retrieval" "$scenario" "$PROMPT_VERSION"; then
            ((PASSED++))
        else
            ((FAILED++))
            log "FAILED: code-exec/$scenario"
        fi
    done
fi

# ── Ablation (optional) ──────────────────────────────────────────────────
if [ "$RUN_ABLATION" = true ]; then
    log "--- ABLATION TESTING ---"

    ABLATION_LESSON="${LESSON_FILTER:-lora-parameter-efficient}"
    ABLATION_SCENARIO="curious_beginner"

    log "Running ablation: lesson=$ABLATION_LESSON scenario=$ABLATION_SCENARIO"
    if uv run python -m evals.run_ablation \
        --lesson "$ABLATION_LESSON" \
        --scenario "$ABLATION_SCENARIO" \
        2>&1 | tee -a "$LOG_FILE"; then
        ((PASSED++))
    else
        ((FAILED++))
        log "FAILED: ablation"
    fi
fi

log "=========================================="
log "EVAL SUITE COMPLETE"
log "Passed: $PASSED"
log "Failed: $FAILED"
log "Results saved to: $LOG_FILE"
log "Individual results in: evals/results/"
log "=========================================="

exit $FAILED
