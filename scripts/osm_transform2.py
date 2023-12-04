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
            self.way_nodes.append(way_coords)
# For nodes, use a separate data file
gpkg_path = 'raw/subway-map-6.gpkg'
data = gpd.read_file(gpkg_path).to_crs(epsg=PROJECTION)

# Read the first 5 rows of the GeoDataFrame
print(data.head())

# Plot the data using geopandas plot function using the x and y columns as the coordinates
ax = data.plot(color='red', markersize=5, label='Station')

# For ways (lines), use the OSM file
input_file = 'raw/tube-data-6.osm'

# Do a first pass of input_file to map node ids to lat/lon
node_map = RefHandler()
node_map.apply_file(input_file)

handler = WayHandler(mapping=node_map.mapping)
handler.apply_file(input_file)

lines = [LineString([Point(lon, lat) for lon, lat in way]) for way in handler.way_nodes]

geoseries = gpd.GeoSeries(lines, crs='EPSG:4326')

geoseries_projected = geoseries.to_crs(epsg=PROJECTION)

# Plot the ways
geoseries_projected.plot(ax=ax, color='black', linewidth=0.5, label='Line')

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
