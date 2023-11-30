import os
import osmium
import shapely.wkb as wkblib

class OSMHandler(osmium.SimpleHandler):
    def __init__(self):
        super(OSMHandler, self).__init__()
        self.filtered_elements = set()  # List to store filtered elements

    def way(self, w):
        if w.tags and w.tags.get('network') == 'London Underground':
            # Process the matched way feature
            for n in w.nodes:
                self.filtered_elements.add(n.ref)

class OSMWriter(osmium.SimpleHandler):
    def __init__(self, writer, nodes):
        super(OSMWriter, self).__init__()
        self.writer = writer
        self.nodes = nodes
        self.ncount = 0
        self.wcount = 0

    def node(self, n):
        if n in self.nodes:
            self.writer.add_node(n)
            self.ncount += 1

    def way(self, w):
        if w.tags and w.tags.get('network') == 'London Underground':
            self.writer.add_way(w)
            self.wcount += 1

# Specify the path to the original OSM PBF file
pbf_file = 'raw/greater-london-latest.osm.pbf'

# Create an instance of the OSMHandler class
handler = OSMHandler()

# Apply the handler to the original OSM PBF file
handler.apply_file(pbf_file)

# Specify the path and filename for the new OSM file
new_pbf_file = 'raw/london-underground.osm'

# Create a new OSM PBF file and write the filtered elements to it
writer = osmium.SimpleWriter(new_pbf_file)
enabler = OSMWriter(writer, handler.filtered_elements)
enabler.apply_file(pbf_file)

# Print how nodes, ways and relations were written in the OSMWriter class
print(f"Nodes: {enabler.ncount}")
print(f"Ways: {enabler.wcount}")
writer.close()