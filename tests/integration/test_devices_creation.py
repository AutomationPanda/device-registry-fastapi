"""
This module contains a test for creating a device.
Its coverage is superseded by test_devices_crud.py and could be deleted.
However, it remains in this project to serve as example code.
Furthermore, be warned that the first two tests do not perform cleanup.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import time


# --------------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------------

def test_create_device(base_url, session):

  # Test data
  thermostat_data = {
    'name': 'Main Thermostat',
    'location': 'Living Room',
    'type': 'Thermostat',
    'model': 'ThermoBest 3G',
    'serial_number': 'TB3G-12345'
  }

  # Create
  device_url = base_url.concat('/devices')
  post_response = session.post(device_url, json=thermostat_data)
  post_data = post_response.json()
  
  # Verify create
  assert post_response.status_code == 200
  assert 'id' in post_data
  assert isinstance(post_data['id'], int)
  thermostat_data['id'] = post_data['id']
  thermostat_data['owner'] = session.auth[0]
  assert post_data == thermostat_data

  # Retrieve
  device_id_url = base_url.concat(f'/devices/{post_data["id"]}')
  get_response = session.get(device_id_url)
  get_data = get_response.json()

  # Verify retrieve
  assert get_response.status_code == 200
  assert get_data == post_data


def test_create_device_with_waiting(base_url, session):

  # This test is a copy of the test_create_device.
  # The "create" steps are identical.
  # The "retrieve" steps, however, actively wait for the device.

  thermostat_data = {
    'name': 'Main Thermostat',
    'location': 'Living Room',
    'type': 'Thermostat',
    'model': 'ThermoBest 3G',
    'serial_number': 'TB3G-12345'
  }

  device_url = base_url.concat('/devices')
  post_response = session.post(device_url, json=thermostat_data)
  post_data = post_response.json()
  
  assert post_response.status_code == 200
  assert 'id' in post_data
  assert isinstance(post_data['id'], int)
  thermostat_data['id'] = post_data['id']
  thermostat_data['owner'] = session.auth[0]
  assert post_data == thermostat_data

  device_id_url = base_url.concat(f'/devices/{post_data["id"]}')
  attempts = 60
  get_code = 0

  while get_code != 200 and attempts > 0:
    attempts -= 1
    time.sleep(1)
    get_response = session.get(device_id_url)
    get_code = get_response.status_code
  
  assert attempts > 0
  assert get_response.status_code == 200
  assert get_response.json() == post_data


def test_create_device_with_fixture(base_url, session, thermostat):

  # Retrieve
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  get_response = session.get(device_url)
  get_data = get_response.json()

  # Verify retrieve
  assert get_response.status_code == 200
  assert get_data == thermostat
