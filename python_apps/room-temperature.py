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
  "boys-room"        : {"metric": "room-temperature", "source": "boys-room", "channel": "1", "sensor_id": "10717"},
  "playroom"         : {"metric": "room-temperature", "source": "playroom", "channel": "1", "sensor_id": "11001"},
  "office"           : {"metric": "room-temperature", "source": "office", "channel": "1", "sensor_id": "12151"},
  "dining-room"      : {"metric": "room-temperature", "source": "dining-room", "channel": "1", "sensor_id": "9991"},
  "front-rm"         : {"metric": "room-temperature", "source": "front-rm", "channel": "1", "sensor_id": "10467"},
  "down-bed"         : {"metric": "room-temperature", "source": "down-bed", "channel": "1", "sensor_id": "8322"},
  "kitchen-temp"     : {"metric": "room-temperature", "source": "kitchen", "channel": "1", "sensor_id": "17296"},
  "kitchen-hum"      : {"metric": "room-humidity", "source": "kitchen", "channel": "3", "sensor_id": "17296"},
  "up-rear-bed-temp" : {"metric": "room-temperature", "source": "up-rear-bed", "channel": "1", "sensor_id": "17520"},
  "up-rear-bed-hum"  : {"metric": "room-humidity", "source": "up-rear-bed", "channel": "3", "sensor_id": "17520"},
  "exterior"         : {"metric": "room-temperature", "source": "exterior", "channel": "1", "sensor_id": "10195"}
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

def read_recent_temps(sensor_name, sensor):
  last_read = to_arexx_time(get_last_reported_time(sensor_name)) + 1
  now       = to_arexx_time(time.time())
  url       = BASE_URL+"?A="+str(last_read)+"&B="+str(now)+"&C="+sensor['sensor_id']+"&D="+sensor['channel']
  print "reading "+url+"\n"
  dom       = minidom.parse(urllib.urlopen(url))
  metrics   = []
  last_time = 0
  for node in dom.getElementsByTagName('value'):
    this_time = to_unix_time(int(node.getAttribute('t')))
    metrics.append({
      'value'        : node.firstChild.nodeValue,
      'source'       : sensor['source'],
      'name'         : sensor['metric'],
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
  payload[key_prefix+"[name]"]         = val['name']
  payload[key_prefix+"[value]"]        = val['value']
  payload[key_prefix+"[source]"]       = val['source']
  payload[key_prefix+"[measure_time]"] = val['measure_time']

if (len(payload) > 0):
  librato.send_metrics(payload)
