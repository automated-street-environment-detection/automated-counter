"""
Author: Adit Prabhu
Purpose: Takes two CSV files and compares them, outputting the differences.
Comments: 
"""
import csv

# Function to compare two CSV files and write the differences to an output file
def csv_diff(file1, file2, output):

    # Open the files and read the data
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        reader1 = csv.reader(f1)
        reader2 = csv.reader(f2)
        rows1 = [row for row in reader1]
        rows2 = [row for row in reader2]

    # Compare the data and write the differences to the output file
    with open(output, 'w') as f:
        writer = csv.writer(f)

        # Write the header for the output file
        writer.writerow(["row name", "column name", "value in file1", "value in file2"])

        # Compare the data and write the differences to the output file
        for i in range(min(len(rows1), len(rows2))):
            for j in range(min(len(rows1[i]), len(rows2[i]))):
                if rows1[i][j] != rows2[i][j]:
                    writer.writerow([rows1[i][0], rows1[0][j], rows1[i][j], rows2[i][j]])
    
    return output

# Example usage
if __name__ == "__main__":
    file1 = "file1.csv" # Replace with the path to your file1
    file2 = "file2.csv" # Replace with the path to your file2
    output = "outputfile.csv" # Replace with the path to your output file
    csv_diff(file1, file2, output)
