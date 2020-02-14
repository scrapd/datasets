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

    for case, entry in old_dict.items():
        old_entry = entry
        new_entry = new_dict.pop(case, None)
        if update and new_entry:
            old_entry = new_entry.copy(deep=True)
        else:
            old_entry.update(new_entry)
        final_dict[case] = old_entry

    final_dict.update(new_dict)
    return list(final_dict.values())


if __name__ == "__main__":
    main()


class TestMerge:
    def test_merge_00(self):
        actual = merge(OLD, NEW, True)
        expected = FINAL
        assert actual == expected

    def test_merge_01(self):
        actual = merge(OLD_SINGLE_TO_MULTI, NEW_SINGLE_TO_MULTI, True)
        expected = FINAL_SINGLE_TO_MULTI
        assert actual[0].dict() == expected[0].dict()


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

OLD_SINGLE_TO_MULTI = [{
    "case": "20-0420110",
    "crash": 15,
    "date": "2020-02-11",
    "fatalities": [{
        "age": 21,
        "dob": "1998-04-28",
        "ethnicity": "White",
        "first": "Owen",
        "gender": "Male",
        "generation": "",
        "last": "Macki",
        "middle": "William"
    }],
    "latitude": 0.0,
    "link": "http://austintexas.gov/news/fatality-crash-15-2",
    "location": "North Capital of Texas Hwy/North Mopac NB Svrd",
    "longitude": 0.0,
    "notes": "",
    "time": "02:02:00"
}]

NEW_SINGLE_TO_MULTI = [{
    "case": "20-0420110",
    "crash": 15,
    "date": "2020-02-11",
    "fatalities": [
        {
            "age": 21,
            "dob": "1998-04-28",
            "ethnicity": "White",
            "first": "Owen",
            "gender": "Male",
            "generation": "",
            "last": "Macki",
            "middle": "William"
        },
        {
            "age": 24,
            "dob": "1995-07-26",
            "ethnicity": "Asian",
            "first": "Raquel",
            "gender": "Female",
            "generation": "",
            "last": "Aveytia",
            "middle": "Gitane"
        },
    ],
    "link": "http://austintexas.gov/news/fatality-crash-15-2",
    "location": "North Capital of Texas Hwy/North Mopac NB Svrd",
    "time": "02:02:00"
}]

FINAL_SINGLE_TO_MULTI = [
    model.Report(
        case='20-0420110',
        crash=15,
        date=datetime.date(2020, 2, 11),
        fatalities=[
            model.Fatality(
                age=21,
                dob=datetime.date(1998, 4, 28),
                ethnicity=model.Ethnicity.white,
                first='Owen',
                gender=model.Gender.male,
                last='Macki',
                middle='William',
            ),
            model.Fatality(
                age=24,
                dob=datetime.date(1995, 7, 26),
                ethnicity=model.Ethnicity.asian,
                first='Raquel',
                gender=model.Gender.female,
                last='Aveytia',
                middle='Gitane',
            ),
        ],
        latitude=0.0,
        link="http://austintexas.gov/news/fatality-crash-15-2",
        location='North Capital of Texas Hwy/North Mopac NB Svrd',
        longitude=0.0,
        notes='',
        time=datetime.time(2, 2),
    )
]
