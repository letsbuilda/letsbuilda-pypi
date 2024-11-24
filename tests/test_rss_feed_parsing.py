"""Test parsing metadata from the RSS feeds."""

from datetime import UTC, datetime
from typing import Final

from letsbuilda.pypi import RSSPackageMetadata

NEW_PACKAGE_DATA: Final[dict[str, str]] = {
    "title": "test-package added to PyPI",
    "link": "https://pypi.org/project/test-package",
    "guid": "https://pypi.org/project/test-package",
    "pubDate": "Wed, 29 Mar 2023 21:30:05 GMT",
}

UPDATED_PACKAGE_DATA: Final[dict[str, str]] = {
    "title": "test-package 1.0.0",
    "link": "https://pypi.org/project/test-package/1.0.0",
    "author": "test-author@example.com",
    "pubDate": "Wed, 29 Mar 2023 21:30:05 GMT",
}


def test_parsing_new_package_data() -> None:
    """Confirm sample new package data gets parsed correctly."""
    parsed_data = RSSPackageMetadata.model_validate(NEW_PACKAGE_DATA)
    assert parsed_data.publication_date == datetime(2023, 3, 29, 21, 30, 5, tzinfo=UTC)
    assert parsed_data.author is None
    assert parsed_data.description is None
    assert parsed_data.version is None


def test_parsing_updated_package_data() -> None:
    """Confirm sample updated package data gets parsed correctly."""
    parsed_data = RSSPackageMetadata.model_validate(UPDATED_PACKAGE_DATA)
    assert parsed_data.version == "1.0.0"
