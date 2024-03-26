import datetime

def print_results(vehicle_loc_counts, vehicle_timestamps, include_milliseconds):
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