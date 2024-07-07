
from txt import *
from textFlash import *
import time 


if __name__ == "__main__":

    text_flash = textFlash("NOTE LAUNCHED!", 0.01, 255, 255, 120, 'blue', 8) #text, scroll speed, (color of text) r, g, b, color of background, #how long to run in seconds
    if not text_flash.process():
        text_flash.print_help()

    '''
    run_text = RunText("hi!", 0.01) #text, scroll speed
    if (not run_text.process()):
        run_text.print_help()
    pulsing_colors = PulsingColors()
    if not pulsing_colors.process():
        pulsing_colors.print_help()
    '''