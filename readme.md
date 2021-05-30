# Vivpi - IoT Terranium Service for Raspberry Pi

The Vivpi service is a python based service written to be a simple smart system for controlling the climate inside a vivarium/terranium.
The sensors suggested can measure air pressure, humidity, and temperature, and perform actions based on the data recieved.
In theory, any sensors can be used as long as the sensor data is put onto a web page that can output a json file to be read.

## Hardware List

* Raspberry Pi 3
* Energenie 4 Way Radio Controlled Extension Lead (ENER010)
* Energenie Pi-mote control board (ENER314)
* Adafruit feather ESP32 controller
* 2x Bosch BME280 sensors

## Wiring

* Below is a diagram of wiring for the project. Other pins can be used but the ESP ``boot.py`` file will have to be adjusted to compensate.
* The version of ESP32 I used is the ``Adafruit HUZZAH32 - ESP32 Feather``

```
From the microcontroller side:
 _______
|       |2  -> 3v   -> To positive pin on both sensors
|       |4  -> GND  -> To ground pin on both sensors
| ESP32 |14 -> A6   -> To SDA pin on cold sensor
|       |18 -> MOSI -> To SCL pin on cold sensor
|       |21 -> GPIO -> To SDA pin on warm sensor
|_______|22 -> SCL  -> To SCL pin on warm sensor

From the sensor side:
 ______                     ______ 
| Hot  |3V  -> 2           | Cold |3V  -> 2
|Sensor|GND -> 4           |Sensor|GND -> 4
|      |SDA -> 21          |      |SDA -> 14 
|______|SCL -> 22          |______|SCL -> 18
```

## Installation 

### ESP Microcontroller

* Connect to the controller with usb and copy all of the files in the ESP file over to microcontroller.
* Rename ``boot.example.py`` to ``boot.py`` and configure the wifi connection information.

### Raspberry Pi

* Once the setup for the Raspberry Pi is complete, ensure ansible is installed on it by running ``sudo apt install ansible``
* Clone this repo to the Pi and configure the playbook.yml to put the install location if you want it somewhere that isnt default.
* Run the playbook by running ``sudo ansible-playbook playbook.yml``

## Configuration

* **IMPORTANT NOTE:** All temperatures are in Celcius!
* All configuration of the vivpi is done within the ``settings.json`` file
* The configuration is validated everytime the server runs, which is configured to run every 20 seconds. If it fails the script will stop running and error out.
* The VivPi will use the hot side sensor to validate whether the tank is hot or humid enough. The cold sensor is just to collect information about the other side of the tank.
* If you have only a mister in your system, you can set the foggers switch number to the same as the mister and it will ignore the mister switch entirely.

## Additional Services

### Thingspeak

* I use this system to do graphing of historical data. I chose it as it is free and allows for posting of data via a url. The system does not require this to be running as it can operate without historical data, I just wanted to have some nice graphs that I can view via my phone.

### Telegram

* Will message you if your config file is not valid.
* The next version of this system will have a telegram bot that will allow you to configure the settings file via the bot, or at least be able to manually flick the switches to turn on a device until the next run. Can be useful to test if a new mister is working properly.

## Quick notes if you want edit this:

* The html on the ESP32 only pulls data from the json in the background.
* You can pull json from the ESP32 with any address as long as it ends in ``.json``
* The json returns all numbers as floats. This is what the python script on the Raspberry Pi is expecting when it recieves the data.
* The config file is validated against a json schema that is embedded in the ``config.py`` file. If this does not validate successfully the server will log an emergency and throw to prevent damage to the physical hardware.
* All the code for the actual server is located in the ``roles/install-vivpi/files`` folder.