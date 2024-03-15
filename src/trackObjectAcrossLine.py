import cv2
import numpy as np
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO("yolov8n.pt", verbose=False)

# Load video
cap = cv2.VideoCapture('video1.mp4')

# Get video properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Initialize variables
prev_frame = None
road_edges = None
rightmost_x = None
object_count = 0
objects_crossed = set()

# Add a counter for the frames
frame_counter = 0

# Set the number of frames to skip before running object detection
skip_frames = 1 # Change this value to adjust the frequency

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run the YOLOv8 detection only every nth frame
    if frame_counter % skip_frames == 0:
        # Run the YOLOv8 detection
        results = model(frame)

        # Filter the results for specific classes (e.g., persons, cars, and motorcycles)
        filtered_results = results[0].boxes[
            (results[0].boxes.cls == 0) |  # Persons
            (results[0].boxes.cls == 2) |  # Cars
            (results[0].boxes.cls == 3)    # Motorcycles
        ]

        # Draw bounding boxes and count objects that cross the line
        for box in filtered_results:
            x1, y1, x2, y2 = map(int, box.xyxy.tolist()[0])
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # If the previous frame is not None
    if prev_frame is not None:
        # Calculate the difference between the current frame and the previous frame
        diff = cv2.absdiff(prev_frame, frame)

        # Apply a threshold to the difference
        _, diff = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        # Convert the difference image to grayscale
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # Find the rightmost contour
        contours, _ = cv2.findContours(diff_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
        angle = np.arctan2(center_y - height, center_x - width / 2)

        # Calculate the slope of the road
        slope = np.tan(angle)

        # Calculate the y-intercept of the road
        y_intercept = height - slope * width / 2

        # Set the left point as (0, y1)
        x1 = 0
        y1 = slope * x1 + y_intercept

        # Set the right point as (width, y2)
        x2 = width
        y2 = slope * x2 + y_intercept

        # Draw the line on the frame
        cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        # Check if the object has crossed the line
        if center_y > y2 and center_x not in objects_crossed:
            object_count += 1
            objects_crossed.add(center_x)

    # Save the current frame
    prev_frame = frame

    # Show the frame
    cv2.imshow('frame', frame)

    # Wait for the next frame to maintain the video's original frame rate
    key = cv2.waitKey(1)

    # If the 'q' key is pressed, exit the loop
    if key == ord('q'):
        break

    # Increment the frame counter
    frame_counter += 1

# Release the video capture object
cap.release()

# Destroy all windows
cv2.destroyAllWindows()

print(f"Total objects crossed: {object_count}")
