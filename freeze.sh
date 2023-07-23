#!/bin/bash
set -e
GREEN='\033[0;32m'
NC='\033[0m' # No Color
MANIFEST="$(pwd)/manifest.py"

if [ -d "lib" ]; then
  echo -e "${GREEN}lib directory exists, clearing it...${NC}"
  
  rm -rf "lib/"
fi

mkdir lib

echo -e "${GREEN}Installing packages...${NC}"
git clone https://github.com/miguelgrinberg/microdot/ lib/microdot

if [ -d "micropython" ]; then
  echo -e "${GREEN}micropython directory exists, clearing it...${NC}"
  
  rm -rf "micropython/"
fi

echo -e "${GREEN}Cloning MicroPython...${NC}"
git clone https://github.com/micropython/micropython
cd micropython/
git fetch --all --tags
git checkout tags/v1.20.0

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

rm -rf "lib/"
rm -rf "micropython/"

echo -e "${GREEN}Directory cleaned! ${NC}"
