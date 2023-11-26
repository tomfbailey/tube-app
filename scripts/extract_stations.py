import json

# Run from the root directory of the project (tube-app)

""" Line Names """
lines = ["bakerloo", "central", "circle", "district", "hammersmith-city", "jubilee", "metropolitan", "northern", "piccadilly", "victoria", "waterloo-city"]
# additional lines
additional_lines = ["dlr", "london-overground", "elizabeth"]
lines += additional_lines
nodes = [] # Empty set of nodes
id_set = set() # Empty set of ids
edges = []  # Empty set (list) of edges
seen_edges = set()

# Geolocation for scaling later
x_values = []
y_values = []

FILE_LOCATION = "raw/"

for line in lines:
    file_path = FILE_LOCATION + line + ".json"
    file_path_seq = FILE_LOCATION + line + "_seq.json"


    # Load JSON data from file
    with open(file_path, 'r', errors="ignore") as file:
        data = json.load(file)


    # Extract edge data from the sequence file, under orderedLineRoutes
    with open(file_path_seq, 'r', errors="ignore") as file:
        seq_data = json.load(file)

    adj_list = {} # Adjacency list of sets
    for route in seq_data.get("orderedLineRoutes", None):
        stops = route.get("naptanIds", None)
        # start is s, end is e.
        # s will be the first stop, e will be the second stop, then s will be the second stop, and e will be the third stop, etc.
        for s, e in zip(stops, stops[1:]):
            # Add s to the adjacency list if it doesn't exist
            if (s, line) not in adj_list:
                adj_list[(s, line)] = set()
            # Add e to the adjacency list if it doesn't exist
            if (e, line) not in adj_list:
                adj_list[(e, line)] = set()
            # Add e to the adjacency list of s
            adj_list[(s, line)].add((e, line))
            # Add s to the adjacency list of e
            adj_list[(e, line)].add((s, line))



    # Now iterate through the adjacency list and add edges in the format 
    """
    [
        {
            data: { id: 'ab', source: 'a', target: 'b' }
        },
        ...
    ]
    """
    for s, line_s in adj_list:
        for e, _ in adj_list[(s, line_s)]:
            if (s, e, line) in seen_edges or (e, s, line) in seen_edges:
                continue
            edges.append({
                "data": {
                    "id": s + "-" + e + "-" + line, # TODO: Will need to make the properly unique
                    "source": s,
                    "target": e,
                    "line": line
                }
            })
            seen_edges.add((s, e, line))
            seen_edges.add((e, s, line))


    # Extract 'lat', 'lon', and 'commonName' from each object
    for item in data:
        lat = item.get("lat", None)
        # Get the longitude, and supply a default value of None if it doesn't exist
        lon = item.get("lon", None)
        naptan_id = item.get("naptanId", None)
        common_name = item.get("commonName", None)
        # line = "victoria" # TODO: Get the line from the file name; actually can get from data itself too

        # Strip any trailing " Underground Station" from the common name
        common_name = common_name.replace(" Underground Station", "")
        common_name = common_name.replace(" Rail Station", "")
        common_name = common_name.replace(" DLR Station", "")
        common_name = common_name.replace(" (London)", "")

        # Convert to CytoScape format and append to nodes
        new_node = {
            "data": {
                "id": naptan_id,
                "label": common_name
            },   
            "position": {
                "x": lon,
                "y": -lat # Since lat is negative in London and would flip the graph
            }
        }

        if naptan_id not in id_set:
            id_set.add(naptan_id)
            nodes.append(new_node)
            x_values.append(lon)
            y_values.append(-lat)

# Now go back and scale the x and y values to be between 0 and 600
# This is because the default size of the canvas is 600 x 600
# Use the mins and maxes to scale the values

# Get the minimum and maximum values
x_min = min(x_values)
x_max = max(x_values)
y_min = min(y_values)
y_max = max(y_values)

# Now scale each value
SCALE_X_MAX = 20000
SCALE_X_MIN = 5000
SCALE_Y_MAX = 10000
SCALE_Y_MIN = 2500
for node in nodes:
    node["position"]["x"] = (SCALE_X_MAX * (node["position"]["x"] - x_min) / (x_max - x_min)) - SCALE_X_MIN
    node["position"]["y"] = (SCALE_Y_MAX * (node["position"]["y"] - y_min) / (y_max - y_min)) - SCALE_Y_MIN


# Combine nodes and edges into a dictionary
graph = {
    "nodes": list(nodes),
    "edges": edges
}

# Write the result to data/graph_data.json
DEST = "graph_data.json"

# Now write the result to the file in the data directory
with open(f"data/{DEST}", "w") as file:
    json.dump(graph, file)

# Display a status message ("Wrote to", etc.)
print(f"Wrote to data/{DEST}")