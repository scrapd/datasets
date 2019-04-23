"""
`scrapd-importer-fatalities-socrata` is a tool to merge Socrata APD data sets into ScrAPD data sets.

The new data will overwrite the old data in case of duplication. If there is no collision, the old data is left intact.

The data sets are expected to be arrays of objects (see test data at the bottom).

Usage examples:

$ python scrapd-importer-fatalities-socrata.py old.json <(cat new.json)
$ cat new.json | python scrapd-importer-fatalities-socrata.py old.json -
"""

import argparse
import datetime
import json
import pprint
import sys

import pytest


def main():
    """Define the main entrypoint of the program."""
    # Create the CLI.
    parser = get_cli_parser()
    args = parser.parse_args()

    # Merge the data.
    results = merge(json.loads(args.old.read()), json.loads(args.infile.read()))
    results_str = json.dumps(results, sort_keys=True, indent=2)

    # Write the data to `old` file.
    if args.in_place:
        args.old.seek(0)
        args.old.truncate()
        args.old.write(results_str)
    else:
        # Display the results.
        print(results_str)


def get_cli_parser():  # pragma: no cover
    """Get the CLI parser."""
    parser = argparse.ArgumentParser(description='Create beautiful releases on GitHub.')
    parser.add_argument('old', type=argparse.FileType('r+t'))
    parser.add_argument('infile', type=argparse.FileType('rt'), default=sys.stdin)
    parser.add_argument('-i', '--in-place', action='store_true', help="Update OLD in place")

    return parser


def merge(scrapd, socrata):
    """
    Merge `socrata` data into `scrapd` data.

    :param list(dict) scrapd: scrapd data
    :param list(dict) socrata: socrata data
    :return: the socrata data merged into the scrapd data
    :rtype: list(dict)
    """
    # Read the scrapd values.
    scrapd_dict = {entry['Case']: entry for entry in scrapd}

    # Map a Socrata entry to ScrAPD entry.
    socrata_dict = {}
    for entry in socrata:
        d = {
            'Age': entry.get('', ''),
            'Case': entry.get('case_number', ''),
            'DOB': entry.get('', ''),
            'Date': clean_date(entry.get('date', '')),
            'Ethnicity': entry.get('', ''),
            'Fatal crashes this year': entry.get('fatal_crash', ''),
            'First Name': entry.get('', ''),
            'Gender': entry.get('', ''),
            'Last Name': entry.get('', ''),
            'Link': entry.get('', ''),
            'Location': entry.get('location', ''),
            'Notes': entry.get('', ''),
            'Time': entry.get('time', ''),

            # Extra fields.
            'Charge': entry.get('charge', '').lower().strip(),
            'Drivers license status': entry.get('dl_status_incident', '').lower().strip(),
            'Hit and run': entry.get('failure_to_stop_and_render_aid', '').lower().strip(),
            'Impairment': entry.get('suspected_impairment', '').lower().strip(),
            'Killed': entry.get('killed_driver_pass', '').lower().strip(),
            'Latitude': clean_coordinates(entry.get('y_coord', '').strip()),
            'Longitude': clean_coordinates(entry.get('x_coord', '').strip()),
            'Ran light/stop': entry.get('ran_red_light_or_stop_sign', '').lower().strip(),
            'Restraint': entry.get('restraint_type', '').lower().strip(),
            'Road type': entry.get('type_of_road', '').strip(),
            'Type': entry.get('type', '').lower().strip(),
        }
        socrata_dict[d.get('Case')] = {k: v for k, v in d.items() if v}

    # Merge the results, giving priority to the ScrAPD entries.
    final_dict = {}
    for entry in scrapd_dict:
        scrapd_entry = scrapd_dict.get(entry, {})
        socrata_entry = socrata_dict.pop(entry, {})
        merged_entries = {**socrata_entry, **scrapd_entry}
        final_dict[entry] = merged_entries
    final_dict.update(socrata_dict)

    return list(final_dict.values())


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
        return datetime.datetime.strftime(dt, "%m/%d/%Y")


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
        ('2018-01-04T00:00:00.000', '01/04/2018'),
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


# Test data.
SCRAPD = """
[
    {
        "Age": 23,
        "Case": "18-0041689",
        "DOB": "11/27/1994",
        "Date": "01/04/2018",
        "Ethnicity": "Hispanic",
        "Fatal crashes this year": "1",
        "First Name": "Ashley",
        "Gender": "female",
        "Last Name": "Martinez",
        "Link": "http://austintexas.gov/news/traffic-fatality-1-3",
        "Location": "5600 N IH 35 Northbound",
        "Notes": "Eloy Herrera, Hispanic male (D.O.B. 4-9-02)",
        "Time": "11:57 p.m."
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
    }
]
"""

FINAL = """
[
    {
        "Age": 23,
        "Case": "18-0041689",
        "Charge": "pending",
        "Drivers license status": "suspended",
        "DOB": "11/27/1994",
        "Date": "01/04/2018",
        "Ethnicity": "Hispanic",
        "Fatal crashes this year": "1",
        "First Name": "Ashley",
        "Gender": "female",
        "Impairment": "driver",
        "Killed": "driver and passenger",
        "Hit and run":"n",
        "Latitude": 30.315355,
        "Last Name": "Martinez",
        "Link": "http://austintexas.gov/news/traffic-fatality-1-3",
        "Location": "5600 N IH 35 Northbound",
        "Longitude": -97.70766,
        "Ran light/stop": "n",
        "Restraint": "unknown",
        "Road type": "IH35",
        "Notes": "Eloy Herrera, Hispanic male (D.O.B. 4-9-02)",
        "Time": "11:57 p.m.",
        "Type": "motor vehicle"
    }
]
"""
