import csv
import datetime
from tkinter import filedialog


def export_to_csv(vehicle_loc_counts, vehicle_timestamps, include_milliseconds):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv")
    if file_path:
        with open(file_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            # Write vehicle_loc_counts to the first sheet
            writer.writerow(["Vehicle", "Count"])
            for vehicle, count in sorted(vehicle_loc_counts.items()):
                writer.writerow([vehicle.capitalize(), count])

            # Add an empty row for separation
            writer.writerow([])

            # Write timestamps to the second sheet
            writer.writerow(["Vehicle", "Timestamp"])

            # Combine all timestamps into a single list
            all_timestamps = []
            for timestamps in vehicle_timestamps.values():
                all_timestamps.extend(timestamps)

            # Sort the combined list of timestamps
            all_timestamps.sort()

            # Print the timestamps along with their corresponding vehicle types
            for timestamp in all_timestamps:
                for vehicle, timestamps in vehicle_timestamps.items():
                    if timestamp in timestamps:
                        if include_milliseconds:
                            time_parts = str(datetime.timedelta(seconds=timestamp)).split(':')[1:]
                            time_str = ":".join(time_parts)
                        else:
                            time_parts = str(datetime.timedelta(seconds=int(timestamp))).split(':')[1:]
                            time_str = ":".join(time_parts)
                        writer.writerow([vehicle.capitalize(), time_str])
                        break

        print(f"Data exported to {file_path}")