#!/bin/bash
set -euo pipefail

# Define variables.
TOPDIR=$(git rev-parse --show-toplevel)
DATASET_DIR="${TOPDIR}/datasets"
TOOL_DIR="${TOPDIR}/tools"
MERGER="${TOPDIR}/tools/scrapd-merger.py"

# Ensure we are in the top directory.
cd "${TOPDIR}"|| exit

# Generate the current data set.
for YEAR in {2017..2020}; do
  echo "=> Processing year ${YEAR}..."
  DATASET="${DATASET_DIR}/fatalities-${YEAR}-raw.json"
  python "${MERGER}" -i -u "${DATASET}" <(scrapd -v --format json --from "Jan 1 ${YEAR}" --to "Dec 31 ${YEAR}");
done
