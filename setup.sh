#!/bin/sh

# Start ArangoDB in the background
arangod \
    --server.endpoint tcp://0.0.0.0:8529 \
    --frontend.proxy-request-check true \
    --frontend.trusted-proxy ${OTTERWEB_IP:-"127.0.0.1"} &
ARANGOD_PID=$!

# Wait until ArangoDB is ready
# NOTE: that the root password is empty for now, but then get's set in init-db.js
echo "Waiting for arangod to be ready..."
sleep 60

# Now run the initialization script
echo "Running ArangoDB init script..."
{ # try
    echo "Trying to initialize with no password..." && 
    arangosh \
	--server.endpoint $DB_LINK_PORT_8529_TCP \
	--server.username root \
	--server.password "" \
	--log.level debug \
	--javascript.execute init-db.js &&
    echo "Arangosh javascript exited with code $?"
} || { # catch/except (in case we've already updated the root password)
    echo "Failed to initialize with code $?, now trying with env var..." &&
    arangosh \
	--server.endpoint $DB_LINK_PORT_8529_TCP \
	--server.username root \
	--server.password "$ARANGO_ROOT_PASSWORD" \
	--log.level debug \
	--javascript.execute init-db.js
}

# python3 setup.py

# now wait until arango is stopped or restarted
wait $ARANGOD_PID
