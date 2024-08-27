#!/bin/bash

# this script removes all data from the otter arangodb database

docker container rm -f otterdb
docker container rm -f otterdb-persist
