# Test code for servo
import RPi.GPIO as GPIO
from time import sleep

SERVO_PIN = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
angle=0.9 # percentage of full range


pwm=GPIO.PWM(SERVO_PIN, 100) # specify hz
pwm.start(0)
while True:
	pwm.ChangeDutyCycle(5)	# 0 degrees
	sleep(3)
	pwm.ChangeDutyCycle(round(5 + angle*20)) # duty cycle 25 max
	sleep(3)

pwm.stop()

GPIO.cleanup()


# Needs python 3.8 +, but 3.7 is default on raspbian buster...
# from gpiozero import Servo
# from time import sleep

# servo = Servo(pin="GPIO13", min_pulse_width=0.5, max_pulse_width=2.0)
# while True:
# 	servo.min()
# 	sleep(0.5)
# 	servo.mid()
# 	sleep(0.5)
# 	servo.max()
# 	sleep(0.5)
