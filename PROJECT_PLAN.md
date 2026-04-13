# Project Plan

## Project Title
Coach DNA Calibration Lab

## Project Goal
Build a SQL and Python project that measures real NFL offensive coaching behavior and turns it into a benchmarking framework for more authentic football coach logic.

## Main Question
How can real NFL offensive decision-making be translated into a structured benchmark for more authentic football coach logic?

## Core Approach
This project uses NFL play-by-play data to:
1. clean and structure offensive decision plays
2. define major football situations and field zones
3. build 2025 team offensive profiles
4. build 2023 to 2025 league baselines
5. compare team behavior to league context at the situation + field-zone level
6. generate interpretable Coach DNA outputs in Python

## Analytical Unit
The main analytical units are:
- **team-season** for 2025 team profiles
- **situation + field-zone context** for behavioral measurement and comparison

League context uses:
- **2023 to 2025** multi-season NFL data

## Season Scope

### Team Profiles
- 2025 season only

### League Baselines
- 2023 season
- 2024 season
- 2025 season

## Why This Scope
Using one season for team profiles keeps the team identity cleaner. It avoids blending different coordinators, quarterbacks, and week-to-week evolution across multiple years into one permanent profile.

Using multiple seasons for league baselines gives a broader comparison point and helps stabilize league expectation.

## In Scope
- play-level cleaning
- situation logic
- field-zone logic
- offensive tendency profiling
- early-down behavior
- third- and fourth-down behavior
- short-yardage behavior
- red-zone, goal-to-go, and goal-line behavior
- score-state behavior
- two-minute behavior
- team-vs-baseline feature engineering
- Coach DNA scoring
- Git/GitHub version control workflow
- notebooks for EDA and profile checks
- exported findings tables

## Out of Scope
- internal EA telemetry
- synthetic gameplay data
- Tableau or BI dashboards as the main deliverable
- advanced machine learning
- game simulation
- player-level scouting analysis
- defensive profiling in this version

## Core Contexts
The project currently evaluates behavior across these situations:
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

These are measured alongside field position.

## Field Zones
The model carries four main field zones:
- backed_up
- own_territory
- fringe
- red_zone

Compressed scoring space is also split more tightly into:
- red_zone
- goal_to_go
- goal_line

## Planned Deliverables
- documented GitHub repo
- raw and processed data folders
- SQL scripts for schema, cleaning, situation views, profiles, and baselines
- Python scripts for config, data loading, feature building, scoring, and exports
- notebooks for EDA and profile checks
- outputs folder with final tables
- README with project framing, process, and findings

## Project Phases

### Phase 1
Project setup and documentation baseline

### Phase 2
Raw data pull and SQL loading

### Phase 3
Play-level cleaning and offensive play filtering

### Phase 4
Situational and field-zone view creation

### Phase 5
2025 team profile creation

### Phase 6
2023 to 2025 league baseline creation

### Phase 7
Python feature engineering and Coach DNA scoring

### Phase 8
Validation, findings extraction, and documentation polish

## Success Criteria
The project is successful if it:
- produces clean, repeatable SQL logic
- creates believable offensive coaching tendency metrics
- compares 2025 teams against multi-season league baselines
- captures behavior at the situation + field-zone level
- generates outputs that support coach-logic design discussion
- shows clean Git/GitHub workflow and documentation

## Current Status
The core SQL and Python pipeline is complete.

Completed work includes:
- raw load into MySQL
- clean offensive play table
- situation views
- field-zone rebuild
- compressed-field split for red_zone, goal_to_go, and goal_line
- 2025 team profiles
- 2023 to 2025 league baselines
- team-vs-baseline feature engineering
- Coach DNA scoring
- export packaging
- EDA and profile check notebooks
- README rewrite

## Next Steps
- finalize 3 to 5 screenshot-ready findings from the upgraded model
- write a tighter findings section for GitHub using proof-backed outputs
- draft a LinkedIn post around the strongest field-zone-related insight
- review whether second-pass scoring refinements are worth adding after findings review
- keep defensive modeling out of scope until the offensive version is fully locked