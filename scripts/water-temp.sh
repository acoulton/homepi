#!/bin/bash

# Ensure that environment variables are set
source /home/pi/.bash_profile

# Send the temperatures
/home/pi/homepi/python_apps/water-temperature.py
