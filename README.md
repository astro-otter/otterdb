# otterdb
Backend database code and data for OTTER

## Contributing Data
We hope data will be contributed through the web interface after it has been published. An incomplete list of accepted journals is given below. 
Data published in other journals will be considered upon reasonable request.

* IOPScience/AAS journals (AJ, ApJ, etc.)
* Oxford Academic journals (e.g., MNRAS, etc.)
* Nature and all related journals
* Astronomy & Astrophysics
* Physical Review Journals
* SPIE proceedings
* Annual Review journals
* Space Science Reviews
* The Journal of the American Association of Variable Star Observers
* Journal of Open Source Software
* The Open Journal of Astrophysics
* Sky and Telescope

## Installing a copy of the database (should only be done by devs)
1. Make sure you have set the following environment variables. If you don't
know what the value should be, contact an existing developer.
```
ARANGO_URL
ARANGO_ROOT_PASSWORD
VETTING_PASSWORD
ARANGO_USER_PASSWORD
```
2. Make sure docker is running. 
3. If you have an arm64 cpu (like a Mac Silicon chip), you will need to 
build the docker container on that cpu architecture. From the otterdb 
directory:
```
docker build -t otterdb:v0.3.6 .
```
4. Then run the docker container from dockerhub (if you built it locally, 
make sure you change the name at the bottom of this command)
```
docker run \
-e ARANGO_ROOT_PASSWORD=$ARANGO_ROOT_PASSWORD \
-e VETTING_PASSWORD=$VETTING_PASSWORD \
-e VETTING_USER="vetting-user" \
-e ARANGO_USER_USERNAME="user-guest" \
-e ARANGO_USER_PASSWORD=$ARANGO_USER_PASSWORD \
-e DB_LINK_PORT_8529_TCP="http://127.0.0.1:8529" \
-p 8529:8529 \
noahfranz13/otterdb:v0.3.6
```
5. Open a new terminal. Then, add a copy of the data to the database from 
the master copy at SciServer. From the otterdb directory, run
```
python3 import_from_sciserver.py
```
