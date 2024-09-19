#!/bin/bash
set -e

# this script builds the database server
# using arangodb and the json files stored in .otter

# first remove the containers we are about to build
echo "WARNING! Removing the otterdb-persist and otterdb containers if they already exist!"

# creates the persistent data docker container
docker create --name otterdb-persist arangodb true

#./run.sh # starts the arangodb server in the background
# ARANGO_ROOT_PASSWORD=$OTTERDB_PASS \
# ARANGO_RANDOM_ROOT_PASSWORD=1
docker run -e ARANGO_NO_AUTH=1 \
       --name otterdb \
       --detach \
       --network otter-net \
       --volumes-from otterdb-persist \
       -p 8529:8529 arangodb


echo "arango server is now running in the background"

sleep 10

python3 -m pip install pyArango --break-system-packages
python3 import_jsons.py # imports the data from the .otter directory
