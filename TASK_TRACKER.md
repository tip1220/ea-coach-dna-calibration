# Task Tracker

## Backlog
- write screenshot-ready findings from upgraded Coach DNA outputs
- build a clean findings section for GitHub with 3–5 proof-backed insights
- draft a LinkedIn post based on the strongest project findings
- decide whether to add a dedicated read-only MySQL user for Python access
- consider second-pass scoring refinements after findings review
- consider defensive expansion in a future version (out of scope for current build)

## In Progress
- prepare final interpretation layer around top team and context signals
- identify strongest situation + field-zone findings for README, GitHub, and LinkedIn
- refine project storytelling for recruiter and hiring-manager review

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
  - `README.md`

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
  - goal line
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

- add field-zone logic to the project:
  - backed_up
  - own_territory
  - fringe
  - red_zone
  - compressed-field splits for:
    - red_zone
    - goal_to_go
    - goal_line

- rebuild team profile logic at the situation + field-zone level
- rebuild league baseline logic at the situation + field-zone level
- validate team-vs-baseline structure and metric consistency
- fix mutually exclusive run vs dropback rate logic
- fix join logic so team and baseline features align on both:
  - `situation_name`
  - `field_zone`

- build 2025 team offensive profile table
- build 2023–2025 league offensive baseline table

- create Python config layer:
  - `python/config.py`

- create Python data loading layer:
  - `python/load_data.py`

- create Python feature engineering layer:
  - `python/build_features.py`

- create scoring layer:
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
  - `coach_dna_situation_strength_summary_2025.csv`
  - `coach_dna_team_summary_presentation_2025.csv`

- create and revise exploratory notebooks:
  - `notebooks/01_eda.ipynb`
  - `notebooks/02_profile_checks.ipynb`

- update notebooks to reflect upgraded field-zone model
- rewrite README in a stronger audience-facing voice
- rewrite notebook markdowns to match project voice and final framing

- push working SQL + Python pipeline milestones to GitHub
- create feature branch for field-zone upgrade work
- complete first end-to-end run from raw load through exported scoring outputs

## Blocked
- none