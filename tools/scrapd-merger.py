"""
`scrapd-merger` is a tool to merge 2 ScrAPD data sets together.

The data sets are expected to be arrays of objects (see test data at the bottom).

Usage examples:

$ python scrapd-merger.py old.json <(cat new.json)
$ cat new.json | python scrapd-merger.py old.json -
"""

import argparse
import datetime
import json
import logging
import pprint
import sys

from scrapd.core import model
from scrapd.core.formatter import to_json


def main():
    """Define the main entrypoint of the program."""
    # Create the CLI.
    parser = get_cli_parser()
    args = parser.parse_args()

    # Merge the data.
    results = merge(json.loads(args.old.read()), json.loads(args.infile.read()), args.update)
    sorted_results = sorted(results, key=lambda x: x.case)

    # Write the data to `old` file.
    if args.in_place:
        args.old.seek(0)
        args.old.truncate()
        args.old.write(to_json(sorted_results))
    else:
        # Display the results.
        print(results_str)


def get_cli_parser():  # pragma: no cover
    """Get the CLI parser."""
    parser = argparse.ArgumentParser(description='Merge ScrAPD data sets.')
    parser.add_argument('old', type=argparse.FileType('r+t'))
    parser.add_argument('infile', type=argparse.FileType('rt'), default=sys.stdin)
    parser.add_argument('-i', '--in-place', action='store_true', help="Update OLD in place")
    parser.add_argument('-u', '--update', action='store_true', help='Update existing fields')

    return parser


def merge(old, new, update):
    """
    Merge `new` data into `old` data.

    :param list(dict) old: old data
    :param list(dict) new: new data
    :return: the new data merged into the old data
    :rtype: list(dict)
    """

    old_dict = {entry['case']: model.Report(**entry) for entry in old}
    new_dict = {entry['case']: model.Report(**entry) for entry in new}
    final_dict = {}

    for entry in old_dict:
        old_entry = old_dict.get(entry)
        new_entry = new_dict.pop(entry, None)
        old_entry.update(new_entry)
        final_dict[entry] = old_entry

    final_dict.update(new_dict)
    return list(final_dict.values())


if __name__ == "__main__":
    main()


class TestMerge:
    def test_merge_00(self):
        actual = merge(OLD, NEW, False)
        expected = FINAL
        assert actual == expected


# Test data
OLD = [
    {
        "case": "19-0400694",
        "crash": 7,
        "date": "2019-02-09",
        "fatalities": [{
            "age": 13,
            "dob": "2005-12-05",
            "ethnicity": "Black",
            "first": "Messiah",
            "gender": "Male",
            "generation": "",
            "last": "Mouton",
            "middle": ""
        }],
        "latitude": 0.0,
        "link": "http://austintexas.gov/news/traffic-fatality-7-4",
        "location": "6000 block of Springdale Road",
        "longitude": 0.0,
        "notes": "The preliminary investigation shows that the driver of a 1997, red BMW was traveling northbound in the 6000 block of Springdale Road and lost control. The vehicle skidded sideways before flipping and striking a utility pole.\n\n\tThe passenger in the vehicle, Messiah Zion Mouton, was pronounced deceased at the scene.",
        "time": "12:48:00"
    },
]

NEW = [
    {
        "case": "19-0400694",
        "crash": 7,
        "date": "2019-02-09",
        "fatalities": [{
            "age": 13,
            "dob": "2005-12-05",
            "ethnicity": "Black",
            "first": "Messiah",
            "gender": "Male",
            "generation": "",
            "last": "Mouton",
            "middle": ""
        }],
        "latitude": 30.303625,
        "link": "http://austintexas.gov/news/traffic-fatality-7-4",
        "location": "6000 block of Springdale Road",
        "longitude": -97.67139,
        "notes": "The preliminary investigation shows that the driver of a 1997, red BMW was traveling northbound in the 6000 block of Springdale Road and lost control. The vehicle skidded sideways before flipping and striking a utility pole.\n\n\tThe passenger in the vehicle, Messiah Zion Mouton, was pronounced deceased at the scene.",
        "time": "12:48:00"
    },
    {
        "case": "19-0150158",
        "crash": 1,
        "date": "2019-01-15",
        "fatalities": [{
            "age": 31,
            "dob": "1987-07-09",
            "ethnicity": "White",
            "first": "David",
            "gender": "Male",
            "generation": "",
            "last": "Sell",
            "middle": ""
        }],
        "latitude": 0.0,
        "link": "http://austintexas.gov/news/traffic-fatality-1-4",
        "location": "10500 block of N IH 35 SB",
        "longitude": 0.0,
        "notes": "The preliminary investigation shows that a 2000 Peterbilt semi truck was travelling southbound in the center lane on IH 35 when it struck pedestrian David Sell. The driver stopped as soon as it was possible to do so and remained on scene. He reported not seeing the pedestrian prior to impact given that it was still dark at the time of the crash. Sell was pronounced deceased at the scene at 6:24 a.m. No charges are expected to be filed.",
        "time": "06:20:00"
    },
]

FINAL_JSON = [
    {
        "case": "19-0400694",
        "crash": 7,
        "date": "2019-02-09",
        "fatalities": [{
            "age": 13,
            "dob": "2005-12-05",
            "ethnicity": "Black",
            "first": "Messiah",
            "gender": "Male",
            "generation": "",
            "last": "Mouton",
            "middle": ""
        }],
        "latitude": 30.303625,
        "link": "http://austintexas.gov/news/traffic-fatality-7-4",
        "location": "6000 block of Springdale Road",
        "longitude": -97.67139,
        "notes": "The preliminary investigation shows that the driver of a 1997, red BMW was traveling northbound in the 6000 block of Springdale Road and lost control. The vehicle skidded sideways before flipping and striking a utility pole.\n\n\tThe passenger in the vehicle, Messiah Zion Mouton, was pronounced deceased at the scene.",
        "time": "12:48:00"
    },
    {
        "case": "19-0150158",
        "crash": 1,
        "date": "2019-01-15",
        "fatalities": [{
            "age": 31,
            "dob": "1987-07-09",
            "ethnicity": "White",
            "first": "David",
            "gender": "Male",
            "generation": "",
            "last": "Sell",
            "middle": ""
        }],
        "latitude": 0.0,
        "link": "http://austintexas.gov/news/traffic-fatality-1-4",
        "location": "10500 block of N IH 35 SB",
        "longitude": 0.0,
        "notes": "The preliminary investigation shows that a 2000 Peterbilt semi truck was travelling southbound in the center lane on IH 35 when it struck pedestrian David Sell. The driver stopped as soon as it was possible to do so and remained on scene. He reported not seeing the pedestrian prior to impact given that it was still dark at the time of the crash. Sell was pronounced deceased at the scene at 6:24 a.m. No charges are expected to be filed.",
        "time": "06:20:00"
    },
]

FINAL = [
    model.Report(
        case="19-0400694",
        crash=7,
        date=datetime.date(2019, 2, 9),
        fatalities=[
            model.Fatality(
                age=13,
                dob=datetime.date(2005, 12, 5),
                ethnicity=model.Ethnicity.black,
                first="Messiah",
                gender=model.Gender.male,
                generation="",
                last="Mouton",
                middle="",
            ),
        ],
        latitude=30.303625,
        link="http://austintexas.gov/news/traffic-fatality-7-4",
        location="6000 block of Springdale Road",
        longitude=-97.67139,
        notes=
        "The preliminary investigation shows that the driver of a 1997, red BMW was traveling northbound in the 6000 block of Springdale Road and lost control. The vehicle skidded sideways before flipping and striking a utility pole.\n\n\tThe passenger in the vehicle, Messiah Zion Mouton, was pronounced deceased at the scene.",
        time="12:48:00"),
    model.Report(
        case="19-0150158",
        crash=1,
        date="2019-01-15",
        fatalities=[
            model.Fatality(
                age=31,
                dob="1987-07-09",
                ethnicity=model.Ethnicity.white,
                first="David",
                gender=model.Gender.male,
                generation="",
                last="Sell",
                middle="",
            ),
        ],
        latitude=0.0,
        link="http://austintexas.gov/news/traffic-fatality-1-4",
        location="10500 block of N IH 35 SB",
        longitude=0.0,
        notes=
        "The preliminary investigation shows that a 2000 Peterbilt semi truck was travelling southbound in the center lane on IH 35 when it struck pedestrian David Sell. The driver stopped as soon as it was possible to do so and remained on scene. He reported not seeing the pedestrian prior to impact given that it was still dark at the time of the crash. Sell was pronounced deceased at the scene at 6:24 a.m. No charges are expected to be filed.",
        time="06:20:00",
    ),
]
