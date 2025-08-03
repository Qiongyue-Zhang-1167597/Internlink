DROP DATABASE IF EXISTS InternLink;
CREATE DATABASE InternLink;

USE InternLink;

CREATE TABLE IF NOT EXISTS `user` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL,
  `full_name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `password_hash` CHAR(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `profile_image` VARCHAR(255) NULL DEFAULT NULL,
  `role` ENUM('student', 'employer', 'admin') NOT NULL,
  `status` ENUM('active', 'inactive', 'pending') NOT NULL DEFAULT 'active',
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC)
);

CREATE TABLE IF NOT EXISTS `student` (
  `student_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `university` VARCHAR(100) NULL,
  `course` VARCHAR(100) NULL,
  `resume_path` VARCHAR(255) NULL,
  PRIMARY KEY (`student_id`),
  INDEX `fk_student_user_idx` (`user_id` ASC),
  CONSTRAINT `fk_student_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`user_id`)
    ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS `employer` (
  `emp_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `company_name` VARCHAR(100) NOT NULL,
  `company_description` TEXT NULL,
  `website` VARCHAR(100) NULL,
  `logo_path` VARCHAR(255) NULL,
  PRIMARY KEY (`emp_id`),
  INDEX `fk_employer_user_idx` (`user_id` ASC),
  CONSTRAINT `fk_employer_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`user_id`)
    ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE `internship` (
  `internship_id` INT NOT NULL AUTO_INCREMENT,
  `company_id` INT NOT NULL,
  `title` VARCHAR(100) NOT NULL,
  `description` TEXT NOT NULL,
  `location` VARCHAR(100) NULL,
  `duration` VARCHAR(50) NULL,
  `skills_required` TEXT NULL,
  `deadline` DATE NOT NULL,
  `stipend` VARCHAR(50) NULL,
  `number_of_opening` INT NULL,
  `additional_req` TEXT NULL,
  PRIMARY KEY (`internship_id`),
  INDEX `fk_internship_employer_idx` (`company_id` ASC),
  CONSTRAINT `fk_internship_employer`
    FOREIGN KEY (`company_id`)
    REFERENCES `employer` (`emp_id`)
    ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE `application` (
  `application_id` INT NOT NULL AUTO_INCREMENT,
  `student_id` INT NOT NULL,
  `internship_id` INT NOT NULL,
  `status` ENUM('pending', 'viewed', 'shortlisted', 'rejected', 'accepted') NOT NULL DEFAULT 'pending',
  `feedback` TEXT NULL,
  PRIMARY KEY (`application_id`),
  INDEX `fk_application_student_idx` (`student_id` ASC),
  INDEX `fk_application_internship_idx` (`internship_id` ASC),
  CONSTRAINT `fk_application_student`
    FOREIGN KEY (`student_id`)
    REFERENCES `student` (`student_id`)
    ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_application_internship`
    FOREIGN KEY (`internship_id`)
    REFERENCES `internship` (`internship_id`)
    ON DELETE CASCADE ON UPDATE NO ACTION
);

ALTER TABLE `application`
ADD COLUMN `resume_url` VARCHAR(255) NULL AFTER `feedback`,
ADD COLUMN `cover_letter` TEXT NULL AFTER `resume_url`,
ADD COLUMN `application_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP AFTER `cover_letter`;

ALTER TABLE internship
ADD COLUMN category VARCHAR(100) NULL DEFAULT NULL AFTER description;

SELECT 'Database InternLink and all tables created successfully.' AS 'Status';