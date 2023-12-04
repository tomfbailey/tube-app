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
from shapely.geometry import LineString, Point
import matplotlib.pyplot as plt

PROJECTION = 27700

# Read the GPKG file using GeoPandas
# gpkg_path = 'raw/london-underground-map.gpkg'

class RefHandler(osmium.SimpleHandler):
    def __init__(self):
        super(RefHandler, self).__init__()
        self.mapping = {}

    def node(self, n):
        self.mapping[n.id] = (n.location.lon, n.location.lat)

class WayHandler(osmium.SimpleHandler):
    def __init__(self, mapping):
        super(WayHandler, self).__init__()
        self.way_nodes = []
        self.mapping = mapping

    def way(self, w):
        if w.nodes:
            way_coords = [self.mapping[n.ref] for n in w.nodes]
            # get the line tag from the way
            line = w.tags.get('line')
            self.way_nodes.append((way_coords, line, w.id))
# For nodes, use a separate data file
gpkg_path = 'raw/subway_stations.gpkg'
data = gpd.read_file(gpkg_path).to_crs(epsg=PROJECTION)

# Read the first 5 rows of the GeoDataFrame
print(data.head())

# Plot the data using geopandas plot function
ax = data.plot(color='white', edgecolor='black', markersize=2, label=data['name'], marker='o')

# Adjust marker edge width and color directly on the PathCollection objects
for collection in ax.collections:
    collection.set_edgecolor('black')  # Set marker edge color
    collection.set_linewidth(0.35)     # Set marker edge width
    # Move marker to the front
    collection.set_zorder(100)

# for index, row in data.iterrows():
#     ax.annotate(row['name'], (row.geometry.x, row.geometry.y), textcoords="offset points", xytext=(5, 5), ha='center', fontsize='xx-small')


# For ways (lines), use the OSM file
input_file = 'raw/london-underground.osm'

# Do a first pass of input_file to map node ids to lat/lon
node_map = RefHandler()
node_map.apply_file(input_file)

handler = WayHandler(mapping=node_map.mapping)
handler.apply_file(input_file)

lines = [(LineString([Point(lon, lat) for lon, lat in way]), line, id) for way, line, id in handler.way_nodes]

gdf_lines = gpd.GeoDataFrame(geometry=[line[0] for line in lines], crs='EPSG:4326')
gdf_lines['line'] = [line[1] for line in lines]
gdf_lines['id'] = [line[2] for line in lines]

# For each in the line column, convert into a list by splitting on semicolons. Then, for now, take the first element of the list
# gdf_lines['line'] = gdf_lines['line'].apply(lambda x: x.split(';')[0])

for index, row in gdf_lines.iterrows():
    if row['line'] is None:
        continue
    elif ';' in row['line']:
        gdf_lines.at[index, 'line'] = row['line'].split(';')[0]
    elif ',' in row['line']:
        gdf_lines.at[index, 'line'] = row['line'].split(',')[0] # don't need to worry about the space after the comma as we're only taking the first element

# Project the GeoDataFrame to the desired CRS
gdf_lines_projected = gdf_lines.to_crs(epsg=PROJECTION)

# Read the first 5 rows of the GeoDataFrame
print(gdf_lines_projected.head())

color_map = {
    'Bakerloo': '#B36305',
    'Central': '#E32017',
    'Circle': '#FFD300',
    'District': '#00782A',
    'DLR': '#00A4A7',
    'Hammersmith & City': '#F3A9BB',
    'Jubilee': '#A0A5A9',
    'Metropolitan': '#9B0056',
    'Northern': '#000000',
    'Piccadilly': '#003688',
    'Victoria': '#0098D4',
    'Waterloo & City': '#95CDBA',
    'London Overground': '#EE7C0E',
    'Elizabeth': '#6950a1'
}

# Plot the ways, according to the color_map dictionary
for line, color in color_map.items():
    particular_line = gdf_lines_projected[gdf_lines_projected['line'] == line]
    if particular_line.empty:
        continue
    particular_line.plot(ax=ax, color=color, label=line, linewidth=0.75)

# Make the plot look nicer
ax.set_aspect('equal')
ax.set_axis_off()

# Set plot title and labels
ax.set_title('Ways and Points Plot')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Save the plot as a PNG file with higher resolution
# plt.savefig('london-underground-map2.png', dpi=1200, bbox_inches='tight')

ax.figure.savefig('tube-map-out.png', dpi=600, bbox_inches='tight')
