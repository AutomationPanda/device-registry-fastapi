"""
This module is the main module for the FastAPI app.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
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
# OpenAPI Customization
# --------------------------------------------------------------------------------

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Device Registry Service",
        version="2.0.0",
        description="A FastAPI web service for managing a smart device registry.",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "logo.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# --------------------------------------------------------------------------------
# Top-Level Routes
# --------------------------------------------------------------------------------

@app.get("/", summary="Redirect to the docs")
def get_root():
  """
  Redirects to '/docs'.
  """

  return RedirectResponse("/docs")


@app.get("/favicon.ico", include_in_schema=False)
def get_favicon():
  """
  Provides the app's favicon.
  """

  return FileResponse('img/favicon.ico')


@app.get("/logo.png", include_in_schema=False)
def get_logo():
  """
  Provides the app's logo.
  """

  return FileResponse('img/logo.png')
