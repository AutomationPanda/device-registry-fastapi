"""
This module is the main module for the FastAPI app.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse

from .routers import status


# --------------------------------------------------------------------------------
# App Creation
# --------------------------------------------------------------------------------

app = FastAPI()
app.include_router(status.router)


# --------------------------------------------------------------------------------
# Top-Level Routes
# --------------------------------------------------------------------------------

@app.get("/favicon.ico", include_in_schema=False)
def get_favicon():
  return FileResponse('app/favicon.ico')


@app.get("/")
def get_root():
  return RedirectResponse("/docs")
