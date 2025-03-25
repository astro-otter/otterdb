# syntax=docker/dockerfile:1
FROM arangodb
EXPOSE 8529

# deal with user stuff
RUN addgroup -g 1001 otteruser && \
    adduser -u 1001 -G otteruser -s /bin/sh -D otteruser

# set the root password
ENV ARANGO_ROOT_PASSWORD=${ARANGO_ROOT_PASSWORD}
ENV ARANGO_NO_AUTH=0

# move all of the data into the database initialization directory
RUN mkdir /otterdb

ADD .otter/ /otterdb/
RUN mkdir /otterdb/.otter
RUN mv /otterdb/*.json /otterdb/.otter

COPY setup.py /otterdb/
COPY setup.sh /otterdb/
COPY init-db.js /otterdb/

# install dependences
RUN apk update && apk add --no-cache python3 py3-pip

RUN pip install --upgrade pip --break-system-packages
RUN pip install --upgrade setuptools setuptools_scm wheel pyArango --break-system-packages

 # Switch to the non-root user after all the installation is done
RUN chown -R otteruser:otteruser /otterdb/
RUN chown -R otteruser:otteruser /var/lib/arangodb3*
USER otteruser

# move into the home directory and run
WORKDIR /otterdb/
RUN /otterdb/setup.sh
