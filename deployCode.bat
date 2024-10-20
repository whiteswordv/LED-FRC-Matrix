@echo off
rem Script to use pscp to copy all of the files in LEDControl to the raspberry pi

rem Using pscp to copy a file from Windows to Raspberry Pi
pscp C:\path\to\local\file.txt pi@<raspberry_pi_ip>:/home/pi/

echo File transfer complete.
pause
