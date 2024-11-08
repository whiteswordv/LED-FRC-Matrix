import sys
import time

# from LEDcontrol.simulation.rgbmatrix import RGBMatrix, RGBMatrixOptions
from simulation.rgbmatrix import RGBMatrix, RGBMatrixOptions # type: ignore

from networktables import NetworkTables

from PIL import Image

from LEDModes import *
from LEDModes.idleMode import IdleMode
# from LEDModes.prootMode import prootMode
from LEDModes.runGif import GifMode
from LEDModes.constants import NetworkTableConstants, GifConstants, ImageConstants
from utils import ImageUtils

"""
This is the main file to be ran on the raspberry pi.
Connects to networktables and manages the LED state.
"""

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.gpio_slowdown = 4
options.chain_length = 2
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

# Do loading screen while gifs are processed
with Image.open(ImageConstants.LOADING) as loadingImage:
    matrix.SetImage(ImageUtils.duplicateScreen(loadingImage))

sd = NetworkTables.getTable(NetworkTableConstants.TABLE_NAME) # this may need to be moved lower to avoid errors

LED_MODES = [GifMode(matrix, GifConstants.IDLE)]

led_mode = LED_MODES[0]

connectionEstablished = False

def connectionListener():
    global connectionEstablished
    connectionEstablished = True


# python's equivalent to a main function
if __name__ == "__main__":
    NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

    # wait until connected to robot
    # while not connectionEstablished:
    #     print(True)
    #     time.sleep(0.1)
    
    # use try statement so the code can be ended via keypress
    # (for testing purposes).
    try:
        print("Press CTRL-C to stop.")
        
        led_mode.startup()

        # Main program loop
        while True:
            # led_index = sd.getNumber(NetworkTableConstants.LED_INDEX_NAME)
            led_index=0

            if led_index != LED_MODES.index(led_mode):
                led_mode.onEnd()
                led_mode = LED_MODES[led_index]
                led_mode.startup()

            led_mode.periodic()

    except KeyboardInterrupt: # For debugging purposes
        led_mode.onEnd()
        sys.exit(0)
    
