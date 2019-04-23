#!/bin/bash
set -euo pipefail

RESOURCE_URL="https://data.austintexas.gov/resource/"
DATASETS="2013:vggi-9ddh 2014:gm9p-snyb 2015:p658-umsa 2016:tiqb-wv3c 2017:ijds-pcyq 2018:9jd4-zjmx"

for DATASET in ${DATASETS}; do
  YEAR=$(echo ${DATASET}|cut -d':' -f1)
  CODE=$(echo ${DATASET}|cut -d':' -f2)
  curl -sL "${RESOURCE_URL}${CODE}.json" -o "socrata-apd-${YEAR}.json"
done
