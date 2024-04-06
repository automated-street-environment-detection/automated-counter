import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk
from vidstab import VidStab
from exportToCSV import export_to_csv
from exportToExcel import export_to_excel
from printResults import print_results

# Initialize vehicle counts
vehicle_counts = {"moto": 0, "car": 0, "bike": 0, "ebike": 0, "bus": 0, "ped": 0, "truck": 0, "minibus/van": 0, "other": 0}

# Initialize vehicle location counts
vehicle_loc_counts = {f"{location}_{vehicle}": 0 for location in ["Lane", "Lim_ww", "Sidewalk"] for vehicle in vehicle_counts.keys()}

# Initialize vehicle timestamps
vehicle_timestamps = {key: [] for key in vehicle_loc_counts}

# Initialize license color counts
license_color_counts = {f"{color}_{vehicle}": 0 for color in ["yellow", "white"] for vehicle in vehicle_counts.keys()}

# Option to include milliseconds in timestamps
include_milliseconds = False

# Global variable to hold the pause state
is_paused = False

# Create the main window
root = tk.Tk()
root.title("Vehicle Counter")
root.geometry("1500x1000")  # Set the window size

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
        selected_color = selected_license_color.get()
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
        if selected_color:  # Only update licenseColor_counts if a color is selected
            color_key = f"{selected_color}_{vehicle}"
            license_color_counts[color_key] += 1
            selected_license_color.set("")  # Uncheck the checkbox after incrementing


    def decrement(vehicle=vehicle, label=count_label):
        selected_location = selected_location_type.get()
        selected_color = selected_license_color.get()
        if not selected_location:
            messagebox.showwarning("Warning", "Please select a location type first.")
            return

        # Decrement license_color_counts
        if selected_color:  # Only update license_color_counts if a color is selected
            color_key = f"{selected_color}_{vehicle}"
            if license_color_counts[color_key] > 0:
                license_color_counts[color_key] -= 1
                selected_license_color.set("")  # Uncheck the checkbox after incrementing
            else:
                messagebox.showerror("Error", "No vehicles to decrement for license color + vehicle type combo.")
                return

        # Decrement vehicle_loc_counts
        key = f"{selected_location}_{vehicle}"
        if vehicle_counts[vehicle] > 0 and vehicle_loc_counts[key] > 0:
            vehicle_counts[vehicle] -= 1
            vehicle_loc_counts[key] -= 1
            label.config(text=str(vehicle_counts[vehicle]))
            if video_capture and vehicle_timestamps[key]:
                vehicle_timestamps[key].pop()
        else:
            messagebox.showerror("Error", "No vehicles to decrement for vehicle type + location combo.")


    increment_button = ttk.Button(vehicle_type_frame, text="+", command=increment)
    increment_button.grid(row=row, column=2, padx=5, pady=5)

    decrement_button = ttk.Button(vehicle_type_frame, text="-", command=decrement)
    decrement_button.grid(row=row, column=3, padx=5, pady=5)

    row += 1

#####################################################################################
## Location Type UI Elements
#####################################################################################

# Create a frame for location types
location_type_frame = ttk.LabelFrame(controls_frame, text="Location Types", padding=10)
location_type_frame.pack(fill=tk.BOTH, expand=True)

location_types = ["Lane", "Lim_ww", "Sidewalk"]
selected_location_type = tk.StringVar()

for i, location_type in enumerate(location_types):
    radio_button = ttk.Radiobutton(location_type_frame, text=location_type.capitalize(),
                                   variable=selected_location_type, value=location_type)
    radio_button.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="w")
#####################################################################################

#####################################################################################
## License Color UI Elements
#####################################################################################

# Create a frame for license color selection
license_color_frame = ttk.LabelFrame(controls_frame, text="License Colors", padding=10)
license_color_frame.pack(fill=tk.BOTH, expand=True)

license_colors = ["yellow", "white"]
selected_license_color = tk.StringVar()

for i, license_color in enumerate(license_colors):
    # check_button = ttk.Checkbutton(license_color_frame, text=license_color.capitalize(),
    #                                variable=selected_license_color, onvalue=license_color, offvalue="")
    # check_button.grid(row=i // 2, column=i % 2, padx=5, pady=5, sticky="w")
    radio_button = ttk.Radiobutton(license_color_frame, text=license_color.capitalize(),
                                   variable=selected_license_color, value=license_color)
    radio_button.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="w")
#####################################################################################

# Create a frame for buttons
button_frame = ttk.Frame(controls_frame)
button_frame.pack(fill=tk.BOTH, pady=10)

# Function to open a video file
video_capture = None


def open_video():
    global video_capture
    file_path = filedialog.askopenfilename()
    if file_path:
        # Ask the user if they want to stabilize the video
        stabilize_video = messagebox.askyesno("Stabilize Video", "Do you want to stabilize the video?")
        if stabilize_video:
            # Create a VidStab object
            stabilizer = VidStab()

            # Stabilize the video
            stabilizer.stabilize(input_path=file_path, output_path='stabilized_output.avi')

            # Open the stabilized video
            video_capture = cv2.VideoCapture('stabilized_output.avi')
        else:
            # Open the video without stabilizing
            video_capture = cv2.VideoCapture(file_path)
        update_video_frame()

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


# Function to print the results
def print_button_clicked():
    print_results(vehicle_loc_counts, license_color_counts, vehicle_timestamps, include_milliseconds)


def export_csv_button_clicked():
    export_to_csv(vehicle_loc_counts, license_color_counts, vehicle_timestamps, include_milliseconds)


def export_excel_button_clicked():
    export_to_excel(vehicle_loc_counts, license_color_counts, vehicle_timestamps, include_milliseconds)


# Row 1
open_button = ttk.Button(button_frame, text="Open Video", command=open_video)
open_button.grid(row=0, column=0, padx=5, pady=5)

pause_button = ttk.Button(button_frame, text="Pause/Resume", command=toggle_pause)
pause_button.grid(row=0, column=1, padx=5, pady=5)

results_button = ttk.Button(button_frame, text="Print Results", command=print_button_clicked)
results_button.grid(row=0, column=2, padx=5, pady=5)

# Row 2
exportCSV_button = ttk.Button(button_frame, text="Export to CSV", command=export_csv_button_clicked)
exportCSV_button.grid(row=1, column=0, padx=5, pady=5)

exportExcel_button = ttk.Button(button_frame, text="Export to Excel", command=export_excel_button_clicked)
exportExcel_button.grid(row=1, column=1, padx=5, pady=5)

# Start the main event loop
root.mainloop()