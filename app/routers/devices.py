"""
This module provides routes for devices.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from .. import db
from ..auth import get_current_username
from ..exceptions import ForbiddenException, NotFoundException

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

class BaseDeviceModel(BaseModel):
  class Config:
    extra = "forbid"


class Device(BaseDeviceModel):
  id: int
  owner: str
  name: str
  location: str
  type: str
  model: str
  serial_number: str


class DevicePostPut(BaseDeviceModel):
  name: str
  location: str
  type: str
  model: str
  serial_number: str


class DevicePatch(BaseDeviceModel):
  name: str | None = None
  location: str | None = None
  

# --------------------------------------------------------------------------------
# Query Functions
# --------------------------------------------------------------------------------

def query_device(device_id: int, username: str):
  device = db.get(doc_id=device_id)

  if not device:
    raise NotFoundException()
  elif device["owner"] != username:
    raise ForbiddenException()

  device['id'] = device_id
  return device


def update_device(device_id: int, data: dict, username: str):
  query_device(device_id, username)
  db.update(data, doc_ids=[device_id])

  device = db.get(doc_id=device_id)
  device['id'] = device_id
  return device
  

# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get("/devices", summary="Get the user's devices", response_model=list[Device])
@router.get("/devices/", include_in_schema=False)
@router.head("/devices", summary="Get the user's devices")
@router.head("/devices/", include_in_schema=False)
def get_devices(
  owner: str = Depends(get_current_username),
  name: str | None = None,
  location: str | None = None,
  type: str | None = None,
  model: str | None = None,
  serial_number: str | None = None):
  """
  Gets a list of all devices owned by the user.
  May optionally take query parameters for filtering results.
  Requires authentication.
  """

  DeviceQuery = Query()
  query = DeviceQuery.owner == owner

  if name is not None:
    query = (query) & (DeviceQuery.name == name)
  if location is not None:
    query = (query) & (DeviceQuery.location == location)
  if type is not None:
    query = (query) & (DeviceQuery.type == type)
  if model is not None:
    query = (query) & (DeviceQuery.model == model)
  if serial_number is not None:
    query = (query) & (DeviceQuery.serial_number == serial_number)

  devices = db.search(query)

  for d in devices:
    d['id'] = d.doc_id

  return devices


@router.post("/devices", summary="Create a new device", response_model=Device)
@router.post("/devices/", include_in_schema=False)
def post_devices(device: DevicePostPut, username: str = Depends(get_current_username)):
  """
  Adds a new device owned by the user.
  Requires authentication.
  """

  new_device = device.dict()
  new_device["owner"] = username
  device_id = db.insert(new_device)

  return query_device(device_id, username)


@router.get("/devices/{device_id}", summary="Get a device by ID", response_model=Device)
@router.get("/devices/{device_id}/", include_in_schema=False)
@router.head("/devices/{device_id}", summary="Get a device by ID")
@router.head("/devices/{device_id}/", include_in_schema=False)
def get_devices_id(device_id: int, username: str = Depends(get_current_username)):
  """
  Gets a device owned by the user.
  Requires authentication.
  """

  return query_device(device_id, username)


@router.put("/devices/{device_id}", summary="Fully update a device", response_model=Device)
@router.put("/devices/{device_id}/", include_in_schema=False)
def put_devices_id(device_id: int, device: DevicePostPut, username: str = Depends(get_current_username)):
  """
  Fully updates a device owned by the user.
  Requires authentication.
  """

  data = device.dict()
  return update_device(device_id, data, username)


@router.patch("/devices/{device_id}", summary="Update a device's name and location", response_model=Device)
@router.patch("/devices/{device_id}/", include_in_schema=False)
def patch_devices_id(device_id: int, device: DevicePatch, username: str = Depends(get_current_username)):
  """
  Partially updates a device owned by the user.
  Can only update name and location - not other fields.
  Requires authentication.
  """

  data = device.dict(exclude_unset=True, exclude_none=True)
  return update_device(device_id, data, username)


@router.delete("/devices/{device_id}", summary="Delete a device by ID", response_model=dict)
@router.delete("/devices/{device_id}/", include_in_schema=False)
def delete_devices_id(device_id: int, username: str = Depends(get_current_username)):
  """
  Deletes a device owned by the user.
  Requires authentication.
  """

  query_device(device_id, username)
  db.remove(doc_ids=[device_id])
  return dict()


@router.get("/devices/{device_id}/report", summary="Download a device report")
@router.get("/devices/{device_id}/report/", include_in_schema=False)
@router.head("/devices/{device_id}/report", summary="Download a device report")
@router.head("/devices/{device_id}/report/", include_in_schema=False)
def get_devices_id_report(device_id: int, username: str = Depends(get_current_username)):
  """
  Prints a text-based report for a device owned by the user.
  Requires authentication.
  """

  device = query_device(device_id, username)

  report = BytesIO()
  report.write(bytes(f'ID: {device_id}\n', 'ascii'))
  report.write(bytes(f'Owner: {device["owner"]}\n', 'ascii'))
  report.write(bytes(f'Name: {device["name"]}\n', 'ascii'))
  report.write(bytes(f'Location: {device["location"]}\n', 'ascii'))
  report.write(bytes(f'Type: {device["type"]}\n', 'ascii'))
  report.write(bytes(f'Model: {device["model"]}\n', 'ascii'))
  report.write(bytes(f'Serial Number: {device["serial_number"]}\n', 'ascii'))
  report.seek(0)

  report_length = str(report.getbuffer().nbytes)

  response = StreamingResponse(report, media_type='text/plain')
  content_disposition = f'attachment; filename="{device["name"]}.txt"'
  response.headers.setdefault("content-disposition", content_disposition)
  response.headers.setdefault("content-length", report_length)
  return response
