# Data sets

Traffic fatality data sets for Austin, TX.

## Data availability

The traffic fatality reports pusblished by APD are hosted on their website for 2 years. Past this point they are
archived and are not publicly accessible anymore.

## Workflow

Our automated workflow is composed of the 4 following steps:

1. Generate the raw data sets.
2. Import/Merge the external data sets.
3. Augment the data sets.
4. Merge the results into `*-all-*.json` data sets.

Using these techniques to generate the data sets, we ensure that they can always be recreated in case of problem would occur.

Each step will be detailed in a dedicated section bellow.

### Generate raw data sets

The data sets named `fatalities-{year}-raw.json` are generated directly from `ScrAPD` without any manual intervention. A data set is created for each year.

### Import/Merge external data sets

Each of these external data sets has a dedicated documentation file in the `docs` folder.

* Socrata

Here is an example showing how the data is imported:

```bash
TOPDIR=$(git rev-parse --show-toplevel); for YEAR in {17..18}; do python ${TOPDIR}/tools/scrapd-importer-fatalities-socrata.py ${TOPDIR}/datasets/fatalities-20${YEAR}-raw.json ${TOPDIR}/external-datasets/socrata-apd-archives/socrata-apd-20${YEAR}.json > ${TOPDIR}/datasets/fatalities-20${YEAR}-augmented.json;done
```

### Augment the data sets

The data sets named `fatalities-{year}-augmented.json` are data sets that have been enhanced, in order to improve the
quality of the data.

```bash
# Generate empty data sets.
for f in fatalities-20{13..20}-augmented.json; do echo "[]" > "${f}"; done
```

Augment the data sets:

```bash
for f in fatalities-20{13..20}-augmented.json; do python "${TOPDIR}/tools/scrapd-augmenter-geocoding-geocensus.py"-i ${f}; done
```

The data sets are being augmented with ScrAPD augmenters that can be found in the `tools` folder. Each augmenter

Currently the following augmenters are available:

* scrapd-augmenter-geocoding-geocensus

#### Manual corrections

Corrections can also be added manually. Corrections can add extra fields or update values in existing fields. They are
applied last.

A correction must be made in a file named `fatalities-{year}-manual.json`. All the corrections for the same year
**MUST** be grouped together in the same file. The order does not matter. If an entry is found several times, the last
one (i.e. the lowest one in the file) will superseed all the others.

```json
[
  {
    "19-0400694": {
      "Type": "Pedestrian",
      "Gender": "Female",
    },
    "19-0320079": {
      "Type": "Bicyle",
      "Gender": "Unknown",
    }
  }
]
```

### "all" data sets

The data sets whose year is `all` are a combination of all the data sets of the same category.

There are generated using the following `jq` command:

```bash
jq -s add fatalities-20{17..20}-raw.json > fatalities-all-raw.json
jq -s add fatalities-20{17..20}-augmented.json > fatalities-augmented-raw.json
```

## Full updates

A full update happens when ScrAPD gets updated with changes that drastically improve the quality of the data which was retrieved.

ScrAPD versions which required a full update:

* 1.5.0
* 1.5.1

As a result, all the data sets were updated with the following command:

```bash
for i in {17..20}; do python tools/scrapd-merger.py -i fatalities-20${i}-raw.json <(scrapd -v --format json --from "Jan 1 20${i}" --to "Dec 31 20${i}"); done
```
