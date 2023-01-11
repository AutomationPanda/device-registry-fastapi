"""
This module contains CRUD integration tests for devices.
CRUD = Create, Retrieve, Update, Delete.
Positive and negative cases are included.
Thorough CRUD tests require more than one call per test.
Therefore, their names do not mirror resource paths.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import pytest


# --------------------------------------------------------------------------------
# Positive CRUD Tests
# --------------------------------------------------------------------------------

def test_create_and_retrieve_device(
  base_url, session, thermostat):

  # Retrieve
  device_id_url = base_url.concat(f'/devices/{thermostat["id"]}')
  get_response = session.get(device_id_url)
  get_data = get_response.json()

  # Verify retrieve
  assert get_response.status_code == 200
  assert get_data == thermostat


def test_full_update_device(
  base_url, session, thermostat, light_data):

  # Put
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  put_response = session.put(device_url, json=light_data)
  put_data = put_response.json()

  # Verify put
  assert put_response.status_code == 200
  light_data['id'] = thermostat['id']
  light_data['owner'] = thermostat['owner']
  assert put_data == light_data

  # Retrieve
  device_id_url = base_url.concat(f'/devices/{light_data["id"]}')
  get_response = session.get(device_id_url)
  get_data = get_response.json()

  # Verify retrieve
  assert get_response.status_code == 200
  assert get_data == light_data


def test_partial_update_device(
  base_url, session, thermostat, thermostat_patch_data):

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
  thermostat_patch_data['owner'] = thermostat['owner']
  assert patch_data == thermostat_patch_data

  # Retrieve
  device_id_url = base_url.concat(f'/devices/{patch_data["id"]}')
  get_response = session.get(device_id_url)
  get_data = get_response.json()

  # Verify retrieve
  assert get_response.status_code == 200
  assert get_data == thermostat_patch_data


@pytest.mark.parametrize(
  'field, value',
  [
    ('name', 'My Favorite Thermostat'),
    ('location', 'My House')
  ]
)
def test_partial_update_device_with_one_field(
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
  assert get_data == thermostat_data


def test_delete_device(
  base_url, session, thermostat, device_creator):

  # Delete
  device_id_url = base_url.concat(f'/devices/{thermostat["id"]}')
  delete_response = session.delete(device_id_url)
  delete_data = delete_response.json()

  # Verify delete
  assert delete_response.status_code == 200
  assert not delete_data

  # Attempt to retrieve the deleted device
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  get_response = session.get(device_url)
  get_data = get_response.json()

  # Verify error
  assert get_response.status_code == 404
  assert get_data['detail'] == 'Not Found'

  # Mark device as deleted
  device_creator.remove(thermostat['id'])


# --------------------------------------------------------------------------------
# Nonexistent ID Tests
# --------------------------------------------------------------------------------

NONEXISTENT_ID = 999999999


def verify_not_found(response):
  body = response.json()
  assert response.status_code == 404
  assert body['detail'] == 'Not Found'


# def test_nonexistent_id_error_for_device_retrieve(
#   base_url, session):

#   # Attempt retrieve
#   device_url = base_url.concat(f'/devices/{NONEXISTENT_ID}')
#   get_response = session.get(device_url)
#   get_data = get_response.json()

#   # Verify error
#   assert get_response.status_code == 404
#   assert get_data['detail'] == 'Not Found'


def test_nonexistent_id_error_for_device_retrieve(
  base_url, session):

  # Attempt retrieve
  device_url = base_url.concat(f'/devices/{NONEXISTENT_ID}')
  get_response = session.get(device_url)

  # Verify error
  verify_not_found(get_response)


def test_nonexistent_id_error_for_device_full_update(
  base_url, session, light_data):

  # Attempt put
  device_url = base_url.concat(f'/devices/{NONEXISTENT_ID}')
  put_response = session.put(device_url, json=light_data)

  # Verify error
  verify_not_found(put_response)


def test_nonexistent_id_error_for_device_partial_update(
  base_url, session, thermostat_patch_data):

  # Attempt patch
  device_url = base_url.concat(f'/devices/{NONEXISTENT_ID}')
  patch_response = session.patch(device_url, json=thermostat_patch_data)

  # Verify error
  verify_not_found(patch_response)


def test_nonexistent_id_error_for_device_delete(
  base_url, session):

  # Delete
  device_id_url = base_url.concat(f'/devices/{NONEXISTENT_ID}')
  delete_response = session.delete(device_id_url)

  # Verify error
  verify_not_found(delete_response)


# --------------------------------------------------------------------------------
# Missing Body Tests
# --------------------------------------------------------------------------------

def verify_body_missing(response):
  body = response.json()
  assert response.status_code == 422
  assert body['detail'] == 'Unprocessable Entity'
  assert body['specifics'] == [{
    'loc': ['body'],
    'msg': 'field required',
    'type': 'value_error.missing'}]


def test_missing_body_error_for_device_create(
  base_url, session):

  # Attempt create
  device_url = base_url.concat('/devices')
  post_response = session.post(device_url)

  # Verify error
  verify_body_missing(post_response)


def test_missing_body_error_for_device_full_update(
  base_url, session, thermostat):

  # Attempt put
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  put_response = session.put(device_url)

  # Verify error
  verify_body_missing(put_response)


def test_missing_body_error_for_device_partial_update(
  base_url, session, thermostat):

  # Attempt patch
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  patch_response = session.patch(device_url)

  # Verify error
  verify_body_missing(patch_response)


# --------------------------------------------------------------------------------
# Missing Field Tests
# --------------------------------------------------------------------------------

FIELDS = ['name', 'location', 'type', 'model', 'serial_number']


def verify_missing_field(response, field):
  body = response.json()
  assert response.status_code == 422
  assert body['detail'] == 'Unprocessable Entity'
  assert body['specifics'] == [{
    'loc': ['body', field],
    'msg': 'field required',
    'type': 'value_error.missing'}]


@pytest.mark.parametrize('field', FIELDS)
def test_missing_field_error_for_device_create(
  field, base_url, session, thermostat_data):

  # Attempt create
  del thermostat_data[field]
  device_url = base_url.concat('/devices')
  post_response = session.post(device_url, json=thermostat_data)
  
  # Verify error
  verify_missing_field(post_response, field)


@pytest.mark.parametrize('field', FIELDS)
def test_missing_field_error_for_device_full_update(
  field, base_url, session, thermostat, light_data):

  # Attempt put
  del light_data[field]
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  put_response = session.put(device_url, json=light_data)

  # Verify error
  verify_missing_field(put_response, field)


# --------------------------------------------------------------------------------
# Invalid Field Name Tests
# --------------------------------------------------------------------------------

def verify_invalid_field_name(response, field):
  body = response.json()
  assert response.status_code == 422
  assert body['detail'] == 'Unprocessable Entity'
  assert body['specifics'] == [{
    'loc': ['body', field],
    'msg': 'extra fields not permitted',
    'type': 'value_error.extra'}]


@pytest.mark.parametrize(
  'field, value',
  [
    ('id', 500),
    ('owner', 'nobody'),
    ('garbage', 'nonsense')
  ]
)
def test_invalid_field_name_error_for_device_create(
  field, value, base_url, session, thermostat_data):

  # Attempt create
  thermostat_data[field] = value
  device_url = base_url.concat('/devices')
  post_response = session.post(device_url, json=thermostat_data)
  
  # Verify error
  verify_invalid_field_name(post_response, field)


@pytest.mark.parametrize(
  'field, value',
  [
    ('id', 500),
    ('owner', 'nobody'),
    ('garbage', 'nonsense')
  ]
)
def test_invalid_field_name_error_for_device_full_update(
  field, value, base_url, session, thermostat, light_data):

  # Attempt put
  light_data[field] = value
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  put_response = session.put(device_url, json=light_data)

  # Verify error
  verify_invalid_field_name(put_response, field)


@pytest.mark.parametrize(
  'field, value',
  [
    ('id', 500),
    ('owner', 'nobody'),
    ('type', 'Light Switch'),
    ('model', 'ABC123'),
    ('serial_number', 'ABC123'),
    ('garbage', 'nonsense')
  ]
)
def test_invalid_field_name_error_for_device_partial_update(
  field, value, base_url, session, thermostat, thermostat_patch_data):

  # Attempt patch
  thermostat_patch_data[field] = value
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  patch_response = session.patch(device_url, json=thermostat_patch_data)

  # Verify error
  verify_invalid_field_name(patch_response, field)


# --------------------------------------------------------------------------------
# Invalid Field Value Tests
# --------------------------------------------------------------------------------

INVALID_VALUES = [
  ('name', None),
  ('location', None),
  ('type', None),
  ('model', None),
  ('serial_number', None)
]


def verify_invalid_field_value(response, field):
  body = response.json()
  assert response.status_code == 422
  assert body['detail'] == 'Unprocessable Entity'
  assert body['specifics'] == [{
    'loc': ['body', field],
    'msg': 'none is not an allowed value',
    'type': 'type_error.none.not_allowed'}]


@pytest.mark.parametrize('field, value', INVALID_VALUES)
def test_invalid_field_value_error_for_device_create(
  field, value, base_url, session, thermostat_data):

  # Attempt create
  thermostat_data[field] = value
  device_url = base_url.concat('/devices')
  post_response = session.post(device_url, json=thermostat_data)
  
  # Verify error
  verify_invalid_field_value(post_response, field)


@pytest.mark.parametrize('field, value', INVALID_VALUES)
def test_invalid_field_value_error_for_device_full_create(
  field, value, base_url, session, thermostat, light_data):

  # Attempt put
  light_data[field] = value
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  put_response = session.put(device_url, json=light_data)

  # Verify error
  verify_invalid_field_value(put_response, field)
