from tkinter import filedialog
import datetime
import pandas as pd

def export_to_excel(vehicle_loc_counts, license_color_counts, vehicle_timestamps, include_milliseconds):
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx")
    if file_path:
        # Prepare data for vehicle_loc_counts
        vehicle_counts_data = [[vehicle.capitalize(), count] for vehicle, count in sorted(vehicle_loc_counts.items())]
        vehicle_counts_df = pd.DataFrame(vehicle_counts_data, columns=["Vehicle", "Count"])

        # Prepare data for license_color_counts
        color_counts_data = [[color.capitalize(), count] for color, count in sorted(license_color_counts.items())]
        color_counts_df = pd.DataFrame(color_counts_data, columns=["Color", "Count"])

        # Combine all timestamps into a single list
        all_timestamps = []
        for timestamps in vehicle_timestamps.values():
            all_timestamps.extend(timestamps)

        # Sort the combined list of timestamps
        all_timestamps.sort()

        # Prepare data for timestamps
        timestamps_data = []

        for timestamp in all_timestamps:
            for vehicle, timestamps in vehicle_timestamps.items():
                if timestamp in timestamps:
                    if include_milliseconds:
                        time_parts = str(datetime.timedelta(seconds=timestamp)).split(':')[1:]
                        time_str = ":".join(time_parts)
                    else:
                        time_parts = str(datetime.timedelta(seconds=int(timestamp))).split(':')[1:]
                        time_str = ":".join(time_parts)
                    timestamps_data.append([vehicle.capitalize(), time_str])
        timestamps_df = pd.DataFrame(timestamps_data, columns=["Vehicle", "Timestamp"])

        # Write to Excel file with two sheets
        with pd.ExcelWriter(file_path) as writer:
            vehicle_counts_df.to_excel(writer, sheet_name='Vehicle Counts', index=False)
            color_counts_df.to_excel(writer, sheet_name='Color Counts', index=False)
            timestamps_df.to_excel(writer, sheet_name='Timestamps', index=False)

        print(f"Data exported to {file_path}")