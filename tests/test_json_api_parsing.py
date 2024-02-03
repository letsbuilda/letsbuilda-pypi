"""Test parsing metadata from the JSON API."""

from datetime import UTC, datetime

from letsbuilda.pypi import JSONPackageMetadata

JSON_API_DATA = {
    "info": {
        "author": "",
        "author_email": "Bradley Reynolds <bradley.reynolds@darbia.dev>",
        "bugtrack_url": None,
        "classifiers": [],
        "description": "# letsbuilda-pypi\n\nA wrapper for [PyPI's API and RSS feeds](https://warehouse.pypa.io/api-reference/index.html).\n",
        "description_content_type": "text/markdown",
        "docs_url": None,
        "download_url": "",
        "downloads": {"last_day": -1, "last_month": -1, "last_week": -1},
        "home_page": "",
        "keywords": "",
        "license": "MIT",
        "maintainer": "",
        "maintainer_email": "",
        "name": "letsbuilda-pypi",
        "package_url": "https://pypi.org/project/letsbuilda-pypi/",
        "platform": None,
        "project_url": "https://pypi.org/project/letsbuilda-pypi/",
        "project_urls": {
            "documentation": "https://docs.letsbuilda.dev/letsbuilda-pypi/",
            "repository": "https://github.com/letsbuilda/letsbuilda-pypi/",
        },
        "release_url": "https://pypi.org/project/letsbuilda-pypi/4.0.0/",
        "requires_dist": [
            "aiohttp",
            "xmltodict",
            "pendulum",
            "black ; extra == 'dev'",
            "isort ; extra == 'dev'",
            "ruff ; extra == 'dev'",
            "sphinx ; extra == 'docs'",
            "furo ; extra == 'docs'",
            "sphinx-autoapi ; extra == 'docs'",
            "releases ; extra == 'docs'",
            "toml ; extra == 'docs'",
            "pytest ; extra == 'tests'",
        ],
        "requires_python": ">=3.10",
        "summary": "A wrapper for PyPI's API and RSS feed",
        "version": "4.0.0",
        "yanked": False,
        "yanked_reason": None,
    },
    "last_serial": 18988479,
    "urls": [
        {
            "comment_text": "",
            "digests": {
                "blake2b_256": "cb63f897bdaa98710f9cb96ca1391742192975a776dc70a5a7b0acfbab50b20b",
                "md5": "f7b5fd97141a4eae7966002634703002",
                "sha256": "67a5925e5a51f761ad3c28f3abf90d0b0b4270c26efd87f596d42e5706a63798",
            },
            "downloads": -1,
            "filename": "letsbuilda_pypi-4.0.0-py3-none-any.whl",
            "has_sig": False,
            "md5_digest": "f7b5fd97141a4eae7966002634703002",
            "packagetype": "bdist_wheel",
            "python_version": "py3",
            "requires_python": ">=3.10",
            "size": 4772,
            "upload_time": "2023-04-26T02:40:03",
            "upload_time_iso_8601": "2023-04-26T02:40:03.919027Z",
            "url": "https://files.pythonhosted.org/packages/cb/63/f897bdaa98710f9cb96ca1391742192975a776dc70a5a7b0acfbab50b20b/letsbuilda_pypi-4.0.0-py3-none-any.whl",
            "yanked": False,
            "yanked_reason": None,
        },
        {
            "comment_text": "",
            "digests": {
                "blake2b_256": "71a0d9b47f7a17efb1d296d189ae83c5381c80efa0e0984a96cb2f719136797e",
                "md5": "27e181efe8b2f558784439b7878d6600",
                "sha256": "0060a9380a89bf772c84c4f39d89417b6529378c4ce39f3b525b40f83c883287",
            },
            "downloads": -1,
            "filename": "letsbuilda-pypi-4.0.0.tar.gz",
            "has_sig": False,
            "md5_digest": "27e181efe8b2f558784439b7878d6600",
            "packagetype": "sdist",
            "python_version": "source",
            "requires_python": ">=3.10",
            "size": 4567,
            "upload_time": "2023-04-26T02:40:05",
            "upload_time_iso_8601": "2023-04-26T02:40:05.331985Z",
            "url": "https://files.pythonhosted.org/packages/71/a0/d9b47f7a17efb1d296d189ae83c5381c80efa0e0984a96cb2f719136797e/letsbuilda-pypi-4.0.0.tar.gz",
            "yanked": False,
            "yanked_reason": None,
        },
    ],
    "vulnerabilities": [],
}


def test_json_api_data_parsing() -> None:
    """Confirm sample JSON API data gets parsed correctly."""
    model = JSONPackageMetadata.from_dict(JSON_API_DATA)

    assert model.info.name == "letsbuilda-pypi"
    assert model.info.version == "4.0.0"
    assert model.urls[0].upload_time == datetime(2023, 4, 26, 2, 40, 3)  # noqa: DTZ001 -- timezone is naive
    assert model.urls[0].upload_time_iso_8601 == datetime(2023, 4, 26, 2, 40, 3, 919027, tzinfo=UTC)
