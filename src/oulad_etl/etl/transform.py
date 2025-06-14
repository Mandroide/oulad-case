import pathlib

import pandas as pd
from pandas import DataFrame

from oulad_etl.etl.models import (
    CoursesSchema,
    StudentInfo,
    Assessments,
    Vle,
    StudentAssessment,
    StudentRegistration,
    StudentVle,
)
from oulad_etl.log import log


def __clean_common_columns__(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia columnas comunes como 'code_module', 'code_presentation', 'id_student'
    convirtiéndolas a strings y eliminando espacios extra.
    """

    for col in [
        CoursesSchema.code_module,
        CoursesSchema.code_presentation,
        StudentInfo.id_student,
        Assessments.id_assessment,
        Vle.id_site,
    ]:
        if col in df.columns:
            # Convertir a string primero para manejar posibles nulos o tipos mixtos antes de strip
            df[col] = df[col].astype(str).str.strip()
    return df


def clean(
    dataframes: dict[str, pd.DataFrame], target: pathlib.Path
) -> dict[str, DataFrame]:
    log.debug("Limpiando 'assessments'...")
    df_assessments = dataframes["assessments"]
    if Assessments.date in df_assessments.columns:
        df_assessments[Assessments.date] = pd.to_numeric(
            df_assessments[Assessments.date], errors="coerce"
        )
        df_assessments[Assessments.weight] = pd.to_numeric(
            df_assessments[Assessments.weight], errors="coerce"
        )
        df_assessments.dropna(
            subset=[Assessments.date, Assessments.weight], inplace=True
        )
        df_assessments[Assessments.weight] = df_assessments[Assessments.weight].fillna(
            df_assessments[Assessments.weight].mean()
        )
    df_assessments = __clean_common_columns__(df_assessments)
    dataframes["assessments"] = (
        df_assessments  # Actualizar el DataFrame limpio en el diccionario
    )
    log.debug(f"  - 'assessments' limpio. Shape: {df_assessments.shape}")

    # DataFrame: courses
    log.debug("Limpiando 'courses'...")
    df_courses = dataframes["courses"]
    df_courses = __clean_common_columns__(df_courses)
    dataframes["courses"] = df_courses
    log.debug(f"  - 'courses' limpio. Shape: {df_courses.shape}")

    # DataFrame: studentAssessment
    log.debug("Limpiando 'studentAssessment'...")
    df_student_assessment = dataframes["studentAssessment"]
    df_student_assessment[StudentAssessment.score] = pd.to_numeric(
        df_student_assessment[StudentAssessment.score], errors="coerce"
    )
    df_student_assessment[StudentAssessment.score] = df_student_assessment[
        StudentAssessment.score
    ].fillna(0)
    df_student_assessment[StudentAssessment.date_submitted] = pd.to_numeric(
        df_student_assessment[StudentAssessment.date_submitted], errors="coerce"
    )
    df_student_assessment.dropna(
        subset=[StudentAssessment.date_submitted], inplace=True
    )
    df_student_assessment = __clean_common_columns__(df_student_assessment)
    dataframes["studentAssessment"] = df_student_assessment
    log.debug(f"  - 'studentAssessment' limpio. Shape: {df_student_assessment.shape}")

    # DataFrame: studentInfo
    log.debug("Limpiando 'studentInfo'...")
    df_student_info = dataframes["studentInfo"]
    for field in [
        StudentInfo.gender,
        StudentInfo.region,
        StudentInfo.highest_education,
        StudentInfo.imd_band,
        StudentInfo.age_band,
        StudentInfo.disability,
        StudentInfo.final_result,
    ]:
        df_student_info[field] = df_student_info[field].fillna(
            df_student_info[field].mode()[0]
        )

    df_student_info[StudentInfo.num_of_prev_attempts] = df_student_info[
        StudentInfo.num_of_prev_attempts
    ].fillna(df_student_info[StudentInfo.num_of_prev_attempts].median())
    df_student_info[StudentInfo.studied_credits] = df_student_info[
        StudentInfo.studied_credits
    ].fillna(df_student_info[StudentInfo.studied_credits].median())

    df_student_info = __clean_common_columns__(df_student_info)
    dataframes["studentInfo"] = df_student_info
    log.debug(f"  - 'studentInfo' limpio. Shape: {df_student_info.shape}")

    # DataFrame: studentRegistration
    log.debug("Limpiando 'studentRegistration'...")
    df_student_registration = dataframes["studentRegistration"]
    df_student_registration[StudentRegistration.date_registration] = pd.to_numeric(
        df_student_registration[StudentRegistration.date_registration], errors="coerce"
    )
    df_student_registration[StudentRegistration.date_unregistration] = pd.to_numeric(
        df_student_registration[StudentRegistration.date_unregistration],
        errors="coerce",
    )

    df_student_registration[StudentRegistration.date_unregistration] = (
        df_student_registration[StudentRegistration.date_unregistration].fillna(-1)
    )
    df_student_registration.dropna(
        subset=[StudentRegistration.date_registration], inplace=True
    )
    df_student_registration = __clean_common_columns__(df_student_registration)
    dataframes["studentRegistration"] = df_student_registration
    log.debug(
        f"  - 'studentRegistration' limpio. Shape: {df_student_registration.shape}"
    )

    # DataFrame: studentVle
    log.debug("Limpiando 'studentVle'...")
    df_student_vle = dataframes["studentVle"]
    df_student_vle[StudentVle.date] = pd.to_numeric(
        df_student_vle[StudentVle.date], errors="coerce"
    )
    df_student_vle[StudentVle.sum_click] = pd.to_numeric(
        df_student_vle[StudentVle.sum_click], errors="coerce"
    )
    df_student_vle.dropna(subset=[StudentVle.date, StudentVle.sum_click], inplace=True)
    df_student_vle = __clean_common_columns__(df_student_vle)
    dataframes["studentVle"] = df_student_vle
    log.debug(f"  - 'studentVle' limpio. Shape: {df_student_vle.shape}")

    # DataFrame: vle
    log.debug("Limpiando 'vle'...")
    df_vle = dataframes["vle"]
    df_vle[Vle.activity_type] = df_vle[Vle.activity_type].fillna(
        df_vle[Vle.activity_type].mode()[0]
    )
    df_vle[Vle.week_from] = pd.to_numeric(df_vle[Vle.week_from], errors="coerce")
    df_vle[Vle.week_to] = pd.to_numeric(df_vle[Vle.week_to], errors="coerce")
    df_vle[Vle.week_from] = df_vle[Vle.week_from].fillna(-1)
    df_vle[Vle.week_to] = df_vle[Vle.week_to].fillna(-1)
    df_vle = __clean_common_columns__(df_vle)
    dataframes["vle"] = df_vle
    log.debug(f"  - 'vle' limpio. Shape: {df_vle.shape}")

    log.info("Proceso de limpieza de datos completado.")

    # --- 4. Guardar los DataFrames limpios en la nueva carpeta ---
    log.info(f"Guardando los datasets limpios en la carpeta: '{target}'...")
    for df_name, df_cleaned in dataframes.items():
        output_file_path = target / f"{df_name}.csv"
        df_cleaned.to_csv(
            output_file_path, index=False
        )  # index=False para no guardar el índice de pandas
        log.debug(f"  - '{df_name}.csv' guardado.")

    log.info("¡Todos los datasets limpios han sido guardados con éxito!")
    return dataframes
