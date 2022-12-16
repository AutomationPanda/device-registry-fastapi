"""
This module provides routes for devices.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from fastapi import APIRouter


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter()


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get("/devices")
def get_devices():
  """
  Gets a list of all devices owned by the user.
  Requires authentication.
  """

  return [
    {
      'id': 1,
      'name': 'Front Porch Light',
      'location': 'Front Porch',
      'type': 'Light Switch',
      'model': 'GenLight 64B',
      'serial_number': 'GL64B-99987',
      'owner': 'pythonista'
    },
    {
      'id': 2,
      'name': 'Main Thermostat',
      'location': 'Living Room',
      'type': 'Thermostat',
      'model': 'ThermoBest 3G',
      'serial_number': 'TB3G-12345',
      'owner': 'pythonista'
    },
    {
      'id': 3,
      'name': 'Family Fridge',
      'location': 'Kitchen',
      'type': 'Refrigerator',
      'model': 'El Gee Mondo21',
      'serial_number': 'LGM-20201',
      'owner': 'engineer'
    }
  ]