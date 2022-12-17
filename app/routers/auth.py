"""
This module provides routes for authentication.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from ..auth import get_current_username, serialize_token

from fastapi import APIRouter, Depends
from pydantic import BaseModel


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter()


# --------------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------------

class Token(BaseModel):
  token: str


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get("/authenticate", summary="Generate an auth token", response_model=Token)
@router.get("/authenticate/", include_in_schema=False)
@router.head("/authenticate", summary="Generate an auth token")
@router.head("/authenticate/", include_in_schema=False)
def get_authenticate(username: str = Depends(get_current_username)):
  """
  Uses HTTP basic authentication to generate an authentication token.
  Any resource that requires authentication can use either basic auth or this token.
  """

  token = serialize_token(username)
  return Token(token=token)