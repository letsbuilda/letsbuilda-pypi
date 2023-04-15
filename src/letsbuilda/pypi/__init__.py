"""letsbuilda-pypi
A wrapper for PyPI's API and RSS feed
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Final

import xmltodict
from aiohttp import ClientSession

__all__: list[str] = [
    "PyPIServices",
    "PackageMetadata",
]


def _parse_publication_date(publication_date: str) -> datetime:
    return datetime.strptime(publication_date, "%a, %d %b %Y %H:%M:%S %Z")


@dataclass(frozen=True, slots=True)
class PackageMetadata:
    """Package metadata"""

    title: str
    package_link: str
    guid: str
    description: str | None
    author: str | None
    publication_date: datetime

    @classmethod
    def build_from(cls, data: dict[str, str]) -> "PackageMetadata":
        """Build an instance from raw data"""
        publication_date: str | None = data.get("pubDate")
        if publication_date is not None:
            publication_date: datetime = _parse_publication_date(publication_date)

        return cls(
            title=data.get("title").split()[0],
            package_link=data.get("link"),
            guid=data.get("guid"),
            description=data.get("description"),
            author=data.get("author"),
            publication_date=publication_date,
        )


class PyPIServices:
    """A class for interacting with PyPI"""

    NEWEST_PACKAGES_FEED_URL: Final[str] = "https://pypi.org/rss/packages.xml"
    PACKAGE_UPDATES_FEED_URL: Final[str] = "https://pypi.org/rss/updates.xml"

    def __init__(self, http_session: ClientSession) -> None:
        self.http_session = http_session

    async def get_rss_feed(self, feed_url: str) -> list[PackageMetadata]:
        """Get the new packages RSS feed"""
        async with self.http_session.get(feed_url) as response:
            response_text = await response.text()
            rss_data = xmltodict.parse(response_text)["rss"]["channel"]["item"]
            return [PackageMetadata.build_from(package_data) for package_data in rss_data]
