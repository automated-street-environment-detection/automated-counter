#!/usr/bin/env python3
# Main Driver file. All used components will be imported from the components folder

# Example import for future reference
from components.toCSV import createCSV

filename = "sample_output.csv"
header = ['Name','Email']
data = [['Mitsuaki', 'MitsuakiEmail@sample.com'], ['Adit', 'AditEmail@sample.com'], ['Jayden', 'JaydenEmail@sample.com'], ['Sishir', 'SishirEmail@sample.com']]

createCSV(filename = filename, header=header, data=data)