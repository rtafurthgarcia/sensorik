#!/bin/bash
set -e
GREEN='\033[0;32m'
NC='\033[0m' # No Color
MANIFEST="$(pwd)/manifest.py"

#if [ -d "MicroWebSrv2" ]; then
#  echo -e "${GREEN}Directory exists, clearing it...${NC}"
#  
#  rm -rf "MicroWebSrv2"
#fi
#echo -e "${GREEN}Cloning MicroWebSrv2...${NC}"
#git clone https://github.com/jczic/MicroWebSrv2

if [ -d "microdot" ]; then
  echo -e "${GREEN}Directory exists, clearing it...${NC}"
  
  rm -rf "microdot"
fi
echo -e "${GREEN}Cloning microdot...${NC}"
git clone https://github.com/miguelgrinberg/microdot/

mv microdot/src microdot-src
rm -rf microdot 
mv microdot-src microdot

if [ -d "micropython" ]; then
  echo -e "${GREEN}Directory exists, clearing it...${NC}"
  
  rm -rf "micropython"
fi

echo -e "${GREEN}Cloning MicroPython...${NC}"
git clone https://github.com/micropython/micropython
cd micropython/

#echo -e "${GREEN}Enabling threads...${NC}"
#file_path="./ports/stm32/mpconfigport.h"
#sed -i 's|#define MICROPY_PY_THREAD           (0)|#define MICROPY_PY_THREAD           (1)|g' "$file_path"

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

rm -rf "microdot"
rm -rf "micropython"

echo -e "${GREEN}Directory cleaned! ${NC}"