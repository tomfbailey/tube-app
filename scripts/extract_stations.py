import json

# Ask the user for the file path optionally
file_path = input("Enter the file path (or press Enter to use default 'stations.json'): ")

DEFAULT_TARGET_FILE = "raw/victoria.json"

# Use default file path if no input is provided
file_path = file_path.strip() if file_path.strip() else DEFAULT_TARGET_FILE

# Load JSON data from file
with open(file_path, 'r') as file:
    data = json.load(file)

nodes = []
edges = []  # Empty set of edges

# Extract 'lat', 'lon', and 'commonName' from each object
for item in data:
    lat = item.get("lat", None)
    # Get the longitude, and supply a default value of None if it doesn't exist
    lon = item.get("lon", None)
    naptan_id = item.get("naptanId", None)
    common_name = item.get("commonName", None)
    line = "victoria" # TODO: Get the line from the file name

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