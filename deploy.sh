#!/bin/bash
shopt -s globstar
set -e

GREEN='\033[0;32m'
NC='\033[0m' # No Color
MANIFEST="$(pwd)/manifest.py"

mpremote cp main.py :main.py
mpremote cp camera.py :camera.py
mpremote cp ds18b20.py :ds18b20.py
mpremote cp -r static/ :
mpremote cp -r templates/ :

rm -rf lib/
echo -e "${GREEN}Installing packages...${NC}"
git clone https://github.com/miguelgrinberg/microdot/ lib/microdot
cd lib/microdot/src
mpremote cp *.py :
cd ../libs/common
mpremote cp -r utemplate/ :

mpremote soft-reset