# Copyright 2018 Google LLC
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/python

import time
import datetime
import json
from google.cloud import pubsub
from oauth2client.client import GoogleCredentials
from Adafruit_BME280 import *
from tendo import singleton

me = singleton.SingleInstance() # will sys.exit(-1) if other instance is running

# constants - change to fit your project and location
SEND_INTERVAL = 60 #seconds
sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
credentials = GoogleCredentials.get_application_default()
# change project to your Project ID
project="weatherproject"
# change topic to your PubSub topic name
topic = "weatherdata"
# set the following four constants to be indicative of where you are placing your weather sensor
sensorID = "s-Googleplex"
sensorZipCode = "94043"
sensorLat = "37.421655"
sensorLong = "-122.085637"

def publish_message(project_name, topic_name, data):
  try:
	publisher = pubsub.PublisherClient()	
	topic = 'projects/' + project_name + '/topics/' + topic_name
	publisher.publish(topic, data, placeholder='')
	print data
  except:
	print "There was an error publishing weather data."
	
def read_sensor(weathersensor):
    tempF = weathersensor.read_temperature_f()
    # pascals = sensor.read_pressure()
    # hectopascals = pascals / 100
    pressureInches = weathersensor.read_pressure_inches()
    dewpoint = weathersensor.read_dewpoint_f()
    humidity = weathersensor.read_humidity()
    temp = '{0:0.2f}'.format(tempF)
    hum = '{0:0.2f}'.format(humidity)
    dew = '{0:0.2f}'.format(dewpoint)
    pres = '{0:0.2f}'.format(pressureInches)
    return (temp, hum, dew, pres)

def createJSON(id, timestamp, zip, lat, long, temperature, humidity, dewpoint, pressure):
    data = {
      'sensorID' : id,
      'timecollected' : timestamp,
      'zipcode' : zip,
      'latitude' : lat,
      'longitude' : long,
      'temperature' : temperature,
      'humidity' : humidity,
      'dewpoint' : dewpoint,
      'pressure' : pressure
    }

    json_str = json.dumps(data)
    return json_str

def main():
  last_checked = 0
  while True:
    if time.time() - last_checked > SEND_INTERVAL:
      last_checked = time.time()
      temp, hum, dew, pres = read_sensor(sensor)
      currentTime = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
      s = ", "
      weatherJSON = createJSON(sensorID, currentTime, sensorZipCode, sensorLat, sensorLong, temp, hum, dew, pres)
      publish_message(project, topic, weatherJSON)
    time.sleep(0.5)

if __name__ == '__main__':
	main()
