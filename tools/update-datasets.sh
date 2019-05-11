#!/bin/bash
set -euo pipefail

# Define variables.
CURRENT_YEAR=$(date +%Y)
TOPDIR=$(git rev-parse --show-toplevel)
DATASET_DIR="${TOPDIR}/datasets"
CURRENT_DATASET="${DATASET_DIR}/fatalities-${CURRENT_YEAR}-raw.json"
TOOL_DIR="${TOPDIR}/tools"
MERGER="${TOPDIR}/tools/scrapd-merger.py"

# Ensure we are in the top directory.
cd "${TOPDIR}"|| exit

# Generate the current data set.
ENTRY_COUNT_BEFORE=$(jq length "${CURRENT_DATASET}")
python "${MERGER}" -i "${CURRENT_DATASET}" <(scrapd -v --format json --from "Jan 1 ${CURRENT_YEAR}" --to "Dec 31 ${CURRENT_YEAR}");
HAS_CHANGE=$(git status -s)

# If nothing changed, we can leave.
if [ -z "${HAS_CHANGE}" ]; then
  echo "There is nothing new to commit."
  exit 0
fi

for YEAR in {2017..2019}; do
  echo "=> Processing year ${YEAR}..."

  # Prepare variables.
  RAW_DATA_SET="${DATASET_DIR}/fatalities-${YEAR}-raw.json"
  AUGMENTED_DATA_SET="${DATASET_DIR}/fatalities-${YEAR}-augmented.json"
  AUGMENTATION_DIR="${TOPDIR}/augmentations/${YEAR}"

  # Create augmented data sets from the raw ones.
  echo -e "\t- Resetting augmented data sets..."
  cp "${RAW_DATA_SET}" "${AUGMENTED_DATA_SET}"

  # Apply the augmentations (1st pass).
  # This is to restore the previous state as we rebuilt the data set from scratch.
  echo -e "\t- Applying augmentations (1st pass)..."
  for AUGMENTATION in "${AUGMENTATION_DIR}"/*.json; do
    echo -e "\t\t- $(basename ${AUGMENTATION})"
    python "${MERGER}" -i "${AUGMENTED_DATA_SET}" "${AUGMENTATION}"
  done

  # Generate the augmentations.
  echo -e "\t- Generating new augmentations..."
  AUGMENTATIONS="scrapd-augmenter-geocoding-geocensus.py:augmentation-geocoding-geocensus-${YEAR}.json"
  for AUGMENTATION in ${AUGMENTATIONS}; do
    TOOL="${TOOL_DIR}/$(echo ${AUGMENTATION}|cut -d':' -f1)"
    AUGMENTATION_FILE="${AUGMENTATION_DIR}/$(echo ${AUGMENTATION}|cut -d':' -f2)"
    echo -e "\t\t- $(basename ${AUGMENTATION_FILE})"
    python "${TOOL}" "${RAW_DATA_SET}" > "${AUGMENTATION_FILE}"
  done

  # Apply the augmentations (2nd pass).
  # This is to add the new augmentations if any.
  echo -e "\t- Applying augmentations (2nd pass)..."
  for AUGMENTATION in "${AUGMENTATION_DIR}"/*.json; do
    echo -e "\t\t- $(basename ${AUGMENTATION})"
    python "${MERGER}" -i "${AUGMENTED_DATA_SET}" "${AUGMENTATION}"
  done
done

# Merge the results.
cd "${TOPDIR}/datasets"|| exit
echo "=> Merging the yearly data sets..."
jq -s add fatalities-20{17..19}-raw.json > fatalities-all-raw.json
jq -s add fatalities-20{17..19}-augmented.json > fatalities-all-augmented.json

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
  -m "$(git status -s)"
pycalver bump -n || pycalver bump -n --patch
git push origin master
git push --tags
