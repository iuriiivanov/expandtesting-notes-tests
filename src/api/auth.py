"""Authentication helpers."""

from typing import Any

import allure

from src.api import endpoints
from src.api.client import ApiClient
from src.models.user import UserLoginRequest, UserRegisterRequest


@allure.step("Register new user with name={name}, email={email}")
def register_user(client: ApiClient, name: str, email: str, password: str) -> dict[str, Any]:
    """Register a new user and return response JSON."""
    payload = UserRegisterRequest(name=name, email=email, password=password).model_dump()
    response = client.post(endpoints.USERS_REGISTER, data=payload)
    response.raise_for_status()
    result: dict[str, Any] = response.json()
    return result


@allure.step("Login user with email={email}")
def login_user(client: ApiClient, email: str, password: str) -> str:
    """Login user and return auth token."""
    payload = UserLoginRequest(email=email, password=password).model_dump()
    response = client.post(endpoints.USERS_LOGIN, data=payload)
    response.raise_for_status()
    data: dict[str, Any] = response.json()
    token: str = data["data"]["token"]
    return token


@allure.step("Logout current user")
def logout_user(client: ApiClient) -> None:
    """Logout current user."""
    response = client.delete(endpoints.USERS_LOGOUT)
    response.raise_for_status()


@allure.step("Delete user account")
def delete_account(client: ApiClient) -> None:
    """Delete current user account."""
    response = client.delete(endpoints.USERS_DELETE_ACCOUNT)
    response.raise_for_status()
