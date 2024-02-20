import cv2

VIDEO_PATH = "path"

def main():
    cap = cv2.VideoCapture(VIDEO_PATH)



    object_detector = cv2.creatBackgroundSubtractorMOG2()
    #improvement object_detector = cv2.creatBackgroundSubtractorMOG2(history=100(high),varThreshold=5(low but may cause false postive))

    while (cap.isOpened()):
        ret, frame = cap.read()
        
        height,weight,_=frame.shape
        
        #extract region of interst
        roi = frame[(the_region_you_want(--:--,--:--))]
        # Extract 
        mask = object_detector.apply(roi)
        _,mask = cv2.threshold(mask,254,255,cv2.THRESH_BINARY)
        contours,__ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        detections = []  #Array stored all the moving object
        object_id = 0

        for cnt in contours :
            #remove small moving element
            area = cv2.contourArea(cnt)
            if area>100: #100pixel(have to adjust)
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(roi,(x,y),(x+w,y+h),(0,255,0),2) #gleen(0,255,0) and thickness2
                detections.append([x,y,w,h,object_id])
                object_id += 1
        
        #need to improve to track the object
        # Draw bounding boxes for tracked objects
        for detection in detections:
            x, y, w, h, did = detection
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(roi, str(did), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        cv2.imshow("roi",roi)
        cv2.imshow("Mask",mask) #only moving object show in the background



        cv2.imshow("Frame", frame)
        key = cv2.waitKey(30)
        if cv2.getWindowProperty("Frame", cv2.WND_PROP_VISIBLE) <1 or key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    
if (__name__ == '__main__'):
    main()