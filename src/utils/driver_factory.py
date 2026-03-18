"""Creates Selenium WebDriver instances."""

from __future__ import annotations

import logging

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

LOGGER = logging.getLogger(__name__)


def create_driver(
    browser: str,
    headless: bool,
    implicit_wait_seconds: int = 2,
) -> webdriver.Remote:
    """Create a Selenium WebDriver for the requested browser."""
    normalized = browser.strip().lower()
    LOGGER.info("Creating browser driver | browser=%s | headless=%s", normalized, headless)

    if normalized == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)
    elif normalized == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.set_window_size(1920, 1080)
    else:
        raise ValueError(f"Unsupported browser requested: {browser}")

    try:
        driver.implicitly_wait(implicit_wait_seconds)
    except WebDriverException as exc:
        LOGGER.warning("Unable to set implicit wait: %s", exc)
    return driver
