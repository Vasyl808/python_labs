-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema pp
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema pp
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `pp` DEFAULT CHARACTER SET utf8 ;
USE `pp` ;

-- -----------------------------------------------------
-- Table `pp`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pp`.`User` (
  `id_user` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NOT NULL,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `age` INT NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `phone_number` VARCHAR(20) NOT NULL,
  `userstatus` ENUM('user', 'pharmacist') NOT NULL,
  PRIMARY KEY (`id_user`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pp`.`Order`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pp`.`Order` (
  `id_order` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `address` VARCHAR(350) NOT NULL,
  `date_of_purchase` DATETIME NOT NULL,
  `shipData` DATETIME NOT NULL,
  `order_status` ENUM('placed', 'approved', 'delivered') NOT NULL,
  `complete` TINYINT NOT NULL,
  PRIMARY KEY (`id_order`),
  INDEX `fk_Order_User_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_Order_User`
    FOREIGN KEY (`user_id`)
    REFERENCES `pp`.`User` (`id_user`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pp`.`Category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pp`.`Category` (
  `id_category` INT NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(255) NOT NULL,
  `description` VARCHAR(300) NOT NULL,
  PRIMARY KEY (`id_category`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pp`.`Medicine`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pp`.`Medicine` (
  `id_medicine` INT NOT NULL AUTO_INCREMENT,
  `medicine_name` VARCHAR(65) NOT NULL,
  `manufacturer` VARCHAR(65) NOT NULL,
  `medicine_description` VARCHAR(255) NOT NULL,
  `category_id` INT NOT NULL,
  `price` INT NOT NULL,
  `medicine_status` ENUM('available', 'pending', 'sold') NOT NULL,
  `demand` TINYINT NOT NULL,
  PRIMARY KEY (`id_medicine`),
  INDEX `fk_Medicine_Category1_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `fk_Medicine_Category1`
    FOREIGN KEY (`category_id`)
    REFERENCES `pp`.`Category` (`id_category`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pp`.`Order_details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pp`.`Order_details` (
  `order_id` INT NOT NULL,
  `medicine_id` INT NOT NULL,
  `count` INT NOT NULL,
  INDEX `fk_Order_details_Order1_idx` (`order_id` ASC) VISIBLE,
  INDEX `fk_Order_details_Medicine1_idx` (`medicine_id` ASC) VISIBLE,
  CONSTRAINT `fk_Order_details_Order1`
    FOREIGN KEY (`order_id`)
    REFERENCES `pp`.`Order` (`id_order`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Order_details_Medicine1`
    FOREIGN KEY (`medicine_id`)
    REFERENCES `pp`.`Medicine` (`id_medicine`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;