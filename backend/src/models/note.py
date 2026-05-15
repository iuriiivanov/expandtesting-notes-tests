"""Pydantic models for Notes API."""

from pydantic import BaseModel, Field


class NoteCreateRequest(BaseModel):
    """Request model for creating a note."""

    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    category: str = Field(..., pattern="^(Home|Work|Personal)$")


class NoteUpdateRequest(BaseModel):
    """Request model for updating a note."""

    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    completed: bool
    category: str = Field(..., pattern="^(Home|Work|Personal)$")


class NoteStatusUpdateRequest(BaseModel):
    """Request model for updating note status."""

    completed: bool


class NoteData(BaseModel):
    """Note data returned by API."""

    id: str
    title: str
    description: str
    completed: bool
    created_at: str
    updated_at: str
    category: str
    user_id: str


class NoteResponse(BaseModel):
    """Response model for single note operations."""

    success: bool
    status: int
    message: str
    data: NoteData


class NotesListResponse(BaseModel):
    """Response model for list of notes."""

    success: bool
    status: int
    message: str
    data: list[NoteData]


class NoteDeleteResponse(BaseModel):
    """Response model for note deletion."""

    success: bool
    status: int
    message: str
