"""Service wrapper"""

from typing import Final

import xmltodict
from aiohttp import ClientSession

from .models import JSONPackageMetadata, RSSPackageMetadata


class PyPIServices:
    """A class for interacting with PyPI"""

    NEWEST_PACKAGES_FEED_URL: Final[str] = "https://pypi.org/rss/packages.xml"
    PACKAGE_UPDATES_FEED_URL: Final[str] = "https://pypi.org/rss/updates.xml"

    def __init__(self, http_session: ClientSession) -> None:
        self.http_session = http_session

    async def get_rss_feed(self, feed_url: str) -> list[RSSPackageMetadata]:
        """Get the new packages RSS feed"""
        async with self.http_session.get(feed_url) as response:
            response_text = await response.text()
            rss_data = xmltodict.parse(response_text)["rss"]["channel"]["item"]
            return [RSSPackageMetadata.build_from(package_data) for package_data in rss_data]

    async def get_package_metadata(self, package_name: str, package_version: str | None = None) -> JSONPackageMetadata:
        """Get metadata for a package"""
        if package_version is not None:
            url = f"https://pypi.org/pypi/{package_name}/{package_version}/json"
        else:
            url = f"https://pypi.org/pypi/{package_name}/json"
        async with self.http_session.get(url) as response:
            return JSONPackageMetadata.from_dict(await response.json())
