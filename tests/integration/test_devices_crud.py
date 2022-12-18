"""
This module contains CRUD integration tests for devices.
CRUD = Create, Retrieve, Update, Delete.
Positive and negative cases are included.
Thorough CRUD tests require more than one call per test.
Therefore, their names do not mirror resource paths.
"""

# --------------------------------------------------------------------------------
# "Constants"
# --------------------------------------------------------------------------------

EXPLICIT_ID = 500
NONEXISTENT_ID = 999999999


# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import pytest


# --------------------------------------------------------------------------------
# Create Tests
# --------------------------------------------------------------------------------

def test_create_and_retrieve_device(base_url, session, thermostat):

  # Retrieve
  device_id_url = base_url.concat(f'/devices/{thermostat["id"]}')
  get_response = session.get(device_id_url)
  get_data = get_response.json()

  # Verify retrieve
  assert get_response.status_code == 200
  assert get_data == thermostat


def test_create_with_no_body_yields_error(base_url, session):

  # Attempt create
  device_url = base_url.concat('/devices')
  post_response = session.post(device_url)
  post_data = post_response.json()

  # Verify error
  assert post_response.status_code == 422
  assert post_data['detail'] == 'Unprocessable Entity'
  assert post_data['specifics'] == [{
    'loc': ['body'],
    'msg': 'field required',
    'type': 'value_error.missing'}]


@pytest.mark.parametrize(
  'field, value',
  [
    ('id', EXPLICIT_ID),
    ('owner', 'nobody'),
    ('garbage', 'nonsense')
  ]
)
def test_create_with_invalid_field_yields_error(
  field, value, base_url, session, thermostat_data):
  thermostat_data[field] = value

  # Attempt create
  device_url = base_url.concat('/devices')
  post_response = session.post(device_url, json=thermostat_data)
  post_data = post_response.json()
  
  # Verify error
  assert post_response.status_code == 422
  assert post_data['detail'] == 'Unprocessable Entity'
  assert post_data['specifics'] == [{
    'loc': ['body', field],
    'msg': 'extra fields not permitted',
    'type': 'value_error.extra'}]


@pytest.mark.parametrize(
  'field',
  ['name', 'location', 'type', 'model', 'serial_number']
)
def test_create_with_missing_field_yields_error(field, base_url, session, thermostat_data):
  del thermostat_data[field]

  # Attempt create
  device_url = base_url.concat('/devices')
  post_response = session.post(device_url, json=thermostat_data)
  post_data = post_response.json()
  
  # Verify error
  assert post_response.status_code == 422
  assert post_data['detail'] == 'Unprocessable Entity'
  assert post_data['specifics'] == [{
    'loc': ['body', field],
    'msg': 'field required',
    'type': 'value_error.missing'}]


# --------------------------------------------------------------------------------
# Retrieve Tests
# --------------------------------------------------------------------------------

def test_retrieve_nonexistent_device_yields_error(base_url, session):

  # Attempt retrieve
  device_url = base_url.concat(f'/devices/{NONEXISTENT_ID}')
  get_response = session.get(device_url)
  get_data = get_response.json()

  # Verify error
  assert get_response.status_code == 404
  assert get_data['detail'] == 'Not Found'


# --------------------------------------------------------------------------------
# Update Tests for PUT
# --------------------------------------------------------------------------------

def test_update_device_via_put(base_url, user, session, thermostat, light_data):

  # Put
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  put_response = session.put(device_url, json=light_data)
  put_data = put_response.json()

  # Verify put
  assert put_response.status_code == 200
  light_data['id'] = thermostat['id']
  light_data['owner'] = user.username
  assert put_data == light_data

  # Retrieve
  device_id_url = base_url.concat(f'/devices/{light_data["id"]}')
  get_response = session.get(device_id_url)
  get_data = get_response.json()

  # Verify retrieve
  assert get_response.status_code == 200
  assert get_data == put_data


def test_update_device_via_put_with_no_body_yields_error(base_url, session, thermostat):

  # Attempt put
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  put_response = session.put(device_url)
  put_data = put_response.json()

  # Verify error
  assert put_response.status_code == 422
  assert put_data['detail'] == 'Unprocessable Entity'
  assert put_data['specifics'] == [{
    'loc': ['body'],
    'msg': 'field required',
    'type': 'value_error.missing'}]


def test_update_nonexistent_device_via_put_yields_error(base_url, session, light_data):

  # Attempt put
  device_url = base_url.concat(f'/devices/{NONEXISTENT_ID}')
  put_response = session.put(device_url, json=light_data)
  put_data = put_response.json()

  # Verify error
  assert put_response.status_code == 404
  assert put_data['detail'] == 'Not Found'


@pytest.mark.parametrize(
  'field, value',
  [
    ('id', EXPLICIT_ID),
    ('owner', 'nobody'),
    ('garbage', 'nonsense')
  ]
)
def test_update_device_via_put_with_invalid_field_yields_error(
  field, value, base_url, session, thermostat, light_data):
  light_data[field] = value

  # Attempt put
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  put_response = session.put(device_url, json=light_data)
  put_data = put_response.json()

  # Verify error
  assert put_response.status_code == 422
  assert put_data['detail'] == 'Unprocessable Entity'
  assert put_data['specifics'] == [{
    'loc': ['body', field],
    'msg': 'extra fields not permitted',
    'type': 'value_error.extra'}]


@pytest.mark.parametrize(
  'field',
  ['name', 'location', 'type', 'model', 'serial_number']
)
def test_update_device_via_put_with_missing_field_yields_error(
  field, base_url, session, thermostat, light_data):
  del light_data[field]

  # Attempt put
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  put_response = session.put(device_url, json=light_data)
  put_data = put_response.json()

  # Verify error
  assert put_response.status_code == 422
  assert put_data['detail'] == 'Unprocessable Entity'
  assert put_data['specifics'] == [{
    'loc': ['body', field],
    'msg': 'field required',
    'type': 'value_error.missing'}]


# --------------------------------------------------------------------------------
# Update Tests for PATCH
# --------------------------------------------------------------------------------

def test_update_device_via_patch(
  base_url, user, session, thermostat, thermostat_patch_data):

  # Patch
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  patch_response = session.patch(device_url, json=thermostat_patch_data)
  patch_data = patch_response.json()

  # Verify patch
  assert patch_response.status_code == 200
  thermostat_patch_data['id'] = thermostat['id']
  thermostat_patch_data['type'] = thermostat['type']
  thermostat_patch_data['model'] = thermostat['model']
  thermostat_patch_data['serial_number'] = thermostat['serial_number']
  thermostat_patch_data['owner'] = user.username
  assert patch_data == thermostat_patch_data

  # Retrieve
  device_id_url = base_url.concat(f'/devices/{patch_data["id"]}')
  get_response = session.get(device_id_url)
  get_data = get_response.json()

  # Verify retrieve
  assert get_response.status_code == 200
  assert get_data == patch_data


@pytest.mark.parametrize(
  'field, value',
  [
    ('name', 'My Favorite Thermostat'),
    ('location', 'My House')
  ]
)
def test_update_device_via_patch_with_one_field(
  field, value, base_url, session, thermostat, thermostat_data):

  # Patch
  request_data = {field: value}
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  patch_response = session.patch(device_url, json=request_data)
  patch_data = patch_response.json()

  # Verify patch
  assert patch_response.status_code == 200
  thermostat_data[field] = value
  assert patch_data == thermostat_data

  # Retrieve
  device_id_url = base_url.concat(f'/devices/{patch_data["id"]}')
  get_response = session.get(device_id_url)
  get_data = get_response.json()

  # Verify retrieve
  assert get_response.status_code == 200
  assert get_data == patch_data


def test_update_device_via_patch_with_no_body_yields_error(
  base_url, session, thermostat):

  # Attempt patch
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  patch_response = session.patch(device_url)
  patch_data = patch_response.json()

  # Verify error
  assert patch_response.status_code == 422
  assert patch_data['detail'] == 'Unprocessable Entity'
  assert patch_data['specifics'] == [{
    'loc': ['body'],
    'msg': 'field required',
    'type': 'value_error.missing'}]


def test_update_nonexistent_device_via_patch_yields_error(
  base_url, session, thermostat_patch_data):

  # Attempt patch
  device_url = base_url.concat(f'/devices/{NONEXISTENT_ID}')
  patch_response = session.patch(device_url, json=thermostat_patch_data)
  patch_data = patch_response.json()

  # Verify error
  assert patch_response.status_code == 404
  assert patch_data['detail'] == 'Not Found'


@pytest.mark.parametrize(
  'field, value',
  [
    ('id', EXPLICIT_ID),
    ('owner', 'nobody'),
    ('type', 'Light Switch'),
    ('model', 'ABC123'),
    ('serial_number', 'ABC123'),
    ('garbage', 'nonsense')
  ]
)
def test_update_device_via_patch_with_invalid_field_yields_error(
  field, value, base_url, session, thermostat, thermostat_patch_data):
  thermostat_patch_data[field] = value

  # Attempt patch
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  patch_response = session.patch(device_url, json=thermostat_patch_data)
  patch_data = patch_response.json()

  # Verify error
  assert patch_response.status_code == 422
  assert patch_data['detail'] == 'Unprocessable Entity'
  assert patch_data['specifics'] == [{
    'loc': ['body', field],
    'msg': 'extra fields not permitted',
    'type': 'value_error.extra'}]


# --------------------------------------------------------------------------------
# Delete Tests
# --------------------------------------------------------------------------------

def test_delete_device(base_url, session, thermostat, device_creator):

  # Delete
  device_id_url = base_url.concat(f'/devices/{thermostat["id"]}')
  delete_response = session.delete(device_id_url)
  delete_data = delete_response.json()

  # Verify delete
  assert delete_response.status_code == 200
  assert not delete_data

  # Mark device as deleted
  device_creator.remove(thermostat['id'])


def test_delete_nonexistent_device(base_url, session):

  # Delete
  device_id_url = base_url.concat(f'/devices/{NONEXISTENT_ID}')
  delete_response = session.delete(device_id_url)
  delete_data = delete_response.json()

  # Verify error
  assert delete_response.status_code == 404
  assert delete_data['detail'] == 'Not Found'
