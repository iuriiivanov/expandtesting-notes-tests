"""Pydantic models for User API."""

from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    """Request model for user registration."""

    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=1)


class UserLoginRequest(BaseModel):
    """Request model for user login."""

    email: EmailStr
    password: str = Field(..., min_length=1)


class UserProfileUpdateRequest(BaseModel):
    """Request model for profile update."""

    name: str = Field(..., min_length=1)
    phone: str | None = None
    company: str | None = None


class UserData(BaseModel):
    """User data returned by API."""

    id: str | int
    name: str
    email: EmailStr


class UserProfileData(BaseModel):
    """User profile data returned by API."""

    id: str
    name: str
    email: EmailStr
    phone: str | None = None
    company: str | None = None


class UserLoginData(BaseModel):
    """Login response data."""

    id: str
    email: EmailStr
    name: str
    token: str


class UserRegisterResponse(BaseModel):
    """Response model for user registration."""

    success: bool
    status: int
    message: str
    data: UserData


class UserLoginResponse(BaseModel):
    """Response model for user login."""

    success: bool
    status: int
    message: str
    data: UserLoginData


class UserProfileResponse(BaseModel):
    """Response model for user profile."""

    success: bool
    status: int
    message: str
    data: UserProfileData


class UserLogoutResponse(BaseModel):
    """Response model for user logout."""

    success: bool
    status: int
    message: str


class UserDeleteResponse(BaseModel):
    """Response model for user deletion."""

    success: bool
    status: int
    message: str
