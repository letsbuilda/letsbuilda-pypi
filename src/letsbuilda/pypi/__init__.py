"""letsbuilda-pypi
A wrapper for PyPI's API and RSS feed
"""

from dataclasses import dataclass
from datetime import datetime
from weakref import finalize
from typing import Final
from asyncio import run

import xmltodict
from aiohttp import ClientSession

__all__: list[str] = [
    "PyPIServices",
    "NewPackageMetadata",
]


def _parse_publication_date(publication_date: str) -> datetime:
    return datetime.strptime(publication_date, "%a, %d %b %Y %H:%M:%S %Z")


@dataclass(frozen=True, slots=True)
class NewPackageMetadata:
    """Package metadata"""

    title: str
    package_link: str
    guid: str
    description: str | None
    author: str | None
    publication_date: datetime

    @classmethod
    def build_from(cls, data: dict[str, str]) -> "NewPackageMetadata":
        """Build an instance from raw data"""
        publication_date: str | None = data.get("pubDate")
        if publication_date is not None:
            publication_date: datetime = _parse_publication_date(publication_date)

        return cls(
            title=data.get("title").removesuffix(" added to PyPI"),
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

    def __init__(self, http_session: ClientSession | None = None) -> None:
        self.http_session = http_session

        self.__param_session = True
        if not http_session:
            self.http_session = self.__create_session()
        finalize(self, self.__kill)

    def __create_session(self):
        async def create():
            return ClientSession()
        return run(create())

    def __kill(self):
        run(self.http_session.close())

    async def get_new_packages_feed(self) -> list[NewPackageMetadata]:
        """Get the new packages RSS feed"""
        async with self.http_session.get(self.NEWEST_PACKAGES_FEED_URL) as response:
            response_text = await response.text()
            rss_data = xmltodict.parse(response_text)["rss"]["channel"]["item"]
            return [NewPackageMetadata.build_from(package_data) for package_data in rss_data]

    async def get_package_updates_feed(self) -> dict:
        """Get the package updates RSS feed"""
        async with self.http_session.get(self.PACKAGE_UPDATES_FEED_URL) as response:
            response_text = await response.text()
            rss_data = xmltodict.parse(response_text)["rss"]["channel"]["item"]
            return rss_data
