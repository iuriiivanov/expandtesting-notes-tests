"""Authentication and user management tests."""

import allure
import pytest

from backend.src.api import endpoints
from backend.src.api.auth import register_user
from backend.src.api.client import ApiClient
from backend.src.models.user import UserLoginResponse, UserRegisterResponse
from backend.src.utils.helpers import generate_unique_email, generate_unique_name


@allure.feature("Authentication")
@allure.story("User Registration")
class TestUserRegistration:
    """Tests for user registration endpoint."""

    @allure.title("Successfully register a new user")
    @pytest.mark.smoke
    def test_register_user_success(self, client: ApiClient, test_password: str) -> None:
        """TC-001.1.1: Successful user registration."""
        email = generate_unique_email()
        password = test_password
        name = generate_unique_name()

        with allure.step("Send registration request"):
            response = client.post(
                endpoints.USERS_REGISTER, data={"name": name, "email": email, "password": password}
            )

        with allure.step("Verify status code 201"):
            assert response.status_code == 201

        with allure.step("Verify response structure and data"):
            result = UserRegisterResponse(**response.json())
            assert result.success is True
            assert result.status == 201
            assert result.data.email == email
            assert result.data.name == name
            assert result.data.id

    @allure.title("Register with duplicate email fails")
    @pytest.mark.regression
    def test_register_duplicate_email(self, client: ApiClient, test_password: str) -> None:
        """TC-001.1.2: Registration with existing email fails."""
        email = generate_unique_email()
        password = test_password
        name = generate_unique_name()

        with allure.step("Register first user"):
            register_user(client, name=name, email=email, password=password)

        with allure.step("Attempt to register with same email"):
            response = client.post(
                endpoints.USERS_REGISTER,
                data={"name": generate_unique_name(), "email": email, "password": password},
            )

        with allure.step("Verify error response"):
            assert response.status_code == 409
            data = response.json()
            assert data["success"] is False

    @allure.title("Register with empty name fails")
    @pytest.mark.regression
    def test_register_empty_name(self, client: ApiClient) -> None:
        """TC-001.1.3: Registration with empty name fails."""
        with allure.step("Send registration with empty name"):
            response = client.post(
                endpoints.USERS_REGISTER,
                data={"name": "", "email": generate_unique_email(), "password": "pass"},
            )

        with allure.step("Verify 400 Bad Request"):
            assert response.status_code == 400
            assert response.json()["success"] is False

    @allure.title("Register with invalid email fails")
    @pytest.mark.regression
    def test_register_invalid_email(self, client: ApiClient) -> None:
        """TC-001.1.4: Registration with invalid email fails."""
        with allure.step("Send registration with invalid email"):
            response = client.post(
                endpoints.USERS_REGISTER,
                data={"name": "Test", "email": "invalid-email", "password": "pass"},
            )

        with allure.step("Verify 400 Bad Request"):
            assert response.status_code == 400

    @allure.title("Register without required fields fails")
    @pytest.mark.regression
    def test_register_missing_fields(self, client: ApiClient) -> None:
        """TC-001.1.6: Registration without required fields returns 400."""
        with allure.step("Send registration without password"):
            response = client.post(
                endpoints.USERS_REGISTER, data={"name": "Test", "email": generate_unique_email()}
            )

        with allure.step("Verify 400 Bad Request"):
            assert response.status_code == 400
            assert response.json()["success"] is False


@allure.feature("Authentication")
@allure.story("User Login")
class TestUserLogin:
    """Tests for user login endpoint."""

    @allure.title("Successfully login with valid credentials")
    @pytest.mark.smoke
    def test_login_success(self, client: ApiClient, test_password: str) -> None:
        """TC-001.2.1: Successful login."""
        email = generate_unique_email()
        password = test_password
        name = generate_unique_name()

        with allure.step("Register user first"):
            register_user(client, name=name, email=email, password=password)

        with allure.step("Login with credentials"):
            response = client.post(
                endpoints.USERS_LOGIN, data={"email": email, "password": password}
            )

        with allure.step("Verify successful login"):
            assert response.status_code == 200
            result = UserLoginResponse(**response.json())
            assert result.success is True
            assert result.data.token
            assert result.data.email == email

    @allure.title("Login with wrong password fails")
    @pytest.mark.regression
    def test_login_wrong_password(self, client: ApiClient, test_password: str) -> None:
        """TC-001.2.2: Login with wrong password returns 401."""
        email = generate_unique_email()
        password = test_password
        name = generate_unique_name()

        with allure.step("Register user"):
            register_user(client, name=name, email=email, password=password)

        with allure.step("Attempt login with wrong password"):
            response = client.post(
                endpoints.USERS_LOGIN, data={"email": email, "password": "WrongPass123!"}
            )

        with allure.step("Verify 401 Unauthorized"):
            assert response.status_code == 401
            assert response.json()["success"] is False

    @allure.title("Login without token access to protected endpoint fails")
    @pytest.mark.regression
    def test_access_without_token(self, client: ApiClient) -> None:
        """TC-005.1.1: Access without token returns 401."""
        with allure.step("Request profile without authentication"):
            response = client.get(endpoints.USERS_PROFILE)

        with allure.step("Verify 401 Unauthorized"):
            assert response.status_code == 401
            assert (
                response.json()["message"]
                == "No authentication token specified in x-auth-token header"
            )


@allure.feature("Authentication")
@allure.story("User Logout")
class TestUserLogout:
    """Tests for user logout."""

    @allure.title("Successfully logout user")
    @pytest.mark.smoke
    def test_logout_success(self, authenticated_client: ApiClient) -> None:
        """TC-001.6.1: Successful logout."""
        with allure.step("Logout user"):
            response = authenticated_client.delete(endpoints.USERS_LOGOUT)

        with allure.step("Verify successful logout"):
            assert response.status_code == 200
            assert response.json()["success"] is True

        with allure.step("Verify token is invalidated"):
            profile_response = authenticated_client.get(endpoints.USERS_PROFILE)
            assert profile_response.status_code == 401
