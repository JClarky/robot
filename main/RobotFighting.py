from imutils.video import VideoStream # For video stream
import imutils # Resizing frame
import cv2, Core # Open CV

tracker = cv2.TrackerKCF_create()

# initialize the FPS throughput estimator
fps = None
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
initBB = None # 4 Part tuple that is (x, y, width, height)
objX = None # X value of the object

turning_threhold = 20

# loop over frames from the video stream
while True:
        # Read video stream frame
        ret, frame = cap.read()

        # Resize the frame
        #frame = imutils.resize(frame, width=500)
        (H, W) = frame.shape[:2]

        frame = cv2.flip(frame, 0) # vert
        frame = cv2.flip(frame, 1) # horz

        print(H,W)

        img_width = W
        img_height = H

        # Check to see if we are currently tracking an object
        if initBB is not None: # We are tracking
                # Get new bounding box coordinates
                (success, box) = tracker.update(frame)
                # check to see if the tracking was a success
                if success:
                        (x, y, w, h) = [int(v) for v in box]
                        # Make a rectangle
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        objX = x+w/2
                        #print(objX)
                        #print(objX)
                        '''if(objX > 250+turning_threhold): # Object center is on the right
                                print("right")
                        elif(objX < 250-turning_threhold): # Object center is on the left
                                print("left")
                        else:
                            print("straight")'''

                        if objX > img_width/2: # Right of centre
                            objX =  img_width/2 - (objX - img_width/2 )
                            r = (objX/(img_width/2)) * 100
                            print('right', 100, r)
                            Core.move(100,r)
                        elif objX < img_width/2: # Left of centre
                            l = (objX/(img_width/2)) * 100
                            print('left', l, 100)
                            Core.move(l,100)
                        else:
                            print("straight", 100, 100)
                            Core.move(100, 100)

        # Show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"): # If the 's' key is selected, we are going to "select" a bounding box to track
                # select the bounding box of the object we want to track
                #initBB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
                x_center = img_width/2
                y_center = img_height/2
                width = 100
                height = 50
                x =  x_center - width/2
                y = y_center - height/2

                initBB = (x, y, width, height)

                tracker.init(frame, initBB) # Track using supplied bounding box coordinates


cv2.destroyAllWindows()
