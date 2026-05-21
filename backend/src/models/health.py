"""Pydantic models for Health Check API."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""

    success: bool
    status: int
    message: str
