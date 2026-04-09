# Project Requirements

## Purpose
Coach DNA Calibration Lab is a SQL and Python project designed to convert real NFL situational behavior into a benchmarking framework for football coach logic and gameplay authenticity.

The project should remain:
- reproducible
- recruiter-ready
- studio-relevant
- grounded in real NFL behavior
- careful not to overclaim beyond the data

## Core Business Requirement
The project must answer this question:

**How can real NFL situational decision-making be translated into a structured benchmark for more authentic football coach logic?**

## Technical Requirements
The project must:
- use **MySQL** for data loading, cleaning, filtering, view creation, and metric generation
- use **Python** for table loading, feature creation, comparison logic, scoring, and export generation
- use **Git and GitHub** as the source of truth for version history
- maintain a clean, reproducible folder structure
- separate raw data, processed data, and final outputs
- keep naming consistent across SQL tables, Python outputs, and exported files
- avoid hardcoding repeated values across multiple files when they can be centralized in config

## Scope Requirements
The project must:
- use **2025** as the team-profile season
- use **2023–2025** as the league-baseline window
- use **team-season** as the main analytical unit for team profiles
- use **NFL play-by-play data** as the core source
- focus on **situational offensive behavior** in the current version
- produce a benchmarking framework, not a one-off descriptive analysis

## Project Constraints
The project must not:
- use internal EA data
- use synthetic gameplay telemetry
- claim to measure internal game logic directly
- depend on dashboard tools for the core project
- mix multiple seasons into one permanent team identity profile
- introduce unnecessary modeling complexity before the benchmark foundation is stable
- frame recommendations as unsupported product claims

## Data Requirements
The project must:
- use public nflverse play-by-play data
- preserve raw source files unchanged after download
- keep raw files in `data/raw/`
- keep processed outputs in `data/processed/`
- preserve source season and source file metadata during loading
- use the following raw source files:
  - `pbp_2023.csv`
  - `pbp_2024.csv`
  - `pbp_2025.csv`

## SQL Layer Requirements
The SQL pipeline must:
- create a raw staging table for loaded play-by-play data
- create a cleaned offensive play table with only valid decision-play rows
- remove non-core rows such as special teams, kneels, spikes, and non-play rows
- create reusable situation views from the cleaned play universe
- create a 2025 team profile table by situation
- create a 2023–2025 league baseline table by situation
- preserve mutually exclusive run vs dropback family logic where required

## Situation Requirements
The benchmarking layer must support, at minimum, the following situations:
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

## Metric Requirements
The project must generate and compare metrics such as:
- play count
- dropback rate
- rush rate
- pass attempt rate
- shotgun rate
- no-huddle rate
- average yards gained
- average EPA
- success rate
- first down rate
- touchdown rate
- turnover rate
- sack rate
- explosive play rate
- explosive dropback rate
- explosive run rate

All major metrics must be:
- clearly defined
- reproducible
- interpretable in football terms
- comparable across team profiles and league baselines

## Python Layer Requirements
The Python pipeline must:
- centralize configuration in `python/config.py`
- connect cleanly to MySQL
- load the core SQL outputs into pandas
- build team-vs-baseline comparison features
- calculate deltas between team profiles and league baselines
- generate first-pass Coach DNA scores
- export recruiter-friendly CSV outputs
- preserve a clean separation between loading, feature building, scoring, and exporting

## Scoring Requirements
The scoring layer should:
- measure how distinct a team is from league baseline
- include tendency-based signal
- include efficiency-based signal
- include explosiveness-based signal
- include stability-based signal
- include sample reliability guardrails
- avoid overrating tiny-sample situations
- remain interpretable enough to explain in a portfolio interview

## Output Requirements
The project must produce:
- cleaned SQL tables and views
- team profile tables
- league baseline tables
- team-vs-baseline feature tables
- situation-level Coach DNA scores
- team-level Coach DNA summary scores
- ranked export tables suitable for GitHub review
- outputs that can be used later in notebooks, a README narrative, or portfolio presentation material

## Documentation Requirements
The project documentation must:
- stay aligned with the latest approved scope
- explain the business question clearly
- describe the pipeline from raw data to final outputs
- document key design choices and tradeoffs
- distinguish clearly between benchmark guidance and unsupported product claims

The following files must remain maintained:
- `README.md`
- `PROJECT_PLAN.md`
- `DECISION_LOG.md`
- `TASK_TRACKER.md`
- `CHANGELOG.md`
- `REQUIREMENTS.md`

## Workflow Requirements
The project workflow must:
- preserve prior logic unless intentionally revised
- use small, logical commits
- keep GitHub updated as milestones are completed
- log meaningful scope changes in `DECISION_LOG.md`
- track progress in `TASK_TRACKER.md`
- keep the project from spiraling into unnecessary side paths before the core benchmark is complete

## Quality Standards
All project work should be:
- readable
- consistent
- testable
- explainable
- practical
- version-controlled
- grounded in real football logic

Outputs should be strong enough that a reviewer can understand:
- what the project does
- why the scope was chosen
- how the pipeline works
- what the benchmark means
- where the project is careful not to overclaim