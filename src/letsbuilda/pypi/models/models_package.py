"""Models for package metadata."""

from pydantic import BaseModel


class Distribution(BaseModel):
    """Metadata for a distribution."""

    filename: str
    url: str


class Release(BaseModel):
    """Metadata for a release."""

    version: str
    distributions: list[Distribution]


class Package(BaseModel):
    """Metadata for a package."""

    title: str
    releases: list[Release]
