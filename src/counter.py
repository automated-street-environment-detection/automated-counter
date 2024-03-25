import tkinter as tk
from tkinter import filedialog, Canvas, Frame, Scrollbar
import cv2
from PIL import Image, ImageTk
import datetime

# Initialize vehicle counts
vehicle_counts = {"moto": 0, "car": 0, "bike": 0, "ebike": 0, "bus": 0, "ped": 0, "truck": 0, "other": 0}
vehicle_loc_counts = {"Lane_moto": 0, "Lane_car": 0, "Lane_bike": 0, "Lane_ebike": 0,"Lane_bus": 0, "Lane_ped": 0, "Lane_truck": 0, "Lane_other": 0,
                  "Lim_ww_moto": 0, "Lim_ww_car": 0, "Lim_ww_bike": 0, "Lim_ww_ebike": 0,"Lim_ww_bus": 0, "Lim_ww_ped": 0, "Lim_ww_truck": 0, "Lim_ww_other": 0,
                  "Sidewalk_moto": 0, "Sidewalk_car": 0, "Sidewalk_bike": 0, "Sidewalk_ebike": 0,"Sidewalk_bus": 0, "Sidewalk_ped": 0, "Sidewalk_truck": 0, "Sidewalk_other": 0}
vehicle_timestamps = {key: [] for key in vehicle_loc_counts}

# Option to include milliseconds in timestamps
include_milliseconds = False

# Global variable to hold the pause state
is_paused = False

# Create the main window
root = tk.Tk()
root.title("Vehicle Counter")
root.geometry("1500x1000")  # Set the window size

# Create a canvas to hold the vehicle frame
canvas = tk.Canvas(root)
canvas.grid(row=0, column=1, padx=20, pady=20, sticky="ns")

# Create a scrollbar for the canvas
# scrollbar = tk.Scrollbar(root, command=canvas.yview)
# scrollbar.grid(row=0, column=2, sticky="ns")

# Configure the canvas to use the scrollbar
# canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold the buttons and labels
vehicle_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=vehicle_frame, anchor="nw")

# Bind the frame to the canvas to adjust its size when the window is resized
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

vehicle_frame.bind("<Configure>", on_frame_configure)

# Create a label for video display
video_label = tk.Label(root)
video_label.grid(row=0, column=0, padx=20, pady=20)

# Create buttons and labels for vehicle types
vehicle_type_frame = tk.Frame(vehicle_frame)
vehicle_type_frame.pack(pady=10)

row = 0
for vehicle in sorted(vehicle_counts.keys()):
    label = tk.Label(vehicle_type_frame, text=vehicle.capitalize(), font=("Arial", 16))
    label.grid(row=row, column=0, sticky="w", padx=10, pady=10)

    count_label = tk.Label(vehicle_type_frame, text="0", font=("Arial", 16))
    count_label.grid(row=row, column=1, sticky="w", padx=10, pady=10)


    def increment(vehicle=vehicle, label=count_label):
        if selected_location_type is None:
            print("Please select a location type first.")
            return
        key = f"{selected_location_type}_{vehicle}"
        vehicle_counts[vehicle] += 1
        vehicle_loc_counts[key] += 1
        label.config(text=str(vehicle_counts[vehicle]))
        if video_capture:
            timestamp = video_capture.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Convert to seconds
            vehicle_timestamps[key].append(timestamp)

    def decrement(vehicle=vehicle, label=count_label):
        if selected_location_type is None:
            print("Please select a location type first.")
            return
        key = f"{selected_location_type}_{vehicle}"
        if vehicle_counts[vehicle] > 0 and vehicle_loc_counts[key] > 0:
            vehicle_counts[vehicle] -= 1
            vehicle_loc_counts[key] -= 1
            label.config(text=str(vehicle_counts[vehicle]))
            if video_capture and vehicle_timestamps[key]:
                vehicle_timestamps[key].pop()
        else:
            print("No vehicles to decrement.")

    increment_button = tk.Button(vehicle_type_frame, text="+", font=("Arial", 16), command=increment)
    increment_button.grid(row=row, column=2, padx=10, pady=10)

    decrement_button = tk.Button(vehicle_type_frame, text="-", font=("Arial", 16), command=decrement)
    decrement_button.grid(row=row, column=3, padx=10, pady=10)

    row += 1

# Create buttons for location types
location_type_frame = tk.Frame(vehicle_frame)
location_type_frame.pack(pady=10)

location_types = ["Lane", "Lim_ww", "Sidewalk"]
location_buttons = []

for i, location_type in enumerate(location_types):
    def select_location_type(event, location_type=location_type):
        for button in location_buttons:
            button.config(relief=tk.RAISED)
        event.widget.config(relief=tk.SUNKEN)
        global selected_location_type
        selected_location_type = location_type

    button = tk.Button(location_type_frame, text=location_type.capitalize(), font=("Arial", 16), relief=tk.RAISED)
    button.grid(row=0, column=i, padx=10, pady=10)
    button.bind("<Button-1>", select_location_type)
    location_buttons.append(button)

selected_location_type = None

# Function to open a video file
video_capture = None
def open_video():
    global video_capture
    file_path = filedialog.askopenfilename()
    if file_path:
        video_capture = cv2.VideoCapture(file_path)
        update_video_frame()

open_button = tk.Button(root, text="Open Video", font=("Arial", 14), command=open_video)
open_button.grid(row=1, column=1)

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
pause_button = tk.Button(root, text="Pause/Resume", font=("Arial", 14), command=toggle_pause)
pause_button.grid(row=3, column=1)

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

results_button = tk.Button(root, text="Print Results", font=("Arial", 14), command=print_results)
results_button.grid(row=2, column=1)

# Start the main event loop
root.mainloop()