"""Models for RSS responses."""

from datetime import datetime

from pydantic import BaseModel


class RSSPackageMetadata(BaseModel):
    """RSS Package metadata."""

    title: str
    version: str | None
    package_link: str
    guid: str | None
    description: str | None
    author: str | None
    publication_date: datetime
