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

@router.get("/authenticate", response_model=Token)
@router.head("/authenticate")
def get_authenticate(username: str = Depends(get_current_username)):
  """
  Uses HTTP basic authentication to generate an authentication token.
  Any resource that requires authentication can use either basic auth or this token.
  """

  token = serialize_token(username)
  return Token(token=token)