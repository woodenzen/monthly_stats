import os, re
import prettytable as pt
from datetime import datetime
from plistlib import load
from urllib.parse import urlparse, unquote

####
# Function for finding the path to The Archive
#####
def TheArchivePath():
    """
    Find the path to The Archive's plist file.

    Returns:
        A string representing the path to The Archive.
    """
    bundle_id = "de.zettelkasten.TheArchive"
    team_id = "FRMDA3XRGC"
    #`fileName` is the path to the plist file that contains the path to the ZK.
    fileName = os.path.expanduser(
        "~/Library/Group Containers/{0}.{1}.prefs/Library/Preferences/{0}.{1}.prefs.plist".format(team_id, bundle_id))
    with open(fileName, 'rb') as fp:
        # load is a special function for use with a plist
        pl = load(fp) 
        # 'archiveURL' is the key that pairs with the zk path
        path = urlparse(pl['archiveURL']) 
    # path is the part of the path that is formatted for use as a path.
        path = urlparse(pl['archiveURL']).path
        decoded_path = unquote(path) 
    return unquote(path) 
 

####
# Function for finding monthly stats
#####        

def count_files_zettelkasten(partial_UID):
    """
    Counts the number of files in the directory specified by `TheArchivePath()` that contain the given `partial_UID` in their filename.

    Args:
        UID (str): The unique identifier to search for in the filenames.

    Returns:
        int: The number of files that contain the given `partial_UID` in their filename.
    """
    directory = TheArchivePath() # gets the path to the directory
    count = 0 # initializes the counter 
    for filename in os.listdir(directory): # iterates over the files in the directory
        if re.search(f".*{partial_UID}\d{{4}}.*", filename): # checks if the partial_UID is in the filename
            file_path = os.path.join(directory, filename) # constructs the full file path
            if os.path.isfile(file_path): # checks if the file is a regular file
                count += 1 # increments the counter variable
    return count # returns the count of files

def oldest_year_in_folder(folder_path):
    """
    Finds the oldest year represented in any file in the given folder.

    Args:
        folder_path (str): The path to the folder to search.

    Returns:
        str: A string representation of the oldest year represented in any file in the folder.
    """
    
    oldest_year = None
    for filename in os.listdir(folder_path):
        match = re.search(r"\d{12}", filename)
        if match:
            year = match.group(0)[:4]
            if oldest_year is None or year < oldest_year:
                oldest_year = year
    return oldest_year

current_year = int(datetime.today().year)
oldest_year_str = oldest_year_in_folder(TheArchivePath())
oldest_year = int(oldest_year_str) if oldest_year_str else year
number_of_years = current_year - oldest_year


# Generate year and month strings for the past stat_years years
today = datetime.today()
partial_UIDs = []
for y in range(today.year-number_of_years, today.year+1): # stat_years years ago to this year
    for m in range(1, 13):
        partial_UIDs.append(f"{y}{m:02d}")

# Create a list of lists to store the counts for each year
counts_by_year = []
for i in range(number_of_years+1):
    year_counts = [count_files_zettelkasten(partial_UIDs[j]) for j in range(i*12, (i+1)*12)]
    counts_by_year.append(year_counts)

# Convert month numbers to month names
month_names = [datetime(2000, i, 1).strftime('%b') for i in range(1, 13)]

# Create a table with the month names as the first column
table = pt.PrettyTable()
table.field_names = ['Stats'] + [str(y) for y in range(today.year-number_of_years, today.year+1)]

def add_month_row(month, divider=False):
    table.add_row([month_names[month]] + [str(counts_by_year[year][month]) for year in range(number_of_years+1)],
                  divider=divider)

# Jan--Nov (without divider), December with divider
for month in range(11):
    add_month_row(month, divider=False)
add_month_row(11, divider=True)

# Append annual sum
table.add_row(['Total']
            + [str(sum(counts_by_year[year])) for year in range(number_of_years+1)])

# Print the table
print(table)
