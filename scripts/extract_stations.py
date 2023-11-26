import json

# Ask the user for the file path optionally
file_path = input("Enter the file path (or press Enter to use default 'stations.json'): ")

DEFAULT_TARGET_FILE = "raw/victoria.json"
DEFAULT_TARGET_FILE_SEQ = "raw/victoria_seq.json"

# Use default file path if no input is provided
if file_path.strip() == "":
    file_path = DEFAULT_TARGET_FILE
    file_path_seq = DEFAULT_TARGET_FILE_SEQ
else:
    file_path = file_path.strip()
    file_path_seq = file_path.split(".")[0] + "_seq.json"

# Load JSON data from file
with open(file_path, 'r') as file:
    data = json.load(file)

nodes = []
# Extract edge data from the sequence file, under orderedLineRoutes
with open(file_path_seq, 'r') as file:
    seq_data = json.load(file)

adj_list = {} # Adjacency list of sets
for route in seq_data.get("orderedLineRoutes", None):
    print(type(route))
    stops = route.get("naptanIds", None)
    print(type(stops), stops)
    # start is s, end is e.
    # s will be the first stop, e will be the second stop, then s will be the second stop, and e will be the third stop, etc.
    for s, e in zip(stops, stops[1:]):
        # Add s to the adjacency list if it doesn't exist
        if s not in adj_list:
            adj_list[s] = set()
        # Add e to the adjacency list if it doesn't exist
        if e not in adj_list:
            adj_list[e] = set()
        # Add e to the adjacency list of s
        adj_list[s].add(e)
        # Add s to the adjacency list of e
        adj_list[e].add(s)

edges = []  # Empty set of edges

# Now iterate through the adjacency list and add edges in the format 
"""
[
      {
        data: { id: 'ab', source: 'a', target: 'b' }
      },
      ...
]
"""
for s in adj_list:
    for e in adj_list[s]:
        edges.append({
            "data": {
                "id": s + e, # TODO: Will need to make the properly unique
                "source": s,
                "target": e,
                "line": "victoria"
            }
        })


# Extract 'lat', 'lon', and 'commonName' from each object
for item in data:
    lat = item.get("lat", None)
    # Get the longitude, and supply a default value of None if it doesn't exist
    lon = item.get("lon", None)
    naptan_id = item.get("naptanId", None)
    common_name = item.get("commonName", None)
    line = "victoria" # TODO: Get the line from the file name; actually can get from data itself too

    # Strip any trailing " Underground Station" from the common name
    common_name = common_name.replace(" Underground Station", "")

    # Convert to CytoScape format and append to nodes
    nodes.append({
        "data": {
            "id": naptan_id,
            "label": common_name,
            "line": line
        },   
        "position": {
            "x": lon,
            "y": -lat # Since lat is negative in London and would flip the graph
        }
    })

# Now go back and scale the x and y values to be between 0 and 600
# This is because the default size of the canvas is 600 x 600
# Use the mins and maxes to scale the values
x_values = [node["position"]["x"] for node in nodes]
y_values = [node["position"]["y"] for node in nodes]

# Get the minimum and maximum values
x_min = min(x_values)
x_max = max(x_values)
y_min = min(y_values)
y_max = max(y_values)

# Now scale each value to be between 0 and 600
SCALE_MAX = 600
for node in nodes:
    node["position"]["x"] = SCALE_MAX * (node["position"]["x"] - x_min) / (x_max - x_min)
    node["position"]["y"] = SCALE_MAX * (node["position"]["y"] - y_min) / (y_max - y_min)


# Combine nodes and edges into a dictionary
graph = {
    "nodes": nodes,
    "edges": edges
}

# Write the result to data/{file_path}.
# First strip everything apart from the base file name
file_name = file_path.split("/")[-1]

# Now write the result to the file in the data directory
with open(f"data/{file_name}", "w") as file:
    json.dump(graph, file)

# Display a status message ("Wrote to", etc.)
print(f"Wrote to data/{file_name}")