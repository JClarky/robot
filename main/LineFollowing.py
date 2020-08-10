# Imports
import cv2
import numpy as np
import time
import Core

# Configure camera capture
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

last_command = ""

def image():
    global cap

    gray_threshold_max = 255
    gray_threshold_min = 70 # ALTER TO MAKE PERFECTOOOOO
    block_size = 119
    img_split = []
    img_width = 640
    img_height = 480
    turning_margin = 10 # How far the line has to be from the center for it to adjust

    # Image Setup
    ret, img = cap.read()
    img = cv2.flip(img, 0) # vert
    img = cv2.flip(img, 1) # horz

    # Height , width
    img = img[150:300, 150:490]
    img_width = img.shape[1]
    img_height = img.shape[0]

    # split image
    div_img_value = int(img_width / 4)
    left_img = img[1:img_height, 0:div_img_value]
    mid_img = img[1:img_height, div_img_value:div_img_value * 3]
    right_img = img[1:img_height, div_img_value * 3:div_img_value * 4]
    img_split = [left_img, mid_img, right_img]
    img_split_contours = []
    lines = [0, 0, 0]
    forward_line = 0

    left = False
    middle = False
    right = False

    ##################
    ### MAKE TURN DECISION
    ##################

    # Lines for split images
    for f in range(0, 3):
        i = img_split[f]
        # Add gray scale effect
        gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
        # Add blur effect
        blurred = cv2.GaussianBlur(gray, (9, 9), 0)
        # Add threshold effect
        rt, threshold = cv2.threshold(blurred, gray_threshold_min, gray_threshold_max, cv2.THRESH_BINARY_INV)
        # Detect lines of the image
        contours, hierarchy = cv2.findContours(threshold.copy(), 1, cv2.CHAIN_APPROX_NONE)
        for i in contours:
            lines[f] = lines[f] + 1
        try:
            # If there are any lines
            if len(contours) > 0:
                c = max(contours, key=cv2.contourArea) # Find biggest contour
                M = cv2.moments(c) # Center of that contour
                cx = int(M['m10'] / M['m00']) # X coordiantes contour
                cy = int(M['m01'] / M['m00']) # Y coordiantes contour
                cv2.line(i, (cx, 0), (cx, 720), (255, 0, 0), 1) # Create line around x axis of contour
                cv2.line(i, (0, cy), (1280, cy), (255, 0, 0), 1) # Create line around y axis of contour
                cv2.drawContours(i, contours, -1, (0, 255, 0), 1) # Draw the lines

                if f == 0: # If left image
                    left = True
                elif f == 1: # If middle image
                    forward_line = cx
                    middle = True
                else: # If right image
                    right = True
            else:
                pass
        except:
            print("failure")

    # Add gray scale effect
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Add blur effect
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    # Add threshold effect
    rt, threshold = cv2.threshold(blurred, gray_threshold_min, gray_threshold_max, cv2.THRESH_BINARY_INV)
    # Detect lines of the image
    contours, hierarchy = cv2.findContours(threshold.copy(), 1, cv2.CHAIN_APPROX_NONE)

    ##############
    ### WHOLE IMAGE
    ##############

    try:
        # If there are any lines
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea) # Find contour with biggest area
            M = cv2.moments(c) # Center of that contour
            cx = int(M['m10'] / M['m00']) # X coordiantes contour
            cy = int(M['m01'] / M['m00']) # Y coordiantes contour
            cv2.line(img, (cx, 0), (cx, 720), (255, 0, 0), 1) # Create line around x axis of contour
            cv2.line(img, (0, cy), (1280, cy), (255, 0, 0), 1) # Create line around y axis of contour
            cv2.drawContours(img, contours, -1, (0, 255, 0), 1) # Draw the lines
            cv2.imshow('raw_video', img)
            #cv2.imshow('gray_scale', gray)
            #cv2.imshow('threshold', threshold)
            #cv2.imshow('left', left_img)
            #cv2.imshow('mid', mid_img)
            #cv2.imshow('right', right_img)

            # NOW DO A CHECK ON WHAT LINE DECISON WAS MADE

            if cv2.waitKey(1) & 0xFF == ord('q'):
                pass

            if left: # Left turn 90 degrees
                return('left', 10, 100)
            elif middle: # Straight
                # Follow straight line
                if forward_line > img_width/2: # Right of centre
                    cx =  img_width/2 - (cx - img_width/2 )
                    r = 1 - (cx/(img_width/2)) *2
                    return('right', 100, r)
                elif forward_line < img_width/2: # Left of centre
                    l = 1 - (cx/(img_width/2)) *2
                    return('left', l, 100)
                else:
                    return("straight", 100, 100)
            elif right: # Right turn 90 degrees
                # Turn right
                return('right', 100, 10)
            else: # No line :^(
                return("no", 0, 0)
        else:
            return('no', 0 ,0)
    except:
        print("failure")


###########
###########
# MAIN LOOP
###########
###########
Core.run = False
Core.move(50, 50)

while True:
    command, l, r = image()
    if command == 'left':
        print('left')
        Core.move(l, r)
    elif command == 'right':
        print('right')
        Core.move(l, r)
    elif command == 'no':
        if last_command == 'left':
            Core.move(0, 100)
            command = 'left'
        print("Find line")
        Core.move(100, 0)
    else:
        print('straight')
        Core.move(80, 65)
    last_command = command
