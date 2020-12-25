-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

CREATE SCHEMA IF NOT EXISTS `konnect_me` ;
USE `konnect_me` ;

-- -----------------------------------------------------
-- Table `mydb`.`Page`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `page` (
  `email` VARCHAR(50) NOT NULL PRIMARY KEY,
  `password` VARCHAR(45),
  `businessId` INT,
  `companyType` VARCHAR(100),
  `title` VARCHAR(45),
  `aboutYou` VARCHAR(1000),
  `city` VARCHAR(45),
  `state` VARCHAR(45),
  `numFollowers` INT);

-- -----------------------------------------------------
-- Table `mydb`.`regular_profile`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `regular_profile` (
  `email` VARCHAR(50) NOT NULL PRIMARY KEY,
  `password` VARCHAR(45),
  `firstName` VARCHAR(45),
  `lastName` VARCHAR(45),
  `gender` VARCHAR(1),
  `dob` DATE,
  `about_you` VARCHAR(1000),
  `work_profile` VARCHAR(500),
  `city` VARCHAR(45),
  `state` VARCHAR(45),
  `p_grad` VARCHAR(250),
  `u_grad` VARCHAR(250),
  `high_school` VARCHAR(250),
  `Further_education` VARCHAR(250),
  `num_followers` INT);

-- -----------------------------------------------------
-- Table `mydb`.`Album`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `album` (
  `album_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `page_email` VARCHAR(50),
  `regular_profile_email` VARCHAR(50),
  `album_col` VARCHAR(45),
  `name` VARCHAR(100),
  `num_photos` INT,
  CONSTRAINT `fk_page_album`
    FOREIGN KEY (`page_email`)
    REFERENCES `page` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_regular_profile_album`
    FOREIGN KEY (`regular_profile_email`)
    REFERENCES `regular_profile` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table `mydb`.`Photos`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `photos` (
  `update_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `status_id` INT NOT NULL,
  `album_id` INT NOT NULL,
  `page_email` VARCHAR(50),
  `regular_profile_email` VARCHAR(50),
  `caption` VARCHAR(500),
  `date` DATETIME,
  `num_likes` INT,
  `num_lhares` INT,
  `location` VARCHAR(100),
  CONSTRAINT `fk_page_photo`
    FOREIGN KEY (`page_email`)
    REFERENCES `page` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_regular_profile_photo`
    FOREIGN KEY (`regular_profile_email`)
    REFERENCES `regular_profile` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_album`
    FOREIGN KEY (`album_id`)
    REFERENCES `album` (`album_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table `mydb`.`Job`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `job` (
  `job_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `page_email` VARCHAR(50) NOT NULL,
  `type` VARCHAR(50),
  `qualification` VARCHAR(200),
  `num_posts` INT,
  `num_hours` INT,
  `salary` VARCHAR(100),
  `description` VARCHAR(300),  
  `contact_detail` VARCHAR(200),
  CONSTRAINT `fk_page_job`
    FOREIGN KEY (`page_email`)
    REFERENCES `page` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table `mydb`.`Status`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `Status` (
  `update_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `status_id` INT NOT NULL,
  `regular_profile_email` VARCHAR(50),
  `page_email` VARCHAR(50),
  `caption` VARCHAR(500),
  `date` DATETIME,
  `num_shares` INT,
  `num_likes` INT,
  `location` VARCHAR(45),
  CONSTRAINT `fk_regular_profile_status`
    FOREIGN KEY (`regular_profile_email`)
    REFERENCES `regular_profile` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_page_status`
    FOREIGN KEY (`page_email`)
    REFERENCES `page` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table `mydb`.`applies_for`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `applies_for` (
  `job_id` INT NOT NULL,
  `regular_profile_email` VARCHAR(50) NOT NULL,
  PRIMARY KEY(`job_id`,`regular_profile_email`),
  CONSTRAINT `fk_applies_for_job`
    FOREIGN KEY (`job_id`)
    REFERENCES `job` (`job_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk__applies_for_regular_profile`
    FOREIGN KEY (`regular_profile_email`)
    REFERENCES `regular_profile` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table `mydb`.`profile_follows_page`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `profile_follows_page` (
  `page_email` VARCHAR(50) NOT NULL ,
  `regular_profile_email` VARCHAR(50) NOT NULL ,
  PRIMARY KEY(`page_email`,`regular_profile_email`),
  CONSTRAINT `fk_profile_follow_page_page`
    FOREIGN KEY (`page_email`)
    REFERENCES `page` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_profile_follow_page_regular_profile`
    FOREIGN KEY (`regular_profile_email`)
    REFERENCES `regular_profile` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table `mydb`.`profile_follows_profile`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `profile_follows_profile` (
  `follower_email` VARCHAR(50) NOT NULL,
  `followed_profile_email` VARCHAR(50) NOT NULL,
  PRIMARY KEY(`follower_email`,`followed_profile_email`),
  CONSTRAINT `fk_profile_follow_profile_follower`
    FOREIGN KEY (`follower_email`)
    REFERENCES `regular_profile` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_profile_follow_profile_followed`
    FOREIGN KEY (`followed_profile_email`)
    REFERENCES `regular_profile` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table `mydb`.`page_follows_page`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `page_follows_page` (
  `follower_email` VARCHAR(50) NOT NULL ,
  `followed_page_email` VARCHAR(50) NOT NULL ,
  PRIMARY KEY(`follower_email`,`followed_page_email`),
  CONSTRAINT `fk_page_follow_page_follower`
    FOREIGN KEY (`follower_email`)
    REFERENCES `page` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_page_follow_page_followed`
    FOREIGN KEY (`followed_page_email`)
    REFERENCES `page` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);
    
    -- -----------------------------------------------------
-- Table `mydb`.`page_follows_profile`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `page_follows_profile` (
  `follower_page_email` VARCHAR(50) NOT NULL ,
  `followed_profile_email` VARCHAR(50) NOT NULL ,
  PRIMARY KEY(`follower_page_email`,`followed_profile_email`),
  CONSTRAINT `fk_page_follow_profile_follower`
    FOREIGN KEY (`follower_page_email`)
    REFERENCES `page` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_page_follow_profile_followed`
    FOREIGN KEY (`followed_profile_email`)
    REFERENCES `regular_profile` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `mydb`.`profile_shares_status`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `profile_shares_status` (
  `update_id` INT NOT NULL ,
  `regular_profile_email` VARCHAR(50) NOT NULL ,
  `share_id` INT NOT NULL ,
  PRIMARY KEY(`update_id`,`regular_profile_email`,`share_id`),
  CONSTRAINT `fk_profile_share_status_regular_profile`
    FOREIGN KEY (`regular_profile_email`)
    REFERENCES `regular_profile` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_profile_share_status_update`
    FOREIGN KEY (`update_id`)
    REFERENCES `status` (`update_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);
-- -----------------------------------------------------
-- Table `mydb`.`profile_shares_photos`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `profile_shares_photos` (
  `update_id` INT NOT NULL ,
  `regular_profile_email` VARCHAR(50) NOT NULL ,
  `share_id` INT NOT NULL ,
  PRIMARY KEY(`update_id`,`regular_profile_email`,`share_id`),
  CONSTRAINT `fk_profile_shares_photo_regular_profile`
    FOREIGN KEY (`regular_profile_email`)
    REFERENCES `regular_profile` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_profile_shares_photo_update`
    FOREIGN KEY (`update_Id`)
    REFERENCES `photos` (`update_Id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table `mydb`.`profile_likes_photos`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `profile_likes_photos` (
  `update_id` INT NOT NULL ,
  `regular_profile_email` VARCHAR(50) NOT NULL ,
  `photo_like_id` INT NOT NULL ,
  PRIMARY KEY(`update_id`,`regular_profile_email`,`photo_like_id`),
  CONSTRAINT `fk_profile_likes_photo_regular_profile`
    FOREIGN KEY (`regular_profile_email`)
    REFERENCES `regular_profile` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_profile_likes_photo_update`
    FOREIGN KEY (`update_id`)
    REFERENCES `photos` (`update_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table `mydb`.`page_likes_photos`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `page_likes_photos` (
  `update_id` INT NOT NULL ,
  `page_email` VARCHAR(50) NOT NULL ,
  `photo_like_id` INT NOT NULL ,
  PRIMARY KEY(`update_id`,`page_email`,`photo_like_id`),
  CONSTRAINT `fk_page_likes_photo_page`
    FOREIGN KEY (`page_email`)
    REFERENCES `page` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_page_likes_photo_update`
    FOREIGN KEY (`update_id`)
    REFERENCES `photos` (`update_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table `mydb`.`profile_likes_Status`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `profile_likes_Status` (
  `update_id` INT NOT NULL ,
  `regular_profile_email` VARCHAR(50) NOT NULL ,
  `status_like_id` INT NOT NULL ,
  PRIMARY KEY(`update_id`,`regular_profile_email`,`status_like_id`),
  CONSTRAINT `fk_profile_likes_status_regular_profile`
    FOREIGN KEY (`regular_profile_email`)
    REFERENCES `regular_profile` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_profile_likes_status_update`
    FOREIGN KEY (`update_id`)
    REFERENCES `status` (`update_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table `mydb`.`page_likes_status`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `page_likes_status` (
  `update_id` INT NOT NULL ,
  `page_email` VARCHAR(50) NOT NULL ,
  `status_like_id` INT NOT NULL ,
  PRIMARY KEY(`update_id`,`page_email`,`status_like_id`),
  CONSTRAINT `fk_page_likes_status_page`
    FOREIGN KEY (`page_email`)
    REFERENCES `page` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_page_likes_status_update`
    FOREIGN KEY (`update_id`)
    REFERENCES `photos` (`update_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table `mydb`.`Skills`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `skills` (
  `email` VARCHAR(50) NOT NULL ,
  `skill` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`email`,`skill`),
  CONSTRAINT `fk_skills_regular_profile`
    FOREIGN KEY (`email`)
    REFERENCES `regular_profile` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table `mydb`.`interests`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `interests` (
  `email` VARCHAR(50) NOT NULL ,
  `interest` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`email`,`interest`),
  CONSTRAINT `fk_interests_regular_profile`
    FOREIGN KEY (`email`)
    REFERENCES `regular_profile` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

SET FOREIGN_KEY_CHECKS=0

    
    
    
    
    
  
  
  