"""
This module contains tests for device reports.
It shows how to test file downloads via REST API.
"""

# --------------------------------------------------------------------------------
# Report Download Tests
# --------------------------------------------------------------------------------

def test_device_report_download(base_url, session, thermostat):

  # Download
  device_id_url = base_url.concat(f'/devices/{thermostat["id"]}/report')
  get_response = session.get(device_id_url)

  # Verify response
  assert get_response.status_code == 200
  assert get_response.headers['content-type'] == 'text/plain; charset=utf-8'
  assert get_response.headers['content-disposition'] == 'attachment; filename="Main Thermostat.txt"'
  assert int(get_response.headers['content-length']) > 0

  # Verify content
  expected_report = \
    f"ID: {thermostat['id']}\n" + \
    f"Owner: {thermostat['owner']}\n" + \
    f"Name: {thermostat['name']}\n" + \
    f"Location: {thermostat['location']}\n" + \
    f"Type: {thermostat['type']}\n" + \
    f"Model: {thermostat['model']}\n" + \
    f"Serial Number: {thermostat['serial_number']}\n" 
  
  assert get_response.text == expected_report
