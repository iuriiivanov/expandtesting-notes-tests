"""Validation and error handling tests."""

import allure
import pytest

from src.api import endpoints
from src.api.client import ApiClient


@allure.feature("Validation")
@allure.story("Error Handling")
class TestValidation:
    """Tests for validation and error responses."""

    @allure.title("Request to non-existent endpoint returns 404")
    @pytest.mark.regression
    def test_nonexistent_endpoint(self, client: ApiClient) -> None:
        """TC-004.1.3: Non-existent endpoint."""
        response = client.get(f"{endpoints.BASE_URL}/nonexistent")
        assert response.status_code == 404

    @allure.title("All error responses follow standard format")
    @pytest.mark.regression
    def test_error_response_structure(self, client: ApiClient) -> None:
        """Verify error response structure."""
        response = client.get(endpoints.NOTES)

        with allure.step("Verify error structure"):
            assert response.status_code == 401
            data = response.json()
            assert "success" in data
            assert "status" in data
            assert "message" in data
            assert data["success"] is False
            assert isinstance(data["status"], int)

