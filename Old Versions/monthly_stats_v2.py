import os, re
import calendar
from plistlib import load
from urllib.parse import urlparse, unquote
from prettytable import PrettyTable
from archive_path import TheArchivePath

# Get the path to the active archive
directory = TheArchivePath()

# Empty dictionary to store the counts
counts = {}

# Regular expression pattern to match the UID
pattern = r'20\d{10}'

# Loop through all the files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".md") or filename.endswith(".txt"): 
    
    # Extract the UID from the filename using the regular expression
        match = re.search(pattern, filename)
        if match:
            uid = match.group()
            year = uid[:4]
            month = uid[4:6]

            # Increment the count for this year and month
            key = f"{year}-{month}"
            counts[key] = counts.get(key, 0) + 1

# Create a table with months as rows and years as columns
table = PrettyTable()
table.field_names = ['Stats'] + sorted(set([key[:4] for key in counts.keys()]))
for month in range(1, 13):
    row = [calendar.month_abbr[month]]
    for year in sorted(set([key[:4] for key in counts.keys()])):
        key = f"{year}-{month:02d}"
        row.append(counts.get(key, 0))
    if month == 12:
        table.add_row(row, divider=True)
    else:
        table.add_row(row)

# Add a row to the bottom of the table that sums the yearly count
yearly_counts = [sum([counts.get(f"{year}-{month:02d}", 0) for month in range(1, 13)]) for year in sorted(set([key[:4] for key in counts.keys()]))]
table.add_row(['Total'] + yearly_counts, divider=True)

# Print the table
print(table)