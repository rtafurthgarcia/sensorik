#!/bin/bash

mpremote cp main.py :main.py
mpremote rmdir :static/
mpremote cp -r static/ :
mpremote soft-reset