# Backend Tests

API test automation for Expand Testing Notes App.

## Stack

- Python 3.13
- pytest
- requests
- Pydantic
- Allure

## Run

```bash
# From project root
uv run pytest backend/tests

# With Allure
uv run pytest backend/tests --alluredir=allure-results
```