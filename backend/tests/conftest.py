"""Pytest fixtures."""

import os
from collections.abc import Generator
from typing import Any

import allure
import pytest
import requests
from backend.src.api.auth import delete_account, login_user, register_user
from backend.src.api.client import ApiClient
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def base_client() -> ApiClient:
    """Return unauthenticated API client."""
    return ApiClient()


@pytest.fixture
def client() -> ApiClient:
    """Return fresh unauthenticated API client."""
    return ApiClient()


@pytest.fixture
def authenticated_client() -> Generator[ApiClient, None, None]:
    """Return authenticated API client with a test user."""
    client = ApiClient()

    with allure.step("Create test user for authenticated client"):
        email = f"auth_test_{os.urandom(4).hex()}@example.com"
        password = "TestPass123!"
        name = f"AuthTest_{os.urandom(4).hex()}"

        register_user(client, name=name, email=email, password=password)
        token = login_user(client, email=email, password=password)
        client.set_token(token)

    yield client

    with allure.step("Cleanup: delete test user"):
        try:
            delete_account(client)
        except (requests.exceptions.RequestException, KeyError, ValueError):
            pass


@pytest.fixture
def note_factory(authenticated_client: ApiClient) -> Generator[Any, None, None]:
    """Factory fixture to create notes and auto-cleanup."""
    from backend.src.api import endpoints
    from backend.src.models.note import NoteCreateRequest

    created_notes: list[str] = []

    def _create(title: str, description: str, category: str) -> dict[str, Any]:
        with allure.step(f"Create note: {title}"):
            payload = NoteCreateRequest(
                title=title, description=description, category=category
            ).model_dump()
            response = authenticated_client.post(endpoints.NOTES, data=payload)
            response.raise_for_status()
            note: dict[str, Any] = response.json()["data"]
            created_notes.append(note["id"])
            return note

    yield _create

    with allure.step("Cleanup: delete created notes"):
        for note_id in created_notes:
            try:
                authenticated_client.delete(endpoints.note_by_id(note_id))
            except (requests.exceptions.RequestException, KeyError, ValueError):
                pass
