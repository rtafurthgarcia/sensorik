#!/bin/bash
set -e
GREEN='\033[0;32m'
NC='\033[0m' # No Color
MANIFEST="$(pwd)/manifest.py"

if [ -d "MicroWebSrv2" ]; then
  echo -e "${GREEN}Directory exists, clearing it...${NC}"
  
  rm -rf "MicroWebSrv2"
fi
echo -e "${GREEN}Cloning MicroPython...${NC}"
git clone https://github.com/jczic/MicroWebSrv2

if [ -d "micropython" ]; then
  echo -e "${GREEN}Directory exists, clearing it...${NC}"
  
  rm -rf "micropython"
fi

echo -e "${GREEN}Cloning MicroPython...${NC}"
git clone https://github.com/micropython/micropython --branch v1.20.0
cd micropython/

echo -e "${GREEN}Building the cross-compiler...${NC}"
make -C mpy-cross

echo -e "${GREEN}Building the firmware itself + the expected modules...${NC}"
cd ports/stm32/
make BOARD=ARDUINO_PORTENTA_H7 submodules

make -j 8 BOARD=ARDUINO_PORTENTA_H7 FROZEN_MANIFEST="${MANIFEST}"
echo -e "${GREEN}Build finished.${NC}"

echo -e "${GREEN}Restarting into the bootloader... ${NC}"
mpremote bootloader

sleep 10

echo -e "${GREEN}Flashing the new firmware and its submodules... ${NC}"
make BOARD=ARDUINO_PORTENTA_H7 deploy

echo -e "${GREEN}Arduino successfully frozen! ${NC}"

rm -rf "MicroWebSrv2"
rm -rf "micropython"

echo -e "${GREEN}Directory cleaned! ${NC}"