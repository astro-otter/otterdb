#!/bin/sh

# Start ArangoDB in the background
arangod --server.endpoint tcp://0.0.0.0:8529 &
sleep 10  # Adjust as needed to ensure ArangoDB is ready

arangosh --javascript.execute init-db.js
python3 setup.py
