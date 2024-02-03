"""Models for JSON responses."""

from dataclasses import dataclass
from datetime import datetime
from typing import Self


@dataclass(frozen=True)
class Vulnerability:
    """Security vulnerability."""

    id: str
    aliases: list[str]
    link: str
    source: str
    withdrawn: datetime | None
    summary: str
    details: str
    fixed_in: list[str]

    @classmethod
    def from_dict(cls: type[Self], data: dict) -> Self:  # type: ignore[type-arg]
        """Build an instance from a dictionary."""
        if data["withdrawn"] is not None:
            data["withdrawn"] = datetime.fromisoformat(data["withdrawn"])

        return cls(**data)


@dataclass(frozen=True)
class Downloads:
    """Release download counts."""

    last_day: int
    last_month: int
    last_week: int

    @classmethod
    def from_dict(cls: type[Self], data: dict) -> Self:  # type: ignore[type-arg]
        """Build an instance from a dictionary."""
        return cls(**data)


@dataclass(frozen=True)
class Digests:
    """URL file digests."""

    blake2_b_256: str
    md5: str
    sha256: str

    @classmethod
    def from_dict(cls: type[Self], data: dict) -> Self:  # type: ignore[type-arg]
        """Build an instance from a dictionary."""
        return cls(**data)


@dataclass(frozen=True)
class URL:
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

    @classmethod
    def from_dict(cls: type[Self], data: dict) -> Self:  # type: ignore[type-arg]
        """Build an instance from a dictionary."""
        data["upload_time"] = datetime.fromisoformat(data["upload_time"])
        data["upload_time_iso_8601"] = datetime.fromisoformat(data["upload_time_iso_8601"])

        return cls(**data)


@dataclass(frozen=True)
class Info:
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

    @classmethod
    def from_dict(cls: type[Self], data: dict) -> Self:  # type: ignore[type-arg]
        """Build an instance from a dictionary."""
        return cls(**data)


@dataclass(frozen=True)
class JSONPackageMetadata:
    """Package metadata."""

    info: Info
    last_serial: int
    urls: list[URL]
    vulnerabilities: list[Vulnerability]

    @classmethod
    def from_dict(cls: type[Self], data: dict) -> Self:  # type: ignore[type-arg]
        """Build an instance from a dictionary."""
        info = Info.from_dict(data["info"])
        return cls(
            info=info,
            last_serial=data["last_serial"],
            urls=[URL.from_dict(url_data) for url_data in data["urls"]],
            vulnerabilities=[Vulnerability.from_dict(vuln_data) for vuln_data in data["vulnerabilities"]],
        )
