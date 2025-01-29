Connect camera, IMU, and relay to RPi

Enable the camera in RPi settings by using:
    sudo raspi-config
and selecting the camera from Interface Options

Enable the SW i2c implementation by adding
    doverlay=i2c-gpio,i2c_gpio_sda=2,i2c_gpio_sc1=3,bus=3
to /boot/config.txt
then rebooting
    (Note: the default i2c bus 1 can also be used but is less reliable
    due to clock stretching by the IMU magnetometer and may generate exceptions)

Create detected_faces directory in rpi dir to temporarily store detected faces

Run:
- Start the server from another device
- Use ngrok to forward to the port the server is running on (ngrok http port#)
- python3 main.py http://serverlink


To set up the script to run at boot time, use crontab via:
    sudo crontab -e
and enter:
    @reboot /home/pi/Desktop/capstone/rpi/launch.sh
You may need to edit the links and paths in the launch.sh file.
(Note: program output will not be printed to the interactive console this way.)