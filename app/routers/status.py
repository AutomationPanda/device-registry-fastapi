"""
This module provides routes for status.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import time

from .. import start_time
from fastapi import APIRouter


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter()


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get("/status")
@router.head("/status")
def get_status():
  """
  Provides uptime information about the web service.
  """
  
  return {
    'online': True,
    'uptime': round(time.time() - start_time, 3)
  }