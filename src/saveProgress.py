from tkinter import filedialog
import json

def exportToJson(vehicle_loc_counts, license_color_counts, vehicle_timestamps, vehicle_counts):
    file_path = filedialog.asksaveasfilename(defaultextension=".json")
    if file_path:
        jsonData = {
            "vehicle_loc_counts": {
                
            },
            "license_color_counts": {},
            "vehicle_timestamps": {},
            "vehicle_counts" : {},
        }
        
        for vehicle, count in vehicle_loc_counts.items():
            jsonData["vehicle_loc_counts"][vehicle] = count
            
        for color, count in license_color_counts.items():
            jsonData["license_color_counts"][color] = count
        
        # Combine all timestamps into a single list
        for vehicle, timestamps in vehicle_timestamps.items():
            jsonData["vehicle_timestamps"][vehicle] = timestamps
            
        for vehicle, count in vehicle_counts.items():
            jsonData["vehicle_counts"][vehicle] = count
        
        with open(file_path, "w") as jsonFile:
            json.dump(jsonData, jsonFile, indent=4)
            jsonFile.close()


def load_save_data(vehicle_loc_counts, license_color_counts, vehicle_timestamps, vehicle_counts):
    file_path = filedialog.askopenfilename(defaultextension=".json")
    if file_path:
        vehicle_loc_counts.clear()
        license_color_counts.clear()
        vehicle_timestamps.clear()
        jsonFile = open(file_path)
        
        jsonData = json.load(jsonFile)
        
        
        
        for vehicle, count in jsonData["vehicle_loc_counts"].items():
            vehicle_loc_counts[vehicle] = count
            print(f'{vehicle} : {count}')
            
        for color, count in jsonData["license_color_counts"].items():
            license_color_counts[color] = count
            
        for vehicle, timestamps in jsonData["vehicle_timestamps"].items():
            vehicle_timestamps[vehicle] = timestamps
            
        for vehicle, count in jsonData["vehicle_counts"].items():
            vehicle_counts[vehicle] = count
        
        jsonFile.close()
         
        