# Coach DNA Calibration Lab

## Overview
Coach DNA Calibration Lab is a SQL and Python portfolio project built to translate real NFL situational behavior into a benchmarking framework for football gameplay authenticity.

The project uses NFL play-by-play data to answer a studio-relevant question: how should team-specific coaching tendencies show up in football decision logic if the goal is to make teams feel more distinct, believable, and situationally authentic?

This is **not** an audit of EA Sports logic, and it does not claim to measure internal game behavior. Instead, it builds an external benchmark from real NFL data that could support design conversations around coach logic, situational aggression, playcalling identity, and late-game behavior.

## Business Question
How can real NFL situational decision-making be translated into a structured benchmark for more authentic football coach logic?

## Why This Project Matters
Football realism is not just about ratings, rosters, or animations. It is also about behavior.

Teams do not all act the same when:
- protecting a lead
- chasing points
- facing short yardage
- operating in the red zone
- playing on third or fourth down
- managing two-minute situations
- leaning into or away from tempo

If every team behaves too similarly in these moments, the game can lose one of the things that makes football feel real: coaching identity.

This project focuses on that layer.

## Project Framing
This project is designed as a **benchmarking framework**, not a direct product audit.

I do **not** have access to:
- internal EA telemetry
- internal gameplay logic
- private tuning rules
- proprietary simulation data

Because of that, all recommendations and takeaways should be interpreted as:
- benchmark guidance from real NFL behavior
- evidence for how teams differ by situation
- inputs that could help shape more authentic coach logic

Not as unsupported claims about any specific game system.

## Scope
This project uses the following scope:

- **2025** NFL play-by-play for team profiles
- **2023–2025** NFL play-by-play for league baselines
- **team-season** as the main analytical unit for profiles
- **SQL + Python only**
- **no dashboarding layer** for the core project

### In Scope
- situational offensive behavior
- team tendency profiling
- league baseline construction
- team-vs-baseline comparisons
- first-pass Coach DNA scoring
- exported recruiter-ready tables

### Out of Scope
- internal game telemetry
- synthetic gameplay data
- proprietary tracking data
- cross-sport expansion
- defensive profiling in this first version

## Data Source
This project uses public NFL play-by-play data from **nflverse**.

Raw files loaded:
- `pbp_2023.csv`
- `pbp_2024.csv`
- `pbp_2025.csv`

## Analytical Approach
The project follows a layered pipeline:

1. **Raw staging**
   - Load nflverse CSVs into MySQL
   - Preserve season/file metadata for reproducibility

2. **Clean play universe**
   - Filter to real offensive decision plays
   - Remove special teams, kneels, spikes, and non-core rows
   - Create reusable flags for game state and situation logic

3. **Situational views**
   - Build reusable play-level views for:
     - early down
     - third down
     - fourth down
     - short yardage
     - red zone
     - goal to go
     - two-minute situations
     - tied / leading / trailing states
     - one-score and two-plus-score contexts

4. **2025 team profiles**
   - Build team-by-situation offensive profiles
   - Measure tendency, efficiency, explosiveness, and stability

5. **2023–2025 league baselines**
   - Build the comparison benchmark for each situation
   - Keep the metric structure aligned to team profiles

6. **Feature engineering**
   - Calculate team-vs-baseline deltas
   - Build reusable comparison tables for downstream scoring

7. **Coach DNA scoring**
   - Create first-pass situation-level and team-level scores
   - Combine tendency distinctiveness with efficiency and sample reliability

8. **Export layer**
   - Produce ranked summary tables
   - Package outputs for portfolio review and GitHub presentation

## Core Tables and Outputs

### SQL Layer
- `raw_pbp`
- `clean_pbp`
- situational views (`vw_sit_*`)
- `team_offense_profiles_2025`
- `league_offense_baselines_2023_2025`

### Python Layer
- `team_baseline_features_2025_vs_2023_2025.csv`
- `coach_dna_situation_scores_2025.csv`
- `coach_dna_team_summary_2025.csv`
- `coach_dna_ranked_team_summary_2025.csv`
- `coach_dna_ranked_situation_scores_2025.csv`
- `coach_dna_top_signal_situations_by_team_2025.csv`
- `coach_dna_team_summary_presentation_2025.csv`

## Current Output Themes
The current scoring framework captures several useful dimensions of team identity:

- **Tendency signal**
  - how far a team’s behavior moves away from league baseline

- **Efficiency signal**
  - whether that behavior actually outperforms the baseline

- **Explosiveness signal**
  - whether the offense creates chunk plays above baseline

- **Stability signal**
  - whether sacks and turnovers stay under control

- **Sample reliability**
  - whether the situation sample is strong enough to trust

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