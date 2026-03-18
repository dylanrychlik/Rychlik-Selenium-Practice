# Selenium-testautomationpractice

Production-ready Python automation framework combining:

- **UI automation** with Selenium WebDriver (Page Object Model)
- **API testing** with requests + pytest

Target systems:

- UI: https://testautomationpractice.blogspot.com/
- API: https://jsonplaceholder.typicode.com/

---

## Tech Stack

- **Language:** Python
- **UI Testing:** Selenium WebDriver
- **API Testing:** requests
- **Test Framework:** pytest
- **Build/Dependency Management:** pip + `requirements.txt`

---

## Project Structure

```text
Selenium-testautomationpractice/
├── config/
│   └── config.yaml
├── src/
│   ├── api/
│   │   └── api_client.py
│   ├── page_objects/
│   │   └── test_automation_practice_page.py
│   └── utils/
│       ├── config_reader.py
│       ├── driver_factory.py
│       └── logger.py
├── tests/
│   ├── api/
│   │   └── test_posts_api.py
│   ├── ui/
│   │   └── test_ui_practice.py
│   └── conftest.py
├── .gitignore
├── pytest.ini
└── requirements.txt
```

---

## Implemented UI Test Cases (5)

1. Verify page loads and title is correct
2. Fill name, email, phone fields and perform submit action
3. Interact with radio buttons and checkboxes
4. Select values from dropdowns and verify selections
5. Handle alerts and validate dynamic result text

### UI Design Choices

- Uses **explicit waits** (`WebDriverWait`) in page object methods
- Uses stable locators (`By.ID`) wherever possible
- Reusable methods encapsulated in a Page Object (`TestAutomationPracticePage`)

---

## Implemented API Test Cases (5)

1. `GET /posts` → verify `200` and response list size
2. `GET /posts/1` → validate specific fields (`id`, `title`)
3. `POST /posts` → create post and validate response payload
4. `PUT /posts/1` → update post and validate response payload
5. `DELETE /posts/1` → verify status code

---

## Configuration

Default config is stored in `config/config.yaml`:

- UI base URL, browser, headless mode, timeouts
- API base URL and request timeout

### Optional Environment Variable Overrides

- `UI_BASE_URL`
- `API_BASE_URL`
- `UI_BROWSER` (`chrome` or `firefox`)
- `UI_HEADLESS` (`true` or `false`)

---

## Setup

### 1) Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run Tests

### Run all tests

```bash
pytest
```

### Run only UI tests

```bash
pytest -m ui
```

### Run only API tests

```bash
pytest -m api
```

### Generate simple test report (JUnit XML)

```bash
pytest --junitxml=reports/results.xml
```

---

## Logging

- Console and file logging enabled through `src/utils/logger.py`
- Log file output path: `logs/test_run.log`

---

## Notes

- UI tests are configured to run headless by default.
- Selenium requires a compatible browser installed locally (Chrome/Firefox).