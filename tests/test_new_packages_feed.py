"""Test parsing metadata from the new packages RSS feed"""

from datetime import datetime

from letsbuilda.pypi import PackageMetadata


def test_parse_publication_date() -> None:
    """Confirm publication date gets parsed correctly"""
    data = {
        "title": "test-package added to PyPI",
        "link": "https://pypi.org/project/test-package",
        "guid": "https://pypi.org/project/test-package",
        "description": "a test package",
        "author": "test-author@example.com",
        "pubDate": "Wed, 29 Mar 2023 21:30:05 GMT",
    }
    parsed_data = PackageMetadata.build_from(data)
    assert parsed_data.publication_date == datetime(2023, 3, 29, 21, 30, 5)


def test_author_missing() -> None:
    """Confirm missing author gets set to None"""
    data = {
        "title": "test-package added to PyPI",
        "link": "https://pypi.org/project/test-package",
        "guid": "https://pypi.org/project/test-package",
        "description": "a test package",
        "pubDate": "Wed, 29 Mar 2023 21:30:05 GMT",
    }
    parsed_data = PackageMetadata.build_from(data)
    assert parsed_data.author is None


def test_description_missing() -> None:
    """Confirm missing description gets set to None"""
    data = {
        "title": "test-package added to PyPI",
        "link": "https://pypi.org/project/test-package",
        "guid": "https://pypi.org/project/test-package",
        "author": "test-author@example.com",
        "pubDate": "Wed, 29 Mar 2023 21:30:05 GMT",
    }
    parsed_data = PackageMetadata.build_from(data)
    assert parsed_data.description is None
