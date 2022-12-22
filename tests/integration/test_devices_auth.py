"""
This module contains integration tests for authentication.
It uses the '/devices' resource.
For complete testing, every endpoint should have authentication tests.
However, that would generate a lot of test cases.
In a risk-based approach, it might be better to cover only a few endpoints.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import requests

from testlib.devices import verify_devices


# --------------------------------------------------------------------------------
# Verification Functions
# --------------------------------------------------------------------------------

def verify_authorized(response):
  data = response.json()
  assert response.status_code == 200
  assert isinstance(data, list)


def verify_unauthorized(response):
  data = response.json()
  assert response.status_code == 401
  assert data['detail'] == 'Unauthorized'


# --------------------------------------------------------------------------------
# Authentication Tests
# --------------------------------------------------------------------------------

def test_devices_get_with_basic_auth(base_url, user):
  url = base_url.concat('/devices')
  auth = (user.username, user.password)
  response = requests.get(url, auth=auth)
  verify_authorized(response)


def test_devices_get_with_basic_auth_session(base_url, session):
  url = base_url.concat('/devices')
  response = session.get(url)
  verify_authorized(response)


def test_devices_get_with_token_auth(base_url, auth_token):
  url = base_url.concat('/devices')
  headers = {'Authorization': 'Bearer ' + auth_token}
  response = requests.get(url, headers=headers)
  verify_authorized(response)


def test_devices_get_with_shared_token_auth(base_url, shared_auth_token):
  url = base_url.concat('/devices')
  headers = {'Authorization': 'Bearer ' + shared_auth_token}
  response = requests.get(url, headers=headers)
  verify_authorized(response)


def test_devices_get_with_no_auth(base_url):
  url = base_url.concat('/devices')
  response = requests.get(url)
  verify_unauthorized(response)


def test_devices_get_with_invalid_username(base_url, user):
  url = base_url.concat('/devices')
  auth = (user.username + 'X', user.password)
  response = requests.get(url, auth=auth)
  verify_unauthorized(response)


def test_devices_get_with_invalid_password(base_url, user):
  url = base_url.concat('/devices')
  auth = (user.username, user.password + 'X')
  response = requests.get(url, auth=auth)
  verify_unauthorized(response)


def test_devices_get_with_invalid_token(base_url, auth_token):
  url = base_url.concat('/devices')
  headers = {'Authorization': 'Bearer ' + auth_token + 'X'}
  response = requests.get(url, headers=headers)
  verify_unauthorized(response)


# --------------------------------------------------------------------------------
# Authorization Tests
# --------------------------------------------------------------------------------

def test_user_authorization_for_devices_get_list(base_url, alt_session, thermostat):
  
  # Get all devices
  device_id_url = base_url.concat(f'/devices/')
  get_response = alt_session.get(device_id_url)
  get_data = get_response.json()

  # Verify the user's device is NOT in the alt_user's list
  assert get_response.status_code == 200
  assert isinstance(get_data, list)
  verify_devices(get_data, excluding=[thermostat['id']])


def test_user_authorization_for_devices_get_by_id(base_url, alt_session, thermostat):
  
  # Attempt retrieve
  device_id_url = base_url.concat(f'/devices/{thermostat["id"]}')
  get_response = alt_session.get(device_id_url)
  get_data = get_response.json()

  # Verify error
  assert get_response.status_code == 403
  assert get_data['detail'] == 'Forbidden'


def test_user_authorization_for_devices_patch(base_url, alt_session, thermostat, thermostat_patch_data):
  
  # Attempt retrieve
  device_id_url = base_url.concat(f'/devices/{thermostat["id"]}')
  get_response = alt_session.patch(device_id_url, json=thermostat_patch_data)
  get_data = get_response.json()

  # Verify error
  assert get_response.status_code == 403
  assert get_data['detail'] == 'Forbidden'


def test_user_authorization_for_devices_put(base_url, alt_session, thermostat, light_data):
  
  # Attempt retrieve
  device_id_url = base_url.concat(f'/devices/{thermostat["id"]}')
  get_response = alt_session.put(device_id_url, json=light_data)
  get_data = get_response.json()

  # Verify error
  assert get_response.status_code == 403
  assert get_data['detail'] == 'Forbidden'


def test_user_authorization_for_devices_delete(base_url, alt_session, thermostat):
  
  # Attempt retrieve
  device_id_url = base_url.concat(f'/devices/{thermostat["id"]}')
  get_response = alt_session.delete(device_id_url)
  get_data = get_response.json()

  # Verify error
  assert get_response.status_code == 403
  assert get_data['detail'] == 'Forbidden'
