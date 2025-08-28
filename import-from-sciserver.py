"""
Import the data from SciServer to a local database

This script should really only be used by developers to import the data
"""
import os
import otter

def main():

    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--local-url", default="http://localhost:8529")
    args = p.parse_args()
    
    # first pull the data from sciserver
    db = otter.Otter(
        url=os.environ['ARANGO_URL'],
        password = os.environ['ARANGO_USER_PASSWORD']
    )

    alldata = db.query()

    db_local = otter.Otter(
        url=args.local_url,
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
