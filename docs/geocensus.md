# Geocensus augmenter

## Running it

```bash
  for year in 20{17..19}; do
    python tools/scrapd-augmenter-geocoding-geocensus.py datasets/"fatalities-${year}-raw.json" > "augmentation/${year}/augmentation-geocoding-geocensus-${year}.json"
  done
```

One liner:

```bash
for year in 20{17..19}; do python tools/scrapd-augmenter-geocoding-geocensus.py datasets/"fatalities-${year}-raw.json" > "augmentation/${year}/augmentation-geocoding-geocensus-${year}.json"; done
```
