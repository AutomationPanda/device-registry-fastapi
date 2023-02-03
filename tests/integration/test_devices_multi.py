"""
This module contains integration tests for the '/devices' resource.
These tests cover GET responses involving multiple devices.
We cannot guarantee that the devices we create will be the only devices in the system.
For example, if tests run in parallel, then other tests might create new devices.
Therefore, test assertions must check only what is covered by the test.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import pytest

from testlib.devices import verify_included, verify_excluded, verify_owner


# --------------------------------------------------------------------------------
# Tests for Multiple Devices
# --------------------------------------------------------------------------------

def test_multiple_device_retrieval(base_url, session, devices):

  # Get all devices
  url = base_url.concat('/devices')
  get_response = session.get(url)
  get_data = get_response.json()

  # Verify all devices
  assert get_response.status_code == 200
  assert isinstance(get_data, list)
  verify_included(get_data, devices)
  verify_owner(get_data, devices[0]['owner'])


def test_delete_device_from_multiple(base_url, session, devices, device_creator):
  
  # Delete
  id_to_delete = devices[1]['id']
  device_id_url = base_url.concat(f'/devices/{id_to_delete}')
  delete_response = session.delete(device_id_url)
  delete_data = delete_response.json()

  # Verify delete
  assert delete_response.status_code == 200
  assert not delete_data

  # Mark device as deleted
  device_creator.remove(id_to_delete)
  del devices[1]

  # Get all devices
  url = base_url.concat('/devices')
  get_response = session.get(url)
  get_data = get_response.json()

  # Verify all devices
  assert get_response.status_code == 200
  assert isinstance(get_data, list)
  verify_included(get_data, devices)
  verify_excluded(get_data, [id_to_delete])


@pytest.mark.parametrize(
  'parameter, value',
  [
    ('name', 'Front Porch Light'),
    ('location', 'Front Porch'),
    ('type', 'Light Switch'),
    ('model', 'GenLight 64B'),
    ('serial_number', 'GL64B-99987')
  ]
)
def test_devices_with_query_parameters(base_url, session, thermostat, light, fridge, parameter, value):

  # Get all devices
  url = base_url.concat('/devices')
  get_response = session.get(url, params={parameter: value})
  get_data = get_response.json()

  # Verify response
  assert get_response.status_code == 200
  assert isinstance(get_data, list)

  # Verify that the response has only the target device
  verify_included(get_data, [light])
  verify_excluded(get_data, [thermostat['id'], fridge['id']])
  

def test_devices_with_invalid_query_parameters_ignored(base_url, session, devices):

  # Get all devices with invalid query parameteres
  url = base_url.concat('/devices')
  get_response = session.get(url, params={'invalid': 'value'})
  get_data = get_response.json()

  # Verify response and devices
  assert get_response.status_code == 200
  assert isinstance(get_data, list)
  verify_included(get_data, devices)


def test_devices_with_multiple_query_parameters(base_url, session, thermostat, light, fridge):

  # Get all devices
  url = base_url.concat('/devices')
  params = {'name': 'Front Porch Light', 'location': 'Front Porch'}
  get_response = session.get(url, params=params)
  get_data = get_response.json()

  # Verify response
  assert get_response.status_code == 200
  assert isinstance(get_data, list)

  # Verify that the response has only the target device
  verify_included(get_data, [light])
  verify_excluded(get_data, [thermostat['id'], fridge['id']])


def test_devices_with_multiple_query_parameters_matching_no_device(base_url, session, devices):

  # Get all devices
  url = base_url.concat('/devices')
  params = {'name': 'Back Porch Light', 'location': 'Front Porch'}
  get_response = session.get(url, params=params)
  get_data = get_response.json()

  # Verify empty response
  assert get_response.status_code == 200
  assert isinstance(get_data, list)
  assert len(get_data) == 0
