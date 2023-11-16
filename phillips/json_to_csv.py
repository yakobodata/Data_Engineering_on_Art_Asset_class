import json
import csv

# Load JSON data from file
with open('past_auctions_art_work_info.json') as f:
    data = json.load(f)

# Open a CSV file for writing
with open('2.csv', 'w',encoding='utf-8' ,newline='') as f:
    writer = csv.writer(f)

    # Write header row
    writer.writerow(data[0].keys())

    # Write data rows
    for row in data:
        writer.writerow(row.values())