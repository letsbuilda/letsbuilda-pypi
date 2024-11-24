"""Models for JSON responses."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class Vulnerability(BaseModel):
    """Security vulnerability."""

    id: str
    aliases: list[str]
    link: str
    source: str
    withdrawn: datetime | None = Field(None)
    summary: str
    details: str
    fixed_in: list[str]


class Downloads(BaseModel):
    """Release download counts."""

    last_day: int
    last_month: int
    last_week: int


class Digests(BaseModel):
    """URL file digests."""

    blake2_b_256: str = Field(validation_alias="blake2b_256")
    md5: str
    sha256: str


class URL(BaseModel):
    """Package release URL."""

    comment_text: str
    digests: Digests
    downloads: int
    filename: str
    has_sig: bool
    md5_digest: str
    packagetype: str
    python_version: str
    requires_python: str | None
    size: int
    upload_time: datetime
    upload_time_iso_8601: datetime
    url: str
    yanked: bool
    yanked_reason: None


class Info(BaseModel):
    """Package metadata internal info block."""

    author: str
    author_email: str
    bugtrack_url: None
    classifiers: list[str]
    description: str
    description_content_type: str
    docs_url: None
    download_url: str
    downloads: Downloads
    home_page: str
    keywords: str
    license: str
    license_expression: str | None
    license_files: list[str] | None
    maintainer: str
    maintainer_email: str
    name: str
    package_url: str
    platform: str | None
    project_url: str
    project_urls: dict[str, str]
    release_url: str
    requires_dist: list[str]
    requires_python: str
    summary: str
    version: str
    yanked: bool
    yanked_reason: str | None
    dynamic: (
        list[
            Literal[
                "Platform",
                "Supported-Platform",
                "Summary",
                "Description",
                "Description-Content-Type",
                "Keywords",
                "Home-page",
                "Download-URL",
                "Author",
                "Author-email",
                "Maintainer",
                "Maintainer-email",
                "License",
                "License-Expression",
                "License-File",
                "Classifier",
                "Requires-Dist",
                "Requires-Python",
                "Requires-External",
                "Project-URL",
                "Provides-Extra",
                "Provides-Dist",
                "Obsoletes-Dist",
            ]
        ]
        | None
    ) = Field(None)
    provides_extra: list[str] | None = Field(None)


class JSONPackageMetadata(BaseModel):
    """Package metadata."""

    info: Info
    last_serial: int
    urls: list[URL]
    vulnerabilities: list[Vulnerability]
