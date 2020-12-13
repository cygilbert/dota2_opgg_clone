-- BUILD DATABASE
-- SET GLOBAL max_allowed_packet = 10 * 1024 * 1024 * 256;
DROP DATABASE IF EXISTS celery_backend;

CREATE DATABASE celery_backend;

DROP DATABASE IF EXISTS dota2_datawarehouse;

CREATE DATABASE dota2_datawarehouse;

USE dota2_datawarehouse;

-- BASE TABLE
DROP TABLE IF EXISTS matchs;

CREATE TABLE matchs
  (
     match_id   BIGINT NOT NULL UNIQUE,
     start_time BIGINT NOT NULL,
     PRIMARY KEY (match_id)
  );

DROP TABLE IF EXISTS heroes;

CREATE TABLE heroes
  (
     hero_id        BIGINT NOT NULL UNIQUE,
     name_hero      VARCHAR(100) NOT NULL,
     localized_name VARCHAR(20) NOT NULL,
     attack_type    VARCHAR(10),
     primary_attr   VARCHAR(10),
     PRIMARY KEY (hero_id),
     INDEX ind_hero_id (hero_id)
  );

DROP TABLE IF EXISTS heroes_roles;

CREATE TABLE heroes_roles
  (
     hero_id BIGINT NOT NULL,
     roles   VARCHAR(10),
     FOREIGN KEY (hero_id) REFERENCES heroes(hero_id)
  );

DROP TABLE IF EXISTS matchs_heroes;

CREATE TABLE matchs_heroes
  (
     match_id BIGINT NOT NULL,
     hero_id  BIGINT NOT NULL,
     is_win   BOOLEAN,
     FOREIGN KEY (match_id) REFERENCES matchs(match_id),
     FOREIGN KEY (hero_id) REFERENCES heroes(hero_id)
  );
