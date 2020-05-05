import csv
import json
csv_list = []
f = open("redtomato.csv")
f2 = open("us-states.json")
f3 = open("full-data.json", 'w')
reader = csv.reader(f)
for row in reader:
    csv_list.append(row)
