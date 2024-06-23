#!/usr/bin/env bash
export HOME=/home/pi

# sudo amixer cset numid=1 95% # to avoid strange noises
cd /home/pi/Tornadoscope_show
source /home/pi/Tornadoscope_show/venv/bin/activate
python crontab_runner.py