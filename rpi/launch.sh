#!/bin/bash
# launch.sh
# run app on startup

env_name="yourenvname"
serverlink="https://711c-2607-f010-2a7-1022-4ddf-55da-af8a-ae4e.ngrok-free.app"

cd /home/pi/Desktop/capstone/rpi
source /home/pi/berryconda3/bin/activate
conda activate yourenvname

python3 main.py $serverlink
