"""
Script to convert existing data sets from the ScrAPD 2 to the ScrAPD 3 format.
"""
import argparse
import datetime
import json
import sys

from scrapd.core import date_utils
from scrapd.core import model
from scrapd.core.formatter import to_json


def main():
    """Define the main entrypoint of the program."""
    # Create the CLI.
    parser = get_cli_parser()
    args = parser.parse_args()

    # Merge the data.
    results = convert(json.loads(args.infile.read()))
    sorted_results = sorted(results, key=lambda x: x.case)

    # Write the data to the data set file.
    if args.in_place:
        try:
            args.infile.seek(0)
            args.infile.truncate()
            args.infile.flush()
            args.infile.write(to_json(sorted_results))
        finally:
            args.infile.close()
    else:
        # Display the results.
        formatter = Formatter('json')
        formatter.print(results)


def get_cli_parser():  # pragma: no cover
    """Get the CLI parser."""
    parser = argparse.ArgumentParser(description='Convert data set from ScrAPD 2 to ScrAPD 3.')
    parser.add_argument('infile', type=argparse.FileType('r+t'), default=sys.stdin)
    parser.add_argument('-i', '--in-place', action='store_true', help="Update OLD in place")

    return parser


def convert(entries):
    result = [load_scrapd2(entry) for entry in entries]
    return result


def load_scrapd2(entry):
    """
    Load a ScrAPD 2 entry and returns a ScrAPD3 one.
    """
    r = model.Report(case=entry['Case'])
    if entry.get('Fatal crashes this year'):
        r.crash = int(entry.get('Fatal crashes this year'))
    if entry.get('Date'):
        r.date = date_utils.parse_date(entry.get('Date'))
    if entry.get('Link'):
        r.link = entry.get('Link')
    if entry.get('Latitude'):
        r.latitude = entry.get('Latitude')
    if entry.get('Location'):
        r.location = entry.get('Location')
    if entry.get('Longitude'):
        r.longitude = entry.get('Longitude')
    if entry.get('Notes'):
        r.notes = entry.get('Notes')
    if entry.get('Time'):
        r.time = date_utils.parse_time(entry.get('Time'))

    f = model.Fatality()
    if entry.get('Age'):
        f.age = int(entry.get('Age'))
    if entry.get('DOB'):
        f.dob = date_utils.parse_date(entry.get('DOB'))
    if entry.get('Ethnicity'):
        try:
            f.ethnicity = model.Ethnicity(entry.get('Ethnicity').capitalize())
        except ValueError:
            f.ethnicity = model.Ethnicity.undefined
    if entry.get('First Name'):
        f.first = entry.get('First Name')
    if entry.get('Gender'):
        try:
            f.gender = model.Gender(entry.get('Gender').capitalize())
        except ValueError:
            f.gender = model.Gender.undefined
    if entry.get('Last Name'):
        f.last = entry.get('Last Name')

    r.fatalities = [f]
    r.compute_fatalities_age()

    return r


if __name__ == "__main__":
    main()


class TestConvert:
    def test_convert_00(self):
        """Ensure a ScrAPD entry is convert from v2 to v3."""
        actual = convert(SCRAPD2_ENTRY)
        expected = [SCRAPD3_ENTRY]
        assert actual == expected


SCRAPD2_ENTRY = [{
    "1": "Cedric Benson | Black male | 12/28/1982 Deceased",
    "2": "Aamna Najam | Asian female | 01/26/1992",
    "Age": 36,
    "Case": "19-2291933",
    "DOB": "12/28/1982",
    "Date": "08/17/2019",
    "Ethnicity": "Black",
    "Fatal crashes this year": "50",
    "First Name": "Cedric",
    "Gender": "male",
    "Last Name": "Benson",
    "Link": "http://austintexas.gov/news/traffic-fatality-50-3",
    "Location": "4500 FM 2222/Mount Bonnell Road",
    "Notes": "The preliminary investigation yielded testimony from witnesses who reported seeing the BMW motorcycle "
    "driven by Cedric Benson traveling at a high rate of speed westbound in the left lane of FM 2222. A white, 2014 "
    "Dodge van was stopped at the T-intersection of Mount Bonnell Road and FM 2222. After checking for oncoming "
    "traffic, the van attempted to turn left on to FM 2222 when it was struck by the oncoming motorcycle. The driver "
    "of the van was evaluated by EMS on scene and refused transport. The passenger of the van and a bystander at the "
    "scene attempted to render aid to Mr. Benson and his passenger Aamna Najam. Cedric Benson and Aamna Najam were "
    "both pronounced on scene. The van driver remained on scene and is cooperating with the ongoing investigation. "
    "The family of Cedric Benson respectfully requests privacy during this difficult time and asks that media refrain "
    "from contacting them.",
    "Time": "10:20 PM"
}]

SCRAPD3_ENTRY = model.Report(
    case='19-2291933',
    crash=50,
    date=datetime.date(2019, 8, 17),
    fatalities=[
        model.Fatality(
            age=36,
            dob=datetime.date(1982, 12, 28),
            ethnicity=model.Ethnicity.black,
            first='Cedric',
            gender=model.Gender.male,
            last='Benson',
        ),
    ],
    link='http://austintexas.gov/news/traffic-fatality-50-3',
    location='4500 FM 2222/Mount Bonnell Road',
    notes='The preliminary investigation yielded testimony from witnesses who reported seeing the '
    'BMW motorcycle driven by Cedric Benson traveling at a high rate of speed westbound in the left '
    'lane of FM 2222. A white, 2014 Dodge van was stopped at the T-intersection of Mount Bonnell Road '
    'and FM 2222. After checking for oncoming traffic, the van attempted to turn left on to FM 2222 '
    'when it was struck by the oncoming motorcycle. The driver of the van was evaluated by EMS '
    'on scene and refused transport. The passenger of the van and a bystander at the scene attempted '
    'to render aid to Mr. Benson and his passenger Aamna Najam. Cedric Benson and Aamna Najam were both '
    'pronounced on scene. The van driver remained on scene and is cooperating with the ongoing '
    'investigation. The family of Cedric Benson respectfully requests privacy during this difficult '
    'time and asks that media refrain from contacting them.',
    time=datetime.time(22, 20),
)
