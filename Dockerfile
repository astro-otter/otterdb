# syntax=docker/dockerfile:1
FROM arangodb
EXPOSE 8529

# set the root password
ENV ARANGO_ROOT_PASSWORD=${ARANGO_ROOT_PASSWORD}
ENV ARANGO_NO_AUTH=0

# move all of the data into the database initialization directory
ADD .otter/ /home/
RUN mkdir /home/.otter
RUN mv /home/*.json /home/.otter

COPY setup.py /home/
COPY setup.sh /home/
COPY init-db.js /home/

# install dependences
RUN apk update && apk add --no-cache python3 py3-pip

RUN pip install --upgrade pip --break-system-packages
RUN pip install --upgrade setuptools setuptools_scm wheel pyArango --break-system-packages

# move into the home directory and run
WORKDIR /home/
RUN /home/setup.sh
