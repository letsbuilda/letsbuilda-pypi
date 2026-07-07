"""Test building a `Package` from the JSON API in `get_package_metadata`."""

import asyncio

import httpx

from letsbuilda.pypi import Package
from letsbuilda.pypi.async_client import PyPIServices as AsyncPyPIServices
from letsbuilda.pypi.sync_client import PyPIServices as SyncPyPIServices
from tests.test_json_api_parsing import JSON_API_DATA


def _handler(_: httpx.Request) -> httpx.Response:
    """Return the sample JSON API data for any request."""
    return httpx.Response(200, json=JSON_API_DATA)


def _assert_package(package: Package) -> None:
    """Confirm the sample data is mapped onto a `Package` correctly."""
    assert package.title == "letsbuilda-pypi"
    assert len(package.releases) == 1

    release = package.releases[0]
    assert release.version == "4.0.0"
    assert [distribution.filename for distribution in release.distributions] == [
        "letsbuilda_pypi-4.0.0-py3-none-any.whl",
        "letsbuilda-pypi-4.0.0.tar.gz",
    ]


def test_sync_get_package_metadata() -> None:
    """Confirm the sync client builds a `Package` from the JSON API data."""
    client = httpx.Client(transport=httpx.MockTransport(_handler))
    package = SyncPyPIServices(client).get_package_metadata("letsbuilda-pypi")
    _assert_package(package)


def test_async_get_package_metadata() -> None:
    """Confirm the async client builds a `Package` from the JSON API data."""

    async def _run() -> Package:
        async with httpx.AsyncClient(transport=httpx.MockTransport(_handler)) as client:
            return await AsyncPyPIServices(client).get_package_metadata("letsbuilda-pypi")

    _assert_package(asyncio.run(_run()))
