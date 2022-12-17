"""
This module is the main module for the FastAPI app.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse

from .routers import auth, devices, status


# --------------------------------------------------------------------------------
# App Creation
# --------------------------------------------------------------------------------

app = FastAPI()
app.include_router(auth.router)
app.include_router(devices.router)
app.include_router(status.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=["*"],
)


# --------------------------------------------------------------------------------
# Top-Level Routes
# --------------------------------------------------------------------------------

@app.get("/favicon.ico", include_in_schema=False)
def get_favicon():
  """
  Provides the app's favicon.
  """

  return FileResponse('app/favicon.ico')


@app.get("/")
def get_root():
  """
  Redirects to '/docs'.
  """

  return RedirectResponse("/docs")
