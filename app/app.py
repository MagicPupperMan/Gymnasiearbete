import os
import time
import json

from flask import Flask, render_template, request

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

from helpers import *

# Configuration file. Stores pin numbers for chip select and channel numbers for sensors.
with open('config/config.json', 'r') as f:
    config = json.load(f)

# Creating an SPI interface
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# Create chip select pin
cs = digitalio.DigitalInOut(pins[config['mcp']['cs']])

# MCP object from Adafruit Library
mcp = MCP.MCP3008(spi, cs)

# Analog Channel objects for each sensor
tdsSensor = AnalogIn(mcp, channels[config['sensors']['tds']])
tempSensor = AnalogIn(mcp, channels[config['sensors']['temp']])

# Initialize flask app
app = Flask('sprout')

# Home page renderer
@app.route('/')
def home():
    # Number of readings to calculate mean value
    n = 40
    
    # Calculate mean values of temp and tds for n readings (account for spikes or noise in voltage)
    temp = round(sum([voltageToTemp(tempSensor.voltage) for x in range(n)])/n, 1)
    tds = round(sum([voltageToTDS(tdsSensor.voltage) for x in range(n)])/n, 1)
    return render_template('index.html', temp = temp, tds = tds)

# Run the app
if __name__ == "__main__":
    app.run('0.0.0.0')