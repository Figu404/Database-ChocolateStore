

import csv
import os
print(os.getcwd())
print(os.path.exists("personalcode.csv"))
try:
    with open("personalcode.csv") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip first row
        f = open("demofile1.csv", "a")
        writer = csv.writer(f)
        writer.writerow(header)
        i = 1000
        for row in reader:
            row[0] = row[0] + f"-{i}"
            i = i+1
            writer.writerow(row)
except FileNotFoundError:
    print("Sorry, the file " + "naaw" + "does not exist.")

