#!/bin/bash
set -euo pipefail

TOPDIR=$(git rev-parse --show-toplevel)
for YEAR in {2017..2018}; do
  AUGMENTATION_DIR="${TOPDIR}/augmentations/${YEAR}"
  SCRAPD_DATASET_DIR="${TOPDIR}/datasets"
  TOOL="${TOPDIR}/tools/scrapd-importer-fatalities-socrata.py"
  RAW_DATASET="${SCRAPD_DATASET_DIR}/fatalities-${YEAR}-raw.json"
  SOCRATA_DATASET="${TOPDIR}/external-datasets/socrata-apd-archives/socrata-apd-${YEAR}.json"
  AUGMENTATION_FILE="${AUGMENTATION_DIR}/augmentation-import-apd-${YEAR}.json"
  echo -e "=> Generating Socrata APD augmentation for ${YEAR}..."
  python "${TOOL}" "${RAW_DATASET}" "${SOCRATA_DATASET}" > "${AUGMENTATION_FILE}"
done
