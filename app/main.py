"""
This module is the main module for the FastAPI app.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from fastapi import FastAPI, Request, status as fastapi_status
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from .routers import auth, devices, root, status


# --------------------------------------------------------------------------------
# App Creation
# --------------------------------------------------------------------------------

app = FastAPI()
app.include_router(auth.router)
app.include_router(devices.router)
app.include_router(root.router)
app.include_router(status.router)


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
# Exception Overrides
# --------------------------------------------------------------------------------

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
  return JSONResponse(
    status_code=fastapi_status.HTTP_422_UNPROCESSABLE_ENTITY,
    content={
      "detail": "Unprocessable Entity",
      "specifics": exc.errors(),
    },
  )