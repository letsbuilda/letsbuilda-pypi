"""The async client."""

from http import HTTPStatus
from typing import Final, Self

import xmltodict
from httpx import AsyncClient

from .exceptions import PackageNotFoundError
from .models import JSONPackageMetadata, Package, RSSPackageMetadata


class PyPIServices:
    """A class for interacting with PyPI."""

    NEWEST_PACKAGES_FEED_URL: Final[str] = "https://pypi.org/rss/packages.xml"
    PACKAGE_UPDATES_FEED_URL: Final[str] = "https://pypi.org/rss/updates.xml"

    def __init__(self: Self, http_client: AsyncClient) -> None:
        self.http_client = http_client

    async def get_rss_feed(self: Self, feed_url: str) -> list[RSSPackageMetadata]:
        """Get the new packages RSS feed.

        Parameters
        ----------
        feed_url
            The URL of the RSS feed.

        Returns
        -------
        list[RSSPackageMetadata]
            The list of new packages.
        """
        response = await self.http_client.get(feed_url)
        rss_data = xmltodict.parse(response.text)["rss"]["channel"]["item"]
        return [RSSPackageMetadata.model_validate(package_data) for package_data in rss_data]

    async def get_package_json_metadata(
        self: Self,
        package_title: str,
        package_version: str | None = None,
    ) -> JSONPackageMetadata:
        """
        Retrieve metadata for a package.

        Raises
        ------
        PackageNotFoundError
            If the package is not found.

        Parameters
        ----------
        package_title
            The title of the package.
        package_version
            The version of the package.

        Returns
        -------
        JSONPackageMetadata
            The metadata for the package.
        """
        if package_version is not None:
            url = f"https://pypi.org/pypi/{package_title}/{package_version}/json"
        else:
            url = f"https://pypi.org/pypi/{package_title}/json"
        response = await self.http_client.get(url)
        if response.status_code == HTTPStatus.NOT_FOUND:
            raise PackageNotFoundError(package_title, package_version)
        return JSONPackageMetadata.model_validate(response.json())

    async def get_package_metadata(
        self: Self,
        package_title: str,
        package_version: str | None = None,
    ) -> Package:
        """Create a `Package` object from its metadata.

        Parameters
        ----------
        package_title
            The title of the package.
        package_version
            The version of the package.

        Returns
        -------
        Package
            The package object.
        """
        return Package.model_validate(
            (await self.get_package_json_metadata(package_title, package_version)).model_dump(),
        )
