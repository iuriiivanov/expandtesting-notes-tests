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

    @allure.title("Access with expired token returns 401")
    @pytest.mark.regression
    def test_expired_token_access(self, authenticated_client: ApiClient) -> None:
        """TC-005.1.1: Access with expired/invalidated token returns 401."""
        with allure.step("Logout to invalidate token"):
            logout_response = authenticated_client.delete(endpoints.USERS_LOGOUT)
            assert logout_response.status_code == 200

        with allure.step("Attempt to access protected endpoint with invalidated token"):
            response = authenticated_client.get(endpoints.NOTES)

        with allure.step("Verify 401 Unauthorized"):
            assert response.status_code == 401
            assert response.json()["success"] is False

    @allure.title("Access with fake token returns 401")
    @pytest.mark.regression
    def test_fake_token_access(self, client: ApiClient) -> None:
        """TC-005.1.2: Fake token rejected."""
        client.set_token("fake-token-12345")
        response = client.get(endpoints.NOTES)
        assert response.status_code == 401

    @allure.title("User cannot access another user's notes")
    @pytest.mark.integration
    def test_note_isolation(self, client: ApiClient, test_password: str) -> None:
        """TC-005.1.3: Data isolation between users."""
        email_a = generate_unique_email()
        password = test_password
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
            assert response.status_code == 404

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
            with allure.step("Verify note was saved as plain text, not executed as SQL"):
                note_id = response.json()["data"]["id"]
                get_response = authenticated_client.get(endpoints.note_by_id(note_id))
                assert get_response.status_code == 200
                assert get_response.json()["data"]["title"] == malicious_title
