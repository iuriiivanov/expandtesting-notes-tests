# Expand Testing Notes App Tests

End-to-end test automation for [Expand Testing Notes app](https://practice.expandtesting.com/notes/app/).

## Project Goals

This project is built to demonstrate my skills and knowledge in automated software testing using Python, pytest, Playwright and related tools. It covers both API and UI layers of a real-world application.

## Stack

| Layer | Tools                                      |
|-------|--------------------------------------------|
| API   | Python, pytest, requests, Pydantic, Allure |
| UI    | Python, Playwright — coming soon           |
| CI/CD | GitHub Actions                             |

## Structure

```bash
├── backend/                API tests (Python, pytest, requests)
│   ├── src/                API client, models, payloads, utils
│   └── tests/              pytest test suites
├── docs/                   API documentation
├── frontend/               UI tests (Python, Playwright) — coming soon
├── run_tests.sh            Test runner with Allure support
├── pyproject.toml          Python dependencies and tool configs
├── docker-compose.yml      Docker setup for test execution
├── Dockerfile              Container image definition
└── README.md               This file
```

## Quick Start

### Installation

```bash
# Install dependencies
uv pip install -e .
```

### Run Tests

#### Via script (recommended):
```bash
# Run all API tests with Allure report generation
./run_tests.sh

# Run with preserved history for trend analysis
./run_tests.sh --keep-history
```

#### Via command line:

```bash
# Run all API tests
uv run pytest backend/tests -v

# Run with Allure report
uv run pytest backend/tests --alluredir=allure-results

# Run specific test file
uv run pytest backend/tests/test_auth.py -v

# Run smoke tests only
uv run pytest backend/tests -m smoke -v

# Run in Docker
docker compose up --build
```

### View Allure Report

```bash
# After running tests with --alluredir
uv run allure serve allure-results
```

### Code Quality Checks

```bash
# Run linter
uv run ruff check backend/src backend/tests

# Run type checker
uv run mypy backend/src backend/tests
```

