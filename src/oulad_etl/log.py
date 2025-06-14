import logging.config
import yaml
import pathlib


def setup_logging() -> None:
    cfg = pathlib.Path(__file__).parent.parent.parent / "config/logging.yml"
    with cfg.open() as f:
        logging.config.dictConfig(yaml.safe_load(f))


setup_logging()
log = logging.getLogger("oulad")
