'''
This file imports the json files from .otter into the arango database
'''

import os
import json
import glob
from pyArango.connection import *

def main():
    c = Connection(username="root", password=os.environ.get('OTTERDB_PASS', None))

    # create the otter database with a transient collection
    print(c.hasDatabase('otter'))
    if c.hasDatabase('otter'):
        db = c['otter']
    else:
        db = c.createDatabase(name="otter")

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
