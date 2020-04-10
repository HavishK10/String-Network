import requests
import os
import csv
import sys



# Get genes from file. Pass as a command line argument and convert to upper case
if(len(sys.argv) >= 1):
    print("Did not supply min argument: file path to gene list")
    os.sys.exit()

file_name = sys.argv[0]
num_interactors = sys.argv[1]
cutoff = sys.argv[2]
geneList = open(file_name).read().splitlines()
for i in range(0,len(geneList)):
    geneList[i] = geneList[i].upper()


# Get Interaction Network

method = "interaction_partners"
my_genes = geneList
species = "9606"
limit = 10
my_app = "WilkieLab"

## Construct the request
request_url = string_api_url + "/" + output_format + "/" + method + "?"
request_url += "identifiers=%s" % "%0d".join(my_genes)
request_url += "&" + "species=" + species
request_url += "&" + "limit=" + str(limit)
request_url += "&" + "caller_identity=" + my_app


try:
    response = requests.post(request_url)
except requests.exceptions.RequestException as e:
    print(e)
    os.sys.exit()

## Read and parse the results
Interactors_Map = {}
for line in response.text.strip().split("\n"):
    l = line.split("\t")
    input_identifier, interactor = l[2], l[3]
    if input_identifier not in Interactors_Map:
        Interactors_Map[input_identifier] = []

    Interactors_Map[input_identifier].append(interactor)
    exp_score = float(l[5])
    #print(exp_score)

# Write to file tab delim column wise
with open("output.txt", "w") as f:
    writer = csv.writer(f, delimiter = "\t")
    writer.writerow(Interactors_Map.keys())
    writer.writerows(zip(*Interactors_Map.values()))
