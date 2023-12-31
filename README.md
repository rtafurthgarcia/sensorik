# sensorik

Sensorik webapp gathering and displaying sensor data

## Setup

1. Make sure to have python3 with venv installed
2. Run `source venv/bin/activate` and `pip install -r requirements.txt`
3. Install the latest realease of [dfu-util](https://dfu-util.sourceforge.net/releases/)
4. Install the ARM compiller `gcc-arm-none-eabi` if you are on Debian or install it from the sources
5. Create a `auth.py` file with `SSID` and `PASS` set as constants to properly configure the access point

The previous steps have to be actually reproduced on WSL in case you want to "freeze" your board on Windows:

### Windows setup 
In case you are running this one build tool on Windows, the following supplementary steps are necessary:
1. Install WSL 2 
2. Setup your favourite distribution (that can run the setup section from above and preferably Debian)
3. Install https://github.com/dorssel/usbipd-win/releases on your Windows client
4. List all devices and find your H7 board's device ID (generally marked as a `COM` port) on Windows with `usbipd list` on a priviledged prompt
5. Permantenly bind your device to your default running distro through `usbipd bind -f --busid $YOUR_DEVICE_ID` also on a priviledged prompt 
6. Connect your device on an unpriviledged prompt (to be able to access the regular's user default distro) with `usbipd wsl attach -d $YOUR_DISTRO --busid $YOUR_DEVICE_ID`
7. Make sure `lsusb` is installed on your disto

If you have troubles connecting to your board, make sure your user is part of the ``tty` or `dialout` group or appropriate yourself the `/dev/ttyACMX` device with `# chown $USER:$USER /dev/ttyACMX`. 

## General use
- run `deploy.sh` to deploy the current python code to your board
- run `freeze.sh` to flash the latest firmware with your libraries

You may check whenever the board is properly connected by looking for the `/dev/ttyACMX` device (whereby X is 0, 1 or something else lol)

## Default firmware install 
1. Download the latest firmware from (here)[https://docs.arduino.cc/micropython/]
2. Flash the firmware as root with `dfu-util -a 0 -d 0x2341:0x035b -D {firmware.dfu}`