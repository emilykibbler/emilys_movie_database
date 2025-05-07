-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema movie_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema movie_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `movie_db` DEFAULT CHARACTER SET utf8 ;
USE `movie_db` ;

-- -----------------------------------------------------
-- Table `movie_db`.`actors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie_db`.`actors` (
  `nconst` VARCHAR(45) NOT NULL,
  `primaryName` VARCHAR(255) NULL,
  `birthYear` INT NULL,
  `deathYear` INT NULL,
  PRIMARY KEY (`nconst`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `movie_db`.`titles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie_db`.`titles` (
  `tconst` VARCHAR(45) NOT NULL,
  `titleType` VARCHAR(255) NULL,
  `primaryTitle` VARCHAR(500) NULL,
  `originalTitle` VARCHAR(500) NULL,
  `isAdult` VARCHAR(45) NULL,
  `startYear` INT NULL,
  `endYear` INT NULL,
  `runtimeMinutes` INT NULL,
  PRIMARY KEY (`tconst`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `movie_db`.`knownFor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie_db`.`knownFor` (
  `nconst` VARCHAR(45) NOT NULL,
  `tconst` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`nconst`, `tconst`),
  INDEX `fk_knownFor_actors_idx` (`nconst` ASC) VISIBLE,
  INDEX `fk_knownFor_titles1_idx` (`tconst` ASC) VISIBLE,
  CONSTRAINT `fk_knownFor_actors`
    FOREIGN KEY (`nconst`)
    REFERENCES `movie_db`.`actors` (`nconst`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_knownFor_titles1`
    FOREIGN KEY (`tconst`)
    REFERENCES `movie_db`.`titles` (`tconst`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;



-- -----------------------------------------------------
-- Table `movie_db`.`genres`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie_db`.`genres` (
  `genreName` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`genreName`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `movie_db`.`professions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie_db`.`professions` (
  `professionName` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`professionName`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `movie_db`.`titles_has_genres`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie_db`.`titles_has_genres` (
  `tconst` VARCHAR(45) NOT NULL,
  `genreName` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`tconst`, `genreName`),
  INDEX `fk_titles_has_genres_genres1_idx` (`genreName` ASC) VISIBLE,
  INDEX `fk_titles_has_genres_titles1_idx` (`tconst` ASC) VISIBLE,
  CONSTRAINT `fk_titles_has_genres_titles1`
    FOREIGN KEY (`tconst`)
    REFERENCES `movie_db`.`titles` (`tconst`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_titles_has_genres_genres1`
    FOREIGN KEY (`genreName`)
    REFERENCES `movie_db`.`genres` (`genreName`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `movie_db`.`actors_has_professions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie_db`.`actors_has_professions` (
  `nconst` VARCHAR(45) NOT NULL,
  `professionName` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`nconst`, `professionName`),
  INDEX `fk_actors_has_professions_professions1_idx` (`professionName` ASC) VISIBLE,
  INDEX `fk_actors_has_professions_actors1_idx` (`nconst` ASC) VISIBLE,
  CONSTRAINT `fk_actors_has_professions_actors1`
    FOREIGN KEY (`nconst`)
    REFERENCES `movie_db`.`actors` (`nconst`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_actors_has_professions_professions1`
    FOREIGN KEY (`professionName`)
    REFERENCES `movie_db`.`professions` (`professionName`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

# Some manual test data entered

INSERT INTO `actors`
  (`nconst`, `primaryName`, `birthYear`) 
  VALUES ('nm0000003','Brigitte Bardot','1934');

INSERT INTO `actors`
(`nconst`, `primaryName`, `birthYear`, `deathYear`) 
VALUES ('nm0000001','Fred Astaire','1899','1987');

alter table `titles` modify `isAdult` int;

INSERT INTO `titles`(
`tconst`, 
`titleType`, 
`primaryTitle`, 
`originalTitle`, 
`isAdult`, 
`startYear`, 
`runtimeMinutes`) VALUES (
"tt0027125",
"movie",
"Top Hat",
"Top Hat",
0,
1935,
101);

INSERT INTO `titles`(
`tconst`, 
`titleType`, 
`primaryTitle`, 
`originalTitle`, 
`isAdult`, 
`startYear`,  
`runtimeMinutes`) VALUES (
"tt0050419",
"movie",
"Funny Face",
"Funny Face",
0,
1957,
103);

# I wrote these queries with string manipulation in R

insert into genres (genreName) values ("Documentary");
insert into genres (genreName) values ("Short");
insert into genres (genreName) values ("Animation");
insert into genres (genreName) values ("Comedy");
insert into genres (genreName) values ("Romance");
insert into genres (genreName) values ("Sport");
insert into genres (genreName) values ("News");
insert into genres (genreName) values ("Drama");
insert into genres (genreName) values ("Fantasy");
insert into genres (genreName) values ("Horror");
insert into genres (genreName) values ("Biography");
insert into genres (genreName) values ("Music");
insert into genres (genreName) values ("War");
insert into genres (genreName) values ("Crime");
insert into genres (genreName) values ("Western");
insert into genres (genreName) values ("Family");
insert into genres (genreName) values ("Adventure");
insert into genres (genreName) values ("Action");
insert into genres (genreName) values ("History");
insert into genres (genreName) values ("Mystery");
insert into genres (genreName) values ("Sci-Fi");
insert into genres (genreName) values ("Musical");
insert into genres (genreName) values ("Thriller");
insert into genres (genreName) values ("Film-Noir");
insert into genres (genreName) values ("Talk-Show");
insert into genres (genreName) values ("Game-Show");
insert into genres (genreName) values ("Reality-TV");
insert into genres (genreName) values ("Adult");

insert into professions (professionName) values ("actor");
insert into professions (professionName) values ("miscellaneous");
insert into professions (professionName) values ("producer");
insert into professions (professionName) values ("actress");
insert into professions (professionName) values ("soundtrack");
insert into professions (professionName) values ("archive_footage");
insert into professions (professionName) values ("music_department");
insert into professions (professionName) values ("writer");
insert into professions (professionName) values ("director");
insert into professions (professionName) values ("stunts");
insert into professions (professionName) values ("make_up_department");
insert into professions (professionName) values ("composer");
insert into professions (professionName) values ("assistant_director");
insert into professions (professionName) values ("camera_department");
insert into professions (professionName) values ("talent_agent");
insert into professions (professionName) values ("archive_sound");
insert into professions (professionName) values ("art_department");
insert into professions (professionName) values ("executive");
insert into professions (professionName) values ("editor");
insert into professions (professionName) values ("animation_department");
insert into professions (professionName) values ("script_department");
insert into professions (professionName) values ("costume_department");
insert into professions (professionName) values ("cinematographer");
insert into professions (professionName) values ("music_artist");
insert into professions (professionName) values ("production_designer");
insert into professions (professionName) values ("special_effects");
insert into professions (professionName) values ("production_manager");
insert into professions (professionName) values ("editorial_department");
insert into professions (professionName) values ("art_director");
insert into professions (professionName) values ("sound_department");
insert into professions (professionName) values ("casting_department");
insert into professions (professionName) values ("costume_designer");
insert into professions (professionName) values ("visual_effects");
insert into professions (professionName) values ("set_decorator");
insert into professions (professionName) values ("location_management");
insert into professions (professionName) values ("casting_director");
insert into professions (professionName) values ("transportation_department");
insert into professions (professionName) values ("manager");
insert into professions (professionName) values ("publicist");
insert into professions (professionName) values ("podcaster");
insert into professions (professionName) values ("legal");
insert into professions (professionName) values ("assistant");
insert into professions (professionName) values ("production_department");
insert into professions (professionName) values ("choreographer");
insert into professions (professionName) values ("electrical_department");
insert into professions (professionName) values ("accountant");

INSERT INTO `actors`
(`nconst`, `primaryName`, `birthYear`, `deathYear`) 
VALUES ('nm0000002','Lauren Bacall','1924','2014');


insert into actor_has_professions (nconst, professionName) values ("nm0000001", "actor");
insert into actor_has_professions (nconst, professionName) values ("nm0000001", "miscellaneous");
insert into actor_has_professions (nconst, professionName) values ("nm0000001", "producer");
insert into actor_has_professions (nconst, professionName) values ("nm0000002", "actress");
insert into actor_has_professions (nconst, professionName) values ("nm0000002", "soundtrack");
insert into actor_has_professions (nconst, professionName) values ("nm0000002", "archive_footage");
insert into actor_has_professions (nconst, professionName) values ("nm0000003", "actress");
insert into actor_has_professions (nconst, professionName) values ("nm0000003", "music_department");
insert into actor_has_professions (nconst, professionName) values ("nm0000003", "producer");

ALTER TABLE actors_has_professions
RENAME TO actor_has_professions;

ALTER TABLE titles_has_genres
RENAME TO title_has_genres;

insert into title_has_genres (tconst, genreName) values ("tt0027125", "Comedy");
insert into title_has_genres (tconst, genreName) values ("tt0027125", "Musical");
insert into title_has_genres (tconst, genreName) values ("tt0027125", "Romance");
insert into title_has_genres (tconst, genreName) values ("tt0049189", "Drama");
insert into title_has_genres (tconst, genreName) values ("tt0049189", "Romance");
insert into title_has_genres (tconst, genreName) values ("tt0050419", "Comedy");
insert into title_has_genres (tconst, genreName) values ("tt0050419", "Musical");
insert into title_has_genres (tconst, genreName) values ("tt0050419", "Romance");
insert into title_has_genres (tconst, genreName) values ("tt0053137", "Drama");
insert into title_has_genres (tconst, genreName) values ("tt0053137", "Romance");
insert into title_has_genres (tconst, genreName) values ("tt0053137", "Sci-Fi");
insert into title_has_genres (tconst, genreName) values ("tt0054452", "Drama");
insert into title_has_genres (tconst, genreName) values ("tt0056404", "Drama");
insert into title_has_genres (tconst, genreName) values ("tt0056404", "Romance");
insert into title_has_genres (tconst, genreName) values ("tt0057345", "Drama");
insert into title_has_genres (tconst, genreName) values ("tt0057345", "Romance");
insert into title_has_genres (tconst, genreName) values ("tt0072308", "Action");
insert into title_has_genres (tconst, genreName) values ("tt0072308", "Drama");
insert into title_has_genres (tconst, genreName) values ("tt0072308", "Thriller");


insert into titles (tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, runtimeMinutes) values (
  "tt0049189", "movie", "...And God Created Woman", "Et Dieu... cr√©a la femme", 0, 1956, 90);
insert into titles (tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, runtimeMinutes) values (
  "tt0053137", "movie", "On the Beach", "On the Beach", 0, 1959, 134);
insert into titles (tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, runtimeMinutes) values (
  "tt0054452", "movie", "The Truth", "La v√©rit√©", 0, 1960, 127);
insert into titles (tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, runtimeMinutes) values (
  "tt0056404", "movie", "Love on a Pillow", "Le repos du guerrier", 0, 1962, 102);
insert into titles (tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, runtimeMinutes) values (
  "tt0057345", "movie", "Contempt", "Le m√©pris", 0, 1963, 102);
insert into titles (tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, runtimeMinutes) values (
  "tt0072308", "movie", "The Towering Inferno", "The Towering Inferno", 0, 1974, 165);


insert into title_has_genres (tconst, genreName) values ("tt0049189", "Drama");
insert into title_has_genres (tconst, genreName) values ("tt0049189", "Romance");
insert into title_has_genres (tconst, genreName) values ("tt0050419", "Comedy");
insert into title_has_genres (tconst, genreName) values ("tt0050419", "Musical");
insert into title_has_genres (tconst, genreName) values ("tt0050419", "Romance");
insert into title_has_genres (tconst, genreName) values ("tt0053137", "Drama");
insert into title_has_genres (tconst, genreName) values ("tt0053137", "Romance");
insert into title_has_genres (tconst, genreName) values ("tt0053137", "Sci-Fi");
insert into title_has_genres (tconst, genreName) values ("tt0054452", "Drama");
insert into title_has_genres (tconst, genreName) values ("tt0056404", "Drama");
insert into title_has_genres (tconst, genreName) values ("tt0056404", "Romance");
insert into title_has_genres (tconst, genreName) values ("tt0057345", "Drama");
insert into title_has_genres (tconst, genreName) values ("tt0057345", "Romance");
insert into title_has_genres (tconst, genreName) values ("tt0072308", "Action");
insert into title_has_genres (tconst, genreName) values ("tt0072308", "Drama");
insert into title_has_genres (tconst, genreName) values ("tt0072308", "Thriller");

# The rest of the data was added using Python
