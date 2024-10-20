import sys

# from LEDcontrol.simulation.rgbmatrix import RGBMatrix, RGBMatrixOptions
from rgbmatrix import RGBMatrix, RGBMatrixOptions # type: ignore

from networktables import NetworkTables

from LEDModes import *
from LEDModes.idleMode import IdleMode
from constants import NetworkTableConstants

LED_MODE = None

"""
This is the main file to be ran on the raspberry pi.
Connects to networktables and manages the LED state.
"""

# def ledModeChanged(table, key, value, isNew):
#     pass

def connectionListener():
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.gpio_slowdown = 4
    options.chain_length = 2
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

    matrix = RGBMatrix(options = options)

    sd = NetworkTables.getTable(NetworkTableConstants.TABLE_NAME)
    LED_MODES = [IdleMode(matrix)]

    try:
        print("Press CTRL-C to stop.")
        LED_MODE.startup()

        while True:
            led_index = sd.getNumber(NetworkTableConstants.LED_INDEX_NAME, default_value=0)
            LED_MODE = LED_MODES[led_index]
            LED_MODE.periodic()

    except KeyboardInterrupt: # For debugging purposes
        LED_MODE.onEnd()
        sys.exit(0)

if __name__ == "__main__":
    NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)
