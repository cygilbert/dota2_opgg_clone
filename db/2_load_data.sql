-- LOAD DATA
USE dota2_datawarehouse;
LOAD data INFILE '/var/lib/mysql-files/matchs.csv' INTO TABLE matchs fields TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 rows;
LOAD data INFILE '/var/lib/mysql-files/heroes.csv' INTO TABLE heroes fields TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 rows;
LOAD data INFILE '/var/lib/mysql-files/matchs_heroes.csv' INTO TABLE matchs_heroes fields TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 rows;
LOAD data INFILE '/var/lib/mysql-files/heroes_roles.csv' INTO TABLE heroes_roles fields TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 rows;