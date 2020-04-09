import requests
import os


##############################################
# Map String IDs to given gene list
##############################################

# Get genes from file. Pass as a command line argument and convert to upper case
geneList = open("humanGPCR.txt").read().splitlines()
for i in range(0,len(geneList)):
    geneList[i] = geneList[i].upper()

# Map genes to String IDs
string_api_url = "http://string-db.org/api"
output_format = "tsv-no-header"
method = "get_string_ids"

params = {

    "identifiers" : "\r".join(geneList), # your protein list
    "species" : 9606, # species NCBI identifier
    "limit" : 1, # only one (best) identifier per input protein
    "echo_query" : 1, # see your input identifiers in the output
    "caller_identity" : "WilkieLab"

}

## construct method URL

request_url = string_api_url + "/" + output_format + "/" + method

## Call STRING

try:
    response = requests.post(request_url, params=params)
except requests.exceptions.RequestException as e:
    print(e)
    os.sys.exit()

## Read and parse the results

geneMap = {}
for line in response.text.strip().split("\n"):
    l = line.split("\t")
    input_identifier, string_identifier = l[0], l[2]
    geneMap[input_identifier] = string_identifier


#####################################
# Get Interaction Network
#####################################


method = "interaction_partners"
my_genes = geneMap.keys()
species = "9606"
limit = 100
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



print(Interactors_Map)

for key in Interactors_Map.keys():
    print(key, " : ", len(Interactors_Map[key]))