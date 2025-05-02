'''
This file imports the json files from .otter into the arango database
'''

import os
import json
import glob
from pyArango.connection import *
import requests

def upload_doc(doc, bearer):

    headers = {
        "Authorization": f"bearer {bearer}",
        "Content-Type": "application/json"
    }
    
    payload = doc.getStore()
    
    r = requests.post(
        f"{os.environ.get('ARANGO_URL', 'http://127.0.0.1:8529')}/_db/otter/_api/document/transients",
        headers=headers,
        json=payload,
    )


def main():

    import argparse
    
    p = argparse.ArgumentParser()
    p.add_argument("--bearer", help="JWT Bearer token", required=True)
    args = p.parse_args()
    
    c = Connection(
        arangoURL=os.environ.get("ARANGO_URL", "http://127.0.0.1:8529"),
        username="root",
        password=os.environ.get("ARANGO_ROOT_PASSWORD", None)
    )

    db = c['otter']
    t = db["transients"]
    
    # import the json files
    otterdir = os.path.join(os.getcwd(), '.otter')
    jsons = glob.glob(os.path.join(otterdir, '*.json'))
    for j in jsons:
        with open(j, 'r') as f:
            data = json.load(f)
    
        try:
            doc = t.createDocument(initDict=data)
        except Exception as exc:
            print(j)
            print(exc)
            import pdb; pdb.set_trace()

        try:
            upload_doc(doc, args.bearer)
        except Exception as e:
            import traceback
            print("Exception:", e)
            traceback.print_exc()
            if hasattr(e, 'resp') and hasattr(e.resp, 'text'):
                print("Response body:", e.resp.text)
            import pdb; pdb.set_trace()
            
        # print(t.fetchAll())
    
if __name__ == "__main__":
    main()
