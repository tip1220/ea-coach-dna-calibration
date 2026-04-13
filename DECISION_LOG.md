# Decision Log

## 2026-04-04
Decision: Use 2025 only for team profiles.
Reason: Avoid blending multiple coaching staffs, coordinators, and team identities across seasons.
Impact: Team tendencies will be measured at the 2025 team-season level.

## 2026-04-04
Decision: Use 2023 to 2025 for league baselines.
Reason: League-wide context benefits from a broader sample and is less sensitive to team-specific coaching changes.
Impact: Baseline comparisons will be more stable than single-season league averages.

## 2026-04-04
Decision: Use NFL data only for the main project.
Reason: Real NFL play-by-play is sufficient to build a meaningful authenticity benchmark without pretending to have access to internal game telemetry.
Impact: Recommendations will be framed as a benchmarking framework, not a direct audit of EA logic.

## 2026-04-04
Decision: Do not use synthetic game telemetry.
Reason: Synthetic telemetry would add complexity and assumptions that are not necessary for the project’s main value.
Impact: The project remains cleaner, more credible, and easier to explain.

## 2026-04-04
Decision: Use SQL and Python only.
Reason: The goal is to demonstrate technical workflow, feature creation, and analytical reasoning without relying on dashboards.
Impact: Final outputs will be code, tables, exports, and documentation rather than BI deliverables.

## 2026-04-04
Decision: Team-season is the main analytical unit.
Reason: Team identity changes over time. Team-season preserves coaching and situational signal more accurately.
Impact: Results will be interpreted as season-specific profiles rather than timeless team identities.

## 2026-04-04
Decision: Use Git and GitHub as the source of truth for code history.
Reason: Long projects get messy when logic changes are not tracked cleanly.
Impact: Work will be committed in small, traceable steps with documentation updates along the way.

## 2026-04-09
Decision: Frame the project as a benchmarking framework, not a product audit.
Reason: The project uses public NFL data and does not have access to internal gameplay telemetry or tuning logic.
Impact: All findings and recommendations must be written as benchmark guidance rather than claims about a specific game system.

## 2026-04-09
Decision: Focus the first version on offensive situational behavior only.
Reason: Offensive behavior is enough to build a strong first-pass benchmark without overextending the scope.
Impact: Defensive profiling is deferred to a future version.

## 2026-04-09
Decision: Build a cleaned offensive play universe before any profiling logic.
Reason: Raw play-by-play includes special teams, non-play rows, kneels, spikes, and other rows that would distort situational benchmarking.
Impact: Downstream views, team profiles, and baselines are built from `clean_pbp`, not `raw_pbp`.

## 2026-04-09
Decision: Use reusable play-level situational views as the intermediate layer.
Reason: Reusable views keep the pipeline modular and make team-profile and league-baseline logic easier to maintain.
Impact: Situational logic is centralized in `04_situational_views.sql` and reused downstream.

## 2026-04-09
Decision: Include both broad score-state buckets and narrower score-pressure buckets.
Reason: Broad buckets like leading/trailing support simple rollups, while one-score vs two-plus-score buckets better reflect scoreboard pressure.
Impact: The view layer includes tied, leading, trailing, leading/trailing one score, leading/trailing two-plus scores, and early-down score-state combinations.

## 2026-04-09
Decision: Store team profiles and league baselines in long format.
Reason: One row per team-plus-situation or situation-only keeps comparisons, scoring, and exports cleaner than a very wide table design.
Impact: `team_offense_profiles_2025` and `league_offense_baselines_2023_2025` are built as long-format analytical tables.

## 2026-04-09
Decision: Use mutually exclusive play-family logic for run vs dropback rates.
Reason: Raw football flags can overlap on plays like scrambles, which inflates rate totals if both are averaged directly.
Impact: Run and dropback rates are calculated from `play_family`, ensuring they sum cleanly to 1.0.

## 2026-04-09
Decision: Use 2023 to 2025 league baselines with 2025 team profiles.
Reason: This preserves a current-year team identity while comparing it against a broader, more stable context window.
Impact: Team-vs-baseline deltas reflect 2025 behavior against a 3-season league reference.

## 2026-04-09
Decision: Build a first-pass Coach DNA scoring layer from team-vs-baseline deltas.
Reason: The project needs a structured way to summarize distinctiveness, efficiency, explosiveness, stability, and reliability into recruiter-friendly outputs.
Impact: Python scoring outputs now include situation-level scores, team-level summary scores, and ranked export tables.

## 2026-04-09
Decision: Keep scoring interpretable rather than over-modeling.
Reason: The portfolio value comes from clarity, defensibility, and studio relevance, not unnecessary modeling complexity.
Impact: The first scoring version uses weighted signal components and sample guardrails instead of a black-box model.

## 2026-04-13
Decision: Add field position as a primary modeling dimension.
Reason: Broad game situations alone were not separating offensive behavior cleanly enough. Teams behave differently based on where the ball is on the field, even inside the same down, score, and clock context.
Impact: The model now evaluates offense at the situation + field-zone level instead of only the situation level.

## 2026-04-13
Decision: Define four core field zones: backed_up, own_territory, fringe, and red_zone.
Reason: These zones create a cleaner football read on how behavior changes as field position changes.
Impact: Team profiles and league baselines now carry field-zone context across the model.

## 2026-04-13
Decision: Split compressed scoring space into red_zone, goal_to_go, and goal_line.
Reason: Those are different playcalling environments and should not be blended into one generic red-zone bucket.
Impact: The model now captures more realistic scoring-space behavior and should support better coach-logic interpretation.

## 2026-04-13
Decision: Align team-to-baseline comparisons on both `situation_name` and `field_zone`.
Reason: After the field-zone rebuild, joining only on situation caused incorrect matches and inflated feature rows.
Impact: The feature layer now reflects the intended model grain and supports more reliable scoring outputs.

## 2026-04-13
Decision: Keep sample reliability as an explicit part of scoring.
Reason: Some field-zone contexts are naturally thinner than others, and the model should not treat all contexts as equally trustworthy.
Impact: Stronger-sample contexts carry more influence, while very thin contexts are still visible but weighted more carefully.