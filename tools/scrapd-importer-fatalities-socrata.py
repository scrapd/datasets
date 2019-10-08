"""
`scrapd-importer-fatalities-socrata` is a tool to generate Socrata APD augmentations.

The data sets are expected to be arrays of objects (see test data at the bottom).

Usage examples:

$ python scrapd-importer-fatalities-socrata.py scrapd-data-set.json <(cat socarata-data-set.json)
$ cat socarata-data-set.json | python scrapd-importer-fatalities-socrata.py old.json -
"""

import argparse
import datetime
import json
import pprint
import sys

import dateparser
import pytest


def main():
    """Define the main entrypoint of the program."""
    # Create the CLI.
    parser = get_cli_parser()
    args = parser.parse_args()

    # Merge the data.
    results = merge(json.loads(args.scrapd.read()), json.loads(args.socrata.read()), args.extras)
    results_str = json.dumps(results, sort_keys=True, indent=2)
    print(results_str)


def get_cli_parser():  # pragma: no cover
    """Get the CLI parser."""
    parser = argparse.ArgumentParser(description='Import Socrata data.')
    parser.add_argument('scrapd', type=argparse.FileType('r+t'))
    parser.add_argument('socrata', type=argparse.FileType('rt'), default=sys.stdin)
    parser.add_argument('--extras', action='store_true', help='Add Socrata entries that do not match a ScrAPD entry')

    return parser


def merge(scrapd, socrata, extras=False):
    """
    Merge `socrata` data into `scrapd` data.

    :param list(dict) scrapd: scrapd data
    :param list(dict) socrata: socrata data
    :return: the socrata data merged into the scrapd data
    :rtype: list(dict)
    """
    # Read the scrapd values.
    scrapd_dict = {entry['case']: entry for entry in scrapd}

    # Map a Socrata entry to ScrAPD entry.
    socrata_dict = {}
    for entry in socrata:
        latitude_value = entry.get('y_coord') or entry.get('ycoord') or ''
        longitude_value = entry.get('x_coord') or entry.get('xcoord') or entry.get('coord_x', '') or ''

        d = {
            'case': entry.get('case_number', '').lower().strip(),
            'latitude': clean_coordinates(latitude_value.strip()),
            'location': entry.get('location', '').lower().strip(),
            'longitude': clean_coordinates(longitude_value.strip()),
            'time': clean_time(entry.get('time', '').lower().strip()),
        }
        socrata_dict[d.get('case')] = {k: v for k, v in d.items() if v}

    # Merge the results.
    final_dict = {}
    for entry in scrapd_dict:
        # Match the Socrata entry with a ScrAPD entry.
        socrata_entry = socrata_dict.pop(entry, {})
        if not socrata_entry:
            continue

        # Remove empty values.
        final_dict[entry] = {k: v for k, v in socrata_entry.items() if v is not None}
    if extras:
        final_dict.update(socrata_dict)

    return list(final_dict.values())


def clean_time(time):
    """
    Ensure the time has a 12 hour format

    :param str time: time to clean up
    """
    try:
        t = dateparser.parse(time)
    except ValueError:
        return ''
    else:
        return t.strftime("%H:%M:%S").lower()


def clean_date(date):
    """
    Ensure a date has the correct English format.

    :param (str) date: date to clean.
    """
    try:
        dt = datetime.datetime.fromisoformat(date)
    except ValueError:
        return ''
    else:
        return datetime.datetime.strftime(dt, "%Y-%m-%d")


def clean_coordinates(coordinate):
    """
    Ensure coordiantes are stored as floats.

    :param str coordinate: a string representing either a latitude, either a longitude.
    :return: the float representing the coordinate
    :rtype: float
    """
    try:
        return float(coordinate)
    except ValueError:
        return None


if __name__ == "__main__":
    main()


class TestMerge:
    def test_merge_00(self):
        actual = merge(json.loads(SCRAPD), json.loads(SOCRATA))
        expected = json.loads(FINAL)
        assert actual == expected

    @pytest.mark.parametrize('input_,expected', [
        ('2018-01-04T00:00:00.000', '2018-01-04'),
        ('01/04/2018', ''),
    ])
    def test_clean_date_00(self, input_, expected):
        actual = clean_date(input_)
        assert actual == expected

    @pytest.mark.parametrize('input_,expected', [
        ('-97.70766', -97.70766),
        ('30.315355', 30.315355),
        ('invalid', None),
    ])
    def test_clean_coordinates_00(self, input_, expected):
        actual = clean_coordinates(input_)
        assert actual == expected

    @pytest.mark.parametrize('input_,expected', [
        ('22:15', '22:15:00'),
        ('8:57', '08:57:00'),
        ('2018-01-04T00:00:00.000', '00:00:00'),
    ])
    def test_clean_time_00(self, input_, expected):
        actual = clean_time(input_)
        assert actual == expected


# Test data.
SCRAPD = """
[
    {
        "case": "18-0041689",
        "date": "01/04/2018",
        "link": "http://austintexas.gov/news/traffic-fatality-1-3",
        "location": "5600 N IH 35 Northbound",
        "time": "11:57 p.m."
    }
]
"""

SOCRATA = """
[
    {
        "area": "ID",
        "case_number": "18-0041689",
        "case_status": "Closed",
        "charge": "Pending",
        "date": "2018-01-04T00:00:00.000",
        "day": "Thu",
        "dl_status_incident": "suspended",
        "failure_to_stop_and_render_aid": "n",
        "fatal_crash_number": "1",
        "hour": "23",
        "killed_driver_pass": "driver and passenger",
        "location": "5600 Block N IH 35 NB",
        "month": "Jan",
        "number_of_fatalities": "2",
        "ran_red_light_or_stop_sign": "n",
        "related": "mv/18 Wheel",
        "restraint_type": "unknown",
        "speeding": "n",
        "suspected_impairment": "driver   ",
        "time": "23:25",
        "type": "MOTOR VEHICLE",
        "type_of_road": "IH35",
        "x_coord": "-97.70766",
        "y_coord": "30.315355"
    },
    {
        "area": "Charlie",
        "case_number": "14-0511533",
        "charge": "DOO",
        "date": "2014-02-20T00:00:00.000",
        "day": "Thu",
        "drivers_license_status": "suspended",
        "fatal_crash": "7",
        "ftsra": "No",
        "hour": "19",
        "killed_driver_pass": "Pedestrian",
        "location": "6400 FM 969",
        "month": "Feb",
        "number_of_fatalities": "1",
        "ran_red_light": "N",
        "related": "MV/PED",
        "restraint_or_helmet": "n/a",
        "speeding": "N",
        "suspected_impairment": "PEDESTRIAN",
        "time": "19:15:00",
        "type": "Pedestrian",
        "type_of_road": "high speed roadway",
        "x_coord": "-97.659822",
        "y_coord": "30.284725"
    }
]
"""

FINAL = """
[
    {
        "case": "18-0041689",
        "latitude": 30.315355,
        "location": "5600 block n ih 35 nb",
        "longitude": -97.70766,
        "time": "23:25:00"
    }
]
"""
