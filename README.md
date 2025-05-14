# otterdb
Backend database code and data for OTTER

## Installing a copy of the database (should only be done by devs)
1. Make sure you have set the following environment variables. If you don't
know what the value should be, contact an existing developer.
```
ARANGO_URL
ARANGO_ROOT_PASSWORD
VETTING_PASSWORD
ARANGO_USER_PASSWORD
```
2. Make sure docker is running. Then run the docker container from dockerhub
```
docker run \
-p 8529:8529 \
-e ARANGO_ROOT_PASSWORD=$ARANGO_ROOT_PASSWORD \ 
-e VETTING_PASSWORD=$VETTING_PASSWORD \
noahfranz13/otterdb:v0.3.6
```
3. Add a copy of the data to the database from the master copy at SciServer.
From the otterdb directory, run
```
python3 import_from_sciserver.py
```

## A note on the classification `confidence` keyword
These confidence scores are *our* **rough** confidence values in the classification
of this object. They were determined using the following, somewhat arbitrary, system:

| Confidence | Reason |
|------------|--------|
| 0.1 | Classifications with these values are from the Open TDE Catalog and either did not have a classification reference or were not strictly classified as a TDE in that catalog |
| 0.5 | These classifications are from TNS. We give classifications from TNS a confidence of 0.5 because there are a select few that are wrong on TNS (e.g. 2017bcc) |
| 1 | We trust the reference for this classification |

**Warning:** This confidence score system is still under development and may have bugs or mistakes, please trust at your own risk!

## Providing Data
We expect the data to come as a zip file that contains a single `meta.csv`
file, a separate csv photometry file for each transient (but not necessarily
required for each transient), and an individual FITS file for every spectra.
More details about each file are below.

### `meta.csv`
This file contains metadata for the transient event you are providing. A list
of possible column names are below.

Required Columns:
* `name`: The name (internal or IAU) of the transient
* `ra`: The right ascencsion of the transient
* `dec`: The declination of the transient
* `ra_units`: The units of the provided RA
* `dec_units`: The units of the provided declination
* `reference`: The ads bibcode associated with this data

Optional Columns:
* `phot_path`: The path of the photometry file, relative to the directory that
the `meta.csv` file is in.
* `spec_path`: The path of the spectrum file, relative to the directory that the `meta.csv` file is in.
* `redshift`: The measured redshift (only provide if YOU measured it)
* `luminosity_distance`:
* `dispersion_measure`:
* `date_discovery`: Discovery date of the transient if you discovered it
* `date_discovery_format`: Format of the discovery date
* `class`: The classification of the transient (e.g. SN, TDE, FRB, etc.)

### The photometry CSV files
There should be one file per event in the meta file. These photometry csv
files have the following columns.

Required Columns:
* `date`: The date the photometric observation was made
* `date_format`: The format of the date given
* `raw`: The raw photometry. This can be a flux, flux density, magnitude,
energy, or count.
* `raw_units`: The units (or system in the case of a magnitude) of `raw`
* `filter`: The name of the telescope filter

Required/Optional Columns (Only required in some cases):
* `telescope_area`: Collecting area of the telescope. Required if the
photometry is given in counts!
* `val_k`: The k-correction value applied. Only required if a k-correction
was applied.
* `val_s`: The s-correction value applied. Required if an s-correction was
applied.
* `val_av`: The value of the applied Milky Way Extinction. Required if the
photometry was corrected for Milky Way Extinction.
* `val_host`: The value of the applied host correction. Required only if the
photometry is host subtracted.
* `val_hostav`: The value of the host extinction. Required if the photometry
was corrected for host extinction.

Optional Columns:
* `raw_err`: The error on the raw photometry value given.
* `date_err`: The error on the date given.
* `upperlimit`: Boolean. True if this is an upperlimit.
* `sigma`: Significance of the upperlimit.
* `instrument`: The instrument used to collect this data.
* `phot_type`: is the photometry PSF, Aperature, or synthetic.
* `exptime`: The exposure time
* `aperature`: The aperature diameter in arcseconds, if aperature photometry.
* `observer`: Name of the observer for this point.
* `reducer`: Name of the person who reduced this data point.
* `pipeline`: Name and version of the pipeline used to reduce this data.
* `filter_eff`: The effective wavelength or frequency of the filter. We will
use the `filter_eff_units` key to determine this.
* `filter_eff_units`: The units of `filter_eff`.
* `telescope`: The name of the telescope or observatory.

### The spectra FITS files
Spectra are not supported at this time.

