# Changelog

## 2026-04-04
- created project folder structure
- initialized local Git repository
- created GitHub repository
- connected local repo to GitHub remote
- pushed initial project structure
- added first draft project documentation files

## 2026-04-09
- updated project scope to use 2025 for team profiles
- updated project scope to use 2023 to 2025 for league baselines
- finalized MySQL schema for raw play-by-play staging
- fixed raw load mapping to align with nflverse CSV structure
- loaded 2023, 2024, and 2025 nflverse play-by-play data into MySQL
- created `clean_pbp` as the cleaned offensive play universe
- filtered out special teams, kneels, spikes, and non-core rows from downstream analysis
- created reusable situational SQL views for down, distance, field position, clock, and score state
- built `team_offense_profiles_2025`
- built `league_offense_baselines_2023_2025`
- validated team-vs-baseline metric consistency
- fixed mutually exclusive run vs dropback rate logic using `play_family`
- created `python/config.py`
- created `python/load_data.py`
- created `python/build_features.py`
- created `python/score_profiles.py`
- created `python/export_outputs.py`
- built `team_baseline_features_2025_vs_2023_2025.csv`
- built `coach_dna_situation_scores_2025.csv`
- built `coach_dna_team_summary_2025.csv`
- built packaged export tables for ranked team summaries, ranked situation scores, and top signal situations
- rewrote project documentation to reflect final scope, pipeline, and benchmark framing
- pushed working SQL and Python pipeline milestones to GitHub