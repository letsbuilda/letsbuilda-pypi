"""Models for package metadata."""

from dataclasses import dataclass
from typing import Self

from .models_json import URL, JSONPackageMetadata


@dataclass(frozen=True)
class Distribution:
    """Metadata for a distribution."""

    filename: str
    url: str

    @classmethod
    def from_json_api_data(cls: type[Self], data: URL) -> Self:
        """Build an instance from the JSON API data.

        Parameters
        ----------
        data
            The URL of the file hosting the distribution.

        Returns
        -------
        Distribution
            An object representing a distribution.
        """
        return cls(
            filename=data.filename,
            url=data.url,
        )


@dataclass(frozen=True)
class Release:
    """Metadata for a release."""

    version: str
    distributions: list[Distribution]

    @classmethod
    def from_json_api_data(cls: type[Self], data: JSONPackageMetadata) -> Self:
        """
        Build an instance from the JSON API data.

        Parameters
        ----------
        data
            The JSON API metadata for a package release.

        Returns
        -------
        Release
            An object representing a package release.
        """
        return cls(
            version=data.info.version,
            distributions=[Distribution.from_json_api_data(json_api_data) for json_api_data in data.urls],
        )


@dataclass(frozen=True)
class Package:
    """Metadata for a package."""

    title: str
    releases: list[Release]

    @classmethod
    def from_json_api_data(cls: type[Self], data: JSONPackageMetadata) -> Self:
        """
        Build an instance from the JSON API data.

        Parameters
        ----------
        data
            The JSON API metadata for a package.

        Returns
        -------
        Package
            An object representing a package.
        """
        return cls(
            title=data.info.name,
            releases=[Release.from_json_api_data(data)],
        )
