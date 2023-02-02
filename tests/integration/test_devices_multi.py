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

from testlib.devices import verify_devices


# --------------------------------------------------------------------------------
# Tests for Multiple Devices
# --------------------------------------------------------------------------------

# def test_multiple_device_creation(base_url, session, devices):
#   url = base_url.concat('/devices')
#   response = session.get(url)
#   data = response.json()

#   assert response.status_code == 200
#   assert isinstance(data, list)

#   actual_devices = sorted(data, key=lambda x: x['id'])
#   assert len(actual_devices) == len(devices)

#   for i in range(len(actual_devices)):
#     verify_device_data(actual_devices[i], devices[i])


def test_multiple_device_creation(base_url, session, devices):

  # Get all devices
  url = base_url.concat('/devices')
  get_response = session.get(url)
  get_data = get_response.json()

  # Verify all devices
  assert get_response.status_code == 200
  assert isinstance(get_data, list)
  verify_devices(get_data, devices)


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
  verify_devices(get_data, devices)


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
def test_devices_with_query_parameters(base_url, session, devices, parameter, value):

  # If testing ID, get its value from the created devices
  if parameter == 'id':
    value = devices[1]['id']

  # Get all devices
  url = base_url.concat('/devices')
  get_response = session.get(url, params={parameter: value})
  get_data = get_response.json()

  # Verify response
  assert get_response.status_code == 200
  assert isinstance(get_data, list)

  # Verify that the response has only the target device
  expected_list = [devices[1]]
  excluding = [devices[0]['id'], devices[2]['id']]
  verify_devices(get_data, expected_list, excluding)
  

def test_devices_with_invalid_query_parameters_ignored(base_url, session, devices):

  # Get all devices with invalid query parameteres
  url = base_url.concat('/devices')
  get_response = session.get(url, params={'invalid': 'value'})
  get_data = get_response.json()

  # Verify response and devices
  assert get_response.status_code == 200
  assert isinstance(get_data, list)
  verify_devices(get_data, devices)


def test_devices_with_multiple_query_parameters(base_url, session, devices):

  # Get all devices
  url = base_url.concat('/devices')
  params = {'name': 'Front Porch Light', 'location': 'Front Porch'}
  get_response = session.get(url, params=params)
  get_data = get_response.json()

  # Verify response
  assert get_response.status_code == 200
  assert isinstance(get_data, list)

  # Verify that the response has only the target device
  expected_list = [devices[1]]
  excluding = [devices[0]['id'], devices[2]['id']]
  verify_devices(get_data, expected_list, excluding)


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
