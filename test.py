import json

import pytest

from tools import scrapd_merger
from tools.scrapd_augmenter_geocoding_geocensus import async_update_entries
from tools.scrapd_augmenter_geocoding_geocensus import sanitize, parse_geocensus_response


class TestMerge:
    def test_merge_00(self):
        actual = scrapd_merger.merge(json.loads(OLD), json.loads(NEW), update=True)
        expected = json.loads(FINAL)
        assert actual == expected


class TestGeolocation:
    def test_sanitize_00(self):
        """Ensure an address is sanitized."""
        actual = sanitize('8100 block of N. Lamar Blvd.')
        expected = '8100 N. Lamar Blvd.'.lower()
        assert actual == expected

    def test_parse_result_00(self):
        """Ensure a valid geocensus response gets parsed correctly."""
        actual = parse_geocensus_response(json.loads(GEOCENSUS_RESPONSE))
        expected = {'Latitude': 38.846565, 'Longitude': -76.926956}
        assert actual == expected

    def test_parse_result_01(self):
        """Ensure an empty geocensus response is parsed as an empty geolocation."""
        actual = parse_geocensus_response({})
        expected = {}
        assert actual == expected

    @pytest.mark.asyncio
    async def test_async_update_entries_00(self):
        entries = [{'Case': '19-0400694', 'Location': '8100 Block of N. Lamar Blvd.'}]
        actual = await async_update_entries(entries)
        assert actual[0]['Latitude'] == 30.350113
        assert actual[0]['Longitude'] == -97.710434

    @pytest.mark.asyncio
    async def test_update_two_entries_from_same_case_with_ID_field(self):
        final = json.loads(FINAL)
        entries = [final[0], final[1]]
        actual = await async_update_entries(entries)
        assert actual[0]['Case'] == '17-0780309'
        assert actual[0]['Latitude'] == 30.399498
        assert actual[0]['Longitude'] == -97.71893
        assert actual[1]['Case'] == '17-0780309'
        assert actual[1]['Latitude'] == 30.399498
        assert actual[1]['Longitude'] == -97.71893

# Test data

GEOCENSUS_RESPONSE = """
{
    "result": {
        "input": {
            "address": {
                "address": "4600 Silver Hill Rd, Suitland, MD 20746"
            },
            "benchmark": {
                "id": 9,
                "benchmarkName": "Public_AR_Census2010",
                "benchmarkDescription": "Public Address  Ranges – Census 2010",
                "isDefault": false
            }
        },
        "addressMatches": [{
            "matchedAddress": "4600 Silver  Hill  Rd, SUITLAND, MD, 20746",
            "coordinates": {
                "x": -76.926956,
                "y": 38.846565
            },
            "tigerLine": {
                "tigerLineId": "613199520",
                "side": "L"
            },
            "addressComponents": {
                "fromAddress": "4600",
                "toAddress": "4712",
                "preQualifier": "",
                "preDirection": "",
                "preType": "",
                "streetName": "Silver Hill",
                "suffixType": "Rd",
                "suffixDirection": "",
                "suffixQualifier": "",
                "city": "SUITLAND",
                "state": "MD",
                "zip": "20746"
            }
        }]
    }
}
"""



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
        "ID": "17-0780309-0",
        "Last Name": "Jackson",
        "Link": "http://austintexas.gov/news/traffic-fatality-15-2",
        "Location": "11600 block of Burnet Rd.",
        "Time": "2:30 a.m."
    },
    {
        "Age": 23,
        "Case": "17-0780309",
        "DOB": "11-8-93",
        "Date": "Sunday, March 19, 2017",
        "Ethnicity": "Black",
        "Fatal crashes this year": "15",
        "First Name": "Second",
        "Gender": "male",
        "ID": "17-0780309-1",
        "Last Name": "Fatality",
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
        "ID": "17-0710136-0",
        "Last Name": "Garcia-Servin",
        "Link": "http://austintexas.gov/news/traffic-fatality-14-3",
        "Location": "10010 N. Lamar Blvd.",
        "Time": "1:21 a.m."
    },
    {
        "Case": "17-0770668",
        "Date": "March 18, 2017",
        "Fatal crashes this year": "13",
        "ID": "17-0770668-0",
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
        "ID": "17-0780309-0",
        "Last Name": "Jackson",
        "Link": "http://austintexas.gov/news/traffic-fatality-15-2",
        "Location": "11600 block of Burnet Rd.",
        "Notes": "This case is still being investigated. Anyone with information regarding this incident is asked to call the APD Vehicular Homicide Unit Detectives at (512) 974-4424. You can also submit tips by downloading APD\u2019s mobile app, Austin PD, for free on iPhone and Android. This is Austin\u2019s 15th fatal traffic crash of 2017. At this time in 2016, there were 14 fatal traffic crashes and 14 traffic fatalities.",
        "Time": "2:30 a.m."
    },
    {
        "Age": 23,
        "Case": "17-0780309",
        "DOB": "11/08/1993",
        "Date": "03/19/2017",
        "Ethnicity": "Black",
        "Fatal crashes this year": "15",
        "First Name": "Second",
        "Gender": "male",
        "ID": "17-0780309-1",
        "Last Name": "Fatality",
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
        "ID": "17-0710136-0",
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
        "ID": "17-0780309-0",
        "Last Name": "Jackson",
        "Link": "http://austintexas.gov/news/traffic-fatality-15-2",
        "Location": "11600 block of Burnet Rd.",
        "Notes": "This case is still being investigated. Anyone with information regarding this incident is asked to call the APD Vehicular Homicide Unit Detectives at (512) 974-4424. You can also submit tips by downloading APD\u2019s mobile app, Austin PD, for free on iPhone and Android. This is Austin\u2019s 15th fatal traffic crash of 2017. At this time in 2016, there were 14 fatal traffic crashes and 14 traffic fatalities.",
        "Time": "2:30 a.m."
    },
        {
        "Age": 23,
        "Case": "17-0780309",
        "DOB": "11/08/1993",
        "Date": "03/19/2017",
        "Ethnicity": "Black",
        "Fatal crashes this year": "15",
        "First Name": "Second",
        "Gender": "male",
        "ID": "17-0780309-1",
        "Last Name": "Fatality",
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
        "ID": "17-0710136-0",
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
        "ID": "17-0770668-0",
        "Link": "http://austintexas.gov/news/traffic-fatality-13-2",
        "Location": "4200 block of Southwest Parkway",
        "Time": "8:07 a.m."
    }
]
"""
