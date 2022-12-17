"""
This module provides routes for status.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import time

from .. import start_time
from fastapi import APIRouter
from pydantic import BaseModel


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter()


# --------------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------------

class Status(BaseModel):
  online: bool
  start_time: float
  uptime: float


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get("/status", summary="Get the status of the service", response_model=Status)
@router.get("/status/", include_in_schema=False)
@router.head("/status", summary="Get the status of the service")
@router.head("/status/", include_in_schema=False)
def get_status():
  """
  Provides uptime information about the web service.
  """

  return Status(
    online=True,
    start_time=start_time,
    uptime=round(time.time() - start_time, 3)
  )