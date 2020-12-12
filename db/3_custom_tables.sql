

USE dota2_datawarehouse;

/*** Build intermediary tables to build custom heroes table ***/
-- Matchs per heroes
DROP TABLE IF EXISTS matchs_count;
CREATE TABLE matchs_count AS 
SELECT
   hero_id,
   count(match_id) AS n_matchs 
FROM
   matchs_heroes 
GROUP BY
   hero_id;

-- Matchs won per heroes
DROP TABLE IF EXISTS matchs_count_won;
CREATE TABLE matchs_count_won AS 
SELECT
   hero_id,
   count(match_id) AS n_matchs_won 
FROM
   matchs_heroes 
WHERE
   is_win = 1 
GROUP BY
   hero_id;

-- Multiple roles concat to one string per hero
DROP TABLE IF EXISTS heroes_concat_roles;
CREATE TABLE heroes_concat_roles AS 
SELECT
   h.hero_id,
   h.name_hero,
   h.localized_name,
   h.attack_type,
   h.primary_attr,
   roles.roles 
FROM
   heroes as h 
   LEFT JOIN
      (
         SELECT
            hero_id,
            GROUP_CONCAT(roles separator ', ') as roles 
         FROM
            heroes_roles 
         GROUP BY
            hero_id 
      )
      AS roles 
      ON h.hero_id = roles.hero_id;

/*** Build custom heroes table, including roles, pick rate and win rate ***/
DROP TABLE IF EXISTS heroes_custom;
CREATE TABLE heroes_custom AS 
SELECT
   h.hero_id,
   h.name_hero,
   h.localized_name,
   h.attack_type,
   h.primary_attr,
   h.roles,
   matchs_count_won.n_matchs_won,
   matchs_count.n_matchs,
   round(100 * matchs_count_won.n_matchs_won / matchs_count.n_matchs, 2) AS win_rate,
   round(100 * matchs_count.n_matchs / (
   SELECT
      count(match_id) 
   FROM
      matchs), 2) AS pick_rate 
   FROM
      heroes_concat_roles AS h 
      LEFT JOIN
         matchs_count 
         ON h.hero_id = matchs_count.hero_id 
      LEFT JOIN
         matchs_count_won 
         ON h.hero_id = matchs_count_won.hero_id;

/*** Build intermediary tables to build custom heroes couple table ***/
-- -- Count matchs won and loose for all couple of heroes
DROP TABLE IF EXISTS count_matchs_heroes_with;
CREATE TABLE count_matchs_heroes_with AS 
SELECT
   hero_id,
   hero_with_id,
   is_win,
   Count(match_id) as n_matchs 
FROM
   (
      -- Heroes in the same team in a given match
      SELECT
         m_1.match_id,
         m_1.hero_id as hero_id,
         m_full.hero_id as hero_with_id,
         m_1.is_win 
      FROM
         matchs_heroes as m_1 
         LEFT JOIN
            matchs_heroes AS m_full 
            ON m_1.match_id = m_full.match_id 
      WHERE
         (
            m_1.is_win = m_full.is_win 
            AND m_1.hero_id <> m_full.hero_id 
         )
   )
   AS hero_wih 
GROUP BY
   hero_id,
   hero_with_id,
   is_win;

-- Count matchs won and loose for all couple of heroes against
DROP TABLE IF EXISTS count_matchs_heroes_against;
CREATE TABLE count_matchs_heroes_against AS 
SELECT
   hero_id,
   hero_against_id,
   is_win,
   Count(match_id) as n_matchs 
FROM
   (
      -- Heroes in the different team in a given match
      SELECT
         m_1.match_id,
         m_1.hero_id as hero_id,
         m_full.hero_id as hero_against_id,
         m_1.is_win 
      FROM
         matchs_heroes as m_1 
         LEFT JOIN
            matchs_heroes AS m_full 
            ON m_1.match_id = m_full.match_id 
      WHERE
         (
            m_1.is_win <> m_full.is_win 
            AND m_1.hero_id <> m_full.hero_id 
         )
   )
   AS hero_against 
GROUP BY
   hero_id,
   hero_against_id,
   is_win;

/*** Build custom heroes couple table, including roles, pick rate and win rate ***/
DROP TABLE IF EXISTS grouped_matchs_heroes_with;
CREATE TABLE grouped_matchs_heroes_with AS 
SELECT
   grouped.hero_id,
   grouped.hero_with_id,
   grouped.n_matchs_won AS n_matchs_won,
   grouped.n_matchs AS n_matchs,
   round(100 * grouped.n_matchs_won / grouped.n_matchs, 2) AS win_rate,
   round(100 * grouped.n_matchs / matchs_per_heroes.n_matchs, 2) AS pick_rate 
FROM
   (
      SELECT
         played_with.hero_id,
         played_with.hero_with_id,
         win_with.n_matchs_won,
         played_with.n_matchs 
      FROM
         (
            -- Total matchs played of two given heroes in the same team
            SELECT
               hero_id,
               hero_with_id,
               SUM(n_matchs) AS n_matchs 
            FROM
               count_matchs_heroes_with 
            GROUP BY
               hero_id,
               hero_with_id 
         )
         AS played_with 
         LEFT JOIN
            (
               -- Total matchs played and won of two given heroes in the same team
               SELECT
                  hero_id,
                  hero_with_id,
                  n_matchs as n_matchs_won 
               FROM
                  count_matchs_heroes_with 
               WHERE
                  is_win = 1 
               ORDER BY
                  hero_id,
                  hero_with_id 
            )
            AS win_with 
            ON played_with.hero_id = win_with.hero_id 
      WHERE
         (
            played_with.hero_id = win_with.hero_id 
            AND played_with.hero_with_id = win_with.hero_with_id 
         )
   )
   AS grouped 
   LEFT JOIN
      matchs_count AS matchs_per_heroes 
      ON grouped.hero_id = matchs_per_heroes.hero_id;

/*** Build custom heroes couple table against, including roles, pick rate and win rate ***/
DROP TABLE IF EXISTS grouped_matchs_heroes_against;
CREATE TABLE grouped_matchs_heroes_against AS 
SELECT
   grouped.hero_id,
   grouped.hero_against_id,
   grouped.n_matchs_won AS n_matchs_won,
   grouped.n_matchs AS n_matchs,
   round(100 * grouped.n_matchs_won / grouped.n_matchs, 2) AS win_rate,
   round(100 * grouped.n_matchs / matchs_per_heroes.n_matchs, 2) AS pick_rate 
FROM
   (
      SELECT
         played_against.hero_id,
         played_against.hero_against_id,
         win_against.n_matchs_won,
         played_against.n_matchs 
      FROM
         (
            -- Total matchs played of two given heroes in a different team
            SELECT
               hero_id,
               hero_against_id,
               SUM(n_matchs) AS n_matchs 
            FROM
               count_matchs_heroes_against 
            GROUP BY
               hero_id,
               hero_against_id 
         )
         AS played_against 
         LEFT JOIN
            (
               -- Total matchs played and won of two given heroes in a different team
               SELECT
                  hero_id,
                  hero_against_id,
                  n_matchs as n_matchs_won 
               FROM
                  count_matchs_heroes_against 
               WHERE
                  is_win = 1 
               ORDER BY
                  hero_id,
                  hero_against_id 
            )
            AS win_against 
            ON played_against.hero_id = win_against.hero_id 
      WHERE
         (
            played_against.hero_id = win_against.hero_id 
            AND played_against.hero_against_id = win_against.hero_against_id
         )
   )
   AS grouped 
   LEFT JOIN
      matchs_count AS matchs_per_heroes 
      ON grouped.hero_id = matchs_per_heroes.hero_id;

/*** DROP intermediary tables ***/
DROP TABLE matchs_count;
DROP TABLE matchs_count_won;
DROP TABLE heroes_concat_roles;
DROP TABLE count_matchs_heroes_with;
DROP TABLE count_matchs_heroes_against;
