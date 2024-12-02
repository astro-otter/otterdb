# syntax=docker/dockerfile:1
FROM arangodb
EXPOSE 8529

# set the root password
ENV ARANGO_ROOT_PASSWORD=${ARANGO_ROOT_PASSWORD}

# move all of the data into the database initialization directory
ADD .otter/ /home/
RUN mkdir /home/.otter
RUN mv /home/*.json /home/.otter

COPY setup.py /home/
COPY setup.sh /home/

# install dependences
RUN apk update && apk add --no-cache python3 py3-pip

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools setuptools_scm wheel pyArango

# move into the home directory and run
WORKDIR /home/
RUN /home/setup.sh
