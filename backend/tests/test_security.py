"""Security tests."""

import allure
import pytest

from backend.src.api import endpoints
from backend.src.api.auth import register_user
from backend.src.api.client import ApiClient
from backend.src.utils.helpers import generate_unique_email, generate_unique_name


@allure.feature("Security")
@allure.story("Authorization")
class TestSecurity:
    """Security-related tests."""

    @allure.title("Access with fake token returns 401")
    @pytest.mark.regression
    def test_fake_token_access(self, client: ApiClient) -> None:
        """TC-005.1.2: Fake token rejected."""
        client.set_token("fake-token-12345")
        response = client.get(endpoints.NOTES)
        assert response.status_code == 401

    @allure.title("User cannot access another user's notes")
    @pytest.mark.integration
    def test_note_isolation(self, client: ApiClient) -> None:
        """TC-005.1.3: Data isolation between users."""
        email_a = generate_unique_email()
        password = "TestPass123!"
        register_user(client, name=generate_unique_name(), email=email_a, password=password)

        from backend.src.api.auth import login_user

        token_a = login_user(client, email=email_a, password=password)

        client_a = ApiClient(token=token_a)
        note_response = client_a.post(
            endpoints.NOTES, data={"title": "Private", "description": "Secret", "category": "Home"}
        )
        note_id = note_response.json()["data"]["id"]

        email_b = generate_unique_email()
        register_user(client, name=generate_unique_name(), email=email_b, password=password)
        token_b = login_user(client, email=email_b, password=password)
        client_b = ApiClient(token=token_b)

        with allure.step("User B attempts to access User A's note"):
            response = client_b.get(endpoints.note_by_id(note_id))

        with allure.step("Verify access denied"):
            assert response.status_code in (400, 401, 403, 404)

    @allure.title("SQL injection attempt is handled safely")
    @pytest.mark.regression
    def test_sql_injection_title(self, authenticated_client: ApiClient) -> None:
        """TC-005.1.4: SQL injection in title handled safely."""
        malicious_title = "' OR '1'='1"
        response = authenticated_client.post(
            endpoints.NOTES,
            data={"title": malicious_title, "description": "Test", "category": "Home"},
        )

        assert response.status_code in (200, 400)
        if response.status_code == 200:
            get_response = authenticated_client.get(endpoints.NOTES)
            notes = get_response.json()["data"]
            assert all(note["title"] == malicious_title for note in notes)
