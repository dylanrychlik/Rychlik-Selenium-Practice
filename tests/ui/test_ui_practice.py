"""UI tests for testautomationpractice.blogspot.com."""

from __future__ import annotations

import pytest

from src.page_objects.test_automation_practice_page import AutomationPracticePage


@pytest.mark.ui
def test_page_loads_and_title_is_correct(practice_page: AutomationPracticePage) -> None:
    practice_page.quick_page_preview()
    expected_title = "Automation Testing Practice"
    practice_page.wait_for_title(expected_title)
    assert practice_page.driver.title == expected_title


@pytest.mark.ui
def test_fill_contact_form_and_submit(practice_page: AutomationPracticePage) -> None:
    practice_page.quick_page_preview()
    input_data = {
        "name": "Alex Tester",
        "email": "alex.tester@example.com",
        "phone": "9876543210",
    }

    practice_page.fill_contact_details(**input_data)
    practice_page.submit_contact_details()

    stored_data = practice_page.get_contact_details()
    assert stored_data == input_data


@pytest.mark.ui
def test_radio_buttons_and_checkboxes(practice_page: AutomationPracticePage) -> None:
    practice_page.quick_page_preview()
    practice_page.select_gender("male")
    practice_page.select_day("monday")
    practice_page.select_day("wednesday")

    assert practice_page.is_selected(practice_page.MALE_RADIO)
    assert practice_page.is_selected(practice_page.MONDAY_CHECKBOX)
    assert practice_page.is_selected(practice_page.WEDNESDAY_CHECKBOX)


@pytest.mark.ui
def test_dropdown_selection_and_verification(practice_page: AutomationPracticePage) -> None:
    practice_page.quick_page_preview()
    practice_page.select_country("India")
    practice_page.select_color("Red")

    assert practice_page.selected_country() == "India"
    assert "Red" in practice_page.selected_colors()


@pytest.mark.ui
def test_alert_handling_and_dynamic_result(practice_page: AutomationPracticePage) -> None:
    practice_page.quick_page_preview()
    alert_text = practice_page.trigger_simple_alert_and_accept()
    assert alert_text == "I am an alert box!"

    confirm_text = practice_page.trigger_confirm_alert(accept=True)
    assert confirm_text == "Press a button!"
    assert practice_page.wait_for_prompt_result() == "You pressed OK!"
