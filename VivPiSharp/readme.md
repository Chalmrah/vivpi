# VivPi Sharp

C# implementation of the VivPi program

## Basic Program flow

### On startup

1. Loads config json file, validates it against a builtin schema leaves the config in ram.
2. Starts main program loop

### Main Program Loop

1. Connects and pulls from web endpoint
2. Confirms temp/humidity against alerting temps and humidity
3. Turns on or off the appropriate appliance if values are over or under configured ranges
4. If the values are over the alerting threshold, sends a telegram message to all users listed in the config
5. Posts its data to thingspeak
6. Sleeps for 30 seconds before looping back to the start.


## Planned Sections

* HTTP endpoint scraper. HTTP GET based. Pulls data from endpoint
* Thingspeak uploader. HTTP POST based.
* Energenie connection module. Unsure how to run this. May be just running a shell command to do the state change
* Logging module. Need to be able to log using systemd properly to allow for people to be able to see what is going on and ship logs if needed.
* Telegram messaging module.
* Config module. Loads from disk into RAM for every other module to read
* Verification module. Take values from endpoint and compare against config values.