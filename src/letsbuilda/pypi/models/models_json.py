"""Models for JSON responses"""

from dataclasses import dataclass

import pendulum
from pendulum import DateTime


@dataclass(frozen=True, slots=True)
class Vulnerability:
    """Security vulnerability"""

    id: str
    aliases: list[str]
    link: str
    source: str
    withdrawn: DateTime | None
    summary: str
    details: str
    fixed_in: list[str]

    @classmethod
    def from_dict(cls, data: dict) -> "Vulnerability":
        if data["withdrawn"] is not None:
            data["withdrawn"]: DateTime = pendulum.parse(data["withdrawn"])

        return cls(**data)


@dataclass(frozen=True, slots=True)
class Downloads:
    """Release download counts"""

    last_day: int
    last_month: int
    last_week: int

    @classmethod
    def from_dict(cls, data: dict) -> "Downloads":
        return cls(**data)


@dataclass(frozen=True, slots=True)
class Digests:
    """URL file digests"""

    blake2_b_256: str
    md5: str
    sha256: str

    @classmethod
    def from_dict(cls, data: dict) -> "Digests":
        return cls(**data)


@dataclass(frozen=True, slots=True)
class URL:
    """Package release URL"""

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
    upload_time: DateTime
    upload_time_iso_8601: DateTime
    url: str
    yanked: bool
    yanked_reason: None

    @classmethod
    def from_dict(cls, data: dict, package_name: str, package_version: str) -> "URL":
        data["upload_time"]: DateTime = pendulum.parse(data["upload_time"])
        data["upload_time_iso_8601"]: DateTime = pendulum.parse(data["upload_time_iso_8601"])

        return cls(**data)


@dataclass(frozen=True, slots=True)
class Info:
    """Package metadata internal info block"""

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
    def from_dict(cls, data: dict) -> "Info":
        return cls(**data)


@dataclass(frozen=True, slots=True)
class JSONPackageMetadata:
    """Package metadata"""

    info: Info
    last_serial: int
    urls: list[URL]
    vulnerabilities: list["Vulnerability"]

    @classmethod
    def from_dict(cls, data: dict) -> "JSONPackageMetadata":
        info = Info.from_dict(data["info"])
        return cls(
            info=info,
            last_serial=data["last_serial"],
            urls=[URL.from_dict(url_data, info.name, info.version) for url_data in data["urls"]],
            vulnerabilities=[Vulnerability.from_dict(vuln_data) for vuln_data in data["vulnerabilities"]],
        )
