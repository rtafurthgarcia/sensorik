#!/bin/bash
set -e
GREEN='\033[0;32m'
NC='\033[0m' # No Color
MANIFEST="$(pwd)/manifest.py"

if [ -d "lib" ]; then
  echo -e "${GREEN}lib directory exists, clearing it...${NC}"
  
  rm -rf "lib/"
fi

mkdir -p lib/microdot

echo -e "${GREEN}Installing packages...${NC}"
pip download --no-binary :all: microdot -d ./lib
git clone https://github.com/pfalcon/utemplate ./lib/utemplate
#pip download --no-binary :all: jinja2 -d ./lib
#tar -xvf "$(find ./lib -name 'Jinja2*.tar.gz' -print -quit)" --strip-components=1 -C ./lib/Jinja2
#tar -xvf "$(find ./lib -name 'MarkupSafe*.tar.gz' -print -quit)" --strip-components=1 -C ./lib/MarkupSafe
tar -xvf "$(find ./lib -name 'microdot*.tar.gz' -print -quit)" --strip-components=1 -C ./lib/microdot
#tar -xvf "$(find ./lib -name 'utemplate*.tar.gz' -print -quit)" --strip-components=1 -C ./lib/utemplate

if [ -d "micropython" ]; then
  echo -e "${GREEN}micropython directory exists, clearing it...${NC}"
  
  rm -rf "micropython/"
fi

echo -e "${GREEN}Cloning MicroPython...${NC}"
git clone https://github.com/micropython/micropython
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

sleep 5

echo -e "${GREEN}Flashing the new firmware and its submodules... ${NC}"
make BOARD=ARDUINO_PORTENTA_H7 deploy

echo -e "${GREEN}Arduino successfully frozen! ${NC}"

rm -rf "lib/"
rm -rf "micropython/"

echo -e "${GREEN}Directory cleaned! ${NC}"