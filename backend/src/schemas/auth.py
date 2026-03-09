"""Pydantic schemas for authentication endpoints."""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import re


class UserRegistrationRequest(BaseModel):
    """Request schema for user registration."""
    email: EmailStr = Field(..., description="User email address")
    phone: Optional[str] = Field(None, description="User phone number")
    password: str = Field(..., min_length=8, description="User password")
    preferred_language: str = Field("en", description="Preferred language code")

    @validator('phone')
    def validate_phone(cls, v):
        if v is not None:
            # Simple phone validation - adjust regex as needed
            phone_pattern = r'^\+?[\d\s\-\(\)]{10,15}$'
            if not re.match(phone_pattern, v.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')):
                raise ValueError('Invalid phone number format')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('Password must contain at least one letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v


class UserLoginRequest(BaseModel):
    """Request schema for user login."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class TokenResponse(BaseModel):
    """Response schema for authentication tokens."""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class TokenRefreshRequest(BaseModel):
    """Request schema for token refresh."""
    refresh_token: str = Field(..., description="Refresh token")


class UserResponse(BaseModel):
    """Response schema for user information."""
    id: str
    email: str
    phone: Optional[str] = None
    preferred_language: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class UserProfileUpdateRequest(BaseModel):
    """Request schema for updating user profile."""
    phone: Optional[str] = Field(None, description="User phone number")
    preferred_language: Optional[str] = Field(None, description="Preferred language code")

    @validator('phone')
    def validate_phone(cls, v):
        if v is not None:
            phone_pattern = r'^\+?[\d\s\-\(\)]{10,15}$'
            if not re.match(phone_pattern, v.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')):
                raise ValueError('Invalid phone number format')
        return v