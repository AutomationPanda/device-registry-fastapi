"""
This module provides security and authentication.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import jwt
import secrets

from . import users, secret_key
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# --------------------------------------------------------------------------------
# Globals
# --------------------------------------------------------------------------------

securityBasic = HTTPBasic(auto_error=False)
securityBearer = HTTPBearer(auto_error=False)


# --------------------------------------------------------------------------------
# Exceptions
# --------------------------------------------------------------------------------

class UnauthorizedException(HTTPException):
  def __init__(self):
    super().__init__(status.HTTP_401_UNAUTHORIZED, "Unauthorized")


# --------------------------------------------------------------------------------
# Serializers
# --------------------------------------------------------------------------------

def serialize_token(username: str):
  return jwt.encode({"username": username}, secret_key, algorithm="HS256")


def deserialize_token(token: str):
  try:
    data = jwt.decode(token, secret_key, algorithms=["HS256"])
    return data['username']
  except:
    return None


# --------------------------------------------------------------------------------
# Authentication Checkers
# --------------------------------------------------------------------------------

def get_current_username(
  basic: HTTPBasicCredentials = Depends(securityBasic),
  bearer: HTTPAuthorizationCredentials = Depends(securityBearer)):

  if basic:
    if basic.username in users:
      if secrets.compare_digest(basic.password, users[basic.username]):
        return basic.username

  elif bearer:
    if current_username := deserialize_token(bearer.credentials):
      if current_username in users:
        return current_username
    
  raise UnauthorizedException()
