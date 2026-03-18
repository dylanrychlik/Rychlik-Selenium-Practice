"""Reads framework configuration from YAML with env overrides."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

CONFIG_PATH = Path("config/config.yaml")


@lru_cache(maxsize=1)
def load_config() -> dict[str, Any]:
    """Load configuration once per process."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

    with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        config: dict[str, Any] = yaml.safe_load(config_file)

    # Environment overrides for runtime flexibility in CI/local.
    if os.getenv("UI_BASE_URL"):
        config["ui"]["base_url"] = os.environ["UI_BASE_URL"]
    if os.getenv("API_BASE_URL"):
        config["api"]["base_url"] = os.environ["API_BASE_URL"]
    if os.getenv("UI_BROWSER"):
        config["ui"]["browser"] = os.environ["UI_BROWSER"].lower()
    if os.getenv("UI_HEADLESS"):
        config["ui"]["headless"] = os.environ["UI_HEADLESS"].lower() == "true"

    return config
