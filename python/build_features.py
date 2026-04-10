from __future__ import annotations

import pandas as pd

from config import (
    BASELINE_END_SEASON,
    BASELINE_START_SEASON,
    LEAGUE_BASELINE_TABLE,
    OUTPUT_TABLES_DIR,
    PROCESSED_DATA_DIR,
    PROFILE_SEASON,
    TEAM_PROFILE_TABLE,
    ensure_output_dirs,
)
from load_data import load_sql_query


# =========================================================
# HELPERS
# =========================================================

DELTA_METRICS = [
    "dropback_rate",
    "rush_rate",
    "pass_attempt_rate",
    "shotgun_rate",
    "no_huddle_rate",
    "avg_yards_gained",
    "avg_epa",
    "success_rate",
    "first_down_rate",
    "touchdown_rate",
    "turnover_rate",
    "sack_rate",
    "explosive_play_rate",
    "explosive_dropback_rate",
    "explosive_run_rate",
]


def build_context_label(situation_name: str, field_zone: str) -> str:
    return f"{situation_name} | {field_zone}"


def load_team_profiles() -> pd.DataFrame:
    query = f"""
    SELECT *
    FROM {TEAM_PROFILE_TABLE}
    ORDER BY team, situation_order, field_zone_order
    """
    return load_sql_query(query)


def load_league_baselines() -> pd.DataFrame:
    query = f"""
    SELECT *
    FROM {LEAGUE_BASELINE_TABLE}
    ORDER BY situation_order, field_zone_order
    """
    return load_sql_query(query)


# =========================================================
# FEATURE BUILD
# =========================================================

def build_team_baseline_features() -> pd.DataFrame:
    """
    Build the team-vs-baseline feature table at the
    team + situation + field_zone grain.
    """
    team_profiles = load_team_profiles().copy()
    baselines = load_league_baselines().copy()

    merged = team_profiles.merge(
        baselines,
        on=["situation_name", "field_zone"],
        how="left",
        suffixes=("_team", "_baseline"),
    )

    merged["situation_order"] = merged["situation_order_team"]
    merged["field_zone_order"] = merged["field_zone_order_team"]

    merged["situation_field_zone_context"] = merged.apply(
        lambda row: build_context_label(row["situation_name"], row["field_zone"]),
        axis=1,
    )

    merged["team_play_count"] = merged["play_count_team"]
    merged["baseline_play_count"] = merged["play_count_baseline"]

    merged["team_sample_quality"] = merged["sample_quality"]
    merged["sample_vs_baseline_context"] = (
        merged["team_sample_quality"].fillna("unknown")
        + "_team_sample_vs_"
        + merged["baseline_quality"].fillna("unknown")
        + "_baseline"
    )

    for metric in DELTA_METRICS:
        merged[f"{metric}_delta"] = (
            merged[f"{metric}_team"] - merged[f"{metric}_baseline"]
        )

    ordered_cols = [
        "profile_season",
        "baseline_type",
        "baseline_start_season",
        "baseline_end_season",
        "team",
        "situation_order",
        "situation_name",
        "field_zone_order",
        "field_zone",
        "situation_field_zone_context",
        "team_play_count",
        "baseline_play_count",
        "season_count",
        "team_count",
        "team_season_count",
        "team_sample_quality",
        "baseline_quality",
        "sample_vs_baseline_context",
        "meets_min_sample_50",
        "meets_min_sample_20",
    ]

    metric_cols = []
    for metric in DELTA_METRICS:
        metric_cols.extend(
            [
                f"{metric}_team",
                f"{metric}_baseline",
                f"{metric}_delta",
            ]
        )

    features = merged[ordered_cols + metric_cols].copy()

    features = features.sort_values(
        ["team", "situation_order", "field_zone_order"]
    ).reset_index(drop=True)

    return features


# =========================================================
# EXPORT
# =========================================================

def export_team_baseline_features(features: pd.DataFrame) -> None:
    ensure_output_dirs()

    filename = f"team_baseline_features_{PROFILE_SEASON}_vs_{BASELINE_START_SEASON}_{BASELINE_END_SEASON}.csv"

    processed_path = PROCESSED_DATA_DIR / filename
    output_path = OUTPUT_TABLES_DIR / filename

    features.to_csv(processed_path, index=False)
    features.to_csv(output_path, index=False)

    print("\nSaved files:")
    print(processed_path)
    print(output_path)


# =========================================================
# SMOKE TEST
# =========================================================

def smoke_test() -> None:
    features = build_team_baseline_features()

    print("\nteam_baseline_features")
    print(f"rows: {len(features):,}")
    print(f"columns: {len(features.columns)}")

    print("\nSample rows:")
    print(
        features[
            [
                "team",
                "situation_name",
                "field_zone",
                "team_play_count",
                "dropback_rate_team",
                "dropback_rate_baseline",
                "dropback_rate_delta",
                "avg_epa_team",
                "avg_epa_baseline",
                "avg_epa_delta",
                "success_rate_team",
                "success_rate_baseline",
                "success_rate_delta",
            ]
        ].head(12)
    )

    print("\nBUF sample:")
    print(
        features.loc[
            features["team"] == "BUF",
            [
                "team",
                "situation_name",
                "field_zone",
                "team_play_count",
                "dropback_rate_delta",
                "rush_rate_delta",
                "avg_epa_delta",
                "success_rate_delta",
                "explosive_play_rate_delta",
            ],
        ].head(12)
    )

    export_team_baseline_features(features)


if __name__ == "__main__":
    smoke_test()