#!/bin/bash

### IMPORT ########################
# run arango import
for f in $1/*.json
do
    arangoimport --file $f --server.database "otter" --collection "tdes" --server.username "admin@otter" --server.password "insecure" --define "key=name['default_name']"
done
