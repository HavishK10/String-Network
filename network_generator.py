import requests
import os
import csv
import sys



# Get genes from file. Pass as a command line argument and convert to upper case

try:
    file_name = sys.argv[1]
except Exception as e:
    print("Did not supply min argument: file path to gene list")
    os.sys.exit()

try:
    num_interactors = int(sys.argv[2])
    limit = num_interactors
except Exception as e:
    limit = 10

try:
    cutoff = float(sys.argv[3])
except Exception as e:
    cutoff = 0

geneList = open(file_name).read().splitlines()
for i in range(0,len(geneList)):
    geneList[i] = geneList[i].upper()


# Get Interaction Network
string_api_url = "http://string-db.org/api"
output_format = "tsv-no-header"

method = "interaction_partners"
my_genes = geneList
species = "9606"
my_app = "WilkieLab"

# Construct the request and send a request per 100 genes
Interactors_Map = {}
chunks = (len(my_genes) - 1) // 100 + 1

for i in range(chunks):
    request_url = string_api_url + "/" + output_format + "/" + method + "?"
    request_url += "identifiers=%s" % "%0d".join(my_genes[i*100:(i+1)*100])
    request_url += "&" + "species=" + species
    if(limit != 0):
        request_url += "&" + "limit=" + str(limit)
    request_url += "&" + "caller_identity=" + my_app


    try:
        response = requests.post(request_url)
        print("Finshed request {}".format(i + 1))
    except requests.exceptions.RequestException as e:
        print(e)
        os.sys.exit()

    ## Read and parse the results

    for line in response.text.strip().split("\n"):
        l = line.split("\t")
        input_identifier, interactor = l[2], l[3]
        if input_identifier not in Interactors_Map:
            Interactors_Map[input_identifier] = []
        exp_score = float(l[5])
        if exp_score > cutoff:
            Interactors_Map[input_identifier].append(interactor)

# Write to file tab delim column wise
outname = file_name.replace(".txt", "") + "_output.txt"
with open(outname, "w") as f:
    for k in Interactors_Map.keys():
        f.write(k)
        f.write("\t")
        for v_j in range(len(Interactors_Map[k])):
            f.write(Interactors_Map[k][v_j])
            f.write("\t")
        f.write("\n")



print("Job completed see results in *_output.txt")
