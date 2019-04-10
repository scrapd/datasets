#!/bin/bash
set -euo pipefail

TOPDIR=$(git rev-parse --show-toplevel)
CURRENT_YEAR=$(date +%Y)
CURRENT_DATASET="fatalities-${CURRENT_YEAR}-raw.json"

cd "${TOPDIR}/datasets"|| exit
ENTRY_COUNT_BEFORE=$(jq length "${CURRENT_DATASET}")
python "${TOPDIR}/tools/scrapd-merger.py" -i "${CURRENT_DATASET}" <(scrapd -v --format json --from "Jan 1 ${CURRENT_YEAR}" --to "Dec 31 ${CURRENT_YEAR}");
HAS_CHANGE=$(git status -s)
if [ -n "${HAS_CHANGE}" ]; then
  # Update the `-all` data set.
  jq -s add fatalities-20*-raw.json > fatalities-all-raw.json

  # Augment the data sets.
  python "${TOPDIR}/tools/scrapd-geolocation.py" -i ${CURRENT_DATASET}
  python "${TOPDIR}/tools/scrapd-geolocation.py" -i fatalities-all-raw.json

  # Compute the number of new entries.
  ENTRY_COUNT_AFTER=$(jq length "${CURRENT_DATASET}")
  NEW_ENTRY_COUNT=$(( ENTRY_COUNT_AFTER - ENTRY_COUNT_BEFORE ))
  echo "There are ${NEW_ENTRY_COUNT} new entries in the current data set."

  # Go back to the top dir.
  cd "${TOPDIR}"|| exit

  # Commit the changes.
  git add .
  git commit -m "Update data sets" \
    -m "There are ${NEW_ENTRY_COUNT} new entries in the current data set." \
    -m "${HAS_CHANGE}"
  pycalver bump -n || pycalver bump -n --patch
  git push origin master
  git push --tags
else
  echo "There is nothing new to commit."
fi
