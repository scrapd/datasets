"""
`scrapd-merger` is a tool to merge 2 ScrAPD data sets together.

The new data will overwrite the old data in case of duplication. If there is no collision, the old data is left intact.

The data sets are expected to be arrays of objects (see test data at the bottom).

Usage examples:

$ python scrapd-merger.py old.json <(cat new.json)
$ cat new.json | python scrapd-merger.py old.json -
"""

import argparse
import json
import logging
import pprint
import sys


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


def merge(old, new):
    """
    Merge `new` data into `old` data.

    :param list(dict) old: old data
    :param list(dict) new: new data
    :return: the new data merged into the old data
    :rtype: list(dict)
    """

    old_dict = {entry['Case']: entry for entry in old}
    new_dict = {entry['Case']: entry for entry in new}
    final_dict = {}
    for entry in old_dict:
        old_entry = old_dict.get(entry, {})
        new_entry = new_dict.pop(entry, {})
        merged_entries = {**old_entry, **new_entry}
        final_dict[entry] = merged_entries
    return list(final_dict.values())


if __name__ == "__main__":
    main()


class TestMerge:
    def test_merge_00(self):
        actual = merge(json.loads(OLD), json.loads(NEW))
        expected = json.loads(FINAL)
        assert actual == expected


# Test data
OLD = """
[
    {
        "Age": 22,
        "Case": "17-0780309",
        "DOB": "11-8-94",
        "Date": "Sunday, March 19, 2017",
        "Ethnicity": "Black",
        "Fatal crashes this year": "15",
        "First Name": "Lamar",
        "Gender": "male",
        "Last Name": "Jackson",
        "Link": "http://austintexas.gov/news/traffic-fatality-15-2",
        "Location": "11600 block of Burnet Rd.",
        "Time": "2:30 a.m."
    },
    {
        "Age": 59,
        "Case": "17-0710136",
        "DOB": "12-21-57)",
        "Date": "March 12, 2017",
        "Ethnicity": "Hispanic",
        "Fatal crashes this year": "14",
        "First Name": "Tomas",
        "Gender": "male",
        "Last Name": "Garcia-Servin",
        "Link": "http://austintexas.gov/news/traffic-fatality-14-3",
        "Location": "10010 N. Lamar Blvd.",
        "Time": "1:21 a.m."
    },
    {
        "Case": "17-0770668",
        "Date": "March 18, 2017",
        "Fatal crashes this year": "13",
        "Link": "http://austintexas.gov/news/traffic-fatality-13-2",
        "Location": "4200 block of Southwest Parkway",
        "Time": "8:07 a.m."
    }
]
"""

NEW = """
[
    {
        "Age": 22,
        "Case": "17-0780309",
        "DOB": "11/08/1994",
        "Date": "03/19/2017",
        "Ethnicity": "Black",
        "Fatal crashes this year": "15",
        "First Name": "Lamar",
        "Gender": "male",
        "Last Name": "Jackson",
        "Link": "http://austintexas.gov/news/traffic-fatality-15-2",
        "Location": "11600 block of Burnet Rd.",
        "Notes": "This case is still being investigated. Anyone with information regarding this incident is asked to call the APD Vehicular Homicide Unit Detectives at (512) 974-4424. You can also submit tips by downloading APD\u2019s mobile app, Austin PD, for free on iPhone and Android. This is Austin\u2019s 15th fatal traffic crash of 2017. At this time in 2016, there were 14 fatal traffic crashes and 14 traffic fatalities.",
        "Time": "2:30 a.m."
    },
    {
        "Age": 59,
        "Case": "17-0710136",
        "DOB": "12/21/1957",
        "Date": "03/12/2017",
        "Ethnicity": "Hispanic",
        "Fatal crashes this year": "14",
        "First Name": "Tomas",
        "Gender": "male",
        "Last Name": "Garcia-Servin",
        "Link": "http://austintexas.gov/news/traffic-fatality-14-3",
        "Location": "10010 N. Lamar Blvd.",
        "Notes": "The preliminary investigation shows that a white 2015 Ford Focus was traveling southbound in the inside lane of the 10010 block of N. Lamar Blvd. A pedestrian was crossing mid-block westbound when he was struck by the Ford\u2019s left front side. The pedestrian was transported to University Medical Center at Brackenridge Hospital with critical injuries. He died as a result of his injuries on Monday, March 20, 2017.",
        "Time": "1:21 a.m."
    }
]
"""

FINAL = """
[
    {
        "Age": 22,
        "Case": "17-0780309",
        "DOB": "11/08/1994",
        "Date": "03/19/2017",
        "Ethnicity": "Black",
        "Fatal crashes this year": "15",
        "First Name": "Lamar",
        "Gender": "male",
        "Last Name": "Jackson",
        "Link": "http://austintexas.gov/news/traffic-fatality-15-2",
        "Location": "11600 block of Burnet Rd.",
        "Notes": "This case is still being investigated. Anyone with information regarding this incident is asked to call the APD Vehicular Homicide Unit Detectives at (512) 974-4424. You can also submit tips by downloading APD\u2019s mobile app, Austin PD, for free on iPhone and Android. This is Austin\u2019s 15th fatal traffic crash of 2017. At this time in 2016, there were 14 fatal traffic crashes and 14 traffic fatalities.",
        "Time": "2:30 a.m."
    },
    {
        "Age": 59,
        "Case": "17-0710136",
        "DOB": "12/21/1957",
        "Date": "03/12/2017",
        "Ethnicity": "Hispanic",
        "Fatal crashes this year": "14",
        "First Name": "Tomas",
        "Gender": "male",
        "Last Name": "Garcia-Servin",
        "Link": "http://austintexas.gov/news/traffic-fatality-14-3",
        "Location": "10010 N. Lamar Blvd.",
        "Notes": "The preliminary investigation shows that a white 2015 Ford Focus was traveling southbound in the inside lane of the 10010 block of N. Lamar Blvd. A pedestrian was crossing mid-block westbound when he was struck by the Ford\u2019s left front side. The pedestrian was transported to University Medical Center at Brackenridge Hospital with critical injuries. He died as a result of his injuries on Monday, March 20, 2017.",
        "Time": "1:21 a.m."
    },
    {
        "Case": "17-0770668",
        "Date": "March 18, 2017",
        "Fatal crashes this year": "13",
        "Link": "http://austintexas.gov/news/traffic-fatality-13-2",
        "Location": "4200 block of Southwest Parkway",
        "Time": "8:07 a.m."
    }
]
"""
