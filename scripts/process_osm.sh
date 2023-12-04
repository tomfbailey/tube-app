# Look for the latest England extract here: https://download.geofabrik.de/europe/great-britain/england.html
# Look for the latest London Underground relation here: https://www.openstreetmap.org/relation/7225135

# Check that raw/ exists
if [ ! -d raw ]; then
    echo "ERROR: raw/ directory does not exist. Please create it and place the England extract in it."
    exit 1
fi

# Check that raw/england-latest.osm.pbf exists
if [ ! -f raw/england-latest.osm.pbf ]; then
    echo "ERROR: raw/england-latest.osm.pbf does not exist. Please download it from https://download.geofabrik.de/europe/great-britain/england.html and place it in the raw/ directory."
    exit 1
fi

# Nodes:
echo "Processing Nodes..."

# Extract (roughly) London from the UK extract
echo "Extracting London from the England extract..."
osmium extract --bbox=-1.225093,51.297993,0.70588,51.847656 raw/england-latest.osm.pbf -o raw/expanded-london.osm.pbf

# Filter these to railway stations
echo "Filtering to railway stations..."
osmium tags-filter raw/expanded-london.osm.pbf --overwrite nwr/railway=station -o raw/subway_stations_tmp.osm

# Filter these to station=subway (i.e. London Underground)
echo "Filtering to London Underground stations..."
osmium tags-filter raw/subway_stations_tmp.osm --overwrite nwr/station=*subway -o raw/subway_stations.osm
# We do *subway because some stations are tagged as station=light_rail;subway instead of just station=subway

# Delete temporary file
echo "Deleting temporary file..."
rm raw/subway_stations_tmp.osm

# Turn the OSM file into a GPKG file
echo "Converting OSM file to GPKG file..."
ogr2ogr -f GPKG -overwrite raw/subway_stations.gpkg raw/subway_stations.osm

# (Leave the OSM file in place for now)


# Ways:
echo "----------------------------------------"
echo "Processing Ways..."

# Extract everything under the London Underground relation
echo "Extracting everything under the London Underground relation..."
osmium getid -r raw/england-latest.osm.pbf r7225135 --output raw/london-underground.osm

# TODO: Redownload geofabrik extract in a few days to see if the northern line way has been fixed

echo "Done."

