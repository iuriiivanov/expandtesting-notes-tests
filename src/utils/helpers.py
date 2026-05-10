"""Helper utilities."""

import uuid


def generate_unique_email() -> str:
    """Generate a unique email address for testing."""
    return f"test_{uuid.uuid4().hex[:8]}@example.com"


def generate_unique_name() -> str:
    """Generate a unique name for testing."""
    return f"TestUser_{uuid.uuid4().hex[:8]}"
