"""Models for RSS responses."""

from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Annotated

from pydantic import BaseModel, Field, model_validator
from pydantic.functional_validators import BeforeValidator

ISODateTime = Annotated[datetime, BeforeValidator(parsedate_to_datetime)]


class RSSPackageMetadata(BaseModel):
    """RSS Package metadata."""

    title: str
    version: str | None = Field(None)
    package_link: str = Field(validation_alias="link")
    guid: str | None = Field(None)
    description: str | None = Field(None)
    author: str | None = Field(None)
    publication_date: ISODateTime = Field(validation_alias="pubDate")

    @model_validator(mode="before")
    @classmethod
    def try_split_title(cls, data: dict) -> dict:  # type: ignore[type-arg]
        """Attempt to split title into package name and version."""
        split_title = data["title"].removesuffix(" added to PyPI").split()
        data["title"] = split_title[0]
        data["version"] = split_title[1] if len(split_title) == 2 else None  # noqa: PLR2004 - is not magic
        return data
