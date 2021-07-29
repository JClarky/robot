import LineFollowing, Manual, RobotFighting, Core, time
from evdev import InputDevice, categorize, ecodes

controller = None

sumoMode = False
mazeMode = False
manualMode = False
mode = 0

# Event Codes for Controller
aBtn = 304
bBtn = 305
xBtn = 307
yBtn = 308
rBumper = 311
lBumper = 310
start = 315
back = 314
lTrig = 2
rTrig = 5
dpadY = 17
dpadX = 16
home = 316

def button(event):
    global mode
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
        if mode == 2:
            mode = 0
        else:
            mode = mode + 1
        print("Mode: " + str(mode))
    elif event.code == lTrig:
        print("left trigger")
    elif event.code == rTrig:
        print("Right trigger")
    else:
        print("Unregistered button with event code",event.code)

def connect_controller():
    global controller
    controller_connected = False
    Core.led_off()
    while not controller_connected:
        print("Controller not found")
        for i in range(0,11): # Cycle through different events
            event = 'event'+str(i) # Set new event
            try:
                controller = InputDevice('/dev/input/'+event) # Set controller
                if controller.name == 'Logitech Gamepad F710': # Is the controller the right one?
                    controller_connected = True
                    print('Connected to controller')
                    Core.led_on()
                    break
            except:
                print(event,"failed.... trying again")
            time.sleep(0.05)


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



left_speed = 0
right_speed = 0
raw_left_speed = 0
raw_right_speed = 0

# Scale value between range
def map(x, min_value, max_value, min_range, max_range):
    return (max_range-min_range)*((x - min_value) / (max_value - min_value))+min_range

def move_calc():
    """if(last_val != 0 and last_val+raw_speed_value == 0): # Filter out sudden polarity changes
        raw_speed_value = last_val
    else:
        last_val = raw_speed_value"""

    #raw_speed_value = -raw_speed_value # Change polarity of raw_speed_value

    print("speeds: ", raw_left_speed, raw_right_speed, left_speed, right_speed)
    left_speed = map(raw_left_speed, -100, 100, joystick_min_value, joystick_max_value)
    right_speed = map(raw_right_speed, -100, 100, joystick_min_value, joystick_max_value)
    Core.move(left_speed, right_speed)

def joystick(event):
    global raw_speed_value, raw_turn_value
    if event.code == 0: # X axis on left joystick
        pass
    elif event.code == 1: # Y axis on left joystick
        raw_left_speed = event.value
        move_calc()
    elif event.code == 3: # X axis on right joystick
        raw_right_speed = event.value
        move_calc()
    elif event.code == 4: # Y axis on right joystick
        pass

connect_controller()

run = True

while run:
    try: # If controller disconnects catch error
        for event in controller.read_loop(): # For each button/joystick event
            if event.type == ecodes.EV_KEY: # If event was button
                if event.value == 1: # If button was pressed(not released)
                    button(event) # Handle button press
            if event.type == 3 and mode == 0: # If event was joystick
                joystick(event) # Handle joystick input
    except OSError: # If controller disconnected
        print("Controller disconnected")
        connect_controller() # Reconnect to controller
