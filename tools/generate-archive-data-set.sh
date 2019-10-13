#!/bin/bash
set -euo pipefail

TOPDIR=$(git rev-parse --show-toplevel)
TOOL="${TOPDIR}/tools/socrata2scrapd-archive.py"
FAKE_JSON="/tmp/fake.json"
SOCRATA_ALL_DATASET="${TOPDIR}/external-datasets/socrata-apd-archives/socrata-apd-all.json"
ARCHIVE_DATASET="${TOPDIR}/datasets/archives-all.json"

echo "[]" > "${FAKE_JSON}"
python "${TOOL}" --extras "${FAKE_JSON}" "${SOCRATA_ALL_DATASET}" > "${ARCHIVE_DATASET}"
