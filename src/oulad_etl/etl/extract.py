import logging.config
import os
from zipfile import ZipFile, BadZipFile

import pandas as pd
import requests
from pathlib import Path

import yaml

with open("logging_config.yaml", "rt") as f:
    config = yaml.safe_load(f.read())
logging.config.dictConfig(config)

logger = logging.getLogger("extract")


def extract(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def get_project_data_raw() -> Path:
    return Path(__file__).absolute().parent.parent.parent.parent / "data" / "raw"


def download_dataset() -> Path:
    url = "https://analyse.kmi.open.ac.uk/open-dataset/download"
    response = requests.get(url, stream=True)
    logger.info(f"Downloading {response.url}")
    root = get_project_data_raw()
    root.mkdir(parents=True, exist_ok=True)
    ouladzip_raw_path = root / "oulad.zip"

    with open(ouladzip_raw_path, "wb") as f:
        logger.info(f"Writing stream to {ouladzip_raw_path}")
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return ouladzip_raw_path


def unzip_dataset(ouladzip_raw_path: Path) -> None:
    try:
        with ZipFile(ouladzip_raw_path, "r") as zip_ref:
            zip_ref.extractall(ouladzip_raw_path.parent)
        os.remove(ouladzip_raw_path)
        logger.info(f"Successfully unzipped '{ouladzip_raw_path}' and deleted it.")
    except FileNotFoundError:
        logger.error(f"Error: Zip file not found at '{ouladzip_raw_path}'")
    except BadZipFile:
        logger.error(f"Error: '{ouladzip_raw_path}' is not a valid zip file.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
