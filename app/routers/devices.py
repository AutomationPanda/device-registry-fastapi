"""
This module provides routes for devices.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from . import db
from fastapi import APIRouter
from pydantic import BaseModel


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter()


# --------------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------------

class Device(BaseModel):
  name: str
  location: str
  type: str
  model: str
  serial_number: str
  owner: str


class DevicePatch(BaseModel):
  name: str | None = None
  location: str | None = None
  type: str | None = None
  model: str | None = None
  serial_number: str | None = None
  owner: str | None = None


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get("/devices", response_model=list[Device])
def get_devices():
  """
  Gets a list of all devices owned by the user.
  Requires authentication.
  """

  return db.all()


@router.post("/devices", response_model=int)
def post_devices(device: Device):
  """
  Adds a new device owned by the user.
  Requires authentication.
  """

  return db.insert(device.dict())


@router.get("/devices/{device_id}", response_model=Device)
def get_devices_id(device_id: int):
  """
  Gets a device owned by the user.
  Requires authentication.
  """

  return db.get(doc_id=device_id)


@router.put("/devices/{device_id}", response_model=Device)
def put_devices_id(device_id: int, device: Device):
  """
  Fully updates a device owned by the user.
  Requires authentication.
  """

  data = device.dict()
  db.update(data, doc_ids=[device_id])
  return db.get(doc_id=device_id)


@router.patch("/devices/{device_id}", response_model=Device)
def patch_devices_id(device_id: int, device: DevicePatch):
  """
  Partially updates a device owned by the user.
  Requires authentication.
  """

  data = device.dict(exclude_unset=True)
  db.update(data, doc_ids=[device_id])
  return db.get(doc_id=device_id)


@router.delete("/devices/{device_id}", response_model=dict)
def delete_devices_id(device_id: int):
  """
  Deletes a device owned by the user.
  Requires authentication.
  """

  db.remove(doc_ids=[device_id])
  return dict()