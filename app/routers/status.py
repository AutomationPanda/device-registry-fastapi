"""
This module provides routes for status.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import time

from . import START_TIME
from fastapi import APIRouter


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter()


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get("/status")
def get_status():
  """
  Provides uptime information about the web service.
  """
  
  return {
    'online': True,
    'uptime': round(time.time() - START_TIME, 3)
  }