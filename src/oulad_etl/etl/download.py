import requests
import zipfile
import io
import pathlib
import logging

URL = "https://analyse.kmi.open.ac.uk/open-dataset/download"


def fetch_zip(target: pathlib.Path) -> pathlib.Path:
    log = logging.getLogger(__name__)
    log.info("Downloading OULAD dataset …")
    resp = requests.get(URL, timeout=60)
    resp.raise_for_status()
    z = zipfile.ZipFile(io.BytesIO(resp.content))
    z.extractall(target)
    log.info("✓ downloaded & extracted to %s", target)
    return target
