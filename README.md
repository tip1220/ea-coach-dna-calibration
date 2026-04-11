# Coach DNA Calibration Lab

## Overview
Coach DNA Calibration Lab is a SQL and Python portfolio project built to translate real NFL offensive behavior into a benchmarking framework for football gameplay authenticity.

The project uses NFL play-by-play data to answer a studio-relevant question: how should team-specific coaching tendencies show up in football decision logic if the goal is to make teams feel more distinct, believable, and situationally authentic?

This is **not** an audit of EA Sports logic, and it does not claim to measure internal game behavior. Instead, it builds an external benchmark from real NFL data that could support design conversations around coach logic, situational aggression, playcalling identity, tempo, and late-game behavior.

The upgraded version of the project measures behavior at the **situation + field-zone** level, which makes the model more useful for CPU-controlled coaching logic. It no longer stops at broad situations like “early down” or “trailing.” It now asks how teams behave in those situations depending on where the ball is on the field.

---

## Business Question
How can real NFL situational decision-making be translated into a structured benchmark for more authentic football coach logic?

---

## Why This Project Matters
Football realism is not just about ratings, rosters, or animations. It is also about behavior.

Teams do not all act the same when they are:
- protecting a lead
- chasing points
- facing short yardage
- operating in the red zone
- playing on third or fourth down
- managing two-minute situations
- working backed up, in own territory, in fringe space, or in compressed scoring space

If every team behaves too similarly in these moments, the game can lose one of the things that makes football feel real: coaching identity.

This project focuses on that layer.

---

## Project Framing
This project is designed as a **benchmarking framework**, not a direct product audit.

I do **not** have access to:
- internal EA telemetry
- internal gameplay logic
- private tuning rules
- proprietary simulation data

Because of that, all recommendations and takeaways should be interpreted as:
- benchmark guidance from real NFL behavior
- evidence for how teams differ by situation and field position
- inputs that could help shape more authentic coach logic

Not as unsupported claims about any specific game system.

---

## Scope
This project uses the following scope:

- **2025** NFL play-by-play for team profiles
- **2023–2025** NFL play-by-play for league baselines
- **team-season** as the main analytical unit for profiles
- **situation + field-zone** as the main behavioral grain
- **SQL + Python only**
- **no dashboarding layer** for the core project

### In Scope
- situational offensive behavior
- field-zone-aware tendency profiling
- compressed-field scoring contexts
- league baseline construction
- team-vs-baseline comparisons
- Coach DNA scoring
- exported recruiter-ready tables

### Out of Scope
- internal game telemetry
- synthetic gameplay data
- proprietary tracking data
- cross-sport expansion
- defensive profiling in this first version

---

## Why Field Zones Were Added
The first pass of the project showed that down, distance, score state, and clock all mattered when profiling offensive behavior.

But that first pass still missed one of the biggest drivers of real football decision-making: **field position**.

A team backed up in minus territory should not behave the same way it behaves:
- in own territory
- in fringe space
- inside the red zone
- inside goal-to-go or goal-line space

Adding field zones made the model more realistic because it now evaluates coaching behavior at the exact context where decisions happen.

That upgrade makes the project more useful for CPU-controlled coaching logic because it helps answer not just:
- what does this team do in this situation?

but:
- what does this team do in this situation, in this part of the field?

---

## Field-Zone Definitions
The upgraded model carries field position alongside each major situation.

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

The model also separates compressed scoring space into:
- **red_zone**: plus 20 to plus 11
- **goal_to_go**: plus 10 to plus 3
- **goal_line**: plus 2 to the end zone

That matters because those are different football environments, and CPU coach logic should not treat them as one blended bucket.

---

## Data Source
This project uses public NFL play-by-play data from **nflverse**.

Raw files loaded:
- `pbp_2023.csv`
- `pbp_2024.csv`
- `pbp_2025.csv`

---

## Analytical Approach
The project follows a layered pipeline:

1. **Raw staging**
   - Load nflverse CSVs into MySQL
   - Preserve season and file metadata for reproducibility

2. **Clean play universe**
   - Filter to real offensive decision plays
   - Remove special teams, kneels, spikes, and non-core rows
   - Create reusable flags for game state, distance, and field position

3. **Situational views**
   - Build reusable play-level views for:
     - early down
     - third down
     - fourth down
     - short yardage
     - red zone
     - goal to go
     - goal line
     - two-minute situations
     - tied / leading / trailing states
     - one-score and two-plus-score contexts

4. **2025 team profiles**
   - Build team-by-situation-by-field-zone offensive profiles
   - Measure tendency, efficiency, explosiveness, and stability

5. **2023–2025 league baselines**
   - Build the comparison benchmark for each situation + field-zone context
   - Keep the metric structure aligned to team profiles

6. **Feature engineering**
   - Calculate team-vs-baseline deltas
   - Build reusable comparison tables for downstream scoring

7. **Coach DNA scoring**
   - Create situation-level and team-level scores
   - Combine tendency distinctiveness with efficiency and sample reliability

8. **Export layer**
   - Produce ranked summary tables
   - Package outputs for portfolio review, screenshots, and GitHub presentation

---

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
- `coach_dna_situation_strength_summary_2025.csv`
- `coach_dna_team_summary_presentation_2025.csv`

---

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

---

## Key Findings

### 1. Field position materially improved the model
Some of the strongest average separation across teams appears in contexts like:
- `all_offense | own_territory`
- `all_offense | fringe`
- `early_down | own_territory`

That supports the field-zone upgrade. Coaching identity does not just change by game situation. It changes by where the ball is on the field.

### 2. The model now surfaces team identity at the exact context where decisions happen
The upgraded model no longer stops at broad situations like:
- early down
- trailing
- red zone

It now identifies team behavior at the **situation + field-zone** level, which is much closer to the kind of logic a game studio would need for more authentic CPU-controlled coaches.

### 3. Buffalo emerged as one of the strongest overall offensive Coach DNA signals
In the upgraded 2025 rankings, Buffalo finished near the top of the model and showed one of its clearest signals in:
- `leading_early_down | own_territory`

That suggests Buffalo should not inherit a generic league-average early-down CPU profile in that context.

### 4. Splitting scoring territory into red zone, goal to go, and goal line improved football realism
The project now treats these as separate environments:
- `red_zone`: plus 20 to plus 11
- `goal_to_go`: plus 10 to plus 3
- `goal_line`: plus 2 to the end zone

That matters because those are not the same playcalling environments, and CPU coaching logic should not treat them as one blended bucket.

### 5. The strongest tuning opportunities are the contexts with both strong separation and strong sample
The best candidates for CPU coach tuning are the places where:
- teams differ clearly from baseline
- the behavior appears stable
- the sample is large enough to trust

That gives the project more practical design value. It does not just show difference. It helps point to **where the difference is safest to tune around**.

---

## Example Business Questions This Project Can Answer
- Which teams have the strongest offensive coaching DNA in 2025?
- Which field-zone contexts create the strongest separation across teams?
- Which teams become more run-heavy than baseline in own territory on early downs?
- Which teams remain aggressive in fringe or scoring territory when the league tends to tighten up?
- Which teams show the clearest leading vs. trailing behavior shift by field zone?
- Which teams have distinctive goal-to-go or goal-line behavior that could improve CPU playcall authenticity?

---

## Output Tables Worth Reviewing First
If you want the fastest path through the project, start here:

- `outputs/tables/coach_dna_ranked_team_summary_2025.csv`  
  Team-level ranking output with top and lowest signal contexts.

- `outputs/tables/coach_dna_ranked_situation_scores_2025.csv`  
  Ranked team-context combinations across the full upgraded model.

- `outputs/tables/coach_dna_top_signal_situations_by_team_2025.csv`  
  The top 3 strongest contexts for each team.

- `outputs/tables/coach_dna_situation_strength_summary_2025.csv`  
  A league-wide view of which contexts create the strongest average separation.

- `outputs/tables/coach_dna_team_summary_presentation_2025.csv`  
  A presentation-friendly version of the team summary ranking.

---

## Why This Matters for EA Sports
Football realism is not just about player ratings. It is also about whether teams and coaches behave differently when the game context changes.

This project is useful because it creates a path toward CPU-controlled coaching logic that is:
- more context-aware
- more team-specific
- more faithful to real football behavior

Instead of treating offensive decision-making as one generic league-average profile, the model helps identify where a team should feel different:
- by situation
- by field position
- by run/pass tendency
- by tempo
- by efficiency profile

That makes the project relevant to gameplay authenticity, coach logic tuning, and situational football design.

---

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
    