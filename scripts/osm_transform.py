import osmium
import geopandas as gpd
from shapely.geometry import LineString
import matplotlib.pyplot as plt

# Path to the OSM file
osm_path = 'raw/london-underground.osm'

# Define a handler to parse OSM data
class OSMHandler(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        self.ways = []

    def way(self, w):
        # if 'highway' in w.tags:  # You can add other tags to filter relevant ways
        self.ways.append(w)

# Instantiate the handler and parse OSM data
handler = OSMHandler()
handler.apply_file(osm_path, locations=True, idx='flex_mem')

# Extracted ways to GeoDataFrame
lines = []
for w in handler.ways:
    coords = [(n.lon, n.lat) for n in w.nodes]
    line = LineString(coords)
    lines.append(line)

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(geometry=lines)

# Define the path for the output shapefile
output_shapefile = 'output/london_underground_ways.shp'

# Save the GeoDataFrame as a shapefile
gdf.to_file(output_shapefile)

# Plot the GeoDataFrame
gdf.plot()
plt.show()

