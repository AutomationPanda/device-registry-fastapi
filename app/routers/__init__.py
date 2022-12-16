"""
This module builds shared parts for other modules.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import time

from tinydb import TinyDB


# --------------------------------------------------------------------------------
# Globals
# --------------------------------------------------------------------------------

START_TIME = time.time()
db = TinyDB('registry.json')

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