"""Authentication utilities for JWT token management."""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
import hashlib
import secrets
from fastapi import HTTPException, status

from ..config import settings


def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with salt."""
    # Generate a random salt
    salt = secrets.token_hex(16)
    # Create hash with salt
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    # Return salt + hash combined
    return f"{salt}:{password_hash}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    try:
        # Split salt and hash
        salt, stored_hash = hashed_password.split(':', 1)
        # Hash the plain password with the stored salt
        password_hash = hashlib.sha256((plain_password + salt).encode()).hexdigest()
        # Compare hashes
        return password_hash == stored_hash
    except ValueError:
        # Invalid hash format
        return False


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire, "type": "access"})
    
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """Create a JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=30)  # Refresh tokens last 30 days
    to_encode.update({"exp": expire, "type": "refresh"})
    
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Dict[str, Any]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        
        # Check token type
        if payload.get("type") != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        # Check expiration
        exp = payload.get("exp")
        if exp is None or datetime.utcnow() > datetime.fromtimestamp(exp):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        
        return payload
        
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


def get_user_id_from_token(token: str) -> str:
    """Extract user ID from JWT token."""
    payload = verify_token(token)
    user_id = payload.get("sub")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    return user_id