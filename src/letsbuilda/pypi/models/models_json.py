"""Models for JSON responses."""

from datetime import datetime

from pydantic import BaseModel, Field


class Vulnerability(BaseModel):
    """Security vulnerability."""

    id: str | None = None
    aliases: list[str] | None = None
    link: str | None = None
    source: str | None = None
    withdrawn: datetime | None = None
    summary: str | None = None
    details: str | None = None
    fixed_in: list[str] | None = None


class Downloads(BaseModel):
    """Release download counts."""

    last_day: int | None = None
    last_month: int | None = None
    last_week: int | None = None


class Digests(BaseModel):
    """URL file digests."""

    blake2_b_256: str | None = Field(None, validation_alias="blake2b_256")
    md5: str | None = None
    sha256: str | None = None


class URL(BaseModel):
    """Package release URL."""

    comment_text: str | None = None
    digests: Digests | None = None
    downloads: int | None = None
    filename: str | None = None
    has_sig: bool | None = None
    md5_digest: str | None = None
    packagetype: str | None = None
    python_version: str | None = None
    requires_python: str | None = None
    size: int | None = None
    upload_time: datetime | None = None
    upload_time_iso_8601: datetime | None = None
    url: str | None = None
    yanked: bool | None = None
    yanked_reason: str | None = None


class Info(BaseModel):
    """Package metadata internal info block."""

    author: str | None = None
    author_email: str | None = None
    bugtrack_url: str | None = None
    classifiers: list[str] | None = None
    description: str | None = None
    description_content_type: str | None = None
    docs_url: str | None = None
    download_url: str | None = None
    downloads: Downloads | None = None
    home_page: str | None = None
    keywords: str | None = None
    license: str | None = None
    license_expression: str | None = None
    license_files: list[str] | None = None
    maintainer: str | None = None
    maintainer_email: str | None = None
    name: str | None = None
    package_url: str | None = None
    platform: str | None = None
    project_url: str | None = None
    project_urls: dict[str, str] | None = None
    release_url: str | None = None
    requires_dist: list[str] | None = None
    requires_python: str | None = None
    summary: str | None = None
    version: str | None = None
    yanked: bool | None = None
    yanked_reason: str | None = None
    dynamic: list[str] | None = None
    provides_extra: list[str] | None = None


class JSONPackageMetadata(BaseModel):
    """Package metadata."""

    info: Info | None = None
    last_serial: int | None = None
    urls: list[URL] | None = None
    vulnerabilities: list[Vulnerability] | None = None
