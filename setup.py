'''
This file imports the json files from .otter into the arango database
'''

import os
import json
import glob
from pyArango.connection import *

def main():
    c = Connection(
        arangoURL=os.environ.get("ARANGO_URL", "http://127.0.0.1:8529"),
        username="root",
        password=os.environ.get("ARANGO_ROOT_PASSWORD", None)
    )
    
    # create the otter database with a transient collection
    print(c.hasDatabase('otter'))
    if c.hasDatabase('otter'):
        db = c['otter']
    else:
        db = c.createDatabase(name="otter")

    # add a vetting collection to the database
    if not db.hasCollection("vetting"):
        _ = db.createCollection(name="vetting")
    
    # add a transients collection to the database    
    if db.hasCollection("transients"):
        t = db["transients"]
    else:
        t = db.createCollection(name="transients")

    # clean out all of the documents in this collection before adding more
    t.truncate() 
        
    # import the json files
    otterdir = os.path.join(os.getcwd(), '.otter')
    jsons = glob.glob(os.path.join(otterdir, '*.json'))
    for j in jsons:
        with open(j, 'r') as f:
            data = json.load(f)
    
        try:
            doc = t.createDocument(initDict=data)
            doc.save()
        except Exception as exc:
            print(exc)
            import pdb; pdb.set_trace()
    print(t.fetchAll())

if __name__ == "__main__":
    main()
