#!/bin/bash

mpremote cp main.py :main.py
mpremote cp -r static/ :
mpremote cp -r templates/ :
mpremote soft-reset