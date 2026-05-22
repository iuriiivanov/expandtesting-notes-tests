"""Health check tests."""

import allure
import pytest
import requests

from backend.src.api import endpoints
from backend.src.models.health import HealthResponse


@allure.feature("Health Check")
@allure.story("API Availability")
@pytest.mark.smoke
def test_health_check() -> None:
    """TC-006.1.1: Verify API health status."""
    with allure.step("Send GET request to /health-check"):
        response = requests.get(endpoints.HEALTH_CHECK, timeout=10)

    with allure.step("Verify response status is 200"):
        assert response.status_code == 200

    with allure.step("Verify response structure and data"):
        result = HealthResponse(**response.json())
        assert result.success is True
        assert result.status == 200


@allure.feature("Health Check")
@allure.story("API Availability")
@pytest.mark.regression
def test_health_check_response_time() -> None:
    """TC-006.1.2: Health check response time under 2 seconds."""
    import time

    with allure.step("Send GET request to /health-check and measure time"):
        start = time.time()
        response = requests.get(endpoints.HEALTH_CHECK, timeout=10)
        elapsed = time.time() - start

    with allure.step(f"Verify response time: {elapsed:.2f}s"):
        assert response.status_code == 200
        assert elapsed < 2.0
