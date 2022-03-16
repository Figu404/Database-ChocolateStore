import csv
import os
import random as r


def uniq(lst):
    last = object()
    for item in lst:
        if item == last:
            continue
        yield item
        last = item


def sort_and_deduplicate(li):
    return list(uniq(sorted(li, reverse=True)))


def makeList(readern):
    li = []
    for row in readern:
        li.append(list(row))
    return li


print(os.getcwd())
print(os.path.exists("personalcode.csv"))

path1 = "data/gillar.csv"
path2 = "data/MOCK_DATA (8).csv"

newFile = "data/likes.csv"

columns1 = [0, 1]
columns2 = [0]
rader = 1000

try:
    with open(path1) as csvfile:
        reader = csv.reader(csvfile)
        y = open(path2, "r")
        reader2 = csv.reader(y)

        header = next(reader)  # Skip first row
        header2 = next(reader2)

        f = open(newFile, "a", newline='')
        writer = csv.writer(f)

        lis = []
        for c in columns1:
            lis.append(header[c])
        for c in columns2:
            lis.append(header2[c])
        writer.writerow(lis)

        i = 0
        for t in header:
            i += 1
        j = 0
        for t in header2:
            j += 1
        lista1 = makeList(reader)
        lista2 = makeList(reader2)
        print(lista1, "naaj")
        rows1 = list(range(0, len(lista1)))

        rows2 = list(range(0, len(lista2)))
        r.shuffle(rows2)
        rows2copy = rows2
        r.shuffle(rows2copy)
        rows2.extend(rows2copy)
        r.shuffle(rows2copy)
        rows2.extend(rows2copy)
        r.shuffle(rows2copy)
        rows2.extend(rows2copy)
        r.shuffle(rows2copy)
        rows2.extend(rows2copy)
        r.shuffle(rows2copy)
        rows2.extend(rows2copy)
        r.shuffle(rows2copy)
        rows2.extend(rows2copy)
        r.shuffle(rows2copy)
        rows2.extend(rows2copy)
        r.shuffle(rows2copy)
        rows2.extend(rows2copy)
        testar = []
        try:
            for b in range(rader):
                row = []
                val1 = rows1[b]
                val2 = rows2[b]
                for c in columns1:
                    row.append(lista1[val1][c])
                for c in columns2:
                    row.append(lista2[val2][c])
                testar.append(row)
        except IndexError as er:
            print("aja" + str(er))
        testar2 = []
        for e in sort_and_deduplicate(testar):
            writer.writerow(e)
        print(len(testar)-len(sort_and_deduplicate(testar)))
except FileNotFoundError as e:
    print("Sorry, the file " + "naaw" + "does not exist." + str(e))
