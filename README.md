# Coach DNA Calibration Lab

## Overview
I built this project to study how real NFL offenses behave in context and turn that into a coach-logic benchmark a football studio could use.

The core question was pretty straightforward: if real teams call games differently depending on score, down, distance, clock, and field position, how should that show up in football decision logic?

I used NFL play-by-play, MySQL, and Python to build the project from raw files up through cleaned tables, team profiles, league baselines, feature engineering, scoring, and export tables.

I’m not auditing EA Sports. I don’t have internal gameplay logic, telemetry, or tuning rules. This is an outside benchmark built from real football behavior.

## Business Question
How can real NFL offensive decision-making be translated into a structured benchmark for more authentic football coach logic?

## Why I Built It
Football games can look good and still feel off if every team calls situations too similarly.

I’m talking about spots like:
- short yardage
- third down
- fourth down
- two-minute situations
- red-zone drives
- protecting a lead
- chasing points
- backed-up possessions
- fringe territory
- goal-to-go and goal-line plays

Those moments are where coaching personality shows up. If that layer gets flattened, teams start feeling the same even when the uniforms and ratings are different.

That’s what I wanted to work on.

## Project Framing
This project is a benchmark, not a product audit.

I don’t have access to:
- internal EA telemetry
- internal coach-logic rules
- private tuning values
- proprietary simulation data

So I’m not making claims about how any specific football game works under the hood.

What I am doing is building a clean, outside reference point from real NFL behavior. That can help frame better design questions around coach logic, situational aggression, tempo, and playcalling identity.

## Scope

### Data window
- 2025 NFL play-by-play for team profiles
- 2023–2025 NFL play-by-play for league baselines

### Main profile grain
- team-season for team identity
- situation + field zone for behavioral context

### Tools
- MySQL
- Python
- pandas
- Git / GitHub

### In scope
- offensive situation profiling
- field-zone-aware behavior modeling
- league baseline construction
- team-vs-baseline deltas
- Coach DNA scoring
- ranked export tables

### Out of scope
- defensive profiling in this version
- dashboards as the main deliverable
- internal game telemetry
- synthetic gameplay data
- proprietary tracking data

## What Changed During the Project
The first version of the model was built around the usual football buckets:
- down
- distance
- score state
- clock

That got me part of the way there. The outputs were useful. They still felt too broad.

Once I started reading through the tables, I could see the model was blending together football situations that weren’t really the same. A team backed up at its own 8 and that same team operating at the opponent’s 35 might both sit inside a broad situation label, but they are dealing with two different problems.

So I rebuilt the project around **situation + field zone**.

That changed the SQL views, the profile tables, the baseline tables, the feature engineering, the scoring layer, and the notebook analysis. It was more rework than I wanted, but it cleaned the logic up.

The numbers got sharper after that. The outputs started sounding more like football.

## Field Zones
I carried field position alongside the major situations so I could stop flattening different parts of the field into the same bucket.

### Core field zones
- **backed_up**
  - `yardline_100 > 80`
  - roughly minus 1 to minus 19

- **own_territory**
  - `yardline_100 between 51 and 80`
  - roughly minus 20 to minus 49

- **fringe**
  - `yardline_100 between 21 and 50`
  - midfield through lower plus territory

- **red_zone**
  - `yardline_100 <= 20`
  - plus 20 and in

### Compressed scoring splits
I also broke scoring territory into three tighter buckets:
- **red_zone**: plus 20 to plus 11
- **goal_to_go**: plus 10 to plus 3
- **goal_line**: plus 2 to the end zone

That helped a lot. A broad red-zone bucket was hiding too much. Once I split those spaces out, the model started surfacing behavior that felt more like real coaching tendencies instead of generic offense.

## Data Source
This project uses public NFL play-by-play data from **nflverse**.

Raw files loaded:
- `pbp_2023.csv`
- `pbp_2024.csv`
- `pbp_2025.csv`

## How I Built It

### 1. Raw staging
I loaded the nflverse CSVs into MySQL and kept source metadata attached so I could trace rows back to season and file.

### 2. Clean play universe
I filtered the data down to real offensive decision plays. I removed kneels, spikes, special teams, and other rows that would muddy the behavior model.

### 3. Situation views
I built reusable play-level views for:
- early down
- third down
- fourth down
- short yardage
- red zone
- goal to go
- goal line
- two-minute half
- two-minute game
- tied / leading / trailing
- one-score and two-plus-score game states

### 4. Team profiles
I built 2025 offensive profiles at the **team + situation + field-zone** level.

### 5. League baselines
I built 2023–2025 league baselines at that same grain so the comparisons would stay clean.

### 6. Feature engineering
I calculated team-vs-baseline deltas for:
- run/dropback tendency
- shotgun usage
- tempo
- EPA
- success rate
- explosiveness
- sack rate
- turnover rate

### 7. Coach DNA scoring
I built a scoring layer that combines:
- tendency distinctiveness
- efficiency
- explosiveness
- stability
- sample reliability

### 8. Export layer
I packaged the outputs into ranked tables so the project is easier to review without opening every notebook or script first.

## Technical Hurdles I Had To Fix
The biggest issue showed up after I upgraded the model grain.

Before field zones, joining team profiles to league baselines by situation was enough. After I added field zones, that join logic broke. The feature table started overmatching and the row counts ballooned. I caught it by checking expected row totals and seeing the table come back much larger than it should have.

The fix was to join on both `situation_name` and `field_zone`, then rebuild the feature layer and everything after it.

I also had to stay honest about sample size. Some contexts are naturally thin. Fourth down backed up is never going to have the same volume as early down in own territory. I built sample-quality flags and reliability weighting into the score so the model wouldn’t treat every context like it deserved the same confidence.

## Core Tables and Outputs

### SQL layer
- `raw_pbp`
- `clean_pbp`
- situation views (`vw_sit_*`)
- `team_offense_profiles_2025`
- `league_offense_baselines_2023_2025`

### Python layer
- `team_baseline_features_2025_vs_2023_2025.csv`
- `coach_dna_situation_scores_2025.csv`
- `coach_dna_team_summary_2025.csv`
- `coach_dna_ranked_team_summary_2025.csv`
- `coach_dna_ranked_situation_scores_2025.csv`
- `coach_dna_top_signal_situations_by_team_2025.csv`
- `coach_dna_situation_strength_summary_2025.csv`
- `coach_dna_team_summary_presentation_2025.csv`

## What The Model Scores
I didn’t want a mystery number with no guts behind it, so I split the score into parts.

- **Tendency signal**
  - how far a team moves from league expectation

- **Efficiency signal**
  - whether that behavior beats the baseline

- **Explosiveness signal**
  - whether the offense creates chunk plays above baseline

- **Stability signal**
  - whether sacks and turnovers stay under control

- **Sample reliability**
  - whether the context has enough volume to trust

That kept the score from rewarding style by itself. I wanted the model to care about whether the difference was real, whether it was productive, and whether I had enough sample to believe it.

## What The Numbers Started Showing

### 1. Field position sharpened the model fast
Some of the strongest average separation across teams showed up in places like:
- `all_offense | own_territory`
- `all_offense | fringe`
- `early_down | own_territory`

That was one of the first signs the rebuild was worth it.

### 2. Team identity started showing up in real football space
Once I pushed the model to situation + field zone, the outputs got more specific.

The questions got better too:
- who gets more run-heavy in own territory?
- who stays aggressive in fringe space?
- who changes tempo when trailing in scoring territory?
- who tightens up near the goal line?
- who looks different in compressed field space and still performs well?

That’s more useful for coach-logic work than broad labels by themselves.

### 3. Buffalo surfaced near the top
Buffalo finished near the top of the 2025 offensive Coach DNA ranking and showed one of its clearest signals in:
- `leading_early_down | own_territory`

That gives me a concrete place where the team should probably feel different from a default CPU profile.

### 4. Splitting scoring space helped
Breaking scoring territory into:
- red zone
- goal to go
- goal line

cleaned up the model. Those aren’t the same football environments, so I didn’t want them blended into one bucket.

### 5. The best tuning candidates combine strong signal and real sample
Some contexts looked interesting but thin. Others had both separation and volume. That second group is where I’d start if I were using this as a gameplay benchmark.

## Example Questions This Project Can Answer
- Which teams have the strongest offensive coaching DNA in 2025?
- Which field-zone contexts separate teams the most?
- Which teams become more run-heavy than baseline in own territory on early downs?
- Which teams stay aggressive in fringe or scoring space?
- Which teams shift most clearly when leading versus trailing?
- Which teams show distinctive goal-to-go or goal-line behavior?

## Tables I’d Review First
If someone only had a few minutes with the repo, I’d start here:

- `outputs/tables/coach_dna_ranked_team_summary_2025.csv`  
  Team-level ranking with top and lowest signal contexts

- `outputs/tables/coach_dna_ranked_situation_scores_2025.csv`  
  Ranked team-context combinations across the full model

- `outputs/tables/coach_dna_top_signal_situations_by_team_2025.csv`  
  Top 3 strongest contexts for each team

- `outputs/tables/coach_dna_situation_strength_summary_2025.csv`  
  Which contexts create the strongest average separation

- `outputs/tables/coach_dna_team_summary_presentation_2025.csv`  
  Cleaner presentation-ready team summary output

## Why A Football Studio Should Care
This project gives a cleaner way to talk about coach identity in a game setting.

It shows where teams behave differently:
- by situation
- by field position
- by run/pass tendency
- by tempo
- by efficiency profile

That gives a studio something more concrete to work from when thinking about CPU-controlled coach logic.

The question I kept building around was simple:
where should team differences show up so the game feels more like football?

That’s what this project is trying to answer.

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