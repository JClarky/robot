from imutils.video import VideoStream # For video stream
import imutils # Resizing frame
import cv2 # Open CV

tracker = cv2.TrackerKCF_create()

# initialize the FPS throughput estimator
fps = None
vs = VideoStream(src=0).start()
initBB = None # 4 Part tuple that is (x, y, width, height) 
objX = None # X value of the object

turning_threhold = 20

# loop over frames from the video stream
while True:
        # Read video stream frame
        frame = vs.read()

        # Resize the frame
        frame = imutils.resize(frame, width=500)
        (H, W) = frame.shape[:2]

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
                        print(objX)
                        if(objX > 250+turning_threhold): # Object center is on the right
                                print("right")
                        elif(objX < 250-turning_threhold): # Object center is on the left
                                print("left")
                        else:
                            print("straight")

        # Show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"): # If the 's' key is selected, we are going to "select" a bounding box to track      
                # select the bounding box of the object we want to track
                #initBB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
                x_center = 250
                y_center = 200
                width = 100
                height = 50
                x =  x_center - width/2
                y = y_center - height/2
                initBB = (x, y, width, height)
                
                tracker.init(frame, initBB) # Track using supplied bounding box coordinates
                
        elif key == ord("q"): # if the `q` key was pressed, break from the loop
                break

vs.stop()
cv2.destroyAllWindows()
