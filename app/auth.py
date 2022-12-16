"""
This module provides security and authentication.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import secrets

from . import users
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


# --------------------------------------------------------------------------------
# Globals
# --------------------------------------------------------------------------------

security = HTTPBasic()


# --------------------------------------------------------------------------------
# Authentication Checkers
# --------------------------------------------------------------------------------

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
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
