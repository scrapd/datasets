#!/bin/bash
set -euo pipefail

# Define variables.
TOPDIR=$(git rev-parse --show-toplevel)
DATASET_DIR="${TOPDIR}/datasets"
TOOL_DIR="${TOPDIR}/tools"
MERGER="${TOOL_DIR}/scrapd-merger.py"

# Ensure we are in the top directory.
cd "${TOPDIR}"|| exit

# Print scrapd version.
echo "==> INFO <=="
scrapd --version
echo "==> <==> <=="

# Generate the current data set.
for YEAR in {2017..2019}; do
  echo "=> Processing year ${YEAR}..."
  DATASET="${DATASET_DIR}/fatalities-${YEAR}-raw.json"
  echo -e "\t>>> BEFORE >>>"
  echo -n -e "\tCrash count:"
  jq '[ .[] | {}] | length' "${DATASET}"
  echo -n -e "\tFatality count:"
  jq '[ .[].fatalities[] | {}] | length' "${DATASET}"
  python "${MERGER}" -i -u "${DATASET}" <(scrapd --format json --from "Jan 1 ${YEAR}" --to "Dec 31 ${YEAR}");
  echo -e "\t<<< AFTER <<<"
  echo -n -e "\tCrash count:"
  jq '[ .[] | {}] | length' "${DATASET}"
  echo -n -e "\tFatality count:"
  jq '[ .[].fatalities[] | {}] | length' "${DATASET}"
done
