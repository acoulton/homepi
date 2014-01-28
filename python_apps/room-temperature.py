#!/usr/bin/env python

# Read the room temperatures and report them to librato. Ensures that all values are reported by tracking
# the most recently read value for each sensor and posting anything newer than that.
import time
import urllib
import os.path
import librato
from xml.dom import minidom

BASE_URL = 'http://192.168.0.5/data.xml'
ROOM_SENSORS = {
  "boys-room"   : "10717",
  "playroom"    : "11001",
  "office"      : "12151",
  "dining-room" : "9991"
}
TMP_FILE_PATH = '/home/pi/homepi/tmp/last-room-temps/'

# Arexx times are since 1-1-2000
AREXX_EPOCH = 946684800

def to_arexx_time(unix_time):
  return int(unix_time) - AREXX_EPOCH

def to_unix_time(arexx_time):
  return arexx_time + AREXX_EPOCH

def get_last_reported_time(sensor_name):
  return os.path.getmtime(TMP_FILE_PATH+sensor_name)

def set_last_reported_time(sensor_name, time):
  os.utime(TMP_FILE_PATH+sensor_name, (time, time))

def read_recent_temps(sensor_name, sensor_id):
  last_read = to_arexx_time(get_last_reported_time(sensor_name)) + 1
  now       = to_arexx_time(time.time())
  url       = BASE_URL+"?A="+str(last_read)+"&B="+str(now)+"&C="+sensor_id+"&D=1"
  dom       = minidom.parse(urllib.urlopen(url))
  metrics   = []
  last_time = 0
  for node in dom.getElementsByTagName('value'):
    this_time = to_unix_time(int(node.getAttribute('t')))
    metrics.append({
      'value'        : node.firstChild.nodeValue,
      'source'       : sensor_name,
      'name'         : 'room-temperature',
      'measure_time' : this_time
    })
    last_time = this_time if (this_time > last_time) else last_time
  if (last_time > 0):
    set_last_reported_time(sensor_name, last_time)
  return metrics

# Execute
all_metrics = []
for (sensor_name, sensor_id) in ROOM_SENSORS.items():
  all_metrics = all_metrics + read_recent_temps(sensor_name, sensor_id)

payload = {}
for i, val in enumerate(all_metrics):
  key_prefix = "gauges["+str(i)+"]"
  payload[key_prefix+"[name]"]         = "room-temperature"
  payload[key_prefix+"[value]"]        = val['value']
  payload[key_prefix+"[source]"]       = val['source']
  payload[key_prefix+"[measure_time]"] = val['measure_time']

if (len(payload) > 0):
  librato.send_metrics(payload)
