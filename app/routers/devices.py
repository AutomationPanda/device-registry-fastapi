"""
This module provides routes for devices.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from .. import db
from ..auth import get_current_username

from io import BytesIO
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from tinydb import Query


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


class DevicePost(BaseModel):
  name: str
  location: str
  type: str
  model: str
  serial_number: str


class DevicePatch(BaseModel):
  name: str | None = None
  location: str | None = None
  type: str | None = None
  model: str | None = None
  serial_number: str | None = None
  owner: str | None = None


# --------------------------------------------------------------------------------
# Query Functions
# --------------------------------------------------------------------------------

def query_device(device_id: int, username: str):
  device = db.get(doc_id=device_id)

  if not device:
    raise Exception("NotFoundError")
  elif device["owner"] != username:
    raise Exception("UserUnauthorizedError")

  return device


def update_device(device_id: int, data: dict, username: str):
  query_device(device_id, username)
  db.update(data, doc_ids=[device_id])
  return db.get(doc_id=device_id)
  

# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get("/devices", response_model=list[Device])
@router.head("/devices")
def get_devices(username: str = Depends(get_current_username)):
  """
  Gets a list of all devices owned by the user.
  Requires authentication.
  """

  return db.search(Query().owner == username)


@router.post("/devices", response_model=int)
def post_devices(device: DevicePost, username: str = Depends(get_current_username)):
  """
  Adds a new device owned by the user.
  Requires authentication.
  """

  new_device = device.dict()
  new_device["owner"] = username
  return db.insert(new_device)


@router.get("/devices/{device_id}", response_model=Device)
@router.head("/devices/{device_id}")
def get_devices_id(device_id: int, username: str = Depends(get_current_username)):
  """
  Gets a device owned by the user.
  Requires authentication.
  """

  return query_device(device_id, username)


@router.put("/devices/{device_id}", response_model=Device)
def put_devices_id(device_id: int, device: Device, username: str = Depends(get_current_username)):
  """
  Fully updates a device owned by the user.
  Requires authentication.
  """

  data = device.dict()
  return update_device(device_id, data, username)


@router.patch("/devices/{device_id}", response_model=Device)
def patch_devices_id(device_id: int, device: DevicePatch, username: str = Depends(get_current_username)):
  """
  Partially updates a device owned by the user.
  Requires authentication.
  """

  data = device.dict(exclude_unset=True)
  return update_device(device_id, data, username)


@router.delete("/devices/{device_id}", response_model=dict)
def delete_devices_id(device_id: int, username: str = Depends(get_current_username)):
  """
  Deletes a device owned by the user.
  Requires authentication.
  """

  query_device(device_id, username)
  db.remove(doc_ids=[device_id])
  return dict()


@router.get("/devices/{device_id}/report")
def get_devices_id_report(device_id: int, username: str = Depends(get_current_username)):
  """
  Prints a text-based report for a device owned by the user.
  Requires authentication.
  """

  device = query_device(device_id, username)

  report = BytesIO()
  report.write(bytes(f'ID: {device_id}\n', 'ascii'))
  report.write(bytes(f'Name: {device["name"]}\n', 'ascii'))
  report.write(bytes(f'Location: {device["location"]}\n', 'ascii'))
  report.write(bytes(f'Type: {device["type"]}\n', 'ascii'))
  report.write(bytes(f'Model: {device["model"]}\n', 'ascii'))
  report.write(bytes(f'Serial Number: {device["serial_number"]}\n', 'ascii'))
  report.write(bytes(f'Owner: {device["owner"]}\n', 'ascii'))
  report.seek(0)

  response = StreamingResponse(report, media_type='text/plain')
  content_disposition = f"attachment; filename*=utf-8''{device['name']}.txt"
  response.headers.setdefault("content-disposition", content_disposition)
  return response
