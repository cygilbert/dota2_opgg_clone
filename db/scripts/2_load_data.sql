-- LOAD DATA

USE dota2_datawarehouse;

LOAD DATA INFILE '/var/lib/mysql-files/matchs.csv' 
INTO TABLE matchs
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '/var/lib/mysql-files/heroes.csv' 
INTO TABLE heroes
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '/var/lib/mysql-files/matchs_heroes.csv' 
INTO TABLE matchs_heroes
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA INFILE '/var/lib/mysql-files/heroes_roles.csv' 
INTO TABLE heroes_roles
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;