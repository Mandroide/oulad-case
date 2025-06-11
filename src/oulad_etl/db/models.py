from enum import StrEnum

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class ForeignKeys(StrEnum):
    courses_code_module = "courses.code_module"
    courses_code_presentation = "courses.code_presentation"


class Base(DeclarativeBase):
    pass


class Courses(Base):
    __tablename__ = "courses"
    code_module: Mapped[str] = mapped_column(primary_key=True)
    code_presentation: Mapped[str] = mapped_column(String(5), primary_key=True)
    module_presentation_length: Mapped[int]


class StudentInfo(Base):
    __tablename__ = "studentinfo"
    code_module: Mapped[str] = mapped_column(
        String(3), ForeignKey(ForeignKeys.courses_code_module), primary_key=True
    )
    code_presentation: Mapped[str] = mapped_column(
        String(5), ForeignKey(ForeignKeys.courses_code_presentation), primary_key=True
    )
    id_student: Mapped[int] = mapped_column(primary_key=True)
    gender: Mapped[str]
    region: Mapped[str]
    highest_education: Mapped[str]
    imd_band: Mapped[str]
    age_band: Mapped[str]
    num_of_prev_attemps: Mapped[int]
    studied_credits: Mapped[int]
    disability: Mapped[str]
    final_result: Mapped[str]


class Assessments(Base):
    __tablename__ = "assessments"
    code_module: Mapped[str] = mapped_column(
        String(3), ForeignKey(ForeignKeys.courses_code_module), primary_key=True
    )
    code_presentation: Mapped[str] = mapped_column(
        String(5), ForeignKey(ForeignKeys.courses_code_presentation), primary_key=True
    )
    id_assessment: Mapped[int] = mapped_column(primary_key=True)
    assessment_type: Mapped[str]
    date: Mapped[int]
    weight: Mapped[float]


class Vle(Base):
    __tablename__ = "vle"
    id_site: Mapped[int] = mapped_column(primary_key=True)
    code_module: Mapped[str] = mapped_column(
        String(3), ForeignKey(ForeignKeys.courses_code_module), primary_key=True
    )
    code_presentation: Mapped[str] = mapped_column(
        String(5), ForeignKey(ForeignKeys.courses_code_presentation), primary_key=True
    )
    activity_type: Mapped[str]
    week_from: Mapped[int]
    week_to: Mapped[int]


class StudentAssessment(Base):
    __tablename__ = "studentassessment"
    id_student: Mapped[int] = mapped_column(primary_key=True)
    id_assessment: Mapped[int] = mapped_column(primary_key=True)
    date_submitted: Mapped[int]
    is_banked: Mapped[int]
    score: Mapped[float]


class StudentRegistration(Base):
    __tablename__ = "studentregistration"
    code_module: Mapped[str] = mapped_column(
        String(3), ForeignKey(ForeignKeys.courses_code_module), primary_key=True
    )
    code_presentation: Mapped[str] = mapped_column(
        String(5), ForeignKey(ForeignKeys.courses_code_presentation), primary_key=True
    )
    id_student: Mapped[int] = mapped_column(primary_key=True)
    date_registration: Mapped[int]
    date_unregistration: Mapped[int]


class StudentVle(Base):
    __tablename__ = "studentvle"
    id_site: Mapped[int] = mapped_column(primary_key=True)
    id_student: Mapped[int] = mapped_column(primary_key=True)
    code_module: Mapped[str] = mapped_column(
        String(3), ForeignKey(ForeignKeys.courses_code_module), primary_key=True
    )
    code_presentation: Mapped[str] = mapped_column(
        String(5), ForeignKey(ForeignKeys.courses_code_presentation), primary_key=True
    )
    date: Mapped[int]
    sum_click: Mapped[int]
