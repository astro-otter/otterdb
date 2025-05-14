# syntax=docker/dockerfile:1
FROM arangodb
EXPOSE 8529

# deal with user stuff
RUN addgroup -g 1001 otteruser && \
    adduser -u 1001 -G otteruser -s /bin/sh -D otteruser

# move all of the data into the database initialization directory
RUN mkdir /otterdb

# COPY setup.py /otterdb/
COPY setup.sh /otterdb/
COPY init-db.js /otterdb/

# Switch to the non-root user after all the installation is done
RUN chown -R otteruser:otteruser /otterdb/
RUN chown -R otteruser:otteruser /var/lib/arangodb3
RUN chown -R otteruser:otteruser /var/lib/arangodb3*
USER otteruser

# move into the home directory and run
WORKDIR /otterdb/
ENTRYPOINT /otterdb/setup.sh
