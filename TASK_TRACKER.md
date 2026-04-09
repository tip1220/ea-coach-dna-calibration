# Task Tracker

## Backlog
- create `notebooks/01_eda.ipynb` for exploratory review of core tables and outputs
- create `notebooks/02_profile_checks.ipynb` for profile validation and sanity checks
- write findings summary from first-pass Coach DNA outputs
- tighten README narrative with specific project findings
- polish GitHub presentation for recruiter review
- decide whether to add a dedicated read-only MySQL user for Python access
- consider second-pass scoring refinements after notebook review
- consider defensive expansion in a future version (out of scope for current build)

## In Progress
- align project documentation to the finished SQL + Python pipeline
- update repo narrative for portfolio presentation
- prepare interpretation layer around top team and situation signals

## Done
- create local project folder structure
- initialize Git locally
- create GitHub repository
- connect local repo to GitHub
- push initial project structure to GitHub

- confirm final project scope:
  - 2025 team-profile season
  - 2023–2025 league-baseline window
  - NFL only
  - SQL + Python only
  - no dashboard requirement
  - benchmarking framework, not product audit

- create and revise core documentation:
  - `PROJECT_PLAN.md`
  - `DECISION_LOG.md`
  - `CHANGELOG.md`
  - `REQUIREMENTS.md`
  - `TASK_TRACKER.md`
  - `README.md` draft/rewrite work started

- create SQL pipeline:
  - `01_schema.sql`
  - `02_load_data.sql`
  - `03_clean_plays.sql`
  - `04_situational_views.sql`
  - `05_team_profiles.sql`
  - `06_baselines.sql`

- load raw nflverse data into MySQL:
  - `pbp_2023.csv`
  - `pbp_2024.csv`
  - `pbp_2025.csv`

- validate raw load and fix column mapping issues
- create cleaned offensive play table
- create situational views for:
  - all offense
  - early down
  - third down
  - fourth down
  - short yardage
  - red zone
  - goal to go
  - two-minute half
  - two-minute game
  - one-score game
  - neutral early down
  - tied
  - leading
  - trailing
  - leading one score
  - leading two-plus scores
  - trailing one score
  - trailing two-plus scores
  - tied early down
  - leading early down
  - trailing early down

- build 2025 team offensive profile table
- build 2023–2025 league offensive baseline table
- validate team-vs-baseline structure and metric consistency
- fix mutually exclusive run vs dropback rate logic

- create Python config layer:
  - `python/config.py`

- create Python data loading layer:
  - `python/load_data.py`

- create Python feature engineering layer:
  - `python/build_features.py`

- create first-pass scoring layer:
  - `python/score_profiles.py`

- create export packaging layer:
  - `python/export_outputs.py`

- export generated outputs:
  - `team_baseline_features_2025_vs_2023_2025.csv`
  - `coach_dna_situation_scores_2025.csv`
  - `coach_dna_team_summary_2025.csv`
  - `coach_dna_ranked_team_summary_2025.csv`
  - `coach_dna_ranked_situation_scores_2025.csv`
  - `coach_dna_top_signal_situations_by_team_2025.csv`
  - `coach_dna_team_summary_presentation_2025.csv`

- push working SQL + Python pipeline milestones to GitHub
- complete first end-to-end run from raw load through exported scoring outputs

## Blocked
- none