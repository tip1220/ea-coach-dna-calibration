# Decision Log

## 2026-04-04
Decision: Use 2024 only for team profiles.
Reason: Avoid blending multiple coaching staffs, coordinators, and team identities across seasons.
Impact: Team tendencies will be measured at the 2024 team-season level.

## 2026-04-04
Decision: Use 2022 to 2024 for league baselines.
Reason: League-wide context benefits from broader sample size and is less sensitive to team-specific coaching changes.
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
Impact: Final outputs will be code, tables, figures, and documentation rather than BI deliverables.

## 2026-04-04
Decision: Team-season is the main analytical unit.
Reason: Team identity changes over time. Team-season preserves the coaching and situational signal more accurately.
Impact: Results will be interpreted as season-specific profiles rather than timeless team identities.

## 2026-04-04
Decision: Use Git and GitHub as the source of truth for code history.
Reason: Long projects get messy when logic changes are not tracked cleanly.
Impact: Work will be committed in small, traceable steps with documentation updates along the way.