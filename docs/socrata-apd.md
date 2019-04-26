# Socrata APD archives

The City of Austin provides data sets of traffic fatalities that are not available on the APD web site. Not all the information is there, but there are some extra fields that we can absolutely use to enhance our data sets.

## Retrieving the data sets

* 2013:
  * www: <https://data.austintexas.gov/Public-Safety/2013-APD-Traffic-Fatalities/vggi-9ddh>
  * json: <https://data.austintexas.gov/resource/vggi-9ddh.json>
* 2014:
  * www: <https://data.austintexas.gov/Public-Safety/2014-APD-Traffic-Fatalities/gm9p-snyb>
  * json: <https://data.austintexas.gov/resource/gm9p-snyb.json>
* 2015:
  * www: <https://data.austintexas.gov/Public-Safety/2015-APD-Traffic-Fatalities/p658-umsa>
  * json: <https://data.austintexas.gov/resource/p658-umsa.json>
* 2016:
  * www: <https://data.austintexas.gov/Public-Safety/2016-APD-Traffic-Fatalities/tiqb-wv3c>
  * json: <https://data.austintexas.gov/resource/tiqb-wv3c.json>
* 2017:
  * www: <https://data.austintexas.gov/Public-Safety/2017-APD-Traffic-Fatalities/ijds-pcyq>
  * json: <https://data.austintexas.gov/resource/ijds-pcyq.json>
* 2018:
  * www: <https://data.austintexas.gov/Public-Safety/2018-APD-Traffic-Fatality-Data-021219/9jd4-zjmx>
  * json: <https://data.austintexas.gov/resource/9jd4-zjmx.json>

## Augment the datasets

```bash
#!/bin/bash
set -xeuo pipefail

TOPDIR=$(git rev-parse --show-toplevel)
for YEAR in {17..18}; do
  python ${TOPDIR}/tools/scrapd-importer-fatalities-socrata.py \
    ${TOPDIR}/datasets/fatalities-20${YEAR}-raw.json \
    ${TOPDIR}/external-datasets/socrata-apd-archives/socrata-apd-20${YEAR}.json \
    > ${TOPDIR}/datasets/fatalities-20${YEAR}-augmented.json
done
```


