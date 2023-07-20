#!/bin/bash

mpremote cp main.py :main.py
mpremote cp camera.py :camera.py
mpremote cp ds18b20.py :ds18b20.py
mpremote cp -r static/ :
mpremote cp -r templates/ :
mpremote soft-reset