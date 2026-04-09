# Coach DNA Calibration Lab

## Project Summary
Coach DNA Calibration Lab is a SQL and Python analytics project built to model real NFL coaching tendencies and translate them into a benchmarking framework for football gameplay authenticity.

The project uses:
- 2025 NFL play-by-play data for team profiles
- 2023 to 2024 NFL play-by-play data for league baselines

The goal is to measure how teams behave in key game situations, then create a structured benchmark a football game studio could use when thinking about coach logic, situational aggression, and playcalling authenticity.

## Business Question
How can real NFL coaching behavior be measured and turned into a benchmark for more authentic football decision-making logic in games?

## Why This Project
Football realism is not just player ratings. It is also about how teams behave:
- when they go for it
- when they get conservative
- when they speed up
- when they throw more often
- when they protect a lead
- when they chase a comeback

If teams and coaches all behave too similarly in key moments, game authenticity leaves value on the table.

## Scope
This project focuses on:
- 2025 team-level profiles
- 2023 to 2025 league baselines
- situational decision-making patterns
- SQL-based data preparation and metric creation
- Python-based scoring, comparison, and interpretation

This project does not use:
- internal EA telemetry
- synthetic game telemetry
- dashboarding tools
- external proprietary data

## Main Outputs
- cleaned play-level SQL tables and views
- situational coaching tendency metrics
- 2025 team profile table
- 2023 to 2025 league baseline table
- Python scoring outputs
- summary tables and figures
- a documented Git/GitHub workflow

## Repo Structure
```text
ea-coach-dna-calibration/
│
├── README.md
├── PROJECT_PLAN.md
├── DECISION_LOG.md
├── TASK_TRACKER.md
├── CHANGELOG.md
├── REQUIREMENTS.md
│
├── data/
│   ├── raw/
│   └── processed/
│
├── sql/
│   ├── 01_schema.sql
│   ├── 02_load_data.sql
│   ├── 03_clean_plays.sql
│   ├── 04_situational_views.sql
│   ├── 05_team_profiles.sql
│   └── 06_baselines.sql
│
├── python/
│   ├── config.py
│   ├── load_data.py
│   ├── build_features.py
│   ├── score_profiles.py
│   └── export_outputs.py
│
├── notebooks/
│   ├── 01_eda.ipynb
│   └── 02_profile_checks.ipynb
│
└── outputs/
    ├── tables/
    └── figures/