## `PROJECT_PLAN.md`

```md
# Project Plan

## Project Title
Coach DNA Calibration Lab

## Project Goal
Build a SQL and Python project that measures real NFL coaching tendencies and turns them into a benchmarking framework for football gameplay authenticity.

## Main Question
How can real NFL situational decision-making be translated into a structured benchmark for more authentic football coach logic?

## Core Approach
This project will use NFL play-by-play data to:
1. clean and structure offensive decision plays
2. define important game situations
3. calculate 2024 team-level profiles
4. calculate 2022 to 2024 league baselines
5. compare team behavior to league context
6. generate interpretable coaching profile outputs in Python

## Analytical Unit
The main analytical unit is:
- team-season for 2024 profiles

League context will use:
- 2022 to 2024 league-wide data

## Season Scope
### Team Profiles
- 2024 season only

### League Baselines
- 2022 season
- 2023 season
- 2024 season

## Why This Scope
Using one season for team profiles avoids blending different coaching staffs, coordinators, quarterbacks, and team identities.

Using multiple seasons for league baselines gives broader context without muddying team-specific profiles.

## In Scope
- play-level cleaning
- situational flags
- offensive decision tendencies
- fourth-down behavior
- red-zone tendencies
- neutral-situation pass rate
- late-game behavior
- Python scoring and comparison
- Git/GitHub version control workflow

## Out of Scope
- internal EA telemetry
- synthetic game telemetry
- Tableau or BI dashboards
- advanced machine learning
- game simulation
- player-level scouting analysis

## Proposed Situations
Initial situations to evaluate:
- neutral situation
- red zone
- fourth-and-short
- plus territory
- late-game trailing
- late-game leading
- early downs
- obvious passing situations

These definitions may be refined during cleaning and EDA.

## Planned Deliverables
- documented GitHub repo
- raw and processed data folders
- SQL scripts for schema, cleaning, views, profiles, and baselines
- Python scripts for feature building and scoring
- notebooks for EDA and profile checks
- outputs folder with final tables and figures
- README with business framing and findings

## Project Phases
### Phase 1
Project setup and documentation baseline

### Phase 2
Raw data pull and SQL loading

### Phase 3
Play-level cleaning and filtering

### Phase 4
Situational view creation

### Phase 5
2024 team profile creation

### Phase 6
2022 to 2024 baseline creation

### Phase 7
Python scoring and interpretation

### Phase 8
Validation and documentation polish

## Success Criteria
The project will be successful if it:
- produces clean, repeatable SQL logic
- creates believable coaching tendency metrics
- compares 2024 teams against multi-season league baselines
- generates product-facing recommendations
- shows clean Git/GitHub workflow and documentation

## Current Phase
Phase 1: Project setup and documentation baseline