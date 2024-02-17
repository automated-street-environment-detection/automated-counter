#!/usr/bin/env python3

import csv

# Given a filename, header, and data. Will create a CSV file. 
def createCSV(filename="default.csv", header=["default"], data=["default"]):
    with open(filename, 'w', newline='') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(header)
        csvwriter.writerows(data)