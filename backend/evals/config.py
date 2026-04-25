"""Eval framework configuration — reads from shared settings.yaml."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from dotenv import load_dotenv
from openai import AsyncOpenAI

EVALS_DIR = Path(__file__).parent
BACKEND_DIR = EVALS_DIR.parent
SCENARIOS_DIR = EVALS_DIR / "scenarios"
RESULTS_DIR = EVALS_DIR / "results"
SETTINGS_PATH = BACKEND_DIR / "settings.yaml"

RESULTS_DIR.mkdir(exist_ok=True)


def _load_yaml() -> dict:
    with open(SETTINGS_PATH) as f:
        return yaml.safe_load(f)


def _api_key() -> str:
    load_dotenv(BACKEND_DIR / ".env")
    key = os.getenv("LLM_API_KEY", "")
    if not key:
        raise RuntimeError("LLM_API_KEY not set in .env")
    return key


_cfg = _load_yaml()


@dataclass
class ModelConfig:
    """Identifies a model on an OpenAI-compatible endpoint."""
    name: str
    model_id: str
    max_tokens: int = 2048
    temperature: float = 0.7


def _model_from_cfg(key: str) -> ModelConfig:
    m = _cfg["models"][key]
    return ModelConfig(
        name=m["name"],
        model_id=m["model_id"],
        max_tokens=m.get("max_tokens", 2048),
        temperature=m.get("temperature", 0.7),
    )


TUTOR_BASELINE = _model_from_cfg("tutor")
JUDGE_MODEL = _model_from_cfg("judge")
STUDENT_SIM_MODEL = _model_from_cfg("student_sim")


@dataclass
class EvalConfig:
    """Top-level config for an evaluation run."""
    tutor_model: ModelConfig = field(default_factory=lambda: TUTOR_BASELINE)
    judge_model: ModelConfig = field(default_factory=lambda: JUDGE_MODEL)
    student_model: ModelConfig = field(default_factory=lambda: STUDENT_SIM_MODEL)
    max_turns: int = _cfg["eval"]["max_turns"]
    lesson_slug: str = _cfg["eval"]["default_lesson"]


def get_openai_client() -> AsyncOpenAI:
    """Shared AsyncOpenAI client for the configured LLM provider."""
    return AsyncOpenAI(
        api_key=_api_key(),
        base_url=_cfg["llm"]["base_url"],
    )
