import cv2
import numpy as np

def nothing():
	pass

def gstreamer_pipeline(
    capture_width=512,
    capture_height=512,
    display_width=512,
    display_height=512,
    framerate=100,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0))

if not cap.isOpened():
	exit()

# Creating a window for later use
window_handle = cv2.namedWindow('result', cv2.WINDOW_AUTOSIZE)

# Starting with 100's to prevent error while masking
h,s,v = 100,100,100

# Creating track bar
cv2.createTrackbar('h', 'result',0,179,nothing)
cv2.createTrackbar('s', 'result',0,255,nothing)
cv2.createTrackbar('v', 'result',0,255,nothing)

while True:

	ret, frame = cap.read()
	#if not ret:
	#	continue
	#converting to HSV
	hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

	# get info from track bar and appy to result
	h = cv2.getTrackbarPos('h','result')
	s = cv2.getTrackbarPos('s','result')
	v = cv2.getTrackbarPos('v','result')

	# Normal masking algorithm
	lower_blue = np.array([h,s,v])
	upper_blue = np.array([180,255,255])

	mask = cv2.inRange(hsv,lower_blue, upper_blue)

	result = cv2.bitwise_and(frame,frame,mask = mask)

	cv2.imshow('result',result)

	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break
cap.release()
cv2.destroyAllWindows()
