from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd

from config import (
    BASELINE_END_SEASON,
    BASELINE_START_SEASON,
    OUTPUT_TABLES_DIR,
    PROCESSED_DATA_DIR,
    PROFILE_SEASON,
    ensure_output_dirs,
)
from load_data import load_league_baselines, load_team_profiles


# =========================================================
# FEATURE SETTINGS
# =========================================================

RATE_METRICS: List[str] = [
    "dropback_rate",
    "rush_rate",
    "pass_attempt_rate",
    "shotgun_rate",
    "no_huddle_rate",
    "success_rate",
    "first_down_rate",
    "touchdown_rate",
    "turnover_rate",
    "sack_rate",
    "explosive_play_rate",
    "explosive_dropback_rate",
    "explosive_run_rate",
]

VALUE_METRICS: List[str] = [
    "avg_yards_gained",
    "avg_epa",
]

ALL_METRICS: List[str] = RATE_METRICS + VALUE_METRICS


# =========================================================
# CORE HELPERS
# =========================================================

def safe_pct_delta(team_value: pd.Series, baseline_value: pd.Series) -> pd.Series:
    """
    Calculate a safe percentage delta:
    (team - baseline) / abs(baseline)

    Returns NaN when the baseline is 0 or null.
    """
    baseline_abs = baseline_value.abs()
    return np.where(
        (baseline_abs > 0) & baseline_value.notna() & team_value.notna(),
        (team_value - baseline_value) / baseline_abs,
        np.nan,
    )


def build_team_baseline_features() -> pd.DataFrame:
    """
    Build a team-vs-baseline comparison table by situation.
    """
    team_profiles = load_team_profiles()
    league_baselines = load_league_baselines()

    baseline_cols = [
        "situation_name",
        "baseline_type",
        "baseline_start_season",
        "baseline_end_season",
        "season_count",
        "team_count",
        "team_season_count",
        "baseline_quality",
    ] + ALL_METRICS

    baseline_df = league_baselines[baseline_cols].copy()

    features = team_profiles.merge(
        baseline_df,
        on="situation_name",
        how="left",
        suffixes=("_team", "_baseline"),
    )

    # -----------------------------------------------------
    # Absolute deltas
    # -----------------------------------------------------
    for metric in ALL_METRICS:
        features[f"{metric}_delta"] = (
            features[f"{metric}_team"] - features[f"{metric}_baseline"]
        )

    # -----------------------------------------------------
    # Relative deltas
    # -----------------------------------------------------
    for metric in ALL_METRICS:
        features[f"{metric}_pct_delta"] = safe_pct_delta(
            features[f"{metric}_team"],
            features[f"{metric}_baseline"],
        )

    # -----------------------------------------------------
    # Direction flags
    # -----------------------------------------------------
    features["is_more_dropback_heavy"] = (
        features["dropback_rate_delta"] > 0
    ).astype(int)

    features["is_more_run_heavy"] = (
        features["rush_rate_delta"] > 0
    ).astype(int)

    features["is_more_shotgun_heavy"] = (
        features["shotgun_rate_delta"] > 0
    ).astype(int)

    features["is_more_no_huddle_heavy"] = (
        features["no_huddle_rate_delta"] > 0
    ).astype(int)

    features["is_more_efficient_epa"] = (
        features["avg_epa_delta"] > 0
    ).astype(int)

    features["is_more_successful"] = (
        features["success_rate_delta"] > 0
    ).astype(int)

    features["is_more_explosive"] = (
        features["explosive_play_rate_delta"] > 0
    ).astype(int)

    # -----------------------------------------------------
    # Sample metadata
    # -----------------------------------------------------
    features["sample_vs_baseline_context"] = np.where(
        features["play_count"] >= 100,
        "stable_team_sample",
        np.where(features["play_count"] >= 50, "usable_team_sample", "small_team_sample"),
    )

    features["meets_strong_team_sample"] = (features["play_count"] >= 100).astype(int)
    features["meets_usable_team_sample"] = (features["play_count"] >= 50).astype(int)

    # -----------------------------------------------------
    # Naming cleanup for clarity
    # -----------------------------------------------------
    rename_map = {
        "play_count": "team_play_count",
        "sample_quality": "team_sample_quality",
        "meets_min_sample_50": "team_meets_min_sample_50",
        "meets_min_sample_20": "team_meets_min_sample_20",
    }
    features = features.rename(columns=rename_map)

    # -----------------------------------------------------
    # Ordering
    # -----------------------------------------------------
    ordered_cols = [
        "profile_season",
        "team",
        "situation_order",
        "situation_name",
        "baseline_type",
        "baseline_start_season",
        "baseline_end_season",
        "season_count",
        "team_count",
        "team_season_count",
        "baseline_quality",
        "team_play_count",
        "team_sample_quality",
        "sample_vs_baseline_context",
        "team_meets_min_sample_50",
        "team_meets_min_sample_20",
        "meets_strong_team_sample",
        "meets_usable_team_sample",
    ]

    metric_pairs = []
    for metric in ALL_METRICS:
        metric_pairs.extend(
            [
                f"{metric}_team",
                f"{metric}_baseline",
                f"{metric}_delta",
                f"{metric}_pct_delta",
            ]
        )

    behavior_flags = [
        "is_more_dropback_heavy",
        "is_more_run_heavy",
        "is_more_shotgun_heavy",
        "is_more_no_huddle_heavy",
        "is_more_efficient_epa",
        "is_more_successful",
        "is_more_explosive",
    ]

    features = features[ordered_cols + metric_pairs + behavior_flags].copy()
    features = features.sort_values(["team", "situation_order"]).reset_index(drop=True)

    return features


def export_team_baseline_features(df: pd.DataFrame) -> None:
    """
    Save the feature table to project output locations.
    """
    ensure_output_dirs()

    processed_path = (
        PROCESSED_DATA_DIR
        / f"team_baseline_features_{PROFILE_SEASON}_vs_{BASELINE_START_SEASON}_{BASELINE_END_SEASON}.csv"
    )
    output_path = (
        OUTPUT_TABLES_DIR
        / f"team_baseline_features_{PROFILE_SEASON}_vs_{BASELINE_START_SEASON}_{BASELINE_END_SEASON}.csv"
    )

    df.to_csv(processed_path, index=False)
    df.to_csv(output_path, index=False)

    print("\nSaved files:")
    print(processed_path)
    print(output_path)


def smoke_test() -> None:
    """
    Build the team-vs-baseline feature table and print a quick summary.
    """
    features = build_team_baseline_features()

    print("\nteam_baseline_features")
    print(f"rows: {len(features):,}")
    print(f"columns: {len(features.columns)}")

    print("\nSample rows:")
    preview_cols = [
        "team",
        "situation_name",
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
    print(features[preview_cols].head(10))

    print("\nBUF sample:")
    print(
        features.loc[
            features["team"] == "BUF",
            [
                "team",
                "situation_name",
                "team_play_count",
                "dropback_rate_delta",
                "rush_rate_delta",
                "avg_epa_delta",
                "success_rate_delta",
                "explosive_play_rate_delta",
            ],
        ].head(10)
    )

    export_team_baseline_features(features)


if __name__ == "__main__":
    smoke_test()