from evdev import InputDevice, categorize, ecodes
import Core
import time

########## Controller Variables
threshold = 5
controller = None
joystick_max_value = 32768
joystick_min_value = -32768
raw_turn_value = 0
raw_speed_value = 0
last_val = 0


def move_calc():
    global raw_speed_value, raw_turn_value, last_val
    if(last_val != 0 and last_val+raw_speed_value == 0): # Filter out sudden polarity changes
        raw_speed_value = last_val
    else:
        last_val = raw_speed_value
    raw_speed_value = -raw_speed_value # Change polarity of raw_speed_value
    # Scale joystick values to motor values
    speed_value = Core.motor_max_value*(raw_speed_value/joystick_max_value)
    turn_value = Core.motor_max_value*(raw_turn_value/joystick_max_value)

    left_speed = speed_value # Set left motor speed variable
    right_speed = speed_value # Set right motor speed variable
    if(raw_speed_value > 0): # If forward
        if(turn_value > 0): # Right turn
            right_speed = right_speed - turn_value # Change right motor speed variable (right is positive)
        else: # Left turn or NO turn
            left_speed = left_speed + turn_value # Change left motor speed variable (left is negative)
    else: # If backwards
        if(turn_value > 0): # Right turn
            right_speed = right_speed + turn_value # Change right motor speed variable (right is positive)
        else: # Left turn or NO turn
            left_speed = left_speed - turn_value # Change left motor speed variable (left is negative)
    Core.move(left_speed, right_speed)

def button(event):
    if event.code == yBtn:
        print("Y")
    elif event.code == bBtn:
        print("B")
    elif event.code == aBtn:
        print("A")
    elif event.code == xBtn:
        print("X")
    elif event.code == rBumper:
        print("Right Bumper")
    elif event.code == lBumper:
        print("Left Bumper")
    elif event.code == start:
        print('Start')
    elif event.code == back:
        print("Back")
    elif event.code == home:
        print("Home")
    elif event.code == lTrig:
        print("left trigger")
    elif event.code == rTrig:
        print("Right trigger")
    else:
        print("Unregistered button with event code",event.code)

def joystick(event):
    global raw_speed_value, raw_turn_value
    if event.code == 0: # X axis on left joystick
        pass
    elif event.code == 1: # Y axis on left joystick
        raw_speed_value = event.value
        move_calc()
    elif event.code == 3: # X axis on right joystick
        raw_turn_value = event.value
        move_calc()
    elif event.code == 4: # Y axis on right joystick
        pass
