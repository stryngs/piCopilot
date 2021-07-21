#!/usr/bin/python

import RPi.GPIO as GPIO
import subprocess
from datetime import datetime
import time

pin = 5
GPIO.setmode(GPIO.BOARD)
#GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(pin, GPIO.IN)

## LED Safety
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)

btnPress = GPIO.wait_for_edge(pin, GPIO.RISING, bouncetime = 200)
if btnPress is not None:
    subprocess.call(['shutdown', '-h', 'now'], shell = False)

### PIN 23 for GREEN
