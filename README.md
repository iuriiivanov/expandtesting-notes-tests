# Expand Testing Notes App Tests

End-to-end test automation for [Expand Testing Notes app](https://practice.expandtesting.com/notes/app/).

## Project Goals

This project is built to demonstrate my skills and knowledge in automated software testing using Python, pytest, Playwright and related tools. It covers both API and UI layers of a real-world application.

## Structure

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

## Quick Start

```bash
# Install dependencies
uv pip install -e .

# Run API tests
uv run pytest backend/tests

# Run in Docker
docker compose up --build
```

## Stack

| Layer | Tools                                      |
|-------|--------------------------------------------|
| API   | Python, pytest, requests, Pydantic, Allure |
| UI    | Python, Playwright — coming soon           |
| CI/CD | GitHub Actions                             |

