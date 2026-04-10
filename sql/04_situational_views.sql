USE ea_coach_dna_calibration;

-- =========================================================
-- SITUATIONAL VIEWS
-- Purpose:
-- Create reusable play-level views for the main football
-- situations that will feed team profile logic and league
-- baselines.
--
-- Design notes:
-- - Built from clean_pbp
-- - Views stay at the play level
-- - Aggregation happens later in 05_team_profiles.sql
--   and 06_baselines.sql
-- - field_zone remains available in every view because each
--   view selects directly from clean_pbp
--
-- Compressed-field scoring area design:
-- - red_zone:
--     plus 20 to plus 11
--     yardline_100 BETWEEN 11 AND 20
-- - goal_to_go:
--     plus 10 to plus 3
--     goal_to_go = 1 AND yardline_100 BETWEEN 3 AND 10
-- - goal_line:
--     plus 2 to the end zone
--     goal_to_go = 1 AND yardline_100 <= 2
--
-- Why this matters:
-- - Coaching behavior changes sharply as field space shrinks
-- - Plus 20 to plus 11 is still red-zone football, but there
--   is more space for routes, motion, and play design
-- - Plus 10 to plus 3 is compressed-field offense where the
--   playbook tightens and situational intent matters more
-- - Plus 2 and in is true goal-line football where formation
--   density, power tendency, and aggressive scoring behavior
--   become even more distinct
-- =========================================================

DROP VIEW IF EXISTS
    vw_sit_all_offense,
    vw_sit_early_down,
    vw_sit_third_down,
    vw_sit_fourth_down,
    vw_sit_short_yardage,
    vw_sit_red_zone,
    vw_sit_goal_to_go,
    vw_sit_goal_line,
    vw_sit_two_minute_half,
    vw_sit_two_minute_game,
    vw_sit_one_score,
    vw_sit_neutral_early_down,
    vw_sit_tied,
    vw_sit_leading,
    vw_sit_trailing,
    vw_sit_leading_one_score,
    vw_sit_leading_two_plus_scores,
    vw_sit_trailing_one_score,
    vw_sit_trailing_two_plus_scores,
    vw_sit_tied_early_down,
    vw_sit_leading_early_down,
    vw_sit_trailing_early_down;

-- =========================================================
-- BASE OFFENSIVE PLAY UNIVERSE
-- =========================================================

CREATE VIEW vw_sit_all_offense AS
SELECT *
FROM clean_pbp;

-- =========================================================
-- EARLY DOWNS
-- =========================================================

CREATE VIEW vw_sit_early_down AS
SELECT *
FROM clean_pbp
WHERE down IN (1, 2);

-- =========================================================
-- THIRD DOWN
-- =========================================================

CREATE VIEW vw_sit_third_down AS
SELECT *
FROM clean_pbp
WHERE down = 3;

-- =========================================================
-- FOURTH DOWN
-- =========================================================

CREATE VIEW vw_sit_fourth_down AS
SELECT *
FROM clean_pbp
WHERE down = 4;

-- =========================================================
-- SHORT YARDAGE
-- =========================================================

CREATE VIEW vw_sit_short_yardage AS
SELECT *
FROM clean_pbp
WHERE ydstogo <= 2;

-- =========================================================
-- RED ZONE
-- Definition:
-- plus 20 to plus 11
-- =========================================================

CREATE VIEW vw_sit_red_zone AS
SELECT *
FROM clean_pbp
WHERE yardline_100 BETWEEN 11 AND 20;

-- =========================================================
-- GOAL TO GO
-- Definition:
-- plus 10 to plus 3
-- =========================================================

CREATE VIEW vw_sit_goal_to_go AS
SELECT *
FROM clean_pbp
WHERE goal_to_go = 1
  AND yardline_100 BETWEEN 3 AND 10;

-- =========================================================
-- GOAL LINE
-- Definition:
-- plus 2 to the end zone
-- =========================================================

CREATE VIEW vw_sit_goal_line AS
SELECT *
FROM clean_pbp
WHERE goal_to_go = 1
  AND yardline_100 <= 2;

-- =========================================================
-- TWO-MINUTE DRILL (HALF)
-- =========================================================

CREATE VIEW vw_sit_two_minute_half AS
SELECT *
FROM clean_pbp
WHERE half_seconds_remaining <= 120;

-- =========================================================
-- TWO-MINUTE DRILL (GAME)
-- =========================================================

CREATE VIEW vw_sit_two_minute_game AS
SELECT *
FROM clean_pbp
WHERE game_seconds_remaining <= 120;

-- =========================================================
-- ONE-SCORE GAME
-- =========================================================

CREATE VIEW vw_sit_one_score AS
SELECT *
FROM clean_pbp
WHERE ABS(score_differential) <= 8;

-- =========================================================
-- NEUTRAL EARLY DOWN
-- Purpose:
-- Standard offensive identity lens:
-- early downs, one-score game, outside final two minutes,
-- outside compressed scoring territory
-- =========================================================

CREATE VIEW vw_sit_neutral_early_down AS
SELECT *
FROM clean_pbp
WHERE down IN (1, 2)
  AND ABS(score_differential) <= 8
  AND game_seconds_remaining > 120
  AND yardline_100 > 20;

-- =========================================================
-- SCORE STATE: TIED / LEADING / TRAILING
-- =========================================================

CREATE VIEW vw_sit_tied AS
SELECT *
FROM clean_pbp
WHERE score_differential = 0;

CREATE VIEW vw_sit_leading AS
SELECT *
FROM clean_pbp
WHERE score_differential > 0;

CREATE VIEW vw_sit_trailing AS
SELECT *
FROM clean_pbp
WHERE score_differential < 0;

-- =========================================================
-- SCORE STATE: ONE SCORE / TWO-PLUS SCORES
-- =========================================================

CREATE VIEW vw_sit_leading_one_score AS
SELECT *
FROM clean_pbp
WHERE score_differential BETWEEN 1 AND 8;

CREATE VIEW vw_sit_leading_two_plus_scores AS
SELECT *
FROM clean_pbp
WHERE score_differential >= 9;

CREATE VIEW vw_sit_trailing_one_score AS
SELECT *
FROM clean_pbp
WHERE score_differential BETWEEN -8 AND -1;

CREATE VIEW vw_sit_trailing_two_plus_scores AS
SELECT *
FROM clean_pbp
WHERE score_differential <= -9;

-- =========================================================
-- EARLY DOWN + SCORE STATE
-- =========================================================

CREATE VIEW vw_sit_tied_early_down AS
SELECT *
FROM clean_pbp
WHERE down IN (1, 2)
  AND score_differential = 0;

CREATE VIEW vw_sit_leading_early_down AS
SELECT *
FROM clean_pbp
WHERE down IN (1, 2)
  AND score_differential > 0;

CREATE VIEW vw_sit_trailing_early_down AS
SELECT *
FROM clean_pbp
WHERE down IN (1, 2)
  AND score_differential < 0;