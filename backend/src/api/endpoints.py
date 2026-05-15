"""API endpoint URLs."""

from config.settings import settings

BASE_URL: str = settings.API_BASE_URL

HEALTH_CHECK: str = f"{BASE_URL}/health-check"

USERS_REGISTER: str = f"{BASE_URL}/users/register"
USERS_LOGIN: str = f"{BASE_URL}/users/login"
USERS_PROFILE: str = f"{BASE_URL}/users/profile"
USERS_LOGOUT: str = f"{BASE_URL}/users/logout"
USERS_FORGOT_PASSWORD: str = f"{BASE_URL}/users/forgot-password"
USERS_VERIFY_RESET_TOKEN: str = f"{BASE_URL}/users/verify-reset-password-token"
USERS_RESET_PASSWORD: str = f"{BASE_URL}/users/reset-password"
USERS_CHANGE_PASSWORD: str = f"{BASE_URL}/users/change-password"
USERS_DELETE_ACCOUNT: str = f"{BASE_URL}/users/delete-account"

NOTES: str = f"{BASE_URL}/notes"


def note_by_id(note_id: str) -> str:
    """Return URL for a specific note."""
    return f"{NOTES}/{note_id}"
