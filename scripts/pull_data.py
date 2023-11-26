import requests

""" Line Names """
# lines = ["bakerloo", "central", "circle", "district", "hammersmith-city", "jubilee", "metropolitan", "northern", "piccadilly", "victoria", "waterloo-city", "dlr", "london-overground", "elizabeth"]
lines = []

for line in lines:
    # Request data from TfL API and store it in the file raw/<line>.json, and store the sequence data in raw/<line>_seq.json
    url = f"https://api.tfl.gov.uk/line/{line}/stoppoints"
    url_seq = f"https://api.tfl.gov.uk/line/{line}/route/sequence/all"
    # TODO: There is likely enough data in url_seq to get the lat and lon of each station, so we don't need to make a second request. Fix later.
    r = requests.get(url)
    r_seq = requests.get(url_seq)
    # Write the data to the file
    with open("raw/" + line + ".json", 'w', encoding="utf-8") as file:
        file.write(r.text) # ignore non-ascii characters
    with open("raw/" + line + "_seq.json", 'w', encoding="utf-8") as file:
        file.write(r_seq.text)
    
# Say we're done
print("Loaded data from TfL API and stored it in raw/<line>.json and raw/<line>_seq.json")