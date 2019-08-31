import json

from tools import scrapd_merger


class TestMerge:
    def test_merge_00(self):
        actual = scrapd_merger.merge(json.loads(OLD), json.loads(NEW), update=True)
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
