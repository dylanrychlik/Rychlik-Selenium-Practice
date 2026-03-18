"""Page Object for https://testautomationpractice.blogspot.com/."""

from __future__ import annotations

import logging

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

LOGGER = logging.getLogger(__name__)


class AutomationPracticePage:
    """Encapsulates actions and assertions for the practice page."""

    NAME_INPUT = (By.ID, "name")
    EMAIL_INPUT = (By.ID, "email")
    PHONE_INPUT = (By.ID, "phone")

    MALE_RADIO = (By.ID, "male")
    FEMALE_RADIO = (By.ID, "female")
    MONDAY_CHECKBOX = (By.ID, "monday")
    WEDNESDAY_CHECKBOX = (By.ID, "wednesday")

    COUNTRY_DROPDOWN = (By.ID, "country")
    COLORS_DROPDOWN = (By.ID, "colors")

    ALERT_BUTTON = (By.ID, "alertBtn")
    CONFIRM_BUTTON = (By.ID, "confirmBtn")
    PROMPT_BUTTON = (By.ID, "promptBtn")
    PROMPT_RESULT = (By.ID, "demo")

    def __init__(self, driver: WebDriver, timeout_seconds: int = 10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout_seconds)

    def open(self, base_url: str) -> None:
        LOGGER.info("Opening UI page: %s", base_url)
        self.driver.get(base_url)

    def wait_for_title(self, expected_title: str) -> None:
        self.wait.until(ec.title_is(expected_title))

    def fill_contact_details(self, name: str, email: str, phone: str) -> None:
        self._type(self.NAME_INPUT, name)
        self._type(self.EMAIL_INPUT, email)
        self._type(self.PHONE_INPUT, phone)

    def submit_contact_details(self) -> None:
        """
        Submit contact details.
        The page does not expose a dedicated form submit for these fields,
        so Enter key is used as submit-like behavior.
        """
        phone = self.wait.until(ec.visibility_of_element_located(self.PHONE_INPUT))
        phone.send_keys(Keys.ENTER)

    def get_contact_details(self) -> dict[str, str]:
        return {
            "name": self._value(self.NAME_INPUT),
            "email": self._value(self.EMAIL_INPUT),
            "phone": self._value(self.PHONE_INPUT),
        }

    def select_gender(self, gender: str) -> None:
        normalized = gender.lower()
        target = self.MALE_RADIO if normalized == "male" else self.FEMALE_RADIO
        self.wait.until(ec.element_to_be_clickable(target)).click()

    def select_day(self, day: str) -> None:
        locator = (By.ID, day.lower())
        self.wait.until(ec.element_to_be_clickable(locator)).click()

    def is_selected(self, locator: tuple[str, str]) -> bool:
        element = self.wait.until(ec.visibility_of_element_located(locator))
        return element.is_selected()

    def select_country(self, visible_text: str) -> None:
        dropdown = self.wait.until(ec.element_to_be_clickable(self.COUNTRY_DROPDOWN))
        Select(dropdown).select_by_visible_text(visible_text)

    def selected_country(self) -> str:
        dropdown = self.wait.until(ec.visibility_of_element_located(self.COUNTRY_DROPDOWN))
        return Select(dropdown).first_selected_option.text.strip()

    def select_color(self, visible_text: str) -> None:
        dropdown = self.wait.until(ec.element_to_be_clickable(self.COLORS_DROPDOWN))
        Select(dropdown).select_by_visible_text(visible_text)

    def selected_colors(self) -> list[str]:
        dropdown = self.wait.until(ec.visibility_of_element_located(self.COLORS_DROPDOWN))
        return [option.text.strip() for option in Select(dropdown).all_selected_options]

    def trigger_simple_alert_and_accept(self) -> str:
        self.wait.until(ec.element_to_be_clickable(self.ALERT_BUTTON)).click()
        alert = self.wait.until(ec.alert_is_present())
        text = alert.text
        alert.accept()
        return text

    def trigger_confirm_alert(self, accept: bool = True) -> str:
        self.wait.until(ec.element_to_be_clickable(self.CONFIRM_BUTTON)).click()
        alert: Alert = self.wait.until(ec.alert_is_present())
        text = alert.text
        if accept:
            alert.accept()
        else:
            alert.dismiss()
        return text

    def wait_for_prompt_result(self) -> str:
        result = self.wait.until(ec.visibility_of_element_located(self.PROMPT_RESULT))
        return result.text.strip()

    def _type(self, locator: tuple[str, str], value: str) -> None:
        element = self.wait.until(ec.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(value)

    def _value(self, locator: tuple[str, str]) -> str:
        element = self.wait.until(ec.visibility_of_element_located(locator))
        return element.get_attribute("value")
