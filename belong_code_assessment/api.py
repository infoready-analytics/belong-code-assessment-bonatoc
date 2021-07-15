import urllib
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from pathlib import Path

import pandas as pd
import requests

from belong_code_assessment.utils import get_logger, preprocess_df, unpack_args


def get_pedestrian_record_count(url):
    """Send GET request to obtain the number of pedestrian records from the Socrata Open Data API.

    Args:
        url (str): API endpoint.

    Raises:
        Exception: If response status code is anything other than 200.

    Returns:
        int: Number of pedestrian records.
    """
    response = requests.get(f"{url}?$select=count(*)")

    if response.status_code != 200:
        raise Exception(f"Could not fetch record counts from {url}.")

    return int(response.json()[0]["count"])


def _get_pedestrian_data_from_api(url, offset, limit=50000):
    """Send GET request to obtain pedestrian records in JSON format from the Socrata Open Data API.

    Args:
        url (str): API endpoint.
        offset (int): Index of the result array where to start the returned list of results.
        limit (int, optional): Number of results to return per request. Defaults to 50000.

    Returns:
        list: JSON representation of pedestrian records.
    """

    response = requests.get(f"{url}?$offset={offset}&$limit={limit}")

    return response.json()


@preprocess_df
def get_pedestrian_data_from_api(url, limit=50000, n_records=0):
    """Entrypoint function for sending a GET request to obtain pedestrian records in JSON format
    from the Socrata Open Data API. Uses a ThreadPool to speed up requests - but will generally be
    slower than downloading the CSV file over HTTP via the function get_pedestrian_data_from_http()
    unless the number of processes is set to at least 6.

    Args:
        url (str): API endpoint.
        limit (int, optional): Number of results to return per request. Defaults to 50000.
        n_records(int, optional): Manually specify the number of records you'd like to fetch.

    Returns:
        pd.DataFrame: Pedestrian count data in DataFrame format.
    """

    n_records = get_pedestrian_record_count(url) if not n_records else n_records
    pool = ThreadPool(processes=int(cpu_count() / 2))

    # build list of arguments for threadpool
    args = (
        [_get_pedestrian_data_from_api, (url, i), {"limit": limit}]
        for i in range(0, n_records + 1, limit)
    )

    data = []
    for json_data in pool.imap_unordered(unpack_args, args):
        data += json_data

    pool.close()
    pool.join()

    return pd.DataFrame(data)


@preprocess_df
def get_pedestrian_data_from_http(url, filepath, retries=3):
    """Download pedestrian records from a network object from a URL to a local file.

    Args:
        url (str): URL of the network object.
        filepath (pathlib.Path or str): Where to save the file to.
        retries (int, optional): Number of attempts at downloading the object before giving up.
        Defaults to 3.

    Returns:
        pd.DataFrame or None: If successful, returns a DataFrame, if unsuccessful returns None.
    """

    while retries > 0:
        try:
            urllib.request.urlretrieve(url, filepath)

            if Path(filepath).exists():
                return pd.read_csv(filepath)
        except Exception as e:
            retries -= 1
            continue

    return None
