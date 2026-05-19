"""CRUD operations tests for Notes API."""

from collections.abc import Callable
from typing import Any

import allure
import pytest

from backend.src.api import endpoints
from backend.src.api.client import ApiClient
from backend.src.models.note import NoteUpdateRequest

NoteFactory = Callable[[str, str, str], dict[str, Any]]


@allure.feature("Notes CRUD")
@allure.story("Create Note")
class TestCreateNote:
    """Tests for POST /notes."""

    @allure.title("Successfully create note with category Home")
    @pytest.mark.smoke
    def test_create_note_home(
        self, authenticated_client: ApiClient, note_factory: NoteFactory
    ) -> None:
        """TC-002.1.1: Create note category Home."""
        with allure.step("Create note via factory"):
            note = note_factory("Home Task", "Do something at home", "Home")

        with allure.step("Verify note data"):
            assert note["title"] == "Home Task"
            assert note["category"] == "Home"
            assert note["completed"] is False
            assert "id" in note

    @allure.title("Successfully create note with category Work")
    @pytest.mark.smoke
    def test_create_note_work(
        self, authenticated_client: ApiClient, note_factory: NoteFactory
    ) -> None:
        """TC-002.1.2: Create note category Work."""
        note = note_factory("Work Task", "Do something at work", "Work")
        assert note["category"] == "Work"

    @allure.title("Successfully create note with category Personal")
    @pytest.mark.smoke
    def test_create_note_personal(
        self, authenticated_client: ApiClient, note_factory: NoteFactory
    ) -> None:
        """TC-002.1.3: Create note category Personal."""
        note = note_factory("Personal Task", "Do something personal", "Personal")
        assert note["category"] == "Personal"

    @allure.title("Create note with empty title fails")
    @pytest.mark.regression
    def test_create_note_empty_title(self, authenticated_client: ApiClient) -> None:
        """TC-002.1.4: Empty title returns 400."""
        response = authenticated_client.post(
            endpoints.NOTES, data={"title": "", "description": "desc", "category": "Home"}
        )
        assert response.status_code == 400
        assert response.json()["success"] is False

    @allure.title("Create note with invalid category fails")
    @pytest.mark.regression
    def test_create_note_invalid_category(self, authenticated_client: ApiClient) -> None:
        """TC-002.1.6: Invalid category returns 400."""
        response = authenticated_client.post(
            endpoints.NOTES, data={"title": "Test", "description": "Test", "category": "Invalid"}
        )
        assert response.status_code == 400

    @allure.title("Create note without token fails")
    @pytest.mark.regression
    def test_create_note_no_token(self, client: ApiClient) -> None:
        """TC-002.1.7: No token returns 401."""
        response = client.post(
            endpoints.NOTES, data={"title": "Test", "description": "Test", "category": "Home"}
        )
        assert response.status_code == 401


@allure.feature("Notes CRUD")
@allure.story("Get Notes")
class TestGetNotes:
    """Tests for GET /notes and GET /notes/{id}."""

    @allure.title("Get all notes returns list")
    @pytest.mark.smoke
    def test_get_all_notes(
        self, authenticated_client: ApiClient, note_factory: NoteFactory
    ) -> None:
        """TC-002.2.1: Get list of notes."""
        note_factory("Note 1", "Desc 1", "Home")
        note_factory("Note 2", "Desc 2", "Work")

        with allure.step("Get all notes"):
            response = authenticated_client.get(endpoints.NOTES)

        with allure.step("Verify response"):
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert len(data["data"]) >= 2

    @allure.title("Get note by ID returns correct note")
    @pytest.mark.smoke
    def test_get_note_by_id(
        self, authenticated_client: ApiClient, note_factory: NoteFactory
    ) -> None:
        """TC-002.3.1: Get note by ID."""
        created = note_factory("Specific Note", "Specific Desc", "Personal")
        note_id = created["id"]

        with allure.step(f"Get note by ID: {note_id}"):
            response = authenticated_client.get(endpoints.note_by_id(note_id))

        with allure.step("Verify note data"):
            assert response.status_code == 200
            data = response.json()["data"]
            assert data["id"] == note_id
            assert data["title"] == "Specific Note"

    @allure.title("Get non-existent note returns error")
    @pytest.mark.regression
    def test_get_note_not_found(self, authenticated_client: ApiClient) -> None:
        """TC-002.3.2: Non-existent note returns 400."""
        response = authenticated_client.get(endpoints.note_by_id("nonexistent123"))
        assert response.status_code == 400


@allure.feature("Notes CRUD")
@allure.story("Update Note")
class TestUpdateNote:
    """Tests for PUT /notes/{id}."""

    @allure.title("Successfully update all note fields")
    @pytest.mark.smoke
    def test_update_note_success(
        self, authenticated_client: ApiClient, note_factory: NoteFactory
    ) -> None:
        """TC-002.4.1: Update all fields."""
        created = note_factory("Original", "Original Desc", "Home")
        note_id = created["id"]

        payload = {
            "title": "Updated Title",
            "description": "Updated Desc",
            "completed": "true",
            "category": "Work",
        }

        with allure.step("Send PUT request"):
            response = authenticated_client.put(endpoints.note_by_id(note_id), data=payload)

        with allure.step("Verify update"):
            assert response.status_code == 200
            data = response.json()["data"]
            assert data["title"] == "Updated Title"
            assert data["completed"] is True
            assert data["category"] == "Work"
            assert data["updated_at"] != created["created_at"]

    @allure.title("Update non-existent note fails")
    @pytest.mark.regression
    def test_update_note_not_found(self, authenticated_client: ApiClient) -> None:
        """TC-002.4.2: Update non-existent note returns 400."""
        payload = NoteUpdateRequest(
            title="Test", description="Test", completed=False, category="Home"
        ).model_dump()
        response = authenticated_client.put(endpoints.note_by_id("nonexistent"), data=payload)
        assert response.status_code == 400


@allure.feature("Notes CRUD")
@allure.story("Delete Note")
class TestDeleteNote:
    """Tests for DELETE /notes/{id}."""

    @allure.title("Successfully delete existing note")
    @pytest.mark.smoke
    def test_delete_note_success(
        self, authenticated_client: ApiClient, note_factory: NoteFactory
    ) -> None:
        """TC-002.5.1: Delete note."""
        created = note_factory("To Delete", "Delete me", "Home")
        note_id = created["id"]

        with allure.step(f"Delete note {note_id}"):
            response = authenticated_client.delete(endpoints.note_by_id(note_id))

        with allure.step("Verify deletion"):
            assert response.status_code == 200
            assert response.json()["success"] is True

        with allure.step("Verify note is gone"):
            get_response = authenticated_client.get(endpoints.note_by_id(note_id))
            assert get_response.status_code == 404

    @allure.title("Delete non-existent note fails")
    @pytest.mark.regression
    def test_delete_note_not_found(self, authenticated_client: ApiClient) -> None:
        """TC-002.5.2: Delete non-existent note returns 400."""
        response = authenticated_client.delete(endpoints.note_by_id("nonexistent"))
        assert response.status_code == 400
