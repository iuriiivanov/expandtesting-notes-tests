"""Tests for note status updates."""

from collections.abc import Callable
from typing import Any

import allure
import pytest

from backend.src.api import endpoints
from backend.src.api.client import ApiClient
from backend.src.models.note import NoteResponse

NoteFactory = Callable[[str, str, str], dict[str, Any]]


@allure.feature("Note Status")
@allure.story("Update Completed Status")
class TestNoteStatus:
    """Tests for PATCH /notes/{id}."""

    @allure.title("Mark note as completed")
    @pytest.mark.smoke
    def test_mark_note_completed(
        self, authenticated_client: ApiClient, note_factory: NoteFactory
    ) -> None:
        """TC-003.1.1: Set completed=true."""
        created = note_factory("Incomplete", "Not done", "Home")
        note_id = created["id"]
        assert created["completed"] is False

        with allure.step("Patch note to completed"):
            response = authenticated_client.patch(
                endpoints.note_by_id(note_id), data={"completed": "true"}
            )

        with allure.step("Verify status updated"):
            assert response.status_code == 200
            result = NoteResponse(**response.json())
            assert result.data.completed is True
            assert result.data.updated_at != created["updated_at"]

    @allure.title("Mark note as not completed")
    @pytest.mark.smoke
    def test_mark_note_not_completed(
        self, authenticated_client: ApiClient, note_factory: NoteFactory
    ) -> None:
        """TC-003.1.2: Set completed=false."""
        created = note_factory("Complete", "Done", "Work")
        note_id = created["id"]

        authenticated_client.patch(endpoints.note_by_id(note_id), data={"completed": "true"})

        with allure.step("Patch note to not completed"):
            response = authenticated_client.patch(
                endpoints.note_by_id(note_id), data={"completed": "false"}
            )

        with allure.step("Verify status updated"):
            assert response.status_code == 200
            assert response.json()["data"]["completed"] is False

    @allure.title("Update status of non-existent note fails")
    @pytest.mark.regression
    def test_update_status_not_found(self, authenticated_client: ApiClient) -> None:
        """TC-003.1.3: Update status of non-existent note returns 400."""
        response = authenticated_client.patch(
            endpoints.note_by_id("nonexistent"), data={"completed": "true"}
        )
        assert response.status_code == 400

    @allure.title("Update note status without token fails")
    @pytest.mark.regression
    def test_update_status_no_token(self, client: ApiClient) -> None:
        """TC-003.1.4: Update note status without token returns 401."""
        response = client.patch(endpoints.note_by_id("some-id"), data={"completed": "true"})
        assert response.status_code == 401
        assert response.json()["success"] is False

    @allure.title("User cannot update status of another user's note")
    @pytest.mark.integration
    def test_update_status_isolation(
        self, authenticated_client: ApiClient, client: ApiClient, test_password: str
    ) -> None:
        """TC-003.1.5: User cannot update status of another user's note."""
        from backend.src.api.auth import login_user, register_user

        email_a = f"isolation_{__import__('os').urandom(4).hex()}@example.com"
        register_user(client, name="UserA", email=email_a, password=test_password)
        token_a = login_user(client, email=email_a, password=test_password)
        client_a = ApiClient(token=token_a)

        note_response = client_a.post(
            endpoints.NOTES, data={"title": "Private", "description": "Secret", "category": "Home"}
        )
        note_id = note_response.json()["data"]["id"]

        with allure.step("User B attempts to update status of User A's note"):
            response = authenticated_client.patch(
                endpoints.note_by_id(note_id), data={"completed": "true"}
            )

        with allure.step("Verify access denied"):
            assert response.status_code == 404
