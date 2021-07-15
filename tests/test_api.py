import os
import tempfile

from belong_code_assessment import api, utils


def test_api_available(api_url):
    """Test API URL is available."""
    assert utils.check_url(api_url) is True


def test_csv_available(csv_url):
    """Test CSV URL is available."""
    assert utils.check_url(csv_url) is True


def test_get_from_api(api_url):
    """Test that we can get pedestrian records from the API URL."""
    records = api.get_pedestrian_data_from_api(api_url, limit=1000, n_records=10000)
    assert len(records) == 11000


def test_download_over_http(csv_url):
    """Test CSV file can be downloaded and that it returns a non-empty file and DataFrame. This
    test generally takes > 1 minute to run."""

    with tempfile.NamedTemporaryFile() as tmp:
        result = api.get_pedestrian_data_from_http(csv_url, filepath=tmp.name)

        # test file is not empty
        assert os.stat(tmp.name).st_size > 0

    # test object type is DataFrame (without importing pandas)
    assert type(result).__name__ == "DataFrame"

    # test DataFrame is not empty
    assert len(result) > 0
