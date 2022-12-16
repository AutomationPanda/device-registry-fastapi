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
# Authentication Checkers
# --------------------------------------------------------------------------------

def get_current_username(
  credentials: HTTPBasicCredentials = Depends(securityBasic),
  authorization: HTTPAuthorizationCredentials = Depends(securityBearer)):

  if credentials:
    current_username = credentials.username.encode("utf8")
    current_password = credentials.password.encode("utf8")

    if current_username in users:
      correct_password = users[current_username]
      if secrets.compare_digest(current_password, correct_password):
        return credentials.username

    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect email or password",
      headers={"WWW-Authenticate": "Basic"},
    )
  
  elif authorization:
    current_username = deserialize_token(authorization.credentials)

    if current_username in users:
      return current_username
    
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
    )
  
  else:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Unauthorized",
    )


# --------------------------------------------------------------------------------
# Serializers
# --------------------------------------------------------------------------------

def serialize_token(username: str):
  return jwt.encode({"username": username}, secret_key, algorithm="HS256")


def deserialize_token(token: str):
  try:
    data = jwt.decode(token, secret_key, algorithms=["HS256"])
  except:
    return None
  if 'username' in data:
    return data['username']