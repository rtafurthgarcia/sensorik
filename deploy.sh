#!/bin/bash
shopt -s globstar
set -e

GREEN='\033[0;32m'
NC='\033[0m' # No Color
MANIFEST="$(pwd)/manifest.py"

mpremote cp main.py :main.py
mpremote cp boot.py :boot.py
mpremote cp auth.py :auth.py
mpremote cp -r static/ :
mpremote cp -r templates/ :

mpremote soft-reset