-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS = @@UNIQUE_CHECKS, UNIQUE_CHECKS = 0;
SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS = 0;
SET @OLD_SQL_MODE = @@SQL_MODE, SQL_MODE =
        'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema oulad
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS oulad;

-- -----------------------------------------------------
-- Schema oulad
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS oulad DEFAULT CHARACTER SET utf8;
USE oulad;

-- -----------------------------------------------------
-- Table `oulad`.`courses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `oulad`.`courses`
(
    `code_module`                CHAR(3) NOT NULL,
    `code_presentation`          CHAR(5) NOT NULL,
    `module_presentation_length` INT     NULL,
    PRIMARY KEY (`code_module`, `code_presentation`)
)
    ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `oulad`.`studentInfo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `oulad`.`studentInfo`
(
    `code_module`           CHAR(3)     NOT NULL,
    `code_presentation`     CHAR(5)     NOT NULL,
    `id_student`            INT         NOT NULL,
    `gender`                CHAR        NULL,
    `region`                VARCHAR(45) NULL,
    `highest_education`     VARCHAR(45) NULL,
    `highest_education_ord` TINYINT     NULL,
    `imd_band`              VARCHAR(16) NULL,
    `imd_band_ord`          TINYINT     NULL,
    `age_band`              VARCHAR(16) NULL,
    `age_band_ord`          TINYINT     NULL,
    `num_of_prev_attempts`  INT         NULL,
    `studied_credits`       INT         NULL,
    `disability`            CHAR        NULL,
    `final_result`          VARCHAR(11) NULL,
    `final_result_ord`      TINYINT     NULL,
    PRIMARY KEY (`code_module`, `code_presentation`, `id_student`),
    INDEX `fk_studentInfo_courses_idx` (`code_module` ASC, `code_presentation` ASC) VISIBLE,
    INDEX `ix_student_id` (`id_student` ASC) VISIBLE,
    CONSTRAINT `fk_studentInfo_courses`
        FOREIGN KEY (`code_module`, `code_presentation`)
            REFERENCES `oulad`.`courses` (`code_module`, `code_presentation`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
)
    ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `oulad`.`assessments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `oulad`.`assessments`
(
    `code_module`       CHAR(3)    NOT NULL,
    `code_presentation` CHAR(5)    NOT NULL,
    `id_assessment`     INT        NOT NULL,
    `assessment_type`   VARCHAR(5) NULL,
    `date`              INT        NULL,
    `weight`            FLOAT      NULL,
    PRIMARY KEY (`code_module`, `code_presentation`, `id_assessment`),
    INDEX `fk_assessments_courses1_idx` (`code_module` ASC, `code_presentation` ASC) VISIBLE,
    UNIQUE INDEX `id_assessment_UNIQUE` (`id_assessment` ASC) VISIBLE,
    CONSTRAINT `fk_assessments_courses1`
        FOREIGN KEY (`code_module`, `code_presentation`)
            REFERENCES `oulad`.`courses` (`code_module`, `code_presentation`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
)
    ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `oulad`.`vle`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `oulad`.`vle`
(
    `id_site`           INT         NOT NULL,
    `code_module`       CHAR(3)     NOT NULL,
    `code_presentation` CHAR(5)     NOT NULL,
    `activity_type`     VARCHAR(45) NULL,
    `week_from`         INT         NULL,
    `week_to`           INT         NULL,
    PRIMARY KEY (`id_site`, `code_module`, `code_presentation`),
    INDEX `fk_vle_courses1_idx` (`code_module` ASC, `code_presentation` ASC) VISIBLE,
    CONSTRAINT `fk_vle_courses1`
        FOREIGN KEY (`code_module`, `code_presentation`)
            REFERENCES `oulad`.`courses` (`code_module`, `code_presentation`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
)
    ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `oulad`.`studentAssessment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `oulad`.`studentAssessment`
(
    `id_student`     INT     NOT NULL,
    `id_assessment`  INT     NOT NULL,
    `date_submitted` INT     NULL,
    `is_banked`      TINYINT NOT NULL,
    `score`          FLOAT   NULL,
    PRIMARY KEY (`id_student`, `id_assessment`),
    INDEX `fk_studentAssessment_studentInfo1_idx` (`id_student` ASC) INVISIBLE,
    INDEX `fk_studentAssessment_assessment1_idx` (`id_assessment` ASC) VISIBLE,
    CONSTRAINT `fk_studentAssessment_assessments1`
        FOREIGN KEY (`id_assessment`)
            REFERENCES `oulad`.`assessments` (`id_assessment`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
    CONSTRAINT `fk_studentAssessment_studentInfo1`
        FOREIGN KEY (`id_student`)
            REFERENCES `oulad`.`studentInfo` (`id_student`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
)
    ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `oulad`.`studentRegistration`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `oulad`.`studentRegistration`
(
    `code_module`         CHAR(3) NOT NULL,
    `code_presentation`   CHAR(5) NOT NULL,
    `id_student`          INT     NOT NULL,
    `date_registration`   INT     NULL,
    `date_unregistration` INT     NULL,
    PRIMARY KEY (`code_module`, `code_presentation`, `id_student`),
    INDEX `fk_studentRegistration_studentInfo1_idx` (`id_student` ASC) VISIBLE,
    CONSTRAINT `fk_studentRegistration_courses1`
        FOREIGN KEY (`code_module`, `code_presentation`)
            REFERENCES `oulad`.`courses` (`code_module`, `code_presentation`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
    CONSTRAINT `fk_studentRegistration_studentInfo1`
        FOREIGN KEY (`id_student`)
            REFERENCES `oulad`.`studentInfo` (`id_student`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
)
    ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `oulad`.`studentVle`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `oulad`.`studentVle`
(
    `id_site`           INT     NOT NULL,
    `id_student`        INT     NOT NULL,
    `code_module`       CHAR(3) NOT NULL,
    `code_presentation` CHAR(5) NOT NULL,
    `date`              INT     NULL,
    `sum_click`         INT     NULL,
    PRIMARY KEY (`id_site`, `id_student`, `code_module`, `code_presentation`),
    INDEX `fk_studentVle_studentInfo1_idx` (`code_module` ASC, `code_presentation` ASC, `id_student` ASC) VISIBLE,
    CONSTRAINT `fk_studentVle_vle1`
        FOREIGN KEY (`id_site`)
            REFERENCES `oulad`.`vle` (`id_site`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
    CONSTRAINT `fk_studentVle_studentInfo1`
        FOREIGN KEY (`code_module`, `code_presentation`, `id_student`)
            REFERENCES `oulad`.`studentInfo` (`code_module`, `code_presentation`, `id_student`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
)
    ENGINE = InnoDB;


SET SQL_MODE = @OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS = @OLD_UNIQUE_CHECKS;
