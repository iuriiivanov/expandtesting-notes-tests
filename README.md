# Expand Testing Notes App Tests

End-to-end test automation for [ExpandTesting Notes app](https://practice.expandtesting.com/notes/app/).

## Project Goals

This project is built to demonstrate my skills and knowledge in automated software testing using Python, pytest, Playwright and related tools. It covers both API and UI layers of a real-world application.

## Structure
├── backend/     API tests (Python, pytest, requests)  
├── frontend/    UI tests (Python, Playwright) — coming soon  
├── docs/        API documentation  
└── scripts/     Utility scripts

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
| ----- | ------------------------------------------ |
| API   | Python, pytest, requests, Pydantic, Allure |
| UI    | Python, Playwright — coming soon           |
| CI/CD | GitHub Actions                             |

