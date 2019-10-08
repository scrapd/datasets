"""
`scrapd-augmenter-geocoding-geocensus` is an augmenter geocoding the crash locations.

It uses the Geo Census database. The script does not recode entries which already have their geolocation.

Usage examples:

$ scrapd-augmenter-geocoding-geocensus fatalities.json
"""
import argparse
import asyncio
import json
import logging
import pprint
import sys

import aiohttp
from loguru import logger
import pytest

GEO_CENSUS_URL = "https://geocoding.geo.census.gov/geocoder/geographies/address"


def main():
    """Define the main entrypoint of the program."""
    # Create the CLI.
    parser = get_cli_parser()
    args = parser.parse_args()

    # Merge the data.
    entries = json.loads(args.infile.read())
    results = asyncio.run(async_update_entries(entries))
    results_str = json.dumps(results, sort_keys=True, indent=2)

    # Write the data to `old` file.
    if args.in_place:
        try:
            args.infile.seek(0)
            args.infile.truncate()
            args.infile.flush()
            args.infile.write(results_str)
        finally:
            args.infile.close()
    else:
        # Display the results.
        print(results_str)


def get_cli_parser():  # pragma: no cover
    """Get the CLI parser."""
    parser = argparse.ArgumentParser(description='Create beautiful releases on GitHub.')
    parser.add_argument('infile', type=argparse.FileType('r+t'))
    parser.add_argument('-i', '--in-place', action='store_true', help="Update OLD in place")

    return parser


async def fetch_json(session, url, params=None):
    """
    Fetch the data from a URL as JSON.

    :param aiohttp.ClientSession session: aiohttp session
    :param str url: request URL
    :param dict params: request paramemters, defaults to None
    :return: the data from a URL as text.
    :rtype: str
    """
    if not params:
        params = {}
    try:
        async with session.get(url, params=params) as response:
            return await response.json()
    except (
            aiohttp.ClientError,
            aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        logger.error(f'aiohttp exception for {url} -> {e}')
    except Exception as e:
        logger.exception(f'non-aiohttp exception occured: {e}')


async def fetch_and_update(session, url, params, entry):
    """
    Parse a fatality page from a URL.

    :param aiohttp.ClientSession session: aiohttp session
    :param str url: detail page URL
    :return: a dictionary representing a fatality.
    :rtype: dict
    """
    # Prepare the result.
    d = {}

    # Ensure twe have a case number.
    case = entry.get('case')
    if not case:
        return d

    # Fetch the geolocation
    response = await fetch_json(session, url, params)

    # Parse it.
    geolocation = parse_geocensus_response(response)
    if not geolocation:
        return d

    # Add the geolocation aumentation.
    d["case"] = case
    d.update(geolocation)

    # Return the result.
    return d


async def async_update_entries(entries):
    """
    Update the entries with the geolocations.
    """
    async with aiohttp.ClientSession() as session:

        # Prepare the requests.
        tasks = [
            fetch_and_update(
                session,
                GEO_CENSUS_URL,
                {
                    "street": sanitize(entry.get('location', '')),
                    "city": "Austin",
                    "state": "TX",
                    "benchmark": "Public_AR_Census2010",
                    "vintage": "Census2010_Census2010",
                    "layers": "14",
                    "format": "json"
                },
                entry,
            ) for entry in entries if not entry.get('Latitude')
        ]
        results = await asyncio.gather(*tasks)
        return [entry for entry in results if entry]


def sanitize(address):
    """
    Sanitize the location field if needed.

    :param str address: address to sanitize
    """
    # Remove 'block of ' from the address.
    addr = address.lower()
    addr = addr.replace('block of ', '')
    addr = addr.replace('block ', '')
    return addr


def parse_geocensus_response(response):
    """
    Parse the geocensus response.

    :param dict result: geocensus response
    """
    d = {}
    if response and response.get('result', {}).get('addressMatches'):
        first_match = response.get('result', {}).get('addressMatches', [])[0]
        latitude = first_match.get('coordinates', {}).get('y', '')
        longitude = first_match.get('coordinates', {}).get('x', '')
        if latitude:
            d['latitude'] = latitude
        if longitude:
            d['longitude'] = longitude

    return d


if __name__ == "__main__":
    main()


class TestGeolocation:
    def test_sanitize_00(self):
        """Ensure an address is sanitized."""
        actual = sanitize('8100 block of N. Lamar Blvd.')
        expected = '8100 N. Lamar Blvd.'.lower()
        assert actual == expected

    def test_parse_result_00(self):
        """Ensure a valid geocensus response gets parsed correctly."""
        actual = parse_geocensus_response(json.loads(GEOCENSUS_RESPONSE))
        expected = {'latitude': 38.846565, 'longitude': -76.926956}
        assert actual == expected

    def test_parse_result_01(self):
        """Ensure an empty geocensus response is parsed as an empty geolocation."""
        actual = parse_geocensus_response({})
        expected = {}
        assert actual == expected

    @pytest.mark.asyncio
    async def test_async_update_entries_00(self):
        entries = [{'case': '19-0400694', 'location': '8100 Block of N. Lamar Blvd.'}]
        actual = await async_update_entries(entries)
        assert actual[0]['latitude'] == 30.350113
        assert actual[0]['longitude'] == -97.710434


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
