#!/bin/bash
# launch.sh
# run app on startup

env_name="yourenvname"
serverlink="https://ocelot-learning-personally.ngrok-free.app"

cd /home/pi/Desktop/capstone/rpi
source /home/pi/berryconda3/bin/activate
conda activate yourenvname

python3 main.py $serverlink
