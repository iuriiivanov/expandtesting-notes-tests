"""CRUD operations tests for Notes API."""

from collections.abc import Callable
from typing import Any

import allure
import pytest

from backend.src.api import endpoints
from backend.src.api.client import ApiClient
from backend.src.models.note import NoteData, NoteDeleteResponse, NoteResponse, NoteUpdateRequest

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

        with allure.step("Verify note data via Pydantic model"):
            validated = NoteData(**note)
            assert validated.title == "Home Task"
            assert validated.category == "Home"
            assert validated.completed is False
            assert validated.id

    @allure.title("Successfully create note with category Work")
    @pytest.mark.smoke
    def test_create_note_work(
        self, authenticated_client: ApiClient, note_factory: NoteFactory
    ) -> None:
        """TC-002.1.2: Create note category Work."""
        note = note_factory("Work Task", "Do something at work", "Work")
        validated = NoteData(**note)
        assert validated.category == "Work"

    @allure.title("Successfully create note with category Personal")
    @pytest.mark.smoke
    def test_create_note_personal(
        self, authenticated_client: ApiClient, note_factory: NoteFactory
    ) -> None:
        """TC-002.1.3: Create note category Personal."""
        note = note_factory("Personal Task", "Do something personal", "Personal")
        validated = NoteData(**note)
        assert validated.category == "Personal"

    @allure.title("Create note with empty title fails")
    @pytest.mark.regression
    def test_create_note_empty_title(self, authenticated_client: ApiClient) -> None:
        """TC-002.1.4: Empty title returns 400."""
        response = authenticated_client.post(
            endpoints.NOTES, data={"title": "", "description": "desc", "category": "Home"}
        )
        assert response.status_code == 400
        assert response.json()["success"] is False

    @allure.title("Create note without description fails")
    @pytest.mark.regression
    def test_create_note_empty_description(self, authenticated_client: ApiClient) -> None:
        """TC-002.1.5: Create note without description returns 400."""
        response = authenticated_client.post(
            endpoints.NOTES, data={"title": "Test", "description": "", "category": "Home"}
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

    @allure.title("Create note with title exceeding max length fails")
    @pytest.mark.regression
    def test_create_note_long_title(self, authenticated_client: ApiClient) -> None:
        """TC-002.1.8: Create note with title > 100 characters returns 400."""
        long_title = "A" * 101

        with allure.step("Send POST with title exceeding 100 characters"):
            response = authenticated_client.post(
                endpoints.NOTES,
                data={"title": long_title, "description": "Test", "category": "Home"},
            )

        with allure.step("Verify 400 Bad Request with validation message"):
            assert response.status_code == 400
            assert response.json()["success"] is False
            assert "100 characters" in response.json()["message"]

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

    @allure.title("Get all notes without token fails")
    @pytest.mark.regression
    def test_get_all_notes_no_token(self, client: ApiClient) -> None:
        """TC-002.2.2: Get notes list without token returns 401."""
        response = client.get(endpoints.NOTES)
        assert response.status_code == 401
        assert response.json()["success"] is False

    @allure.title("Get notes list when no notes exist returns empty array")
    @pytest.mark.regression
    def test_get_all_notes_empty(self, authenticated_client: ApiClient) -> None:
        """TC-002.2.3: Get notes list when no notes returns 200 with empty data."""
        with allure.step("Get all notes for user with no notes"):
            response = authenticated_client.get(endpoints.NOTES)

        with allure.step("Verify empty array response"):
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["data"] == []

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
            result = NoteResponse(**response.json())
            assert result.data.id == note_id
            assert result.data.title == "Specific Note"
            assert result.data.category == "Personal"
            assert result.data.completed is False

    @allure.title("Get non-existent note returns error")
    @pytest.mark.regression
    def test_get_note_not_found(self, authenticated_client: ApiClient) -> None:
        """TC-002.3.2: Non-existent note returns 400."""
        response = authenticated_client.get(endpoints.note_by_id("nonexistent123"))
        assert response.status_code == 400

    @allure.title("User cannot access another user's note")
    @pytest.mark.integration
    def test_get_note_isolation(
        self, authenticated_client: ApiClient, client: ApiClient, test_password: str
    ) -> None:
        """TC-002.3.3: User cannot access another user's note."""
        from backend.src.api.auth import login_user, register_user

        email_a = f"isolation_{__import__('os').urandom(4).hex()}@example.com"
        register_user(client, name="UserA", email=email_a, password=test_password)
        token_a = login_user(client, email=email_a, password=test_password)
        client_a = ApiClient(token=token_a)

        note_response = client_a.post(
            endpoints.NOTES, data={"title": "Private", "description": "Secret", "category": "Home"}
        )
        note_id = note_response.json()["data"]["id"]

        with allure.step("User B attempts to access User A's note"):
            response = authenticated_client.get(endpoints.note_by_id(note_id))

        with allure.step("Verify access denied"):
            assert response.status_code == 404

    @allure.title("Get note by ID without token fails")
    @pytest.mark.regression
    def test_get_note_by_id_no_token(self, client: ApiClient) -> None:
        """TC-002.3.4: Get note by ID without token returns 401."""
        response = client.get(endpoints.note_by_id("some-id"))
        assert response.status_code == 401
        assert response.json()["success"] is False


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
            result = NoteResponse(**response.json())
            assert result.data.title == "Updated Title"
            assert result.data.completed is True
            assert result.data.category == "Work"
            assert result.data.updated_at != created["updated_at"]

    @allure.title("Update non-existent note fails")
    @pytest.mark.regression
    def test_update_note_not_found(self, authenticated_client: ApiClient) -> None:
        """TC-002.4.2: Update non-existent note returns 400."""
        payload = NoteUpdateRequest(
            title="Test", description="Test", completed=False, category="Home"
        ).model_dump()
        response = authenticated_client.put(endpoints.note_by_id("nonexistent"), data=payload)
        assert response.status_code == 400

    @allure.title("Update note without token fails")
    @pytest.mark.regression
    def test_update_note_no_token(self, client: ApiClient) -> None:
        """TC-002.4.3: Update note without token returns 401."""
        response = client.put(
            endpoints.note_by_id("some-id"),
            data={"title": "Test", "description": "Test", "completed": "true", "category": "Home"},
        )
        assert response.status_code == 401
        assert response.json()["success"] is False

    @allure.title("Update note with invalid category fails")
    @pytest.mark.regression
    def test_update_note_invalid_category(
        self, authenticated_client: ApiClient, note_factory: NoteFactory
    ) -> None:
        """TC-002.4.4: Update note with invalid category returns 400."""
        created = note_factory("Original", "Original Desc", "Home")
        note_id = created["id"]

        payload = {
            "title": "Updated",
            "description": "Updated",
            "completed": "false",
            "category": "InvalidCategory",
        }

        with allure.step("Send PUT with invalid category"):
            response = authenticated_client.put(endpoints.note_by_id(note_id), data=payload)

        with allure.step("Verify 400 Bad Request"):
            assert response.status_code == 400
            assert response.json()["success"] is False

    @allure.title("User cannot update another user's note")
    @pytest.mark.integration
    def test_update_note_isolation(
        self, authenticated_client: ApiClient, client: ApiClient, test_password: str
    ) -> None:
        """TC-002.4.5: User cannot update another user's note."""
        from backend.src.api.auth import login_user, register_user

        email_a = f"isolation_{__import__('os').urandom(4).hex()}@example.com"
        register_user(client, name="UserA", email=email_a, password=test_password)
        token_a = login_user(client, email=email_a, password=test_password)
        client_a = ApiClient(token=token_a)

        note_response = client_a.post(
            endpoints.NOTES, data={"title": "Private", "description": "Secret", "category": "Home"}
        )
        note_id = note_response.json()["data"]["id"]

        payload = {
            "title": "Hacked",
            "description": "Hacked",
            "completed": "true",
            "category": "Work",
        }

        with allure.step("User B attempts to update User A's note"):
            response = authenticated_client.put(endpoints.note_by_id(note_id), data=payload)

        with allure.step("Verify access denied"):
            assert response.status_code == 404


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
            result = NoteDeleteResponse(**response.json())
            assert result.success is True

        with allure.step("Verify note is gone"):
            get_response = authenticated_client.get(endpoints.note_by_id(note_id))
            assert get_response.status_code == 404

    @allure.title("Delete non-existent note fails")
    @pytest.mark.regression
    def test_delete_note_not_found(self, authenticated_client: ApiClient) -> None:
        """TC-002.5.2: Delete non-existent note returns 400."""
        response = authenticated_client.delete(endpoints.note_by_id("nonexistent"))
        assert response.status_code == 400

    @allure.title("Delete note without token fails")
    @pytest.mark.regression
    def test_delete_note_no_token(self, client: ApiClient) -> None:
        """TC-002.5.3: Delete note without token returns 401."""
        response = client.delete(endpoints.note_by_id("some-id"))
        assert response.status_code == 401
        assert response.json()["success"] is False

    @allure.title("Re-delete already deleted note fails")
    @pytest.mark.regression
    def test_delete_note_twice(
        self, authenticated_client: ApiClient, note_factory: NoteFactory
    ) -> None:
        """TC-002.5.5: Re-delete already deleted note returns 404."""
        created = note_factory("To Delete Twice", "Delete me", "Home")
        note_id = created["id"]

        with allure.step("Delete note first time"):
            first_response = authenticated_client.delete(endpoints.note_by_id(note_id))
            assert first_response.status_code == 200

        with allure.step("Attempt to delete same note again"):
            second_response = authenticated_client.delete(endpoints.note_by_id(note_id))

        with allure.step("Verify 400 Bad Request"):
            assert second_response.status_code == 404
            assert second_response.json()["success"] is False

    @allure.title("User cannot delete another user's note")
    @pytest.mark.integration
    def test_delete_note_isolation(
        self, authenticated_client: ApiClient, client: ApiClient, test_password: str
    ) -> None:
        """TC-002.5.4: User cannot delete another user's note."""
        from backend.src.api.auth import login_user, register_user

        email_a = f"isolation_{__import__('os').urandom(4).hex()}@example.com"
        register_user(client, name="UserA", email=email_a, password=test_password)
        token_a = login_user(client, email=email_a, password=test_password)
        client_a = ApiClient(token=token_a)

        note_response = client_a.post(
            endpoints.NOTES, data={"title": "Private", "description": "Secret", "category": "Home"}
        )
        note_id = note_response.json()["data"]["id"]

        with allure.step("User B attempts to delete User A's note"):
            response = authenticated_client.delete(endpoints.note_by_id(note_id))

        with allure.step("Verify access denied"):
            assert response.status_code == 404
