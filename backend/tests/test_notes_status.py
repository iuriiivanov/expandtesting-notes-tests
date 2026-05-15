"""Tests for note status updates."""

from collections.abc import Callable
from typing import Any

import allure
import pytest
from api import ApiClient, endpoints

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
            data = response.json()["data"]
            assert data["completed"] is True
            assert data["updated_at"] != created["created_at"]

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
