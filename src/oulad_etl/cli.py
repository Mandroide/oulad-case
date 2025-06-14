import pathlib

import click

from oulad_etl.etl.models import TablesSchema
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

    # Merge
    df_etl = transform.merge(
        df_student_assessment=dataframes[TablesSchema.studentAssessment],
        df_assessments=dataframes[TablesSchema.assessments],
        df_student_info=dataframes[TablesSchema.studentInfo],
    )

    load.save_to_csv(
        df=df_etl, target_file_path=target_processed_path / "etl_output.csv"
    )

    # Encode studentInfo fields as ordinals
    dataframes[TablesSchema.studentInfo] = transform.encode_as_ordinal(
        dataframes[TablesSchema.studentInfo]
    )
    load.save_to_csv(
        df=dataframes[TablesSchema.studentInfo],
        target_file_path=target_processed_path / "studentInfo_ordinal.csv",
    )

    log.info("Pipeline completed ✅")


if __name__ == "__main__":
    cli()
