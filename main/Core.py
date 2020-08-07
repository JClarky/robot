import time
import RPi.GPIO as GPIO

########## GPIO Setup
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

########## Motor Variables
motor_max_value = 100
motor_min_value = 0
pin_left_forward = 13
pin_left_backward = 6
pin_right_forward = 5
pin_right_backward = 12
GPIO.setup(pin_left_forward, GPIO.OUT)
GPIO.setup(pin_left_backward, GPIO.OUT)
GPIO.setup(pin_right_forward, GPIO.OUT)
GPIO.setup(pin_right_backward, GPIO.OUT)
lpf = GPIO.PWM(pin_left_forward, 1000) #Left Pin Forward
lpf.start(0)
lpb = GPIO.PWM(pin_left_backward, 1000) #Left Pin Backward
lpb.start(0)
rpf = GPIO.PWM(pin_right_forward, 1000) #Right Pin Forward
rpf.start(0)
rpb = GPIO.PWM(pin_right_backward, 1000) #Right Pin Backward
rpb.start(0)

########## LED Variables
led_pin = 24
led_state = False
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, 0)

threshold = 10

def move(l, r):
    global threshold
    global lpf, lpb, rpf, rpb
    r = r - 10
    '''if l < threshold and l > 0:
        l = 0
    elif l > threshold and l < 0:
        l = 0
    if r < threshold and r > 0:
        r = 0
    elif r > threshold and r < 0:
        r = 0'''
    if r > 100:
        r = 100
    else if r < 0:
        r = 0
    if l > 100:
        l = 100
    else if l < 0:
        l = 0

    try:
        if l > 0:
            lpb.ChangeDutyCycle(0)
            lpf.ChangeDutyCycle(l)
        elif l < 0:
            l = -l
            lpf.ChangeDutyCycle(0)
            lpb.ChangeDutyCycle(l)
        else:
            lpf.ChangeDutyCycle(0)
            lpb.ChangeDutyCycle(0)
        if r > 0:
            rpb.ChangeDutyCycle(0)
            rpf.ChangeDutyCycle(r)
        elif r < 0:
            r = -r
            rpf.ChangeDutyCycle(0)
            rpb.ChangeDutyCycle(r)
        else:
            rpf.ChangeDutyCycle(0)
            rpb.ChangeDutyCycle(0)
    except ValueError:
        print("VALUE ERROR L:"+str(l)+" R:"+str(r))


def led_on():
    global led_pin
    GPIO.output(led_pin, 1)

def led_off():
    global led_pin
    GPIO.output(led_pin, 0)

def left_turn():
    move(0, 100)
    time.sleep(0.5)

def right_turn():
    move(100, 0)
    time.sleep(0.5)
