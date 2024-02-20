'''
Code to convert the data from tde.space into the right format for 
'''

import os, glob, warnings
from copy import deepcopy
import numpy as np
import pandas as pd
import json
from otter import Otter, Transient
from otter import constants as otter_const
from otter.helpers import *
from astroquery.simbad import Simbad
import astropy.units as u

def main():

    datapath = os.path.relpath('../tde-1980-2025')
    exc = {'ASAS-SN Supernovae', 'MAST'}

    mappedsrc = lambda source_map, src: [source_map[key] for key in src if key in source_map]

    for file in glob.glob(os.path.join(datapath, '*.json')):
        print(f'Reformating {file}')
        with open(file, 'r') as f:
            j = json.load(f)[0]

        # copy over the references
        schema = deepcopy(otter_const.schema)
        source_map = {}
        for src in j['sources']:
            if 'bibcode' not in src and src['name'] in exc:
                bib = src['name']
            elif 'bibcode' not in src:
                print(f'No bibcode for {src}, skipping!')
                continue
            else:
                bib = src['bibcode']

            sub = deepcopy(otter_const.subschema['reference_alias'])
            sub['name'] = bib
            if 'reference' in src:
                sub['human_readable_name'] = src['reference']
            else:
                sub['human_readable_name'] = src['name']

            schema['reference_alias'].append(sub)

            source_map[src['alias']] = bib

        # copy over names and aliases
        schema['name/default_name'] = j['name']
        for val in j['alias']:
            sub = deepcopy(otter_const.subschema['name/alias'])
            sub['value'] = val['value']
            sub['reference'] = mappedsrc(source_map, val['source'].split(','))
            schema['name/alias'].append(sub)

        # copy over coordinates
        if 'ra' in j and 'dec' in j:
            key1, key2 = 'ra', 'dec'
        elif 'hostra' in j and 'hostdec' in j:
            key1, key2 = 'hostra', 'hostdec'
        else:
            print(f'Skipping {file} because no ra and dec associated with it!')
            continue

        for ra, dec in zip(j[key1], j[key2]):
            sub = deepcopy(otter_const.subschema['coordinate'])
            if ra['source'] != dec['source']:
                src = list(set(ra['source'].split(',')) or set(ra['source'].split(',')))
            else:
                src = ra['source'].split(',')

            if not any(s in source_map for s in src):
                print(f'Skipping {(ra, dec)} because it does not have a reliable reference!')
                continue

        sub['ra'] = ra['value']
        sub['dec'] = dec['value']
        sub['ra_units'] = ra['u_value']
        sub['dec_units'] = dec['u_value']
        sub['reference'] = mappedsrc(source_map, src)
        schema['coordinate'].append(clean_schema(sub))

        # copy over distance measurements
        # first redshift
        if 'redshift' in j:
            for ii, z in enumerate(j['redshift']):
                src = z['source'].split(',')
                if not any(s in source_map for s in src):
                    print(f'Skipping {z} because it does not have a reliable reference!')
                    continue

                sub = deepcopy(otter_const.subschema['distance/redshift'])
                sub['value'] = z['value']
                sub['reference'] = mappedsrc(source_map, src)
                sub['computed'] = False
                if ii == 0:
                    sub['default'] = True
                    schema['distance/redshift'].append(clean_schema(sub))
                    del j['redshift']

        if 'lumdist' in j:
            for ii, d in enumerate(j['lumdist']):
                src = d['source'].split(',')
                if not any(s in source_map for s in src):
                    print(f'Skipping {d} because it does not have a reliable reference!')
                    continue

                sub = deepcopy(otter_const.subschema['distance/luminosity_distance'])
                sub['value'] = d['value']
                sub['reference'] = mappedsrc(source_map, src)
                sub['computed'] = False
                sub['unit'] = d['u_value']
                if ii == 0:
                    sub['default'] = True
                    schema['distance/luminosity_distance'].append(clean_schema(sub))
                    del j['lumdist']

        if 'comovingdist' in j:
            for ii, d in enumerate(j['comovingdist']):
                src = d['source'].split(',')
                if not any(s in source_map for s in src):
                    print(f'Skipping {d} because it does not have a reliable reference!')
                    continue

                sub = deepcopy(otter_const.subschema['distance/comoving_distance'])
                sub['value'] = d['value']
                sub['reference'] = mappedsrc(source_map, src)
                sub['computed'] = False
                sub['unit'] = d['u_value']
                if ii == 0:
                    sub['default'] = True
                    schema['distance/comoving_distance'].append(clean_schema(sub))
                    del j['comovingdist']

        # dates
        if 'discoverdate' in j:
            for ii, d in enumerate(j['discoverdate']):
                src = d['source'].split(',')
                if not any(s in source_map for s in src):
                    print(f'Skipping {d} because it does not have a reliable reference!')
                    continue

                if '/' in d['value']:
                    indate = d['value'].replace('/', '-') + ' 00:00:00.000' 
                    sub['date_format'] = 'iso'
                elif isinstance(d['value'], str) and len(d['value']) == 4: # this is just a year
                    indate = d['value'] + '-01-01 00:00:00.000'
                    sub['date_format'] = 'iso'
                else:
                    print(j['discoverdate'])
                    raise ValueError('New Type of date found, please fix!')

                sub = deepcopy(otter_const.subschema['date_reference'])
                sub['value'] = indate
                sub['reference'] = mappedsrc(source_map, src)
                sub['measurement_type'] = 'discovery'
                if 'derived' in d:
                    sub['computed'] = d['derived']
                else:
                    sub['computed'] = False

                sub['computed'] = False
                if ii == 0:
                    sub['default'] = True
                    schema['date_reference'].append(clean_schema(sub))
                    del j['discoverdate']

        # copy classification
        if 'claimedtype' in j:
            #print(json.dumps(j, indent=4))
            for ii, d in enumerate(j['claimedtype']):
                src = d['source'].split(',')
                if not any(s in source_map for s in src):
                    print(f'Skipping {d} because it does not have a reliable reference!')
                    continue

                sub = deepcopy(otter_const.subschema['classification'])
                sub['object_class'] = d['value']
                sub['reference'] = mappedsrc(source_map, src)
                sub['confidence'] = 1.0
                schema['classification'].append(clean_schema(sub))

            del j['claimedtype']

        # copy photometry
        if 'photometry' in j:
            phot = pd.DataFrame(j['photometry'])
            if 'telescope' in phot and 'u_time' in phot:
                gby = ['source', 'telescope', 'u_time']
            elif 'u_time' in phot:
                gby = ['source', 'u_time']
            else:
                gby = ['source']

            for grouped_by, group in phot.groupby(gby):

                if len(grouped_by) == 3:
                    ref, telescope, tfmt = grouped_by
                elif len(grouped_by) == 2:
                    ref, tfmt = grouped_by
                    telescope = None
                else:
                    ref = grouped_by
                    telescope = None
                    raise ValueError('Time format uncertain') # for now, hopefully we never come to this anyways...

                # clean up group
                group = group.dropna(axis=1, how='any')
                #print(group)
                sub = deepcopy(otter_const.subschema['photometry'])
                src = ref.split(',')
                if not any(s in source_map for s in src):
                    print(f'Skipping {d} because it does not have a reliable reference!')
                    continue

                sub['reference'] = mappedsrc(source_map, src)
                sub['telescope'] = telescope

                usedFluxForRaw = False
                if 'magnitude' in group:
                    sub['raw'] = list(group.magnitude)
                    if 'e_magnitude' in group:
                        sub['raw_err'] = list(group.e_magnitude)
                    if 'system' in group:
                        sub['raw_units'] = list(group.system)
                    else:
                        sub['raw_units'] = 'AB'
                    if 'band' in group:
                        sub['filter'] = list(group.band)
                    else:
                        print(f'Skipping {group} because no filter given so unreliable!')
                        continue # don't add this one

                    sub['date'] = list(group['time'])
                    sub['date_format'] = tfmt
                    
                elif 'countrate' in group:
                    ctrate = np.array(group.countrate)
                    if ctrate.ndim > 1:
                        ctrate = ctrate[:,0]
                        
                    sub['raw'] = list(ctrate)
                    if 'e_countrate' in group:
                        err = np.array(group.e_countrate)
                        if err.ndim > 1:
                            err = err[:,0]

                        sub['raw_err'] = list(err)
                    
                    if 'u_countrate' in group:
                        sub['raw_units'] = list(group.u_countrate)
                    else:
                        print(f'Skipping {group} because no units given so unreliable!')
                        continue # don't add this one
                    if 'energy' in group:
                        sub['filter'] = [item[0]+'-'+item[1] for item in group.energy]
                    else:
                        raise ValueError()
                        print(f'Skipping {group} because no filter given so unreliable!')
                        continue # don't add this one

                    date = [val[0] if isinstance(val, list) else val for val in group['time']]
                    sub['date'] = list(date)
                    sub['date_format'] = tfmt
                    
                elif 'flux' in group and 'u_flux' in group: # we will just use the flux for the raw data
                    usedFluxForRaw = True
                    sub['raw'] = list(group.flux)
                    sub['value_units'] = list(group.u_flux)
                    if 'e_flux' in group:
                        sub['value_err'] = list(group.e_flux)
                    if 'band' in group:
                        sub['filter'] = list(group.band)
                    elif 'energy' in group:
                        sub['filter'] = [item[0]+'-'+item[1] for item in group.energy]
                    else:
                        print(f'Skipping {group} because no filter given so unreliable!')
                        raise ValueError()
                        continue # don't add this one

                    date = [val[0] if isinstance(val, list) else val for val in group['time']]
                    sub['date'] = list(date)
                    sub['date_format'] = tfmt
                    
                else:
                    # for radio data, throw an error for now
                    print(group)
                    #raise ValueError('Unknown type of photometry! Please Fix!')
                    print('Skipping this photometry point because it is an unknown type! Please fix!')

                if 'flux' in group and 'u_flux' in group and not usedFluxForRaw:
                    sub['value'] = list(group.flux)
                    sub['value_units'] = list(group.u_flux)
                    if 'e_flux' in group:
                        sub['value_err'] = list(group.e_flux)
                                            
                if 'upperlimit' in group:
                    sub['upperlimit'] = list(group['upperlimit'])
                else:
                    sub['upperlimit'] = [False]*len(group) # james tended to only store this if it is True

                schema['photometry'].append(clean_schema(sub))

            del j['photometry']

        # ADD SPECTRA ONCE WE HAVE A BETTER IDEA OF FORMATTING

        # ADD HOST INFO ONCE WE HAVE A BETTER IDEA OF FORMATTING

        # remove everything we've added from j to help keep track
        del j['name']
        del j['alias']
        del j['sources']
        del j[key1]
        del j[key2]

        print(j.keys())
        #print(json.dumps(j, indent=4))

        # get rid of sub distance measurements cause none of these have it
        for subkey in ['dispersion_measure', 'redshift', 'luminosity_distance', 'comoving_distance']:
            if len(schema[f'distance/{subkey}']) == 0:
                del schema['distance'][subkey]

        outpath = os.path.relpath(f'../tdedotspace_reformated/{os.path.basename(file)}')

        out = json.dumps(clean_schema(dict(schema)), indent=4)
        out = '[' + out
        out += ']'

        #print(out, '->', outpath)
        # some checks of the outputs
        assert len(schema['coordinate']) > 0
        assert len(schema['name/alias']) > 0
        assert len(schema['reference_alias']) > 0
        
        with open(outpath, 'w+') as outfile:
            outfile.write(out)
        
if __name__ == '__main__':
    main()
