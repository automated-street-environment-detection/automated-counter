# draw the box on the video and save the box coordinates to the csv file as perisitance data
import cv2
import csv

# Global variables
drawing_box = False
box_start = (0, 0)
box_end = (100, 100)

# Read CSV file to get video filenames and their corresponding box coordinates
def read_csv_file(csv_filename):
    video_data = {}
    with open(csv_filename, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            video_data[row[0]] = (eval(row[1]), eval(row[2]))  
    return video_data

# Write updated box coordinates to CSV file
def write_to_csv(csv_filename, video_data):
    with open(csv_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for video_filename, (box_start, box_end) in video_data.items():
            csvwriter.writerow([video_filename, box_start, box_end])

# Mouse callback function for drawing box
def draw_box(event, x, y, flags, param):
    global box_start, box_end, drawing_box
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing_box = True
        box_start = (x, y)
        print("Box start:", box_start)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing_box:
            box_end = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing_box = False
        box_end = (x, y)
        print("Box end:", box_end)
    

# Function to process video and store data
def process_video(video_filename, video_data):
    global box_start, box_end
    if video_filename not in video_data:
        # Default box coordinates for the video
        default_box_coordinates = ((0, 450), (1200, 700))
        video_data[video_filename] = default_box_coordinates
    
    # Get the box coordinates for the video
    box_start, box_end = video_data[video_filename]
    # Open the video file
    video_capture = cv2.VideoCapture(video_filename)
    # Get the width and height of the video
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_video = cv2.VideoWriter('output_video.mov', fourcc, 30.0, (width, height))
    # Create a window and set the mouse callback function
    cv2.namedWindow('Video')
    cv2.setMouseCallback('Video', draw_box)

    # Loop through each frame of the video
    for _ in range(int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))):
        ret, frame = video_capture.read()
        if not ret:
            break
        # Draw the box on the frame
        cv2.rectangle(frame, box_start, box_end, (0, 255, 0), 2)
        output_video.write(frame)
        cv2.imshow('Video', frame)
        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and writer objects
    video_capture.release()
    output_video.release()
    
    # Close all OpenCV windows
    cv2.destroyAllWindows()
    print("Video processing complete.")

    # Write updated box coordinates to CSV file
    video_data[video_filename] = (box_start, box_end)
    write_to_csv('video_data.csv', video_data)  

# Main function
video_filename = 'test.mov' # 'test.mov' is the video file name replace the name if needed
video_data = read_csv_file('video_data.csv')  # replace the name of the csv file if needed
process_video(video_filename, video_data)  # Process video and update CSV file

