"""User profile tests."""

import allure
import pytest

from backend.src.api import endpoints
from backend.src.api.client import ApiClient
from backend.src.models.user import UserProfileResponse, UserProfileUpdateRequest


@allure.feature("Authentication")
@allure.story("User Profile")
class TestUserProfile:
    """Tests for user profile endpoint."""

    @allure.title("Retrieve profile of authenticated user")
    @pytest.mark.smoke
    def test_get_profile_success(self, authenticated_client: ApiClient) -> None:
        """TC-001.3.1: Retrieve profile of an authenticated user."""
        with allure.step("Send GET /users/profile with valid token"):
            response = authenticated_client.get(endpoints.USERS_PROFILE)

        with allure.step("Verify successful response"):
            assert response.status_code == 200
            result = UserProfileResponse(**response.json())
            assert result.success is True
            assert result.data.name
            assert result.data.email

    @allure.title("Retrieve profile without token fails")
    @pytest.mark.regression
    def test_get_profile_no_token(self, client: ApiClient) -> None:
        """TC-001.3.2: Retrieve profile without token returns 401."""
        with allure.step("Send GET /users/profile without x-auth-token"):
            response = client.get(endpoints.USERS_PROFILE)

        with allure.step("Verify 401 Unauthorized"):
            assert response.status_code == 401
            assert response.json()["success"] is False

    @allure.title("Update profile with valid data")
    @pytest.mark.smoke
    def test_update_profile_success(self, authenticated_client: ApiClient) -> None:
        """TC-001.3.3: Update profile with valid data."""
        new_name = "UpdatedName"
        new_phone = "1234567890"
        new_company = "TestCorp"

        payload = UserProfileUpdateRequest(
            name=new_name, phone=new_phone, company=new_company
        ).model_dump()

        with allure.step("Send PATCH /users/profile with new data"):
            response = authenticated_client.patch(endpoints.USERS_PROFILE, data=payload)

        with allure.step("Verify successful update"):
            assert response.status_code == 200
            result = UserProfileResponse(**response.json())
            assert result.success is True
            assert result.data.name == new_name
            assert result.data.phone == new_phone
            assert result.data.company == new_company

    @allure.title("Update profile with empty name fails")
    @pytest.mark.regression
    def test_update_profile_empty_name(self, authenticated_client: ApiClient) -> None:
        """TC-001.3.4: Update profile with empty name returns 400."""
        payload = {"name": "", "phone": "", "company": ""}

        with allure.step("Send PATCH /users/profile with empty name"):
            response = authenticated_client.patch(endpoints.USERS_PROFILE, data=payload)

        with allure.step("Verify 400 Bad Request"):
            assert response.status_code == 400
            assert response.json()["success"] is False
