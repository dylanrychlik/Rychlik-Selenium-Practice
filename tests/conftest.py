"""Shared pytest fixtures for UI and API test suites."""

from __future__ import annotations

import logging
from collections.abc import Generator

import pytest
from selenium.common.exceptions import WebDriverException

from src.api.api_client import APIClient
from src.page_objects.test_automation_practice_page import AutomationPracticePage
from src.utils.config_reader import load_config
from src.utils.driver_factory import create_driver
from src.utils.logger import configure_logger

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def setup_logging() -> None:
    configure_logger()


@pytest.fixture(scope="session")
def config() -> dict:
    return load_config()


@pytest.fixture(scope="session")
def api_client(config: dict) -> Generator[APIClient, None, None]:
    client = APIClient(
        base_url=config["api"]["base_url"],
        timeout_seconds=config["api"]["timeout_seconds"],
    )
    yield client
    client.close()


@pytest.fixture
def driver(config: dict):
    ui_config = config["ui"]
    browser = ui_config["browser"]
    headless = ui_config["headless"]
    implicit_wait = ui_config["implicit_wait_seconds"]

    try:
        driver_instance = create_driver(
            browser=browser,
            headless=headless,
            implicit_wait_seconds=implicit_wait,
        )
    except WebDriverException as exc:
        pytest.skip(f"UI tests skipped: browser driver setup failed ({exc})")
    yield driver_instance
    LOGGER.info("Closing browser")
    driver_instance.quit()


@pytest.fixture
def practice_page(driver, config: dict) -> AutomationPracticePage:
    ui_config = config["ui"]
    scroll_behavior = ui_config.get("scroll_behavior", "auto")
    if ui_config.get("headless") and scroll_behavior == "smooth":
        # Headless environments are more stable with non-animated scrolling.
        scroll_behavior = "auto"

    page = AutomationPracticePage(
        driver,
        timeout_seconds=ui_config["explicit_wait_seconds"],
        enable_visual_steps=ui_config.get("enable_visual_steps", False),
        action_pause_seconds=ui_config.get("action_pause_seconds", 0.0),
        scroll_pause_seconds=ui_config.get("scroll_pause_seconds", 0.0),
        scroll_behavior=scroll_behavior,
    )
    page.open(config["ui"]["base_url"])
    return page
