import os
import re
import calendar
import datetime
import pandas as pd
from flask import Flask, render_template
from archive_path import TheArchivePath

# Get the path to the active archive
directory = TheArchivePath()

app = Flask(__name__)

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

# Create a list of dictionaries with months as rows and years as columns
rows = []
for month in range(1, 13):
    row = {'Stats': calendar.month_name[month]}
    for year in sorted(set([key[:4] for key in counts.keys()])) + [str(datetime.datetime.now().year)]:
        key = f"{year}-{month:02d}"
        row[year] = counts.get(key, 0)
    rows.append(row)

# Convert the list of dictionaries to a Pandas DataFrame
df = pd.DataFrame(rows)

# # Add a row to the bottom of the table that sums the yearly count
# yearly_counts = df.sum(numeric_only=True)
# df = pd.concat([df, pd.DataFrame([yearly_counts], columns=yearly_counts.index, index=pd.Index(['Yearly Total']))], keys=['', 'Yearly Total'], names=['', 'Stats'])
# print(df)

# Reorder the columns to have the years in ascending order
df = df[['Stats'] + sorted(df.columns[1:])]


# Calculate the sum of each year column
yearly_totals = df.sum()[1:]

# Append the yearly totals as a new row to the DataFrame
df.loc[len(df)] = ['Yearly Total'] + list(yearly_totals)

# Define a route that will render the HTML template
@app.route('/')
def index():
    # Generate the HTML table using the to_html method
    table_html = df.to_html(index=False)
    
    # Return the rendered HTML template
    return render_template('index.html', table=table_html)

if __name__ == '__main__':
    app.run()