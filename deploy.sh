#!/bin/bash

mpremote cp main.py :main.py
mpremote cp boot.py :boot.py
mpremote cp auth.py :auth.py
mpremote cp -r static/ :
mpremote cp -r templates/ :
mpremote soft-reset