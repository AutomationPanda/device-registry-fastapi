"""
This module provides top-level routes.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from fastapi import APIRouter
from fastapi.responses import FileResponse, RedirectResponse


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter()


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get("/", summary="Redirect to the docs")
def get_root():
  """
  Redirects to '/docs'.
  """

  return RedirectResponse("/docs")


@router.get("/favicon.ico", include_in_schema=False)
def get_favicon():
  """
  Provides the app's favicon.
  """

  return FileResponse('img/favicon.ico')


@router.get("/logo.png", include_in_schema=False)
def get_logo():
  """
  Provides the app's logo.
  """

  return FileResponse('img/logo.png')
