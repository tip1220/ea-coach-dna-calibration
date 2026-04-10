USE ea_coach_dna_calibration;

-- =========================================================
-- TEAM OFFENSIVE PROFILES (2025)
-- Purpose:
-- Build team-by-situation-by-field-zone offensive profiles
-- for the 2025 season only.
--
-- Design notes:
-- - One row per team + situation + field_zone
-- - Built from play-level situation views
-- - field_zone is carried alongside each situation rather
--   than treated as a separate standalone situation list
-- - This lets the project capture how the same coaching
--   situation can produce different behavior depending on
--   field position
-- - Long format keeps later baseline comparisons cleaner
-- - "Success rate" is defined here as EPA > 0
-- - Explosive play thresholds:
--     * dropback: 15+ yards
--     * run: 10+ yards
--
-- Why field zones matter:
-- - Coaching behavior is shaped not just by down, distance,
--   score, and time, but also by field position
-- - A team backed up in minus territory should not behave
--   like that same team in fringe or red-zone space
-- - Adding field_zone helps make the benchmark more realistic
--   for CPU-controlled coaching logic because it captures
--   where aggression, tempo, run-pass balance, and play
--   selection should shift based on field position
--
-- Field zone definitions:
-- - backed_up:
--     yardline_100 > 80
--     roughly minus 1 to minus 19
--
-- - own_territory:
--     yardline_100 between 51 and 80
--     roughly minus 20 to minus 49
--
-- - fringe:
--     yardline_100 between 21 and 50
--     midfield through lower plus territory
--
-- - red_zone:
--     yardline_100 <= 20
--     plus 20 and in
--
-- Compressed-field scoring situations:
-- - red_zone:
--     plus 20 to plus 11
-- - goal_to_go:
--     plus 10 to plus 3
-- - goal_line:
--     plus 2 to the end zone
-- =========================================================

DROP TABLE IF EXISTS team_offense_profiles_2025;

CREATE TABLE team_offense_profiles_2025 AS
SELECT
    2025 AS profile_season,
    posteam AS team,
    situation_order,
    situation_name,

    CASE
        WHEN field_zone = 'backed_up' THEN 1
        WHEN field_zone = 'own_territory' THEN 2
        WHEN field_zone = 'fringe' THEN 3
        WHEN field_zone = 'red_zone' THEN 4
        ELSE 99
    END AS field_zone_order,
    field_zone,

    COUNT(*) AS play_count,

    ROUND(AVG(CASE WHEN play_family = 'dropback' THEN 1 ELSE 0 END), 4) AS dropback_rate,
    ROUND(AVG(CASE WHEN play_family = 'run' THEN 1 ELSE 0 END), 4) AS rush_rate,
    ROUND(AVG(COALESCE(is_pass_attempt, 0)), 4) AS pass_attempt_rate,

    ROUND(AVG(COALESCE(shotgun, 0)), 4) AS shotgun_rate,
    ROUND(AVG(COALESCE(no_huddle, 0)), 4) AS no_huddle_rate,

    ROUND(AVG(yards_gained), 4) AS avg_yards_gained,
    ROUND(AVG(epa), 4) AS avg_epa,
    ROUND(AVG(CASE WHEN epa > 0 THEN 1 ELSE 0 END), 4) AS success_rate,

    ROUND(AVG(COALESCE(first_down, 0)), 4) AS first_down_rate,
    ROUND(AVG(COALESCE(touchdown, 0)), 4) AS touchdown_rate,
    ROUND(AVG(COALESCE(is_turnover, 0)), 4) AS turnover_rate,
    ROUND(AVG(COALESCE(is_sack, 0)), 4) AS sack_rate,

    ROUND(
        AVG(
            CASE
                WHEN play_family = 'dropback' AND yards_gained >= 15 THEN 1
                WHEN play_family = 'run' AND yards_gained >= 10 THEN 1
                ELSE 0
            END
        ),
        4
    ) AS explosive_play_rate,

    ROUND(
        AVG(
            CASE
                WHEN play_family = 'dropback' AND yards_gained >= 15 THEN 1
                ELSE 0
            END
        ),
        4
    ) AS explosive_dropback_rate,

    ROUND(
        AVG(
            CASE
                WHEN play_family = 'run' AND yards_gained >= 10 THEN 1
                ELSE 0
            END
        ),
        4
    ) AS explosive_run_rate,

    CASE
        WHEN COUNT(*) >= 100 THEN 'strong'
        WHEN COUNT(*) >= 50 THEN 'good'
        WHEN COUNT(*) >= 20 THEN 'thin'
        ELSE 'very_thin'
    END AS sample_quality,

    CASE
        WHEN COUNT(*) >= 50 THEN 1
        ELSE 0
    END AS meets_min_sample_50,

    CASE
        WHEN COUNT(*) >= 20 THEN 1
        ELSE 0
    END AS meets_min_sample_20

FROM (
    SELECT 1 AS situation_order, 'all_offense' AS situation_name,
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_all_offense
    WHERE season = 2025

    UNION ALL
    SELECT 2, 'early_down',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_early_down
    WHERE season = 2025

    UNION ALL
    SELECT 3, 'third_down',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_third_down
    WHERE season = 2025

    UNION ALL
    SELECT 4, 'fourth_down',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_fourth_down
    WHERE season = 2025

    UNION ALL
    SELECT 5, 'short_yardage',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_short_yardage
    WHERE season = 2025

    UNION ALL
    SELECT 6, 'red_zone',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_red_zone
    WHERE season = 2025

    UNION ALL
    SELECT 7, 'goal_to_go',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_goal_to_go
    WHERE season = 2025

    UNION ALL
    SELECT 8, 'goal_line',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_goal_line
    WHERE season = 2025

    UNION ALL
    SELECT 9, 'two_minute_half',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_two_minute_half
    WHERE season = 2025

    UNION ALL
    SELECT 10, 'two_minute_game',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_two_minute_game
    WHERE season = 2025

    UNION ALL
    SELECT 11, 'one_score',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_one_score
    WHERE season = 2025

    UNION ALL
    SELECT 12, 'neutral_early_down',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_neutral_early_down
    WHERE season = 2025

    UNION ALL
    SELECT 13, 'tied',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_tied
    WHERE season = 2025

    UNION ALL
    SELECT 14, 'leading',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_leading
    WHERE season = 2025

    UNION ALL
    SELECT 15, 'trailing',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_trailing
    WHERE season = 2025

    UNION ALL
    SELECT 16, 'leading_one_score',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_leading_one_score
    WHERE season = 2025

    UNION ALL
    SELECT 17, 'leading_two_plus_scores',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_leading_two_plus_scores
    WHERE season = 2025

    UNION ALL
    SELECT 18, 'trailing_one_score',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_trailing_one_score
    WHERE season = 2025

    UNION ALL
    SELECT 19, 'trailing_two_plus_scores',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_trailing_two_plus_scores
    WHERE season = 2025

    UNION ALL
    SELECT 20, 'tied_early_down',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_tied_early_down
    WHERE season = 2025

    UNION ALL
    SELECT 21, 'leading_early_down',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_leading_early_down
    WHERE season = 2025

    UNION ALL
    SELECT 22, 'trailing_early_down',
           posteam, field_zone, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_trailing_early_down
    WHERE season = 2025
) t
GROUP BY
    posteam,
    situation_order,
    situation_name,
    field_zone
ORDER BY
    posteam,
    situation_order,
    field_zone_order;

ALTER TABLE team_offense_profiles_2025
ADD COLUMN team_profile_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;

CREATE INDEX idx_team_profiles_2025_team
    ON team_offense_profiles_2025 (team);

CREATE INDEX idx_team_profiles_2025_situation
    ON team_offense_profiles_2025 (situation_name);

CREATE INDEX idx_team_profiles_2025_field_zone
    ON team_offense_profiles_2025 (field_zone);

CREATE INDEX idx_team_profiles_2025_team_situation_zone
    ON team_offense_profiles_2025 (team, situation_name, field_zone);

CREATE INDEX idx_team_profiles_2025_profile_season
    ON team_offense_profiles_2025 (profile_season);