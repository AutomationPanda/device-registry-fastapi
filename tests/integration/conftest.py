"""
This module provides fixtures for integration tests.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import json
import pytest
import requests
import time

from testlib.api import BaseUrl, User, TokenHolder
from testlib.devices import DeviceCreator


# --------------------------------------------------------------------------------
# Private Functions
# --------------------------------------------------------------------------------

def _build_user(inputs, index):
  users = inputs['users']
  user = User(users[index]['username'], users[index]['password'])
  return user


def _build_session(user):
  session = requests.Session()
  session.auth = (user.username, user.password)
  return session


# --------------------------------------------------------------------------------
# Config Fixture
# --------------------------------------------------------------------------------

@pytest.fixture(scope='session')
def test_inputs():
  with open('tests/integration/inputs.json') as config_json:
    data = json.load(config_json)
  return data


@pytest.fixture
def base_url(test_inputs):
  return BaseUrl(test_inputs['base_url'])


@pytest.fixture
def user(test_inputs):
  return _build_user(test_inputs, 0)


@pytest.fixture
def alt_user(test_inputs):
  return _build_user(test_inputs, 1)


# --------------------------------------------------------------------------------
# Session Fixtures
# --------------------------------------------------------------------------------

@pytest.fixture
def session(user):
  return _build_session(user)


@pytest.fixture
def alt_session(alt_user):
  return _build_session(alt_user)


# --------------------------------------------------------------------------------
# Token Fixtures
# --------------------------------------------------------------------------------

@pytest.fixture
def auth_token(base_url, user):
  url = base_url.concat('/authenticate/')
  auth = (user.username, user.password)
  response = requests.get(url, auth=auth)
  data = response.json()

  assert response.status_code == 200
  assert 'token' in data

  return data['token']


@pytest.fixture(scope='session')
def token_holder():
  return TokenHolder(None, None)


@pytest.fixture
def shared_auth_token(base_url, user, token_holder):
  current_time = time.time()

  if not token_holder.token or current_time - token_holder.start_time >= 3600:
    url = base_url.concat('/authenticate/')
    auth = (user.username, user.password)
    response = requests.get(url, auth=auth)
    data = response.json()

    assert response.status_code == 200
    assert 'token' in data
    
    token_holder.token = data['token']
    token_holder.start_time = current_time
  
  return token_holder.token


# --------------------------------------------------------------------------------
# Device Fixtures
# --------------------------------------------------------------------------------

@pytest.fixture
def thermostat_data():
  return {
    'name': 'Main Thermostat',
    'location': 'Living Room',
    'type': 'Thermostat',
    'model': 'ThermoBest 3G',
    'serial_number': 'TB3G-12345'
  }


@pytest.fixture
def light_data():
  return {
    'name': 'Front Porch Light',
    'location': 'Front Porch',
    'type': 'Light Switch',
    'model': 'GenLight 64B',
    'serial_number': 'GL64B-99987'
  }


@pytest.fixture
def fridge_data():
  return {
    'name': 'Family Fridge',
    'location': 'Kitchen',
    'type': 'Refrigerator',
    'model': 'El Gee Mondo21',
    'serial_number': 'LGM-20201'
  }


@pytest.fixture
def thermostat_patch_data():
  return {
    'name': 'Upstairs Thermostat',
    'location': 'Master Bedroom'
  }


@pytest.fixture
def device_creator(base_url):
  creator = DeviceCreator(base_url)
  yield creator
  creator.cleanup()


@pytest.fixture
def thermostat(device_creator, session, thermostat_data):
  return device_creator.create(session, thermostat_data)
