USE ea_coach_dna_calibration;

-- =========================================================
-- CLEAN PLAY TABLE
-- Purpose:
-- Convert raw nflverse play-by-play into a cleaner analytical
-- table centered on real offensive decision plays.
--
-- Included seasons:
-- - 2023 baseline
-- - 2024 baseline
-- - 2025 team-profile + baseline
--
-- Key design choices:
-- - Regular season only
-- - Keep true offensive snaps
-- - Exclude special teams, spikes, kneels, and non-play rows
-- =========================================================

DROP TABLE IF EXISTS clean_pbp;

CREATE TABLE clean_pbp AS
SELECT
    raw_pbp_id,
    play_id,
    game_id,
    old_game_id,
    game_date,
    season,
    source_season,
    source_file,
    season_type,
    week,

    home_team,
    away_team,
    posteam,
    defteam,
    side_of_field,

    yardline_100,
    qtr,
    quarter_seconds_remaining,
    half_seconds_remaining,
    game_seconds_remaining,
    game_clock,
    down,
    ydstogo,
    goal_to_go,

    posteam_score,
    defteam_score,
    score_differential,

    play_description,
    play_type,
    yards_gained,
    epa,
    wpa,
    wp,
    def_wp,
    home_wp,
    away_wp,

    shotgun,
    no_huddle,
    qb_dropback,
    qb_kneel,
    qb_spike,
    rush_attempt,
    pass_attempt,
    complete_pass,
    incomplete_pass,
    sack,
    interception,
    fumble,
    penalty,
    first_down,
    touchdown,
    pass_touchdown,
    rush_touchdown,
    return_touchdown,

    air_yards,
    yards_after_catch,
    pass_location,
    run_location,
    run_gap,

    -- Core analytical flags
    CASE
        WHEN rush_attempt = 1 THEN 'run'
        WHEN pass_attempt = 1 OR sack = 1 OR qb_dropback = 1 THEN 'dropback'
        ELSE 'other'
    END AS play_family,

    CASE
        WHEN pass_attempt = 1 OR sack = 1 OR qb_dropback = 1 THEN 1
        ELSE 0
    END AS is_dropback,

    CASE
        WHEN rush_attempt = 1 THEN 1
        ELSE 0
    END AS is_rush,

    CASE
        WHEN pass_attempt = 1 THEN 1
        ELSE 0
    END AS is_pass_attempt,

    CASE
        WHEN sack = 1 THEN 1
        ELSE 0
    END AS is_sack,

    CASE
        WHEN interception = 1 OR fumble = 1 THEN 1
        ELSE 0
    END AS is_turnover,

    CASE
        WHEN down = 3 THEN 1
        ELSE 0
    END AS is_third_down,

    CASE
        WHEN down = 4 THEN 1
        ELSE 0
    END AS is_fourth_down,

    CASE
        WHEN yardline_100 <= 20 THEN 1
        ELSE 0
    END AS is_red_zone,

    CASE
        WHEN goal_to_go = 1 THEN 1
        ELSE 0
    END AS is_goal_to_go_play,

    CASE
        WHEN game_seconds_remaining <= 120 THEN 1
        ELSE 0
    END AS is_final_two_minutes,

    CASE
        WHEN ABS(score_differential) <= 8 THEN 1
        ELSE 0
    END AS is_one_score_game,

    CASE
        WHEN ydstogo <= 2 THEN 'short'
        WHEN ydstogo <= 6 THEN 'medium'
        ELSE 'long'
    END AS distance_bucket,

    CASE
        WHEN yardline_100 > 80 THEN 'backed_up'
        WHEN yardline_100 > 50 THEN 'own_territory'
        WHEN yardline_100 > 20 THEN 'fringe'
        ELSE 'red_zone'
    END AS field_zone,

    CASE
        WHEN score_differential > 8 THEN 'leading_2plus_scores'
        WHEN score_differential BETWEEN 1 AND 8 THEN 'leading_1_score'
        WHEN score_differential = 0 THEN 'tied'
        WHEN score_differential BETWEEN -8 AND -1 THEN 'trailing_1_score'
        ELSE 'trailing_2plus_scores'
    END AS score_state_bucket

FROM raw_pbp
WHERE 1 = 1
    AND season IN (2023, 2024, 2025)
    AND season_type = 'REG'
    AND posteam IS NOT NULL
    AND defteam IS NOT NULL
    AND down BETWEEN 1 AND 4
    AND yardline_100 IS NOT NULL
    AND ydstogo IS NOT NULL
    AND game_seconds_remaining IS NOT NULL
    AND NOT (qb_kneel = 1 OR qb_spike = 1)
    AND kickoff_attempt = 0
    AND punt_attempt = 0
    AND field_goal_attempt = 0
    AND extra_point_attempt = 0
    AND two_point_attempt = 0
    AND (rush_attempt = 1 OR pass_attempt = 1 OR sack = 1 OR qb_dropback = 1);

-- =========================================================
-- ADD PRIMARY KEY
-- =========================================================

ALTER TABLE clean_pbp
ADD COLUMN clean_pbp_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;

-- =========================================================
-- INDEXES
-- =========================================================

CREATE INDEX idx_clean_pbp_season          ON clean_pbp (season);
CREATE INDEX idx_clean_pbp_week            ON clean_pbp (week);
CREATE INDEX idx_clean_pbp_game_id         ON clean_pbp (game_id);
CREATE INDEX idx_clean_pbp_posteam         ON clean_pbp (posteam);
CREATE INDEX idx_clean_pbp_defteam         ON clean_pbp (defteam);
CREATE INDEX idx_clean_pbp_play_family     ON clean_pbp (play_family);
CREATE INDEX idx_clean_pbp_play_type       ON clean_pbp (play_type);
CREATE INDEX idx_clean_pbp_down_distance   ON clean_pbp (down, ydstogo);
CREATE INDEX idx_clean_pbp_field_position  ON clean_pbp (yardline_100);
CREATE INDEX idx_clean_pbp_game_state      ON clean_pbp (game_seconds_remaining, score_differential);