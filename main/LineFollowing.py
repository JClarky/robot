# Imports
import cv2
import numpy as np
import time
import Core

# Configure camera capture
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

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
    img = img[0:100, 50:400]
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
                print(cx)
                if f == 0:
                    left = True
                elif f == 1:
                    forward_line = cx
                    middle = True
                else:
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
        else:
            return('no')
    except:
        print("failure")

    # Captured images in frames
    cv2.imshow('raw_video', img)
    #cv2.imshow('gray_scale', gray)
    #cv2.imshow('threshold', threshold)
    #cv2.imshow('left', left_img)
    #cv2.imshow('mid', mid_img)
    #cv2.imshow('right', right_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        pass

    # Figure out robot commands to send

    if left:
        # left turn 90 degrees
        print("here at left turn")
        return('left')
    elif middle:
        # go straight/asjust straight angle
        center_pixel = img_width/4 # Find center x pixel
        print(forward_line)
        if forward_line > center_pixel:
            if forward_line-center_pixel > turning_margin:
                return('slight_right')
        else:
            if center_pixel-forward_line > turning_margin:
                return('slight_left')
    elif right:
        # turn right
        return('right')
    else:
        # no line :^(
        return("no")


###########
###########
# MAIN LOOP
###########
###########
Core.run = False
Core.move(50, 50)

while True:
    time.sleep(0.3)
    command = image()
    if command == 'left':
        print('left')
        Core.left_turn()
    elif command == 'right':
        print('right')
        Core.right_turn()
    elif command == 'slight_left':
        print('slight left')
        Core.move(50, 100)
    elif command == 'slight_right':
        print('slight right')
        Core.move(100, 50)
    elif command == 'no':
        print("Find line")
        Core.move(100,-80)
    else:
        print('straight')
        Core.move(80, 65)
