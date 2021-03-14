import imutils
import cv2
#arg(Hue,Saturation, Value)
redLower = (157, 93, 203)
redUpper = (179, 255, 255)

#initialize cam
cam = cv2.VideoCapture(1)
address = "http://192.168.2.107:8080/video"
cam.open(address)
while True:
    (grabbed, frame) = cam.read()
    #resizing frame
    frame = imutils.resize(frame, width = 600)
    #smoothen frame
    blurred = cv2.GaussianBlur(frame, (11,11), 0)
    #convert bgr to hsv
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    #mask the certain color
    mask = cv2.inRange(hsv, redLower, redUpper)
    # removing holes and making one image
    mask = cv2.erode(mask, None, iterations = 2)
    mask = cv2.dilate(mask, None, iterations = 2)
    #identify shapes of object
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE) [-2]
    #initialize center
    center = None
    if len(cnts) > 0:
        c = max(cnts, key = cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        #get center coordinate
        M =cv2.moments(c)
        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
        if radius > 10:
            #draw a circle
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0,255), -1)
            if radius > 250:
                print("stop")
            else:
                if(center[0] > 150):
                    print("left")
                elif(center[0] > 450):
                    print("right")
                elif(center < 250):
                    print("center")
                else:
                    print("stop")
    cv2.imshow("frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()    
    
    
