
from txt import *
from textFlash import *
import time 
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import sys
import LEDmode
import prootMode

REFRESH_RATE = 0.03


if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.gpio_slowdown = 4
    options.chain_length = 2
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

    matrix = RGBMatrix(options = options)
    LED_MODE = prootMode(matrix)

    try:
        print("Press CTRL-C to stop.")
        LED_MODE.startup()

        while True:
            LED_MODE.periodic()
            time.sleep(REFRESH_RATE)

    except KeyboardInterrupt:
        LED_MODE.onEnd()
        sys.exit(0)
