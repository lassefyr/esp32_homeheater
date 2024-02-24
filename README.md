# esp32_homeheater

Program your board using the esptool.py program.

## Windows programming ##
esptool --chip esp32 --port COM3 erase_flash
esptool --chip esp32 --port COM3 --baud 460800 write_flash -z 0x1000 esp32-20230426-v1.20.0.bin

espefuse summary --chip esp32 --port COM4
esptool --chip esp32 --port COM4 erase_flash
esptool --chip esp32 --port COM4 --baud 460800 write_flash -z 0x1000 esp32-20230426-v1.20.0.bin

## UNIX programming ##
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-20230426-v1.20.0.bin

## Make bytecode files ##
  * https://github.com/micropython/micropython-esp32/tree/esp32

* web server files made to bytecode with podman environment
  * microdot.py
  * microdot vs picoweb vs tinyweb vs MicroWebSrv
  * https://www.donskytech.com/how-to-create-a-micropython-web-server-the-easy-way/

* real time chart update
  * https://www.donskytech.com/real-time-sensor-chart-display-of-sensor-readings-esp8266-esp32/

## INSTALL UTEMPLATE ##
Thonny ->tools>manage packages 
install utemplate

Installed version: 1.4.1
Installed to: /lib

Latest stable version: 1.4.1
Summary: Very lightweight, memory-efficient, dependency-free template engine (compiles to Python source).
Author: Paul Sokolovsky
License: MIT

Creates LIB directory to your device.
Contains utemplate and utemplate-1.4.1.dist-info directories

## secrets.py ##
Add secrets.py directly on your esp32 device.  
This file should contain the following two lines
```
SSID = "MY_WIFI_NETWORK_NAME"
PASSWORD = "MY_WIFI_PASSWORD"
```
