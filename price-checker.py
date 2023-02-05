import json
import linecache
import subprocess
import os

# Functons:
def runcmd(cmd, verbose = False, *args, **kwargs):

    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass



    
# Create request string
# Only prices request implemented for now
requestBase = "https://www.albion-online-data.com/api/v2/stats/"
requestPrice = requestBase + "Prices/"


# Search for the item ID:
print("Item name: ",end='')
item = input()
itemFile = "items.txt"


#Show all the items that fit the criteria:
# TO DO : make the list more easy to read
with open(itemFile) as f:
    for line in f:
        if item in line:
            print(line)
    #Choose item:
    print("Item number: ", end='')
    number = int(input())
    #Extract item id:
    itemLine = linecache.getline(itemFile, number)
    itemLine = itemLine.strip()
    itemLineArray = itemLine.split()
    print("Item ID: ",end='')
    print(itemLineArray[1])

itemID = itemLineArray[1]
itemID_JSON = itemID + ".json"
requestItemPrice = requestPrice + itemID_JSON

# the problem with this is that I will never update prices this way
# i need to find a way to check the time and update if long enough has passed
#Check if the file already exists:
file_exists = False
directory  = os.scandir()
for entry in directory:
    print(entry.name)
    if entry.name == itemID_JSON:
        print("File already exists, skipping download...")
        file_exists = True
if file_exists == False:
    #Download the file:
    print(requestItemPrice)
    runcmd("wget " + requestItemPrice + " --directory-prefix=data", verbose = True)


# Process data
# Make output more readable, make it so it shows the time
# Maybe use tabulate? 

file = "data/" + itemID_JSON
with open(file) as f:
        data = json.load(f)
print("Showing prices for " + data[0]["item_id"])
for element in data:
    print("Location: ", end='')
    print(element["city"])
    print("Price: ", end='')
    print(element["sell_price_min"])
    
