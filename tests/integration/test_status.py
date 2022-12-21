"""
This module contains integration tests for the '/status' resource.
The main method for '/status' is GET.
HEAD and OPTIONS methods are also supported.
Unsupported methods should return 405 status codes.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import pytest
import requests


# --------------------------------------------------------------------------------
# Tests for GET
# --------------------------------------------------------------------------------

def test_status_get(base_url):
  url = base_url.concat('/status')
  response = requests.get(url)
  data = response.json()
  
  assert response.status_code == 200
  assert data['online'] == True
  assert data['uptime'] > 0


# --------------------------------------------------------------------------------
# Tests for HEAD
# --------------------------------------------------------------------------------

def test_status_head(base_url):

  # Call HEAD
  url = base_url.concat('/status')
  response = requests.head(url)
  
  # Response should be successful without a body
  assert response.status_code == 200
  assert response.text == ''

  # Response headers should match GET responses
  get_response = requests.get(url)
  assert len(response.headers) == len(get_response.headers)

  # Compare each header value
  for header in response.headers:
    assert header in get_response.headers

    if header == 'content-length':
      head_length = int(response.headers[header])
      get_length = int(get_response.headers[header])
      assert abs(head_length - get_length) <= 4
    elif header != 'date':
      assert response.headers[header] == get_response.headers[header]


# --------------------------------------------------------------------------------
# Tests for OPTIONS
# --------------------------------------------------------------------------------

def test_status_options(base_url):

  # Call OPTIONS
  url = base_url.concat('/status')
  headers = {'Origin': 'localhost', 'Access-Control-Request-Method': 'GET'}
  response = requests.options(url, headers=headers)
  
  # Response should be successful
  assert response.status_code == 200
  assert response.text == 'OK'

  # Response header should list supported methods
  allow_string = response.headers['access-control-allow-methods']
  allowed = sorted(allow_string.split(', '))
  assert allowed == ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'PATCH', 'POST', 'PUT']


# --------------------------------------------------------------------------------
# Tests for Unsupported Methods
# --------------------------------------------------------------------------------

@pytest.mark.parametrize(
  'method',
  ['DELETE', 'PATCH', 'POST', 'PUT']
)
def test_status_invalid_method(base_url, method):

  # Call the unsupported method
  url = base_url.concat('/status')
  response = requests.request(method, url)
  data = response.json()

  # Response should be a 405 error
  assert response.status_code == 405
  assert data['detail'] == 'Method Not Allowed'

