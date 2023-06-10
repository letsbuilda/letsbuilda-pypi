"""Interactions with parsing package metadata and contents"""

import tarfile
from io import BytesIO
from zipfile import ZipFile

import aiohttp


async def fetch_package_distribution(
    http_session: aiohttp.ClientSession,
    package_source_download_url: str,
) -> BytesIO:
    """Fetch a package distribution from PyPI"""
    buffer = BytesIO()
    async with http_session.get(package_source_download_url) as response:
        buffer.write(await response.content.read())
    buffer.seek(0)
    return buffer


def read_distribution_tarball(buffer: BytesIO) -> dict[str, str]:
    """Return a dictionary mapping filenames to content"""
    files = {}
    with tarfile.open(fileobj=buffer) as file:
        for tarinfo in file:
            if tarinfo.isreg():
                files[tarinfo.name] = file.extractfile(tarinfo).read().decode(encoding="UTF-8", errors="ignore")
    return files


def read_distribution_wheel(buffer: BytesIO) -> dict[str, str]:
    """Return a dictionary mapping filenames to content"""
    files = {}
    with ZipFile(file=buffer) as zip_file:
        for zip_info in zip_file.infolist():
            if not zip_info.is_dir():
                files[zip_info.filename] = zip_file.read(zip_info).decode(encoding="UTF-8", errors="ignore")
    return files
