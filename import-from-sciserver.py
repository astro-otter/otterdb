"""
Import the data from SciServer to a local database

This script should really only be used by developers to import the data
"""
import os
import otter

def main():

    # first pull the data from sciserver
    db = otter.Otter(
        url=os.environ['ARANGO_URL'],
        password = os.environ['ARANGO_USER_PASSWORD']
    )

    alldata = db.query()

    db_local = otter.Otter(
        url="http://localhost:8529",
        username="root",
        password=os.environ['ARANGO_ROOT_PASSWORD']
    )
    for t in alldata:
        doc = dict(t)
        del doc["_key"]
        del doc["_id"]
        del doc["_rev"]
        db_local.upload(doc, collection="transients")
    
if __name__ == "__main__":
    main()
