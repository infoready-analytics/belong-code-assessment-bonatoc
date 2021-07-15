import pytest


def pytest_addoption(parser):
    parser.addoption("--api_url", action="store", required=True)
    parser.addoption("--csv_url", action="store", required=True)


@pytest.fixture()
def api_url(request):
    return request.config.getoption("api_url")


@pytest.fixture()
def csv_url(request):
    return request.config.getoption("csv_url")
