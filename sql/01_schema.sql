CREATE DATABASE IF NOT EXISTS ea_coach_dna_calibration;
USE ea_coach_dna_calibration;

-- =========================================================
-- RAW STAGING TABLE
-- Purpose:
-- Holds imported NFL play-by-play rows for 2023-2025.
-- This is a staging table, not the final analytical table.
-- 2025 will support team profile creation, while 2023-2025
-- provide league baseline context for comparison.
-- =========================================================

DROP TABLE IF EXISTS raw_pbp;

CREATE TABLE raw_pbp (
    raw_pbp_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,

    play_id BIGINT NULL,
    game_id VARCHAR(20) NULL,
    old_game_id VARCHAR(20) NULL,
    home_team VARCHAR(10) NULL,
    away_team VARCHAR(10) NULL,
    season_type VARCHAR(10) NULL,
    week INT NULL,
    posteam VARCHAR(10) NULL,
    defteam VARCHAR(10) NULL,
    side_of_field VARCHAR(10) NULL,
    yardline_100 DECIMAL(6,2) NULL,
    game_date DATE NULL,
    quarter_seconds_remaining INT NULL,
    half_seconds_remaining INT NULL,
    game_seconds_remaining INT NULL,
    qtr INT NULL,
    down INT NULL,
    ydstogo INT NULL,
    goal_to_go TINYINT(1) NULL,
    game_clock VARCHAR(10) NULL,
    yrdln VARCHAR(20) NULL,
    play_description TEXT NULL,
    play_type VARCHAR(20) NULL,
    yards_gained DECIMAL(8,2) NULL,
    shotgun TINYINT(1) NULL,
    no_huddle TINYINT(1) NULL,
    qb_dropback TINYINT(1) NULL,
    qb_kneel TINYINT(1) NULL,
    qb_spike TINYINT(1) NULL,
    rush_attempt TINYINT(1) NULL,
    pass_attempt TINYINT(1) NULL,
    penalty TINYINT(1) NULL,
    first_down TINYINT(1) NULL,
    touchdown TINYINT(1) NULL,
    pass_touchdown TINYINT(1) NULL,
    rush_touchdown TINYINT(1) NULL,
    return_touchdown TINYINT(1) NULL,
    extra_point_attempt TINYINT(1) NULL,
    two_point_attempt TINYINT(1) NULL,
    field_goal_attempt TINYINT(1) NULL,
    kickoff_attempt TINYINT(1) NULL,
    punt_attempt TINYINT(1) NULL,
    complete_pass TINYINT(1) NULL,
    incomplete_pass TINYINT(1) NULL,
    interception TINYINT(1) NULL,
    sack TINYINT(1) NULL,
    safety TINYINT(1) NULL,
    fumble TINYINT(1) NULL,
    complete_pass_epa DECIMAL(10,4) NULL,
    incomplete_pass_epa DECIMAL(10,4) NULL,
    air_yards DECIMAL(8,2) NULL,
    yards_after_catch DECIMAL(8,2) NULL,
    run_location VARCHAR(20) NULL,
    run_gap VARCHAR(20) NULL,
    pass_location VARCHAR(20) NULL,
    score_differential DECIMAL(8,2) NULL,
    posteam_score DECIMAL(8,2) NULL,
    defteam_score DECIMAL(8,2) NULL,
    wp DECIMAL(10,6) NULL,
    def_wp DECIMAL(10,6) NULL,
    home_wp DECIMAL(10,6) NULL,
    away_wp DECIMAL(10,6) NULL,
    wpa DECIMAL(10,6) NULL,
    epa DECIMAL(10,6) NULL,
    season INT NULL,

    -- Helpful metadata for project management
    source_season INT NOT NULL,
    source_file VARCHAR(255) NOT NULL,
    load_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (raw_pbp_id)
);

-- =========================================================
-- OPTIONAL INDEXES
-- These help later filtering and analysis
-- =========================================================

CREATE INDEX idx_raw_pbp_season    ON raw_pbp (season);
CREATE INDEX idx_raw_pbp_week      ON raw_pbp (week);
CREATE INDEX idx_raw_pbp_game_id   ON raw_pbp (game_id);
CREATE INDEX idx_raw_pbp_posteam   ON raw_pbp (posteam);
CREATE INDEX idx_raw_pbp_defteam   ON raw_pbp (defteam);
CREATE INDEX idx_raw_pbp_play_type ON raw_pbp (play_type);