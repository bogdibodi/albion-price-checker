import json
import linecache
import subprocess
import os
import time

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


def file_age(filepath):
	fileStat = os.stat(filepath)
	# Return age of file in hours
	return (fileStat.st_mtime / 60) / 60

    
# Create request string
# Only prices request implemented for now
requestBase = "https://www.albion-online-data.com/api/v2/stats/"
requestPrice = requestBase + "Prices/"
itemFile = "items.txt"

# Search for the item ID:
print("Item name: ",end='')
item = input()



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
    print("")

itemID_JSON = itemLineArray[1] + ".json"
requestItemPrice = requestPrice + itemID_JSON
ageTreshold = 6 # set the limit for how old the file can be before needing to download it again


file_exists = False
# Go into data folder
os.chdir("data/")
directory = os.scandir()
itemPath = os.getcwd() + "/" + itemID_JSON


for entry in directory:
	if entry.name == itemID_JSON:
		# Make sure file is not older than the treshold
		print("File already exists, checking age...")
		if file_age(itemPath) > ageTreshold:
			print("File is too old, downloading...")
			os.remove(itemPath)	
			break
		print("File age OK, skipping download...") 
		print("")
		file_exists = True
# Go back to albion-data folder
os.chdir("..")

if file_exists == False:
	#Download the file:
	print(requestItemPrice)
	runcmd("wget " + requestItemPrice + " --directory-prefix=data", verbose = True)



# Process data
# Make output more readable, make it so it shows the time
# Maybe use tabulate? 

file = "data/" +  itemID_JSON
with open(file) as f:
	data = json.load(f)
print("Showing prices for " + data[0]["item_id"])
for element in data:
	print("Location: ", end='')
	print(element["city"])
	print("Price: ", end='')
	print(element["sell_price_min"])   
