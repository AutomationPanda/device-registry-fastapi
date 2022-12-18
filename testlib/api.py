"""
This module provides support for testing the REST API.
"""

# --------------------------------------------------------------------------------
# Class: BaseUrl
# --------------------------------------------------------------------------------

class BaseUrl:
  
  def __init__(self, base_url):
    self.base_url = base_url
  
  def concat(self, resource):
    return self.base_url + resource


# --------------------------------------------------------------------------------
# Class: User
# --------------------------------------------------------------------------------

class User:

  def __init__(self, username, password):
    self.username = username
    self.password = password


# --------------------------------------------------------------------------------
# Class: TokenHolder
# --------------------------------------------------------------------------------

class TokenHolder:

  def __init__(self, token, start_time):
    self.token = token
    self.start_time = start_time
