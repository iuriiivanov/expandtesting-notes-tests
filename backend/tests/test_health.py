"""Health check tests."""

import allure
import pytest
import requests
from api import endpoints


@allure.feature("Health Check")
@allure.story("API Availability")
@pytest.mark.smoke
def test_health_check() -> None:
    """Verify API health endpoint returns success."""
    with allure.step("Send GET request to /health-check"):
        response = requests.get(endpoints.HEALTH_CHECK, timeout=10)

    with allure.step("Verify response status is 200"):
        assert response.status_code == 200

    with allure.step("Verify response contains success=true"):
        data = response.json()
        assert data["success"] is True
        assert data["status"] == 200
