import cv2
import numpy as np

# Load video
cap = cv2.VideoCapture('video1.mp4')

# Get video properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Initialize variables
prev_frame = None
road_edges = None
rightmost_x = None  # Add this line

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blur, 50, 150)

    # If the previous frame is not None
    if prev_frame is not None:
        # Calculate the difference between the current frame and the previous frame
        diff = cv2.absdiff(edges, prev_frame)

        # Apply a threshold to the difference
        _, diff = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        # Find the contours of the difference
        contours, _ = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the rightmost contour
        rightmost_contour = max(contours, key=cv2.contourArea)

        # Get the bounding rectangle of the rightmost contour
        x, y, w, h = cv2.boundingRect(rightmost_contour)

        # If rightmost_x is None, update it with the current rightmost x-coordinate
        if rightmost_x is None:
            rightmost_x = x + w

        # Calculate the center of the bounding rectangle
        center_x = rightmost_x  # Use the stored rightmost_x here
        center_y = y + h // 2

        # Calculate the angle of the road
        angle = np.arctan2(center_y - height, center_x - width/2)

        # Calculate the slope of the road
        slope = np.tan(angle)

        # Calculate the y-intercept of the road
        y_intercept = height - slope * width/2

        # Set the left point as (0, y1)
        x1 = 0
        y1 = slope * x1 + y_intercept

        # Set the right point as (width, y2)
        x2 = width
        y2 = slope * x2 + y_intercept

        # Draw the line on the frame
        cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    # Save the current frame
    prev_frame = edges

    # Show the frame
    cv2.imshow('frame', frame)

    # If the 'q' key is pressed, exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()

# Destroy all windows
cv2.destroyAllWindows()
