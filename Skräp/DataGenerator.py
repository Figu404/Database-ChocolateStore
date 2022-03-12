import csv
import os
import random as r
from sqlite3 import Row
from traceback import print_tb
def makeList(readern):
    l = []
    for row in readern:
        print(type(row))
        l.append(list(row))
        print(l, "Fungerar=")
    print("jag är klar nu dags att dra")
    print(l, "eller?")
    return l
print(os.getcwd())
print(os.path.exists("personalcode.csv"))

path1 = "personalcode.csv"
path2 = "dominos.csv"
newFile = "blandad.csv"

columns1 = [0, 1]
columns2 = [1,2]
rader = 4

try:
    with open(path1) as csvfile:
        reader = csv.reader(csvfile)
        y = open(path2, "r")
        reader2 = csv.reader(y)

        header = next(reader)  # Skip first row
        header2 = next(reader2)

        f = open(newFile, "a")
        writer = csv.writer(f)

        lis = []
        for c in columns1:
            lis.append(header[c])
        for c in columns2:
            lis.append(header2[c])
        writer.writerow(lis)

        i = 0
        for t in header:
            i +=1
        j = 0
        for t in header2:
            j +=1
        lista1 = makeList(reader)
        lista2 = makeList(reader2)
        print(lista1, "naaj")
        rows1 = list(range(0,len(lista1)))
        rows2 = list(range(0,len(lista2)))
        
        r.shuffle(rows1)
        r.shuffle(rows2)
        
        for b in range(rader):
            row = []
            val1 = rows1[b]
            val2 = rows2[b]
            
            for c in columns1:
                row.append(lista1[val1][c])
            for c in columns2:
                row.append(lista2[val2][c])
            writer.writerow(row)
except FileNotFoundError:
    print("Sorry, the file " + "naaw" + "does not exist.")

# def find(number, csv_file):
#     for row in csv_file:
#     #if current rows 2nd value is equal to input, print that row
#         if number == row[1]:
#             return row[]
