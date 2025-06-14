import pathlib

import click

from .log import log  # global logging setup
from .etl import download, ddl_loader, transform, load, summary


@click.group()
def cli():
    # This is a grouping method
    pass


@cli.command()
@click.option(
    "--data-dir", default="data/raw", show_default=True, help="Data raw directory"
)
def run(data_dir: str):
    ddl_loader.apply_ddl()
    target_raw_path = download.fetch_zip(pathlib.Path(data_dir))

    dataframes = load.load_raw(target_raw_path)
    summary.raw_summary(dataframes)

    target_processed_path = target_raw_path.with_name("processed")
    dataframes = transform.clean(dataframes, target_processed_path)

    load.bulk_insert(dataframes)

    log.info("Pipeline completed ✅")


if __name__ == "__main__":
    cli()
