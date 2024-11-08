
# from rgbmatrix import RGBMatrix, RGBMatrixOptions # type: ignore
from simulation.rgbmatrix import RGBMatrix, RGBMatrixOptions
import sys

from LEDModes.runGif import GifMode
from LEDModes.constants import GifConstants
from utils import ImageUtils
from PIL import Image

"""
This file is for testing LED states without having to hook up the raspberry pi to the robot.
"""

if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.gpio_slowdown = 4
    options.chain_length = 2
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

    Currentgif = "startup.gif"

    matrix = RGBMatrix(options = options)

    with Image.open(Currentgif) as loadingImage:
        matrix.SetImage(ImageUtils.duplicateScreen(loadingImage))

    LED_MODE = GifMode(matrix, Currentgif) # this directory will change

    try:
        print("Press CTRL-C to stop.")
        LED_MODE.startup()

        while True:
            LED_MODE.periodic()

    except KeyboardInterrupt: # for debugging purposes
        LED_MODE.onEnd()
        sys.exit(0)
