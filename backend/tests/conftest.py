"""Pytest fixtures."""

import os
from collections.abc import Callable, Generator
from typing import Any

import allure
import pytest
import requests

from backend.src.api.auth import delete_account, login_user, register_user
from backend.src.api.client import ApiClient
from backend.src.utils.logger import TestLogger


@pytest.fixture(scope="session")
def test_logger(request: pytest.FixtureRequest) -> Generator[TestLogger]:
    """Create logger for test."""
    logger = TestLogger()
    yield logger
    logger.save()


@pytest.fixture(autouse=True)
def _set_current_test(test_logger: TestLogger, request: pytest.FixtureRequest) -> None:
    """Automatically set current test name before each test."""
    test_logger.set_test(request.node.nodeid)


@pytest.fixture(scope="session")
def base_client() -> ApiClient:
    """Return unauthenticated API client."""
    return ApiClient()


@pytest.fixture
def client() -> ApiClient:
    """Return fresh unauthenticated API client."""
    return ApiClient()


@pytest.fixture
def test_password() -> str:
    """Return consistent test password for all auth tests."""
    return "TestPass123!"


@pytest.fixture
def authenticated_client(test_password: str, test_logger: TestLogger) -> Generator[ApiClient]:
    """Return authenticated API client with a test user."""
    client = ApiClient()

    with allure.step("Create test user for authenticated client"):
        test_logger.info("Setup", "Creating authenticated client", {"action": "register_and_login"})
        email = f"auth_test_{os.urandom(4).hex()}@example.com"
        password = test_password
        name = f"AuthTest_{os.urandom(4).hex()}"

        register_user(client, name=name, email=email, password=password)
        token = login_user(client, email=email, password=password)
        client.set_token(token)
        test_logger.info("Setup", "Authenticated client created", {"email": email, "name": name})

    yield client

    with allure.step("Cleanup: delete test user"):
        try:
            delete_account(client)
            test_logger.info("Teardown", "Test user deleted", {"email": email})
        except requests.exceptions.HTTPError:
            try:
                new_token = login_user(client, email=email, password=password)
                client.set_token(new_token)
                delete_account(client)
                test_logger.info("Teardown", "Test user deleted after re-login", {"email": email})
            except (requests.exceptions.RequestException, KeyError, ValueError) as e:
                test_logger.error(
                    "Teardown", "Failed to delete test user after re-login", {"error": str(e)}
                )
        except (requests.exceptions.RequestException, KeyError, ValueError) as e:
            test_logger.error("Teardown", "Failed to delete test user", {"error": str(e)})


@pytest.fixture
def note_factory(
    authenticated_client: ApiClient, test_logger: TestLogger
) -> Generator[Callable[[str, str, str], dict[str, Any]]]:
    """Factory fixture to create notes and auto-cleanup."""
    from backend.src.api import endpoints
    from backend.src.models.note import NoteCreateRequest

    created_notes: list[str] = []

    def _create(title: str, description: str, category: str) -> dict[str, Any]:
        with allure.step(f"Create note: {title}"):
            test_logger.info(
                "NoteFactory", f"Creating note: {title}", {"title": title, "category": category}
            )
            payload = NoteCreateRequest(
                title=title, description=description, category=category
            ).model_dump()
            response = authenticated_client.post(endpoints.NOTES, data=payload)
            response.raise_for_status()
            note: dict[str, Any] = response.json()["data"]
            created_notes.append(note["id"])
            test_logger.info(
                "NoteFactory",
                "Note created successfully",
                {"note_id": note["id"], "title": note["title"]},
            )
            return note

    yield _create

    with allure.step("Cleanup: delete created notes"):
        for note_id in created_notes:
            try:
                authenticated_client.delete(endpoints.note_by_id(note_id))
                test_logger.info("NoteFactory", "Note deleted", {"note_id": note_id})
            except (requests.exceptions.RequestException, KeyError, ValueError) as e:
                test_logger.error(
                    "NoteFactory", "Failed to delete note", {"note_id": note_id, "error": str(e)}
                )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Any, call: Any) -> Any:
    """Attach log to Allure report if test failed."""
    _ = call
    outcome: Any = yield
    report: Any = outcome.get_result()

    if report.when == "call" and report.failed:
        logger: Any = item.funcargs.get("test_logger")
        if logger:
            log_content = logger.save()
            allure.attach(
                log_content,
                name="test_execution_log.json",
                attachment_type=allure.attachment_type.JSON,
            )
