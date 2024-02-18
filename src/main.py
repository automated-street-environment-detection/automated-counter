# Main Driver file. All used components will be imported from the components folder
import cv2

def main():
    cap = cv2.VideoCapture("pathToVideo")

    while (cap.isOpened()):
        ret, frame = cap.read()
        
        cv2.imshow("Frame", frame)
        
        key = cv2.waitKey(30)

        if cv2.getWindowProperty("Frame", cv2.WND_PROP_VISIBLE) <1 or key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    
if (__name__ == '__main__'):
    main()