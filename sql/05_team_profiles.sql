USE ea_coach_dna_calibration;

-- =========================================================
-- TEAM OFFENSIVE PROFILES (2025)
-- Purpose:
-- Build team-by-situation offensive profiles for the
-- 2025 season only.
--
-- Design notes:
-- - One row per team + situation
-- - Built from play-level situation views
-- - Long format keeps later baseline comparisons cleaner
-- - "Success rate" is defined here as EPA > 0
-- - Explosive play thresholds:
--     * dropback: 15+ yards
--     * run: 10+ yards
-- =========================================================

DROP TABLE IF EXISTS team_offense_profiles_2025;

CREATE TABLE team_offense_profiles_2025 AS
SELECT
    2025 AS profile_season,
    posteam AS team,
    situation_order,
    situation_name,

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
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_all_offense
    WHERE season = 2025

    UNION ALL
    SELECT 2, 'early_down',
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_early_down
    WHERE season = 2025

    UNION ALL
    SELECT 3, 'third_down',
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_third_down
    WHERE season = 2025

    UNION ALL
    SELECT 4, 'fourth_down',
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_fourth_down
    WHERE season = 2025

    UNION ALL
    SELECT 5, 'short_yardage',
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_short_yardage
    WHERE season = 2025

    UNION ALL
    SELECT 6, 'red_zone',
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_red_zone
    WHERE season = 2025

    UNION ALL
    SELECT 7, 'goal_to_go',
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_goal_to_go
    WHERE season = 2025

    UNION ALL
    SELECT 8, 'two_minute_half',
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_two_minute_half
    WHERE season = 2025

    UNION ALL
    SELECT 9, 'two_minute_game',
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_two_minute_game
    WHERE season = 2025

    UNION ALL
    SELECT 10, 'one_score',
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_one_score
    WHERE season = 2025

    UNION ALL
    SELECT 11, 'neutral_early_down',
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_neutral_early_down
    WHERE season = 2025

    UNION ALL
    SELECT 12, 'tied',
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_tied
    WHERE season = 2025

    UNION ALL
    SELECT 13, 'leading',
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_leading
    WHERE season = 2025

    UNION ALL
    SELECT 14, 'trailing',
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_trailing
    WHERE season = 2025

    UNION ALL
    SELECT 15, 'leading_one_score',
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_leading_one_score
    WHERE season = 2025

    UNION ALL
    SELECT 16, 'leading_two_plus_scores',
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_leading_two_plus_scores
    WHERE season = 2025

    UNION ALL
    SELECT 17, 'trailing_one_score',
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_trailing_one_score
    WHERE season = 2025

    UNION ALL
    SELECT 18, 'trailing_two_plus_scores',
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_trailing_two_plus_scores
    WHERE season = 2025

    UNION ALL
    SELECT 19, 'tied_early_down',
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_tied_early_down
    WHERE season = 2025

    UNION ALL
    SELECT 20, 'leading_early_down',
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_leading_early_down
    WHERE season = 2025

    UNION ALL
    SELECT 21, 'trailing_early_down',
           posteam, play_family, is_pass_attempt,
           shotgun, no_huddle, yards_gained, epa, first_down, touchdown,
           is_turnover, is_sack
    FROM vw_sit_trailing_early_down
    WHERE season = 2025
) t
GROUP BY
    posteam,
    situation_order,
    situation_name
ORDER BY
    posteam,
    situation_order;

ALTER TABLE team_offense_profiles_2025
ADD COLUMN team_profile_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;

CREATE INDEX idx_team_profiles_2025_team
    ON team_offense_profiles_2025 (team);

CREATE INDEX idx_team_profiles_2025_situation
    ON team_offense_profiles_2025 (situation_name);

CREATE INDEX idx_team_profiles_2025_team_situation
    ON team_offense_profiles_2025 (team, situation_name);

CREATE INDEX idx_team_profiles_2025_profile_season
    ON team_offense_profiles_2025 (profile_season);