# Convert the OSM.PBF to an OSM file using "osmium getid -r greater-london-latest.osm.pbf r7225135 --output tube-data-1.osm"
#  (I checked that all tube data is contained within london by doing the same on the england dataset then using diff)

# Then use ogr2ogr to convert to a shapefile ("ogr2ogr -f GPKG london-underground-map.gpkg london-underground.osm")

# Now we have our gpkg file, we can display it using geopandas

# import geopandas as gpd
# import matplotlib.pyplot as plt
# import ast

# # Path to the GeoPackage file
# gpkg_path = 'path/to/your/file.gpkg'

# # Read the GeoPackage file using GeoPandas
# data = gpd.read_file("raw/london-underground-map.gpkg")

# def parse_other_tags(tags_str):
#     tags = {}
#     if tags_str:
#         tags_list = tags_str.strip('{}').split(',')
#         for tag in tags_list:
#             key, value = tag.split('=>')
#             tags[key.strip('"')] = value.strip('"')
#     return tags

# # Filter only to stops
# filtered_data = []
# for index, row in data.iterrows():
#     other_tags = row['other_tags']
#     if other_tags:
#         tags_dict = parse_other_tags(other_tags)
#         # tags_dict = ast.literal_eval(other_tags)
#         if 'railway' in tags_dict and tags_dict['railway'] == 'stop':
#             filtered_data.append(row)

# # Plot the GeoDataFrame
# fig, ax = plt.subplots(figsize=(10, 10))  # Adjust the figure size as needed

# # Plot the data using geopandas plot function and label each point with the name column
# filtered_data = gpd.GeoDataFrame(filtered_data)
# filtered_data.plot(ax=ax, color='red', markersize=10, label='Station')


# # Set plot title and labels
# plt.title('GeoPackage Data Plot')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')

# # Save the plot as a PNG file
# plt.savefig('london-underground-map.png', dpi=300, bbox_inches='tight')

import osmium
import geopandas as gpd
from shapely.geometry import LineString
import matplotlib.pyplot as plt
import copy


# Read the GPKG file using GeoPandas
# gpkg_path = 'raw/london-underground-map.gpkg'

# For nodes
gpkg_path = 'raw/subway-map-6.gpkg'
data = gpd.read_file(gpkg_path)

# Define a handler to parse ways from OSM data
class WayHandler(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        self.ways = []
        self.line_count = 0
        self.line_map = {} # map of a line id to a list of nodes (172912837 -> (0,pos), 12318237 -> 0, 129382171 -> 1, etc.)

    def way(self, w):
        coords = []
        line = []
        for i, n in enumerate(w.nodes):
            line.append((n.ref, i))
            if n.ref not in self.line_map:
                self.line_map[n.ref] = [(self.line_count, i)]
            else:
                self.line_map[n.ref].append((self.line_count, i))
        self.line_count += 1
        self.ways.append(line) # [[172912837, 12318237], [129382171, etc.], etc.]

class RefHandler(osmium.SimpleHandler):
    def __init__(self, ways_list, ext_line_map):
        osmium.SimpleHandler.__init__(self)
        # empty list of lists with the same dimensions as ways_list
        self.groups = copy.deepcopy(ways_list)
        # Now zero out the lists
        for i in range(len(self.groups)):
            self.groups[i] = [None] * len(self.groups[i])
        self.line_map = ext_line_map

    def node(self, n):
        if n.id in self.line_map:
            line_number, position = self.line_map[n.id].pop()
            self.groups[line_number][position] = (n.location.lon, n.location.lat)

# Assuming 'raw/london-underground.osm' is your OSM file containing ways
# osm_file = 'raw/london-underground.osm'
osm_file = 'raw/tube-data-6.osm'

# Instantiate the handler and parse OSM data
handler = WayHandler()
handler.apply_file(osm_file)

refhandler = RefHandler(handler.ways, handler.line_map)
refhandler.apply_file(osm_file)

# Plot each way using the coordinates from the nodes
lines = []
# TODO: Nones here could be part of the problem
for group in refhandler.groups:
    # Remove any None values from the list
    group = [x for x in group if x is not None]
    # Create a LineString from the pairs of coordinates in the group list
    if len(group) > 1:
        lines.append(LineString(group))

# Create a GeoDataFrame from the list of LineStrings
gdf_ways = gpd.GeoDataFrame({'geometry': lines})

# Plot both points and ways
fig, ax = plt.subplots(figsize=(20, 20))  # Adjust the figure size as needed
ax = data.plot(markersize=1, color='red')  # Plot points
# TODO: Will need to filter out points that are not stations - to do with other_tags col. 
# TODO: May also need to filter out points that are not on the tube lines, and fix gaps between lines.
# TODO: This could be because we are limited by depth, so may have to have an OSM file for each line. Doesn't seem to be the case
# TODO: Maybe it is that nodes for ways can be shared between ways, so our line_map is not unique. (or rather in reality, 17819231 -> (1 and 5), 129312 -> 1, etc.)
# Plot ways
gdf_ways.plot(ax=ax, color='black', linewidth=0.5)

# Make the plot look nicer
ax.set_aspect('equal')
ax.set_axis_off()

# Set plot title and labels
plt.title('Ways and Points Plot')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Save the plot as a PNG file with higher resolution
# plt.savefig('london-underground-map2.png', dpi=1200, bbox_inches='tight')

plt.savefig('tube-map-6.png', dpi=1200, bbox_inches='tight')
