import tkinter as tk
from tkinter import ttk, filedialog
import cv2
from PIL import Image, ImageTk
import datetime

# Initialize vehicle counts
vehicle_counts = {"moto": 0, "car": 0, "bike": 0, "ebike": 0, "bus": 0, "ped": 0, "truck": 0, "other": 0}
vehicle_loc_counts = {"Lane_moto": 0, "Lane_car": 0, "Lane_bike": 0, "Lane_ebike": 0, "Lane_bus": 0, "Lane_ped": 0, "Lane_truck": 0, "Lane_other": 0,
                      "Lim_ww_moto": 0, "Lim_ww_car": 0, "Lim_ww_bike": 0, "Lim_ww_ebike": 0, "Lim_ww_bus": 0, "Lim_ww_ped": 0, "Lim_ww_truck": 0, "Lim_ww_other": 0,
                      "Sidewalk_moto": 0, "Sidewalk_car": 0, "Sidewalk_bike": 0, "Sidewalk_ebike": 0, "Sidewalk_bus": 0, "Sidewalk_ped": 0, "Sidewalk_truck": 0, "Sidewalk_other": 0}
vehicle_timestamps = {key: [] for key in vehicle_loc_counts}

# Option to include milliseconds in timestamps
include_milliseconds = False

# Global variable to hold the pause state
is_paused = False

# Create the main window
root = tk.Tk()
root.title("Vehicle Counter")
root.geometry("1200x800")  # Set the window size

# Create a style for the app
style = ttk.Style()
style.theme_use("clam")

# Create a frame for the video display
video_frame = ttk.Frame(root)
video_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a label for video display
video_label = ttk.Label(video_frame)
video_label.pack(fill=tk.BOTH, expand=True)

# Create a frame for the controls
controls_frame = ttk.Frame(root)
controls_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH)

# Create a frame for vehicle types
vehicle_type_frame = ttk.LabelFrame(controls_frame, text="Vehicle Types", padding=10)
vehicle_type_frame.pack(fill=tk.BOTH, expand=True)

# Create buttons and labels for vehicle types
vehicle_buttons = []
row = 0
for vehicle in sorted(vehicle_counts.keys()):
    label = ttk.Label(vehicle_type_frame, text=vehicle.capitalize(), font=("Arial", 14))
    label.grid(row=row, column=0, sticky="w", padx=5, pady=5)

    count_label = ttk.Label(vehicle_type_frame, text="0", font=("Arial", 14))
    count_label.grid(row=row, column=1, sticky="w", padx=5, pady=5)

    def increment(vehicle=vehicle, label=count_label):
        selected_location = selected_location_type.get()
        if not selected_location:
            print("Please select a location type first.")
            return
        key = f"{selected_location}_{vehicle}"
        vehicle_counts[vehicle] += 1
        vehicle_loc_counts[key] += 1
        label.config(text=str(vehicle_counts[vehicle]))
        if video_capture:
            timestamp = video_capture.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Convert to seconds
            vehicle_timestamps[key].append(timestamp)

    def decrement(vehicle=vehicle, label=count_label):
        selected_location = selected_location_type.get()
        if not selected_location:
            print("Please select a location type first.")
            return
        key = f"{selected_location}_{vehicle}"
        if vehicle_counts[vehicle] > 0 and vehicle_loc_counts[key] > 0:
            vehicle_counts[vehicle] -= 1
            vehicle_loc_counts[key] -= 1
            label.config(text=str(vehicle_counts[vehicle]))
            if video_capture and vehicle_timestamps[key]:
                vehicle_timestamps[key].pop()
        else:
            print("No vehicles to decrement.")

    increment_button = ttk.Button(vehicle_type_frame, text="+", command=increment)
    increment_button.grid(row=row, column=2, padx=5, pady=5)

    decrement_button = ttk.Button(vehicle_type_frame, text="-", command=decrement)
    decrement_button.grid(row=row, column=3, padx=5, pady=5)

    row += 1

# Create a frame for location types
location_type_frame = ttk.LabelFrame(controls_frame, text="Location Types", padding=10)
location_type_frame.pack(fill=tk.BOTH, expand=True)

location_types = ["Lane", "Lim_ww", "Sidewalk"]
selected_location_type = tk.StringVar()

for i, location_type in enumerate(location_types):
    radio_button = ttk.Radiobutton(location_type_frame, text=location_type.capitalize(), variable=selected_location_type, value=location_type)
    radio_button.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="w")

# Create a frame for buttons
button_frame = ttk.Frame(controls_frame)
button_frame.pack(fill=tk.BOTH, pady=10)

# Function to open a video file
video_capture = None
def open_video():
    global video_capture
    file_path = filedialog.askopenfilename()
    if file_path:
        video_capture = cv2.VideoCapture(file_path)
        update_video_frame()

open_button = ttk.Button(button_frame, text="Open Video", command=open_video)
open_button.pack(side=tk.LEFT, padx=5)

# Function to update the video frame
def update_video_frame():
    global is_paused
    if is_paused:
        return
    if video_capture:
        ret, frame = video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (960, 540))  # Resize the frame
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            video_label.configure(image=photo)
            video_label.image = photo  # Keep a reference to prevent garbage collection
            video_label.after(40, update_video_frame)  # Update every 40 ms (0.5x speed)

# Function to toggle pause state
def toggle_pause():
    global is_paused
    is_paused = not is_paused
    if not is_paused:
        update_video_frame()

# Button to pause/resume video
pause_button = ttk.Button(button_frame, text="Pause/Resume", command=toggle_pause)
pause_button.pack(side=tk.LEFT, padx=5)

# Function to print the results
def print_results():
    print("Total Vehicle Counts:")
    for vehicle, count in vehicle_loc_counts.items():
        print(f"{vehicle.capitalize()}: {count}")

    print("\nTimestamps:")
    for vehicle, timestamps in vehicle_timestamps.items():
        print(f"{vehicle.capitalize()}:")
        for timestamp in timestamps:
            if include_milliseconds:
                time_parts = str(datetime.timedelta(seconds=timestamp)).split(':')[1:]
                time_str = ":".join(time_parts)
            else:
                time_parts = str(datetime.timedelta(seconds=int(timestamp))).split(':')[1:]
                time_str = ":".join(time_parts)
            print(f"  {time_str}")

results_button = ttk.Button(button_frame, text="Print Results", command=print_results)
results_button.pack(side=tk.LEFT, padx=5)

# Start the main event loop
root.mainloop()