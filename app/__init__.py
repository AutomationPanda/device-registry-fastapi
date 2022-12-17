"""
This module builds shared parts for other modules.
It reads in the `config.json` file for app configuration.
Warning: No error-checking is done for the config.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import json
import time
import tinydb


# --------------------------------------------------------------------------------
# Set Start Time
# --------------------------------------------------------------------------------

start_time = time.time()


# --------------------------------------------------------------------------------
# Read Configuration
# --------------------------------------------------------------------------------

with open('config.json') as config_json:
  config = json.load(config_json)


# --------------------------------------------------------------------------------
# Connect the Database
# --------------------------------------------------------------------------------

db = tinydb.TinyDB(config['db_file'])


# --------------------------------------------------------------------------------
# Establish the Secret Key
# --------------------------------------------------------------------------------

secret_key = config['secret_key']


# --------------------------------------------------------------------------------
# Establish the Users
# --------------------------------------------------------------------------------

users = config['users']


# --------------------------------------------------------------------------------
# Insert Data into the Database
# --------------------------------------------------------------------------------

# db.insert(
#   {
#     'name': 'Front Porch Light',
#     'location': 'Front Porch',
#     'type': 'Light Switch',
#     'model': 'GenLight 64B',
#     'serial_number': 'GL64B-99987',
#     'owner': 'pythonista'
#   }
# )
# db.insert(
#   {
#     'name': 'Main Thermostat',
#     'location': 'Living Room',
#     'type': 'Thermostat',
#     'model': 'ThermoBest 3G',
#     'serial_number': 'TB3G-12345',
#     'owner': 'pythonista'
#   }
# )
# db.insert(
#   {
#     'name': 'Family Fridge',
#     'location': 'Kitchen',
#     'type': 'Refrigerator',
#     'model': 'El Gee Mondo21',
#     'serial_number': 'LGM-20201',
#     'owner': 'engineer'
#   }
# )