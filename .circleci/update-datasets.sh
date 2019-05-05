#!/bin/bash
set -xeuo pipefail

# Define variables.
TOPDIR=$(git rev-parse --show-toplevel)
CURRENT_YEAR=$(date +%Y)
CURRENT_DATASET="fatalities-${CURRENT_YEAR}-raw.json"

# Generate the current data set.
cd "${TOPDIR}/datasets"|| exit
ENTRY_COUNT_BEFORE=$(jq length "${CURRENT_DATASET}")
python "${TOPDIR}/tools/scrapd-merger.py" -i "${CURRENT_DATASET}" <(scrapd -v --format json --from "Jan 1 ${CURRENT_YEAR}" --to "Dec 31 ${CURRENT_YEAR}");
HAS_CHANGE=$(git status -s)

# If nothing changed, we can leave.
if [ -z "${HAS_CHANGE}" ]; then
  echo "There is nothing new to commit."
  exit 0
fi

# Create augmented data sets from the raw ones if needed.
for YEAR in {17..19}; do
  [ ! -f "fatalities-20${YEAR}-augmented.json" ] && cp "fatalities-20${YEAR}-raw.json" "fatalities-20${YEAR}-augmented.json"
done

# Import external data sets.
for YEAR in {17..19}; do
  # Import data from Socrata.
  SOCRATA_DATA_SET="${TOPDIR}/external-datasets/socrata-apd-archives/socrata-apd-20${YEAR}.json"
  # [ -f "${SOCRATA_DATA_SET}" ] && python "${TOPDIR}/tools/scrapd-importer-fatalities-socrata.py" "fatalities-20${YEAR}-raw.json" "${SOCRATA_DATA_SET}" > "fatalities-20${YEAR}-augmented.json"
done

# Augment the current data set.
for f in fatalities-20{17..19}-augmented.json; do
  # Augment the data with geocoding information from geocensus.
  [ -f "${f}" ] && python "${TOPDIR}/tools/scrapd-augmenter-geocoding-geocensus.py" -i ${f};
done

# Merge the results.
jq -s add fatalities-20{17..19}-raw.json > fatalities-all-raw.json
jq -s add fatalities-20{17..19}-augmented.json > fatalities-all-augmented.json

# Compute the number of new entries.
ENTRY_COUNT_AFTER=$(jq length "${CURRENT_DATASET}")
NEW_ENTRY_COUNT=$(( ENTRY_COUNT_AFTER - ENTRY_COUNT_BEFORE ))
echo "There are ${NEW_ENTRY_COUNT} new entries in the current data set."

# Go back to the top dir.
cd "${TOPDIR}"|| exit
exit 0
# Commit the changes.
git add .
git commit -m "Update data sets" \
  -m "There are ${NEW_ENTRY_COUNT} new entries in the current data set." \
  -m "${HAS_CHANGE}"
pycalver bump -n || pycalver bump -n --patch
git push origin master
git push --tags
