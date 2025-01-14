"""Retrieves information stored in stache entry secrets."""

import requests
import json
import os


def auth(key, url, cred_type=None):
    """Takes api keys and returns the desired from the stache entry's secret.

    Arguments:
        key: The stache X-STACHE-READ-KEY.
        url: The stache endpoint.
        cred_type: Key mapping to desired cred within stache secret, where
            nested dictionary keys are separated by '/'.

    Returns:
        Requested credentials if found, None if they could not be found.

    Requirements:
        The secret must be a json-able dictionary, with any number of nested
            dictionaries within it.
    """
    response = requests.get(url, headers=key)
    response.raise_for_status()
    response = response.json()

    result = json.loads(response["secret"])

    if cred_type:
        for key in cred_type.split('/'):
            result = result.get(key)

    return result


def get_entry(filename):
    """Loads file from filename and returns the stache information as a tuple.

    Arguments:
        filename: name of file which stores X-STACHE-READ-KEY and endpoint as
            a JSON. The stache token file must be in the format:
        {
            "X-STACHE-READ-KEY": "stache_read_key",
            "endpoint": "stache_endpoint"
        }
        and must be saved in the cwd of the file that imports stache_creds.

    Returns:
        returns (key, url) of the api entry as a tuple.
    """
    with open(filename, "r") as file:
        creds = json.loads(file.read())
    # Get key and api endpoint for url.
    read_key = creds["X-STACHE-READ-KEY"]
    end_point = creds["endpoint"]

    # Format for request.
    key = {"X-STACHE-READ-KEY": read_key}
    url = f"https://stache.arizona.edu{end_point}"
    return key, url
